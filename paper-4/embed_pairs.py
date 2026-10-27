"""Stage 2c (PROTOCOL_STAGE2C.md): per-response embeddings for the VPL / PAL reimplementations on MultiPref.
For every comparison: last-token final-layer hidden state of the chat (user: prompt, assistant: response A) → E_A, same for B → E_B, and of the prompt alone (user turn + generation prompt) → E_P.
Writes paper-2/phase2/features/multipref_overall/pairs_Qwen2.5-7B-Instruct.npz (float16; not tracked)."""
import os, sys, json, numpy as np, torch
HERE = os.path.dirname(os.path.abspath(__file__)); P2 = os.path.abspath(os.path.join(HERE, "..", "paper-2", "phase2")); sys.path.insert(0, P2)
import data_panels
from transformers import AutoTokenizer, AutoModelForCausalLM
MODEL = "Qwen/Qwen2.5-7B-Instruct"; tok = AutoTokenizer.from_pretrained(MODEL); model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.bfloat16, device_map="cuda"); model.eval()
rows = [json.loads(l) for l in open(data_panels.MULTIPREF)]; MC = 2500
def emb(msgs, gen):
    t = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=gen); ids = tok(t, add_special_tokens=False, return_tensors="pt").input_ids.to("cuda")
    return model(input_ids=ids, output_hidden_states=True).hidden_states[-1][0, -1].float().cpu().numpy().astype(np.float16)
EA, EB, EP = [], [], []
with torch.no_grad():
    for i, r in enumerate(rows):
        p = str(r["text"])[:MC]
        EP.append(emb([{"role": "user", "content": p}], True))
        EA.append(emb([{"role": "user", "content": p}, {"role": "assistant", "content": str(r["completion_a"])[:MC]}], False))
        EB.append(emb([{"role": "user", "content": p}, {"role": "assistant", "content": str(r["completion_b"])[:MC]}], False))
        if (i + 1) % 500 == 0: print(f"{i+1}/{len(rows)}", flush=True)
out = f"{P2}/features/multipref_overall/pairs_Qwen2.5-7B-Instruct.npz"
np.savez(out, E_A=np.array(EA), E_B=np.array(EB), E_P=np.array(EP), item_ids=np.array([r["comparison_id"] for r in rows]).astype(str)); print("saved", out)
