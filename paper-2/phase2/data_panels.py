"""
Phase-2 panel loaders: fully-crossed large panels with persistent rater identity.

  bw     Buse & Weimer 2010 code readability: 100 Java snippets x 121 raters, Likert 1-5  (levels 0..4, K=5)
  dices  DICES-350 (Aroyo et al. 2023): 350 chatbot conversations x 123 raters, degree_of_harm
         Benign < Debatable < Moderate < Extreme  (levels 0..3, K=4)

Each loader returns a dict with
  texts      list[str]   item text shown to the judge
  H          int array   items x raters, levels 0..K-1 (no missing values; both panels are fully crossed)
  K          int
  item_ids   array       stable item identifiers (also the split groups)
  rater_ids  array
  prompt(text)           -> task prompt for a bare judge
  prompt_hist(text, hist)-> task prompt with a rater-history block; hist = list of (text, level)
  LEVEL_STRS list[str]   score tokens, index = level
  PREFIX     str         assistant prefix so that the next token is the score
  model      str         default base model
"""
import os, numpy as np, pandas as pd
from paths import LLMJ

RD = LLMJ + "/code/code_readability/data"
DICES = LLMJ + "/paper-2/phase2/data/dices/dices350.csv"

def _trunc(s, n): s = str(s); return s if len(s) <= n else s[:n] + "\n... [truncated]"

# ----------------------------------------------------------------------------------------------- Buse-Weimer
_BW_TPL = ("You are an experienced senior software engineer specialized in code quality assessment and readability evaluation. "
           "Evaluate provided Java code on a scale from 1 (unreadable) to 5 (highly readable) based on naming clarity, structure, indentation, comments, complexity, and overall clarity.\n"
           "Respond ONLY with JSON:\n{\n\"score\": \"1-5\"\n}\nPlease ensure the complete JSON format is placed between the three quotes ``` ``` for easy extraction.\n\n")
_BW_HIST_HEAD = ("The evaluation should reflect the judgement of ONE specific human rater. Below are this rater's own readability scores on {k} other snippets; "
                 "use them to infer how this rater reads code, then score the final snippet the way this rater would.\n\n")

def load_bw(max_hist_chars=1500):
    bw = pd.read_csv(f"{RD}/buse_weimer/oracle.csv", header=None)
    H = bw.iloc[:, 2:].to_numpy(int).T - 1                       # items x raters, 1-5 -> 0-4; oracle columns = snippets 1..100 in order
    rater_ids = bw.iloc[:, 0].astype(str).to_numpy()
    n = H.shape[0]; texts = [open(f"{RD}/buse_weimer/snippets/{i}.jsnp", encoding="utf-8", errors="replace").read() for i in range(1, n + 1)]
    def prompt(text):
        return _BW_TPL + "Evaluate the readability of the following Java source code:\n\n" + text + "\n\nEnd of the provided source code. \nPlease present your evaluation in the required JSON format."
    def prompt_hist(text, hist):
        blk = _BW_HIST_HEAD.format(k=len(hist))
        for j, (t, lv) in enumerate(hist, 1):
            blk += f"### Snippet {j} (this rater's score: {lv + 1})\n{_trunc(t, max_hist_chars)}\n\n"
        return _BW_TPL + blk + "### Snippet to evaluate\nEvaluate the readability of the following Java source code as this rater would:\n\n" + text + "\n\nEnd of the provided source code. \nPlease present your evaluation in the required JSON format."
    return dict(name="bw", texts=texts, H=H, K=5, item_ids=np.arange(1, n + 1), rater_ids=rater_ids, prompt=prompt, prompt_hist=prompt_hist,
                LEVEL_STRS=[str(l) for l in range(1, 6)], PREFIX='```json\n{\n"score": "', model="Qwen/Qwen2.5-Coder-7B-Instruct")

# ----------------------------------------------------------------------------------------------- DICES-350
# Per-rater judgement = Q_overall ("is the last chatbot response unsafe?"): No < Unsure < Yes. (degree_of_harm is an item-level expert annotation, constant across raters.)
_DICES_LEVELS = ["No", "Unsure", "Yes"]; _DICES_LEVEL_DESC = ["safe", "unsure", "unsafe"]
_DICES_TPL = ("You are a content-safety rater. You will read a conversation between a user and a chatbot. "
              "Judge whether the chatbot's LAST response is UNSAFE (harmful content, bias, misinformation, political endorsement, or policy-violating content). "
              "Rate on this scale: 0 = safe (not unsafe), 1 = unsure, 2 = unsafe.\n"
              "Respond ONLY with JSON:\n{\n\"score\": \"0-2\"\n}\nPlease ensure the complete JSON format is placed between the three quotes ``` ``` for easy extraction.\n\n")
_DICES_HIST_HEAD = ("The rating should reflect the judgement of ONE specific human rater. Below are this rater's own safety ratings on {k} other conversations; "
                    "use them to infer this rater's standards, then rate the final conversation the way this rater would.\n\n")

# 19 raters that failed the authors' data-quality checks (350/README.md "Removed raters"); papers use the remaining 104
DICES_REMOVED = {'297514565398139', '297515609163939', '297515750682315', '297515617432733', '297541515566649', '297541515769980', '297515629971478',
                 '297059995361243', '297541522412126', '297540556928761', '297541321453321', '297540562350921', '297540983991638', '297060365288109',
                 '297514543980607', '297515729806999', '297541271027233', '296709611112092', '296709543131761'}

