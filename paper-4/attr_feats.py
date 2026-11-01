"""Stage 9 (PROTOCOL_STAGE9.md): the SAP attribute dictionary — 24 interpretable attribute differences attr(B) − attr(A) of a response pair, standardised over items.
Counts enter as log(1 + count), ratios / means as plain differences; attribute 1 is the log length ratio."""
import re, numpy as np
from sem_feats import LIST, PHR as HEDGE
NAMES = ["length", "list/heading lines", "hedging/refusal", "code blocks", "bold/italic", "digits", "question marks", "exclamation marks", "first person", "second person",
         "sentence length", "word length", "paragraphs", "URLs", "examples", "safety/disclaimer", "summary markers", "emojis", "evidence phrases", "politeness",
         "strict refusal", "type-token ratio", "prompt overlap", "headings"]
WORD = re.compile(r"[a-zA-Z']+"); SENT = re.compile(r"[.!?]+(?:\s|$)"); EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")
PH = {"examples": ("for example", "e.g.", "for instance", "such as"), "safety": ("consult", "professional", "not a substitute", "seek medical", "seek help", "disclaimer"),
      "summary": ("in summary", "in conclusion", "overall", "to summarize", "in short"), "evidence": ("according to", "studies", "research", "evidence", "source"),
      "polite": ("please", "thank", "glad", "happy to", "great question"), "refuse": ("i cannot", "i can't", "i won't", "unable to", "not able to")}
def _cnt(t, ph): return sum(t.count(p) for p in ph)
def attrs(resp, prompt):
    t = resp.replace("’", "'"); lo = t.lower(); w = WORD.findall(lo); nw = max(1, len(w)); ns = max(1, len(SENT.findall(t))); pw = set(WORD.findall(prompt.lower()))
    L = np.log1p
    return np.array([np.log(max(1, len(t))), L(len(LIST.findall(t))), L(_cnt(lo, HEDGE)), L(t.count("```") // 2), L(len(re.findall(r"\*\*[^*]+\*\*|__[^_]+__|(?<!\*)\*[^*\s][^*]*\*(?!\*)", t))),
                     L(len(re.findall(r"\d", t))), L(t.count("?")), L(t.count("!")), L(sum(x in ("i", "me", "my", "mine", "i'm", "i've", "i'd", "i'll") for x in w)),
                     L(sum(x in ("you", "your", "yours", "you're", "you've", "you'll") for x in w)), nw / ns, np.mean([len(x) for x in w]) if w else 0.0,
                     L(len([p for p in re.split(r"\n\s*\n", t) if p.strip()])), L(len(re.findall(r"https?://", t))), L(_cnt(lo, PH["examples"])), L(_cnt(lo, PH["safety"])),
                     L(_cnt(lo, PH["summary"])), L(len(EMOJI.findall(t))), L(_cnt(lo, PH["evidence"])), L(_cnt(lo, PH["polite"])), L(_cnt(lo, PH["refuse"])),
                     len(set(w)) / nw, len(set(w) & pw) / max(1, len(set(w))), L(len(re.findall(r"^\s*#+\s", t, re.M)))], float)
def attr_G(A, B, P):
    """A, B: response texts; P: prompts (lists of equal length) → (n, 24) standardised differences"""
    D = np.stack([attrs(str(b), str(p)) - attrs(str(a), str(p)) for a, b, p in zip(A, B, P)]); sd = D.std(0); sd[sd == 0] = 1.0
    return (D - D.mean(0)) / sd
def multipref_G(raw): return attr_G([r["completion_a"] for r in raw], [r["completion_b"] for r in raw], [r["text"] for r in raw])
