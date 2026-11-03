"""Stage 8 (PROTOCOL_STAGE8.md): Qwen2.5-7B-Instruct features for Community Alignment first-turn pairs. E_A / E_B = last-layer state at the final token of the
chat-formatted (prompt, response) of each response (each text truncated at 4,000 characters); E_P = the same for the prompt alone. Unique texts are embedded once,
in length-sorted batches. Writes paper-2/phase2/features/ca_pairs/pairs_Qwen2.5-7B-Instruct.npz (not tracked)."""
import os, sys, numpy as np, torch
HERE = os.path.dirname(os.path.abspath(__file__)); P2 = os.path.abspath(os.path.join(HERE, "..", "paper-2", "phase2")); sys.path.insert(0, P2)
import data_panels
from transformers import AutoTokenizer, AutoModelForCausalLM
P = data_panels.load(os.environ.get("CA_PANEL", "ca_pairs")); MODEL = "Qwen/Qwen2.5-7B-Instruct"
tok = AutoTokenizer.from_pretrained(MODEL); tok.padding_side = "right"
model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.bfloat16, device_map="cuda"); model.eval()
def chat(p, r=None):
    m = [{"role": "user", "content": p[:4000]}] + ([{"role": "assistant", "content": r[:4000]}] if r is not None else [])
    return tok.apply_chat_template(m, tokenize=False, add_generation_prompt=r is None)
keys = sorted({(p, a) for p, a in zip(P["texts"], P["resp_A"])} | {(p, b) for p, b in zip(P["texts"], P["resp_B"])}) + [(p, None) for p in sorted(set(P["texts"]))]
strs = [chat(p, r) for p, r in keys]; lens = np.array([len(s) for s in strs]); order = np.argsort(-lens); emb = np.zeros((len(keys), 3584), np.float16)
print(f"{len(keys)} unique texts", flush=True); MAXTOK = 24000; i = 0; done = 0
with torch.no_grad():
    while i < len(order):
        L0 = len(tok(strs[order[i]], add_special_tokens=False).input_ids); bs = max(1, min(64, MAXTOK // max(L0, 1))); idx = order[i:i + bs]
        enc = tok([strs[j] for j in idx], add_special_tokens=False, return_tensors="pt", padding=True).to("cuda")
        h = model.model(input_ids=enc.input_ids, attention_mask=enc.attention_mask).last_hidden_state; last = enc.attention_mask.sum(1) - 1
        emb[idx] = h[torch.arange(len(idx)), last].float().cpu().numpy().astype(np.float16); i += bs; done += len(idx)
        if done // 10000 != (done - len(idx)) // 10000: print(f"{done}/{len(keys)}", flush=True)
pos = {k: j for j, k in enumerate(keys)}
EA = emb[[pos[(p, a)] for p, a in zip(P["texts"], P["resp_A"])]]; EB = emb[[pos[(p, b)] for p, b in zip(P["texts"], P["resp_B"])]]; EP = emb[[pos[(p, None)] for p in P["texts"]]]
out = f"{P2}/features/{P['name']}"; os.makedirs(out, exist_ok=True); np.savez(f"{out}/pairs_Qwen2.5-7B-Instruct.npz", E_A=EA, E_B=EB, E_P=EP, item_ids=np.asarray(P["item_ids"]).astype(str)); print("saved", EA.shape, flush=True)