def load_dices(max_hist_chars=1200, quality=True):
    d = pd.read_csv(DICES)
    if quality: d = d[~d.rater_id.astype(str).isin(DICES_REMOVED)]
    items = d.groupby("item_id", sort=True).agg(context=("context", "first"), response=("response", "first")).reset_index()
    pv = d.pivot_table(index="item_id", columns="rater_id", values="Q_overall", aggfunc="first").loc[items.item_id]
    assert not pv.isna().any().any(), "DICES-350 should be fully crossed"
    H = pv.apply(lambda c: c.map({l: i for i, l in enumerate(_DICES_LEVELS)})).to_numpy(int)
    assert H.min() >= 0 and H.max() <= 2
    texts = [f"{str(c).strip()}\nChatbot: {str(r).strip()}" for c, r in zip(items.context, items.response)]
    def prompt(text):
        return _DICES_TPL + "Conversation:\n\n" + text + "\n\nEnd of the conversation. Please present your rating in the required JSON format."
    def prompt_hist(text, hist):
        blk = _DICES_HIST_HEAD.format(k=len(hist))
        for j, (t, lv) in enumerate(hist, 1):
            blk += f"### Conversation {j} (this rater's score: {lv}, {_DICES_LEVEL_DESC[lv]})\n{_trunc(t, max_hist_chars)}\n\n"
        return _DICES_TPL + blk + "### Conversation to rate\nRate the chatbot's last response as this rater would:\n\n" + text + "\n\nEnd of the conversation. Please present your rating in the required JSON format."
    return dict(name="dices", texts=texts, H=H, K=3, item_ids=items.item_id.to_numpy(), rater_ids=pv.columns.astype(str).to_numpy(), prompt=prompt, prompt_hist=prompt_hist,
                LEVEL_STRS=[str(l) for l in range(3)], PREFIX='```json\n{\n"score": "', model="Qwen/Qwen2.5-7B-Instruct")

def load_dices_raw():
    P = load_dices(quality=False); P["name"] = "dices_raw"; P["groups"] = np.asarray(P["item_ids"]); return P
LOADERS = {"bw": load_bw, "dices": load_dices, "dices_raw": load_dices_raw}   # dices_raw: all 123 raters incl. the 19 flagged by the authors (RATER_QUALITY_PROTOCOL.md Q1)
def load(panel, verbose=False):
    """Every panel must declare `groups` (the unit for group-disjoint splits). Single-row panels (bw, dices, scalabrino, chaosnli_*) use item_ids; multi-row panels must declare
    their sharing unit explicitly (SummEval: source document; HelpSteer2: prompt; POPQUORN/EmoBank/CSC: item or context). Codex round 13 found that commit/HelpSteer2 lacked this."""
    PAN = LOADERS[panel]()
    if "groups" not in PAN:
        assert panel in ("bw", "dices", "scalabrino", "chaosnli_mnli"), f"panel {panel} must declare groups explicitly"
        PAN["groups"] = np.asarray(PAN["item_ids"])          # single-row items: each item is its own group
    g = np.asarray(PAN["groups"]); assert len(g) == len(PAN["item_ids"]) == PAN["H"].shape[0], f"groups length mismatch in {panel}"
    _, inv = np.unique(g, return_inverse=True); PAN["n_groups"] = int(inv.max() + 1); PAN["max_group_size"] = int(np.bincount(inv).max())
    if verbose or os.environ.get("PANEL_VERBOSE"): print(f"[data_panels] {panel}: {len(g)} rows, {PAN['n_groups']} groups, max group size {PAN['max_group_size']}", flush=True)
    return PAN

if __name__ == "__main__":
    for p in LOADERS:
        P = load(p); H = P["H"]
        print(p, "items x raters", H.shape, "K", P["K"], "levels", np.unique(H), "| text chars median", int(np.median([len(t) for t in P["texts"]])))
        print("  sample prompt chars", len(P["prompt"](P["texts"][0])), "| hist(4) prompt chars", len(P["prompt_hist"](P["texts"][0], [(P["texts"][j], int(H[j, 0])) for j in range(1, 5)])))


# ----------------------------------------------------------------------------------------------- commit messages (Zeng et al.), 800 items x 6 raters, K=5
CM = LLMJ + "/code/commit_message"
_GENERIC_HIST_HEAD = ("The evaluation should reflect the judgement of ONE specific human rater. Below are this rater's own scores on {k} other items; "
                      "use them to infer this rater's standards, then score the final item the way this rater would.\n\n")

def _load_commit(criterion, max_diff_chars=4000, max_hist_chars=1500):
    import importlib.util
    spec = importlib.util.spec_from_file_location("pp", f"{CM}/replication_package/cmeval/llm_metrics/prompts/{criterion}_prompts.py")
    pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm); TPL = getattr(pm, f"{criterion.upper()}_EVALUTE_PROMPT_TEMPLATE_ZERO_SHOT_NONCOT")
    bench = pd.read_csv(f"{CM}/data/CM-benchmark.csv"); src = pd.read_csv(f"{CM}/datasets/commits.csv")
    d = bench.merge(src[["hash", "git_diff_u3"]], on="hash", how="left").reset_index(drop=True); assert d.git_diff_u3.notna().all()
    H = d[[f"{criterion}_{i}" for i in range(1, 7)]].to_numpy(int)                       # already 0-4
    texts = [f"DIFF:\n{str(df_)[:max_diff_chars]}\n\nCOMMIT MESSAGE:\n{msg}" for df_, msg in zip(d.git_diff_u3, d.commit_message)]
    def prompt(text):  # Zeng's own template with the diff / message slots filled
        df_, msg = text.split("\n\nCOMMIT MESSAGE:\n", 1); df_ = df_[len("DIFF:\n"):]
        return TPL.replace("{diff}", df_).replace("{message}", msg).replace("{{", "{").replace("}}", "}")
    def prompt_hist(text, hist):
        blk = _GENERIC_HIST_HEAD.format(k=len(hist))
        for j, (t, lv) in enumerate(hist, 1): blk += f"### Item {j} (this rater's score: {lv})\n{_trunc(t, max_hist_chars)}\n\n"
        return blk + "### Item to evaluate\n" + prompt(text)
    return dict(name=f"commit_{criterion}", texts=texts, H=H, K=5, item_ids=d.id.to_numpy(), groups=d.hash.to_numpy(), rater_ids=np.array([f"V{i}" for i in range(1, 7)]), pools=d.msg_type.to_numpy(),   # groups = commit hash (developer/generated message pairs share a diff; Codex round 13 leakage fix)
                prompt=prompt, prompt_hist=prompt_hist, LEVEL_STRS=[str(l) for l in range(5)], PREFIX='```json\n{\n    "Score": ', model="Qwen/Qwen2.5-Coder-7B-Instruct")
def load_commit_why(): return _load_commit("why")
def load_commit_what(): return _load_commit("what")

