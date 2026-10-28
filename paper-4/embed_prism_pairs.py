"""Stage 2c Amendment 4: features for PRISM pairs. E_A / E_B = the stage-2a PRISM per-utterance judge-prompt embeddings (features/prism/Qwen2.5-7B-Instruct.npz, E_last) of the two
responses; E_P = last-token final-layer state of the user prompt alone (new extraction, same model). Writes paper-2/phase2/features/prism_pairs/pairs_Qwen2.5-7B-Instruct.npz (not tracked)."""
import os, sys, numpy as np, torch
HERE = os.path.dirname(os.path.abspath(__file__)); P2 = os.path.abspath(os.path.join(HERE, "..", "paper-2", "phase2")); sys.path.insert(0, P2)
import data_panels
from transformers import AutoTokenizer, AutoModelForCausalLM
P = data_panels.load("prism_pairs"); F = np.load(f"{P2}/features/prism/Qwen2.5-7B-Instruct.npz", allow_pickle=True)
pos = {str(u): j for j, u in enumerate(F["item_ids"])}; E = F["E_last"]
EA = np.stack([E[pos[u]] for u in P["utt_A"]]).astype(np.float16); EB = np.stack([E[pos[u]] for u in P["utt_B"]]).astype(np.float16)
MODEL = "Qwen/Qwen2.5-7B-Instruct"; tok = AutoTokenizer.from_pretrained(MODEL); model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.bfloat16, device_map="cuda"); model.eval()
uniq = sorted(set(P["texts"])); emb = {}
with torch.no_grad():
    for i, t in enumerate(uniq):
        s = tok.apply_chat_template([{"role": "user", "content": t[:2500]}], tokenize=False, add_generation_prompt=True)
        ids = tok(s, add_special_tokens=False, return_tensors="pt").input_ids.to("cuda"); emb[t] = model(input_ids=ids, output_hidden_states=True).hidden_states[-1][0, -1].float().cpu().numpy().astype(np.float16)
        if (i + 1) % 2000 == 0: print(f"{i+1}/{len(uniq)}", flush=True)
EP = np.stack([emb[t] for t in P["texts"]])
out = f"{P2}/features/prism_pairs"; os.makedirs(out, exist_ok=True); np.savez(f"{out}/pairs_Qwen2.5-7B-Instruct.npz", E_A=EA, E_B=EB, E_P=EP, item_ids=np.asarray(P["item_ids"]).astype(str)); print("saved", EA.shape)
