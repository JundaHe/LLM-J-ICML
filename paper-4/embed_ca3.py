"""Stage 13 S13-3 Am. 3 (PROTOCOL_STAGE13.md): history-conditioned Qwen2.5-7B-Instruct features for CA third turns, label-blind with respect to third-turn choices.
For each complete third-turn conversation: E_R[c, x] = final-token state of (history, response x), E_P[c] = state of the history alone. Resumable (30-min checkpoints)."""
import os, sys, time, numpy as np, pandas as pd, torch
HERE = os.path.dirname(os.path.abspath(__file__)); P2 = os.path.abspath(os.path.join(HERE, "..", "paper-2", "phase2")); sys.path.insert(0, P2)
import data_panels
from transformers import AutoTokenizer, AutoModelForCausalLM
T1, T2, T3 = "first_turn_", "second_turn_", "third_turn_"
c = ["conversation_id"] + [t + "prompt" for t in (T1, T2, T3)] + [T1 + "preferred_response", T2 + "preferred_response"] + [f"{t}response_{x}" for t in (T1, T2, T3) for x in "abcd"]
d = pd.read_csv(data_panels.CA_CSV, usecols=c).sort_values("conversation_id").reset_index(drop=True)   # no third-turn preference, no feedback column
ok = d[[f"{T3}response_{x}" for x in "abcd"]].notna().all(1) & d[T3 + "prompt"].notna() & d[T1 + "prompt"].notna() & d[T2 + "prompt"].notna()
for t in (T1, T2): ok &= d[t + "preferred_response"].isin([f"response_{x}" for x in "abcd"])
d = d[ok].reset_index(drop=True)
def history(r):
    ex = [(str(r[T1 + "prompt"])[:4000], str(r[T1 + r[T1 + "preferred_response"]])[:4000]), (str(r[T2 + "prompt"])[:4000], str(r[T2 + r[T2 + "preferred_response"]])[:4000])]; cur = str(r[T3 + "prompt"])[:4000]
    while ex and sum(len(a) + len(b) for a, b in ex) + len(cur) > 6000: ex = ex[1:]
    return [m for a, b in ex for m in ({"role": "user", "content": a}, {"role": "assistant", "content": b})] + [{"role": "user", "content": cur}]
MODEL = "Qwen/Qwen2.5-7B-Instruct"; tok = AutoTokenizer.from_pretrained(MODEL); tok.padding_side = "right"
H = [history(r) for _, r in d.iterrows()]; strs = []
for h, (_, r) in zip(H, d.iterrows()):
    strs += [tok.apply_chat_template(h + [{"role": "assistant", "content": str(r[f"{T3}response_{x}"])[:4000]}], tokenize=False) for x in "abcd"] + [tok.apply_chat_template(h, tokenize=False, add_generation_prompt=True)]
print(f"{len(d)} conversations, {len(strs)} texts", flush=True)
model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.bfloat16, device_map="cuda"); model.eval()
lens = np.array([len(s) for s in strs]); order = np.argsort(-lens); emb = np.zeros((len(strs), 3584), np.float16); MAXTOK = 24000; i = 0; done = 0
out = f"{P2}/features/ca_third_hist"; os.makedirs(out, exist_ok=True); CK = f"{out}/ckpt.npz"; t_ck = time.time()
if os.path.exists(CK):
    z = np.load(CK); assert z["emb"].shape == emb.shape; emb[:] = z["emb"]; i = done = int(z["i"]); print(f"resumed at {i}", flush=True)
with torch.no_grad():
    while i < len(order):
        L0 = len(tok(strs[order[i]], add_special_tokens=False).input_ids); bs = max(1, min(64, MAXTOK // max(L0, 1))); idx = order[i:i + bs]
        enc = tok([strs[j] for j in idx], add_special_tokens=False, return_tensors="pt", padding=True).to("cuda")
        h = model.model(input_ids=enc.input_ids, attention_mask=enc.attention_mask).last_hidden_state; last = enc.attention_mask.sum(1) - 1
        emb[idx] = h[torch.arange(len(idx)), last].float().cpu().numpy().astype(np.float16); i += bs; done += len(idx)
        if done // 10000 != (done - len(idx)) // 10000: print(f"{done}/{len(strs)}", flush=True)
        if time.time() - t_ck > 1800: np.savez(CK + ".tmp.npz", emb=emb, i=i); os.replace(CK + ".tmp.npz", CK); t_ck = time.time(); print(f"checkpoint at {i}", flush=True)
E = emb.reshape(len(d), 5, 3584); np.savez(f"{out}/hist_Qwen2.5-7B-Instruct.npz", conversation_id=d.conversation_id.astype(str).to_numpy(), E_R=E[:, :4], E_P=E[:, 4]); print("saved", E.shape, flush=True)
if os.path.exists(CK): os.remove(CK)