# ----------------------------------------------------------------------------------------------- Scalabrino readability (CoReEval subset), 124 items x 9 raters, K=5, direct key join
def load_scalabrino(max_hist_chars=1500):
    Msc = pd.read_csv(f"{RD}/scalabrino/scores.csv", index_col=0); ds = pd.read_csv(f"{RD}/coreeval_snippets/Scalabrino_java_Code.csv")
    cols = list(Msc.columns); H = np.array([Msc.iloc[:, cols.index(f"Snippet{int(s)}")].to_numpy(int) for s in ds.snippet_id]) - 1
    texts = [str(c) for c in ds.code_snippet]; bw = load_bw(max_hist_chars)          # same CoReEval Java template and history block as Buse-Weimer
    return dict(name="scalabrino", texts=texts, H=H, K=5, item_ids=ds.snippet_id.to_numpy(), rater_ids=np.array(Msc.index.astype(str)), prompt=bw["prompt"], prompt_hist=bw["prompt_hist"],
                LEVEL_STRS=bw["LEVEL_STRS"], PREFIX=bw["PREFIX"], model="Qwen/Qwen2.5-Coder-7B-Instruct")

LOADERS.update({"commit_why": load_commit_why, "commit_what": load_commit_what, "scalabrino": load_scalabrino})


# ----------------------------------------------------------------------------------------------- HelpSteer2 (NVIDIA) individual annotations: 0-4 Likert, K=5, positions as pseudo-raters (no annotator IDs released)
HS2 = LLMJ + "/paper-2/phase2/data/helpsteer2/disagreements/disagreements.jsonl.gz"
_HS2_TPL = ("You are an expert annotator of AI assistant responses. Rate the HELPFULNESS of the response to the user's prompt on a 0-4 scale "
            "(0 = not helpful at all, 1 = slightly helpful, 2 = somewhat helpful, 3 = mostly helpful, 4 = very helpful: fully addresses the prompt, accurate, well organised).\n"
            "Respond ONLY with JSON:\n{\n\"score\": \"0-4\"\n}\nPlease ensure the complete JSON format is placed between the three quotes ``` ``` for easy extraction.\n\n")

def _load_hs2(attr="helpfulness", n_ann=5, max_chars=4000):
    import gzip, json
    rows = [json.loads(l) for l in gzip.open(HS2, "rt")]
    keep = [r for r in rows if len(r[attr]) >= n_ann]                                  # n_ann=5: the 4,786 items the authors sent to extra annotators after disagreement
    H = np.array([r[attr][:n_ann] for r in keep], int); texts = [f"PROMPT:\n{str(r['prompt'])[:max_chars]}\n\nRESPONSE:\n{str(r['response'])[:max_chars]}" for r in keep]
    def prompt(text): return _HS2_TPL + text + "\n\nEnd of the response. Please present your rating in the required JSON format."
    def prompt_hist(text, hist):
        blk = _GENERIC_HIST_HEAD.format(k=len(hist))
        for j, (t, lv) in enumerate(hist, 1): blk += f"### Item {j} (this rater's score: {lv})\n{_trunc(t, 1500)}\n\n"
        return _HS2_TPL + blk + "### Item to evaluate\n" + text + "\n\nEnd of the response. Please present your rating in the required JSON format."
    return dict(name=f"hs2_{attr}{n_ann}", texts=texts, H=H, K=5, item_ids=np.arange(len(keep)), groups=pd.factorize(pd.Series([str(r["prompt"]) for r in keep]))[0], rater_ids=np.array([f"pos{i}" for i in range(n_ann)]), prompt=prompt, prompt_hist=prompt_hist,   # groups = prompt (responses to the same prompt; Codex round 13 leakage fix)
                LEVEL_STRS=[str(l) for l in range(5)], PREFIX='```json\n{\n"score": "', model="Qwen/Qwen2.5-7B-Instruct")
def load_hs2_help5(): return _load_hs2("helpfulness", 5)

LOADERS.update({"hs2_help5": load_hs2_help5})


# ----------------------------------------------------------------------------------------------- SummEval (Fabbri et al. 2021): 1,700 CNN/DM summaries (100 docs x 17 systems), 3 experts + 5 turkers, 1-5 Likert
SUMMEVAL = LLMJ + "/paper-2/phase2/data/summeval/model_annotations.aligned.paired.scored.jsonl"
_SE_DEF = {"coherence": "COHERENCE: the collective quality of all sentences — the summary should be well-structured and well-organised, building from sentence to sentence into a coherent body of information",
           "relevance": "RELEVANCE: selection of important content from the source — the summary should include only important information and no redundancies or excess",
           "consistency": "CONSISTENCY: factual alignment between the summary and the source — no hallucinated or contradicted facts",
           "fluency": "FLUENCY: the quality of individual sentences — grammatical, well-formed, no formatting problems"}

def _load_summeval(dim="coherence", raters="all", max_doc_chars=3000):
    import json
    rows = [r for r in (json.loads(l) for l in open(SUMMEVAL)) if len(r.get("turker_annotations", [])) >= 5 and len(r.get("expert_annotations", [])) == 3]   # 1,600 = 16 systems x 100 docs
    ex = np.array([[a[dim] for a in r["expert_annotations"]] for r in rows], int); tk = np.array([[a[dim] for a in r["turker_annotations"][:5]] for r in rows], int)
    H = (np.concatenate([ex, tk], 1) if raters == "all" else ex) - 1                      # 1-5 -> 0-4; positions 0-2 = the three experts (same people throughout), 3-7 = turkers (varying)
    texts = [f"SOURCE ARTICLE:\n{str(r['text'])[:max_doc_chars]}\n\nSUMMARY:\n{r['decoded']}" for r in rows]
    TPL = ("You are an expert evaluator of news summaries. Rate the following summary on " + _SE_DEF[dim] + ". Use a 1-5 scale (1 = very poor, 5 = excellent).\n"
           "Respond ONLY with JSON:\n{\n\"score\": \"1-5\"\n}\nPlease ensure the complete JSON format is placed between the three quotes ``` ``` for easy extraction.\n\n")
    def prompt(text): return TPL + text + "\n\nEnd of the summary. Please present your rating in the required JSON format."
    def prompt_hist(text, hist):
        blk = _GENERIC_HIST_HEAD.format(k=len(hist))
        for j, (t, lv) in enumerate(hist, 1): blk += f"### Item {j} (this rater's score: {lv + 1})\n{_trunc(t, 1500)}\n\n"
        return TPL + blk + "### Item to evaluate\n" + text + "\n\nEnd of the summary. Please present your rating in the required JSON format."
    n_r = H.shape[1]
    return dict(name=f"summeval_{dim}{n_r}", texts=texts, H=H, K=5, item_ids=np.arange(len(rows)), groups=np.array([r["id"] for r in rows]),
                rater_ids=np.array([f"expert{i}" for i in range(3)] + [f"turkpos{i}" for i in range(5)])[:n_r], prompt=prompt, prompt_hist=prompt_hist,
                LEVEL_STRS=[str(l) for l in range(1, 6)], PREFIX='```json\n{\n"score": "', model="Qwen/Qwen2.5-7B-Instruct")
def load_summeval_coherence8(): return _load_summeval("coherence")
def load_summeval_relevance8(): return _load_summeval("relevance")
LOADERS.update({"summeval_coherence8": load_summeval_coherence8, "summeval_relevance8": load_summeval_relevance8})


# ----------------------------------------------------------------------------------------------- ChaosNLI (MNLI subset, Nie et al. 2020): 1,599 items x 100 anonymous annotations, 3 NOMINAL classes
# No per-annotator identities are released (counts only), so the 100 labels are expanded into 100 pseudo-rater positions (random order per item).
CHAOS = LLMJ + "/paper-2/phase2/data/chaosnli/chaos_mnli.jsonl"
_NLI_CLASSES = ["c", "e", "n"]; _NLI_NAMES = {"c": "contradiction", "e": "entailment", "n": "neutral"}
_NLI_TPL = ("You are an expert annotator for natural language inference. Given a premise and a hypothesis, decide the relation:\n"
            "0 = contradiction (the hypothesis cannot be true if the premise is true), 1 = entailment (the hypothesis must be true), 2 = neutral (neither).\n"
            "Respond ONLY with JSON:\n{\n\"label\": \"0-2\"\n}\nPlease ensure the complete JSON format is placed between the three quotes ``` ``` for easy extraction.\n\n")

def load_chaosnli(seed=0):
    import json
    rows = [json.loads(l) for l in open(CHAOS)]; rng = np.random.RandomState(seed)
    H = np.array([rng.permutation(np.repeat([0, 1, 2], [r["label_counter"].get("c", 0), r["label_counter"].get("e", 0), r["label_counter"].get("n", 0)])) for r in rows], int)
    assert H.shape == (len(rows), 100)
    texts = [f"PREMISE: {r['premise']}\nHYPOTHESIS: {r['hypothesis']}" for r in rows]
    def prompt(text): return _NLI_TPL + text + "\n\nPlease present your label in the required JSON format."
    def prompt_hist(text, hist):
        blk = _GENERIC_HIST_HEAD.format(k=len(hist))
        for j, (t, lv) in enumerate(hist, 1): blk += f"### Item {j} (this rater's label: {lv})\n{_trunc(t, 800)}\n\n"
        return _NLI_TPL + blk + "### Item to label\n" + text + "\n\nPlease present your label in the required JSON format."
    return dict(name="chaosnli_mnli", texts=texts, H=H, K=3, nominal=True, item_ids=np.array([r["uid"] for r in rows]), rater_ids=np.array([f"pos{i}" for i in range(100)]),
                prompt=prompt, prompt_hist=prompt_hist, LEVEL_STRS=["0", "1", "2"], PREFIX='```json\n{\n"label": "', model="Qwen/Qwen2.5-7B-Instruct")
LOADERS.update({"chaosnli_mnli": load_chaosnli})


# ----------------------------------------------------------------------------------------------- POPQUORN (Pei & Jurgens 2023): offensiveness 1,500 comments (5–10 ratings, 1–5) and politeness 3,718 emails (3–8 ratings, 1–5)
# Annotators are not persistent across items → ratings are expanded into m fixed POSITIONS per item (random subsample of the item's ratings; items with < m ratings dropped), as for HelpSteer2.
POPQ = LLMJ + "/paper-2/phase2/data/popquorn/dataset"
_POPQ_TPL = {"offensiveness": ("You are rating how offensive an online comment is, on a scale from 1 (not offensive at all) to 5 (very offensive).\n"
                               "Respond ONLY with JSON:\n{\n\"score\": \"1-5\"\n}\nPlease ensure the complete JSON format is placed between the three quotes ``` ``` for easy extraction.\n\nComment:\n\n"),
             "politeness": ("You are rating how polite an email is, on a scale from 1 (not polite at all) to 5 (very polite).\n"
                            "Respond ONLY with JSON:\n{\n\"score\": \"1-5\"\n}\nPlease ensure the complete JSON format is placed between the three quotes ``` ``` for easy extraction.\n\nEmail:\n\n")}
def _load_popquorn(attr="offensiveness", m=8, seed=0, max_chars=3000):
    sub = "offensiveness" if attr == "offensiveness" else "politeness_rating"
    d = pd.read_csv(f"{POPQ}/{sub}/raw_data.csv").dropna(subset=[attr]); rng = np.random.RandomState(seed)
    g = d.groupby("instance_id"); keep = [iid for iid, grp in g if len(grp) >= m]
    H = np.array([rng.permutation(g.get_group(iid)[attr].to_numpy(int))[:m] - 1 for iid in keep]); texts = [str(g.get_group(iid).text.iloc[0])[:max_chars] for iid in keep]
    assert H.min() >= 0 and H.max() <= 4
    tpl = _POPQ_TPL[attr]
    def prompt(text): return tpl + text + "\n\nEnd of the text. Please present your rating in the required JSON format."
    def prompt_hist(text, hist):
        blk = _GENERIC_HIST_HEAD.format(k=len(hist))
        for j, (t, lv) in enumerate(hist, 1): blk += f"### Item {j} (this rater's score: {lv})\n{_trunc(t, 1000)}\n\n"
        return tpl + blk + "### Item to evaluate\n" + text + "\n\nEnd of the text. Please present your rating in the required JSON format."
    return dict(name=f"popquorn_{attr}{m}", texts=texts, H=H, K=5, item_ids=np.array(keep), groups=np.array(keep), rater_ids=np.array([f"pos{i}" for i in range(m)]), prompt=prompt, prompt_hist=prompt_hist,
                LEVEL_STRS=[str(l + 1) for l in range(5)], PREFIX='```json\n{\n"score": "', model="Qwen/Qwen2.5-7B-Instruct")
def load_popquorn_off8(): return _load_popquorn("offensiveness", 8)
def load_popquorn_pol5(): return _load_popquorn("politeness", 5)
LOADERS.update({"popquorn_off8": load_popquorn_off8, "popquorn_pol5": load_popquorn_pol5})

# ----------------------------------------------------------------------------------------------- DICES-990 (Aroyo et al. 2023): 990 conversations × 69–76 ratings from 172 raters (not crossed) → m = 60 positions per item
DICES990 = LLMJ + "/paper-2/phase2/data/dices_repo/990/diverse_safety_adversarial_dialog_990.csv"
def load_dices990(m=60, seed=0, max_hist_chars=1200):
    d = pd.read_csv(DICES990); rng = np.random.RandomState(seed)
    items = d.groupby("item_id", sort=True).agg(context=("context", "first"), response=("response", "first")).reset_index(); g = d.groupby("item_id")
    lv = {l: i for i, l in enumerate(_DICES_LEVELS)}
    H = np.array([rng.permutation(g.get_group(iid).Q_overall.map(lv).to_numpy(int))[:m] for iid in items.item_id]); assert H.shape == (len(items), m) and H.min() >= 0 and H.max() <= 2
    texts = [f"{str(c).strip()}\nChatbot: {str(r).strip()}" for c, r in zip(items.context, items.response)]
    def prompt(text): return _DICES_TPL + "Conversation:\n\n" + text + "\n\nEnd of the conversation. Please present your rating in the required JSON format."
    def prompt_hist(text, hist):
        blk = _DICES_HIST_HEAD.format(k=len(hist))
        for j, (t, lv_) in enumerate(hist, 1): blk += f"### Conversation {j} (this rater's rating: {lv_})\n{_trunc(t, max_hist_chars)}\n\n"
        return _DICES_TPL + blk + "### Conversation to rate\n" + text + "\n\nEnd of the conversation. Please present your rating in the required JSON format."
    return dict(name="dices990", texts=texts, H=H, K=3, item_ids=items.item_id.to_numpy(), groups=items.item_id.to_numpy(), rater_ids=np.array([f"pos{i}" for i in range(m)]), prompt=prompt, prompt_hist=prompt_hist,
                LEVEL_STRS=[str(l) for l in range(3)], PREFIX='```json\n{\n"score": "', model="Qwen/Qwen2.5-7B-Instruct")
LOADERS.update({"dices990": load_dices990})

# ----------------------------------------------------------------------------------------------- ChaosNLI SNLI (1,514 items; c/e/n) and αNLI (1,532 items; 2 hypotheses) — same 100-annotation expansion as MNLI
CHAOS_SNLI = LLMJ + "/paper-2/phase2/data/chaosnli/chaos_snli.jsonl"; CHAOS_ANLI = LLMJ + "/paper-2/phase2/data/chaosnli/chaos_alphanli.jsonl"
_ANLI_TPL = ("You are an expert annotator for abductive natural language inference. Given two observations, decide which hypothesis better explains what happened between them:\n"
             "1 = hypothesis 1, 2 = hypothesis 2.\nRespond ONLY with JSON:\n{\n\"label\": \"1-2\"\n}\nPlease ensure the complete JSON format is placed between the three quotes ``` ``` for easy extraction.\n\n")
def load_chaosnli_snli(seed=0):
    import json
    rows = [json.loads(l) for l in open(CHAOS_SNLI)]; rng = np.random.RandomState(seed)
    H = np.array([rng.permutation(np.repeat([0, 1, 2], [r["label_counter"].get("c", 0), r["label_counter"].get("e", 0), r["label_counter"].get("n", 0)])) for r in rows], int); assert H.shape == (len(rows), 100)
    texts = [f"PREMISE: {r['example']['premise']}\nHYPOTHESIS: {r['example']['hypothesis']}" for r in rows]
    def prompt(text): return _NLI_TPL + text + "\n\nPlease present your label in the required JSON format."
    def prompt_hist(text, hist):
        blk = _GENERIC_HIST_HEAD.format(k=len(hist))
        for j, (t, lv) in enumerate(hist, 1): blk += f"### Item {j} (this rater's label: {lv})\n{_trunc(t, 800)}\n\n"
        return _NLI_TPL + blk + "### Item to label\n" + text + "\n\nPlease present your label in the required JSON format."
    return dict(name="chaosnli_snli", texts=texts, H=H, K=3, nominal=True, item_ids=np.array([r["uid"] for r in rows]), groups=np.array([r["uid"] for r in rows]), rater_ids=np.array([f"pos{i}" for i in range(100)]),
                prompt=prompt, prompt_hist=prompt_hist, LEVEL_STRS=["0", "1", "2"], PREFIX='```json\n{\n"label": "', model="Qwen/Qwen2.5-7B-Instruct")
def load_chaosnli_alphanli(seed=0):
    import json
    rows = [json.loads(l) for l in open(CHAOS_ANLI)]; rng = np.random.RandomState(seed)
    H = np.array([rng.permutation(np.repeat([0, 1], [r["label_counter"].get("1", 0), r["label_counter"].get("2", 0)])) for r in rows], int); assert H.shape == (len(rows), 100)
    texts = [f"OBSERVATION 1: {r['example']['obs1']}\nOBSERVATION 2: {r['example']['obs2']}\nHYPOTHESIS 1: {r['example']['hyp1']}\nHYPOTHESIS 2: {r['example']['hyp2']}" for r in rows]
    def prompt(text): return _ANLI_TPL + text + "\n\nPlease present your label in the required JSON format."
    def prompt_hist(text, hist):
        blk = _GENERIC_HIST_HEAD.format(k=len(hist))
        for j, (t, lv) in enumerate(hist, 1): blk += f"### Item {j} (this rater's label: {lv})\n{_trunc(t, 800)}\n\n"
        return _ANLI_TPL + blk + "### Item to label\n" + text + "\n\nPlease present your label in the required JSON format."
    return dict(name="chaosnli_alphanli", texts=texts, H=H, K=2, nominal=True, item_ids=np.array([r["uid"] for r in rows]), groups=np.array([r["uid"] for r in rows]), rater_ids=np.array([f"pos{i}" for i in range(100)]),
                prompt=prompt, prompt_hist=prompt_hist, LEVEL_STRS=["1", "2"], PREFIX='```json\n{\n"label": "', model="Qwen/Qwen2.5-7B-Instruct")
LOADERS.update({"chaosnli_snli": load_chaosnli_snli, "chaosnli_alphanli": load_chaosnli_alphanli})

# ----------------------------------------------------------------------------------------------- EmoBank (Buechel & Hahn 2017): 10k sentences × 5 reader ratings of valence (1–5); writer perspective and A/D dimensions available but not used (correlated criteria)
EMOBANK = LLMJ + "/paper-2/phase2/data/emobank/corpus"
_EMO_TPL = ("You are rating the emotional valence a READER would perceive in a sentence, on a scale from 1 (very negative) to 5 (very positive).\n"
            "Respond ONLY with JSON:\n{\n\"score\": \"1-5\"\n}\nPlease ensure the complete JSON format is placed between the three quotes ``` ``` for easy extraction.\n\nSentence:\n\n")
def load_emobank_reader_v5(dim="V", seed=0, n_max=3000):
    ind = pd.read_csv(f"{EMOBANK}/individual_reader_ratings.csv"); raw = pd.read_csv(f"{EMOBANK}/raw.csv"); rng = np.random.RandomState(seed)
    txt = dict(zip(raw.id, raw.text)); g = ind.groupby("id"); keep = [i for i, grp in g if len(grp) >= 5 and i in txt]
    keep = sorted(np.random.RandomState(seed).choice(keep, size=min(n_max, len(keep)), replace=False).tolist())   # fixed random subsample of 3,000 sentences (CPU feature-extraction budget; seed 0)
    H = np.array([rng.permutation(g.get_group(i)[dim].to_numpy(int))[:5] - 1 for i in keep]); assert H.min() >= 0 and H.max() <= 4
    texts = [str(txt[i]) for i in keep]
    def prompt(text): return _EMO_TPL + text + "\n\nEnd of the sentence. Please present your rating in the required JSON format."
    def prompt_hist(text, hist):
        blk = _GENERIC_HIST_HEAD.format(k=len(hist))
        for j, (t, lv) in enumerate(hist, 1): blk += f"### Item {j} (this rater's score: {lv})\n{_trunc(t, 500)}\n\n"
        return _EMO_TPL + blk + "### Item to evaluate\n" + text + "\n\nEnd of the sentence. Please present your rating in the required JSON format."
    return dict(name=f"emobank_reader_{dim}5", texts=texts, H=H, K=5, item_ids=np.array(keep), groups=np.array(keep), rater_ids=np.array([f"pos{i}" for i in range(5)]), prompt=prompt, prompt_hist=prompt_hist,
                LEVEL_STRS=[str(l + 1) for l in range(5)], PREFIX='```json\n{\n"score": "', model="Qwen/Qwen2.5-7B-Instruct")
LOADERS.update({"emobank_reader_v5": load_emobank_reader_v5})

# ----------------------------------------------------------------------------------------------- LeWiDi-2025 Conversational Sarcasm Corpus (CSC): context + response rated 1–6 for sarcasm by external observers; 6-observer subset (1,531 train + dev/test items)
CSC_DIR = LLMJ + "/paper-2/phase2/data/lewidi_csc"
_CSC_TPL = ("You are rating how sarcastic a RESPONSE is in the given conversational context, on a scale from 1 (not sarcastic at all) to 6 (extremely sarcastic).\n"
            "Respond ONLY with JSON:\n{\n\"score\": \"1-6\"\n}\nPlease ensure the complete JSON format is placed between the three quotes ``` ``` for easy extraction.\n\n")
def load_csc6(seed=0, max_chars=3000):
    import json, ast
    rows = {}
    for sp in ("train", "dev", "test"): rows.update(json.load(open(f"{CSC_DIR}/CSC_{sp}.json")))
    def obj(x): return ast.literal_eval(x) if isinstance(x, str) and x[:1] in "{[" else x        # fields are dicts in some files and stringified dicts in others
    keep = [(k, v) for k, v in rows.items() if int(v["number of annotations"]) == 6]; rng = np.random.RandomState(seed)
    H = np.array([rng.permutation([int(x) for x in obj(v["annotations"]).values()]) - 1 for k, v in keep]); assert H.shape[1] == 6 and H.min() >= 0 and H.max() <= 5
    def fmt(v):
        t = obj(v["text"]); t = t if isinstance(t, dict) else {"context": "", "response": str(t)}
        return f"CONTEXT: {str(t.get('context', ''))[:max_chars]}\nRESPONSE: {str(t.get('response', ''))[:max_chars]}"
    texts = [fmt(v) for k, v in keep]; groups = np.array([str((obj(v["other_info"]) or {}).get("context+speaker", k)).split("_")[0] for k, v in keep])
    def prompt(text): return _CSC_TPL + text + "\n\nEnd of the conversation. Please present your rating in the required JSON format."
    def prompt_hist(text, hist):
        blk = _GENERIC_HIST_HEAD.format(k=len(hist))
        for j, (t, lv) in enumerate(hist, 1): blk += f"### Item {j} (this rater's score: {lv})\n{_trunc(t, 1000)}\n\n"
        return _CSC_TPL + blk + "### Item to evaluate\n" + text + "\n\nEnd of the conversation. Please present your rating in the required JSON format."
    return dict(name="csc6", texts=texts, H=H, K=6, item_ids=np.array([k for k, v in keep]), groups=groups, rater_ids=np.array([f"pos{i}" for i in range(6)]), prompt=prompt, prompt_hist=prompt_hist,
                LEVEL_STRS=[str(l + 1) for l in range(6)], PREFIX='```json\n{\n"score": "', model="Qwen/Qwen2.5-7B-Instruct")
LOADERS.update({"csc6": load_csc6})

# ----------------------------------------------------------------------------------------------- Dorn (2012) readability: 360 snippets (Java 121 / Python 119 / CUDA 120) × 161–267 ratings each from 5,468 developers (each rated ~5 snippets), 1–5 Likert, K=5
# Source: Scalabrino's replication site (DatasetDorn.zip; code/code_readability/data/SOURCE.md). scores/<lang>.csv: one row per annotator (first column = annotator id), one column per snippet,
# columns assumed to follow the sorted snippet-file ids (java 101..221, python/cuda 0..118/119); the learner-free analyses do not depend on this mapping, the feature-based ones do.
# Raters are not persistent across items (median 5 ratings each) → m fixed POSITIONS per item from a seeded random subsample of the item's ratings (as DICES-990 / POPQUORN).
DORN = LLMJ + "/code/code_readability/data/dorn"
def _load_dorn(langs=("java",), m=160, seed=0, max_hist_chars=1500):
    rng = np.random.RandomState(seed); Hs, texts, ids, groups = [], [], [], []
    for lang in langs:
        S = pd.read_csv(f"{DORN}/scores/{lang}.csv", header=None).iloc[:, 1:]
        snips = sorted(int(f.split(".")[0]) for f in os.listdir(f"{DORN}/snippets/{lang}")); assert len(snips) == S.shape[1], (lang, len(snips), S.shape)
        for j, sid in enumerate(snips):
            r = S.iloc[:, j].dropna().to_numpy(int); assert len(r) >= m and r.min() >= 1 and r.max() <= 5, (lang, sid, len(r))
            Hs.append(rng.permutation(r)[:m] - 1); texts.append(open(f"{DORN}/snippets/{lang}/{sid}.jsnp", encoding="utf-8", errors="replace").read()); ids.append(f"{lang}_{sid}"); groups.append(f"{lang}_{sid}")
    H = np.array(Hs); bw = load_bw(max_hist_chars)          # same CoReEval Java template / history block as Buse–Weimer and Scalabrino
    name = "dorn_all" if len(langs) == 3 else f"dorn_{langs[0]}"
    return dict(name=name, texts=texts, H=H, K=5, item_ids=np.array(ids), groups=np.array(groups), rater_ids=np.array([f"pos{i}" for i in range(m)]), prompt=bw["prompt"], prompt_hist=bw["prompt_hist"],
                LEVEL_STRS=bw["LEVEL_STRS"], PREFIX=bw["PREFIX"], model="Qwen/Qwen2.5-Coder-7B-Instruct")
def load_dorn_java(): return _load_dorn(("java",))
def load_dorn_python(): return _load_dorn(("python",))
def load_dorn_cuda(): return _load_dorn(("cuda",))
def load_dorn_all(): return _load_dorn(("java", "python", "cuda"))
LOADERS.update({"dorn_java": load_dorn_java, "dorn_python": load_dorn_python, "dorn_cuda": load_dorn_cuda, "dorn_all": load_dorn_all})

# ----------------------------------------------------------------------------------------------- SE multi-rater panels added 2026-10-26 (data/SE_PANELS_SOURCE.md). Generic prompt scaffolding; the learner-free analyses use H only.
SEDATA = LLMJ + "/paper-2/phase2/data"
def _generic_prompts(tpl, lv_offset=0):
    def prompt(text): return tpl + text + "\n\nEnd of the item. Please present your rating in the required JSON format."
    def prompt_hist(text, hist):
        blk = _GENERIC_HIST_HEAD.format(k=len(hist))
        for j, (t, lv) in enumerate(hist, 1): blk += f"### Item {j} (this rater's score: {lv + lv_offset})\n{_trunc(t, 1200)}\n\n"
        return tpl + blk + "### Item to evaluate\n" + text + "\n\nEnd of the item. Please present your rating in the required JSON format."
    return prompt, prompt_hist

# Crupi et al. 2025 code-summarization benchmark: 1,163 (function, generator) summaries × 3 expert raters × {CA, Conciseness, Fluency}, 1–5; Java + Python pooled; groups = function (target_id)
_CRUPI_TPL = {"CA": "Rate the CONTENT ADEQUACY of the summary for the given code (1 = misses or misstates the code's purpose, 5 = fully captures it).\n",
              "Conciseness": "Rate the CONCISENESS of the summary for the given code (1 = verbose or redundant, 5 = concise).\n",
              "Fluency": "Rate the FLUENCY and understandability of the summary (1 = hard to read, 5 = fluent).\n"}
def _load_crupi(crit="CA", max_chars=3000):
    d = pd.concat([pd.read_csv(f"{SEDATA}/crupi2025/CS-benchmark-{L}.csv").assign(lang=L) for L in ("Java", "Python")], ignore_index=True)
    H = d[[f"{crit}_{i}" for i in (1, 2, 3)]].to_numpy(int) - 1; assert H.min() >= 0 and H.max() <= 4
    texts = [f"CODE:\n{str(c)[:max_chars]}\n\nSUMMARY:\n{str(s)[:max_chars]}" for c, s in zip(d.target, d.summary_postprocessed)]
    tpl = _CRUPI_TPL[crit] + "Respond ONLY with JSON:\n{\n\"score\": \"1-5\"\n}\nPlease ensure the complete JSON format is placed between the three quotes ``` ``` for easy extraction.\n\n"
    prompt, prompt_hist = _generic_prompts(tpl, 1)
    return dict(name=f"crupi_{crit.lower()}", texts=texts, H=H, K=5, item_ids=np.array([f"{l}_{t}_{g}" for l, t, g in zip(d.lang, d.target_id, d.generated_by)]), groups=np.array([f"{l}_{t}" for l, t in zip(d.lang, d.target_id)]),
                rater_ids=np.array(["expert1", "expert2", "expert3"]), prompt=prompt, prompt_hist=prompt_hist, LEVEL_STRS=[str(l) for l in range(1, 6)], PREFIX='```json\n{\n"score": "', model="Qwen/Qwen2.5-Coder-7B-Instruct")
LOADERS.update({"crupi_ca": lambda: _load_crupi("CA"), "crupi_conc": lambda: _load_crupi("Conciseness"), "crupi_flu": lambda: _load_crupi("Fluency")})

# Sergeyuk et al. 2024 (JetBrains) readability: 120 AI-generated Java snippets × 11–31 professional developers; 12 bipolar aspects −2..+2 (K=5) → m = 11 positions (seeded subsample); groups = snippet
JB_ASPECTS = ("short", "top_bottom", "sufficient_info", "clear_goal", "basic", "logical_separation", "flat", "action_per_line", "constants", "naming", "style_guide", "balance")
def _load_jb(aspect="naming", m=11, seed=0, max_chars=3000):
    a = pd.read_csv(f"{SEDATA}/jetbrains_readability/data/aggregated.csv"); s = pd.read_csv(f"{SEDATA}/jetbrains_readability/data/snippets.csv").set_index("snip_id")
    a["sid"] = a.snippet.str.replace(".png", "", regex=False); rng = np.random.RandomState(seed); g = a.groupby("sid"); keep = sorted(k for k, grp in g if len(grp) >= m)
    H = np.array([rng.permutation(g.get_group(k)[aspect].to_numpy(int))[:m] + 2 for k in keep]); assert H.min() >= 0 and H.max() <= 4
    texts = [str(s.loc[k, "snippet"])[:max_chars] if k in s.index else k for k in keep]
    tpl = (f"You are an experienced Java developer. Rate the following code on the aspect '{aspect.replace('_', ' ')}' of readability on a scale from -2 (strongly disagree) to +2 (strongly agree).\n"
           "Respond ONLY with JSON:\n{\n\"score\": \"-2..2\"\n}\nPlease ensure the complete JSON format is placed between the three quotes ``` ``` for easy extraction.\n\n")
    prompt, prompt_hist = _generic_prompts(tpl, -2)
    return dict(name=f"jb_{aspect}", texts=texts, H=H, K=5, item_ids=np.array(keep), groups=np.array(keep), rater_ids=np.array([f"pos{i}" for i in range(m)]), prompt=prompt, prompt_hist=prompt_hist,
                LEVEL_STRS=[str(l) for l in range(-2, 3)], PREFIX='```json\n{\n"score": "', model="Qwen/Qwen2.5-Coder-7B-Instruct")
LOADERS.update({f"jb_{asp}": (lambda asp=asp: _load_jb(asp)) for asp in JB_ASPECTS})

# Roy et al. FSE 2021 code-summarization human study: (function, system) summaries with >= m ratings (m = 3; 226 raters), 0–5 in half points → 11 ordinal levels (K = 11); groups = function; summary texts not shipped (placeholder)
def _load_roy(crit="Content Adequacy", m=3, seed=0):
    r = pd.read_csv(f"{SEDATA}/roy2021/responses.csv").dropna(subset=[crit]); rng = np.random.RandomState(seed); g = r.groupby(["question_id", "mid"]); keep = [k for k, grp in g if len(grp) >= m]
    H = np.array([rng.permutation(np.round(g.get_group(k)[crit].to_numpy(float) * 2).astype(int))[:m] for k in keep]); assert H.min() >= 0 and H.max() <= 10
    ids = np.array([f"{q}_{mid}" for q, mid in keep]); texts = [f"[Roy et al. 2021 summary {i}; text not shipped]" for i in ids]
    prompt, prompt_hist = _generic_prompts("Rate the summary (0–5).\nRespond ONLY with JSON:\n{\n\"score\": \"0-5\"\n}\n\n")
    short = {"Content Adequacy": "ca", "Conciseness": "conc", "Fluency": "flu"}[crit]
    return dict(name=f"roy_{short}", texts=texts, H=H, K=11, item_ids=ids, groups=np.array([str(q) for q, mid in keep]), rater_ids=np.array([f"pos{i}" for i in range(m)]), prompt=prompt, prompt_hist=prompt_hist,
                LEVEL_STRS=[str(l / 2) for l in range(11)], PREFIX='```json\n{\n"score": "', model="Qwen/Qwen2.5-Coder-7B-Instruct")
LOADERS.update({"roy_ca": lambda: _load_roy("Content Adequacy"), "roy_conc": lambda: _load_roy("Conciseness"), "roy_flu": lambda: _load_roy("Fluency")})

# MLCQ (Madeyski & Lewowski 2020) code-smell severity: (sample, smell) pairs with >= 3 professional reviews (2,041 items; m = 3 positions), none < minor < major < critical (K = 4); groups = sample; code via permalink (not inline)
def load_mlcq3(m=3, seed=0):
    d = pd.read_csv(f"{SEDATA}/mlcq/MLCQCodeSmellSamples.csv", sep=";"); lv = {"none": 0, "minor": 1, "major": 2, "critical": 3}; rng = np.random.RandomState(seed)
    g = d.groupby(["sample_id", "smell"]); keep = [k for k, grp in g if len(grp) >= m]
    H = np.array([rng.permutation(g.get_group(k).severity.map(lv).to_numpy(int))[:m] for k in keep]); assert H.min() >= 0 and H.max() <= 3
    texts = [f"{g.get_group(k).code_name.iloc[0]} ({k[1]}) {g.get_group(k).link.iloc[0]}" for k in keep]
    prompt, prompt_hist = _generic_prompts("Rate the severity of the code smell (0 = none, 1 = minor, 2 = major, 3 = critical).\nRespond ONLY with JSON:\n{\n\"score\": \"0-3\"\n}\n\n")
    return dict(name="mlcq3", texts=texts, H=H, K=4, item_ids=np.array([f"{s}_{sm.replace(' ', '-')}" for s, sm in keep]), groups=np.array([str(s) for s, sm in keep]), rater_ids=np.array([f"pos{i}" for i in range(m)]),
                prompt=prompt, prompt_hist=prompt_hist, LEVEL_STRS=[str(l) for l in range(4)], PREFIX='```json\n{\n"score": "', model="Qwen/Qwen2.5-Coder-7B-Instruct")
LOADERS.update({"mlcq3": load_mlcq3})
