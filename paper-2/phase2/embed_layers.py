"""
Per-layer frozen representations (DECODING_PROTOCOL.md Amendment 2 — INSPECTOR-style probing, Li et al. ICLR 2026): for every item, mean- and last-token-pooled hidden
states at EVERY layer, each layer reduced by a label-free PCA to d_pre components (fitted on the panel's items; no ratings used) so the file stays small.
Writes features_layers/<panel>/<model_tag>.npz with  mean[L, n, d_pre], last[L, n, d_pre], item_ids, layers, explained[L, 2]
Usage: python embed_layers.py --panel summeval_coherence8 [--model ...] [--d_pre 128]
"""
import argparse, os, sys, numpy as np, torch
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import data_panels
from transformers import AutoTokenizer, AutoModelForCausalLM
p = argparse.ArgumentParser(); p.add_argument("--panel", required=True); p.add_argument("--model", default=None); p.add_argument("--d_pre", type=int, default=128); p.add_argument("--dtype", default="bf16")
args = p.parse_args(); PAN = data_panels.load(args.panel); MODEL = args.model or PAN["model"]; tag = MODEL.split("/")[-1]
out_dir = f"{HERE}/features_layers/{args.panel}"; os.makedirs(out_dir, exist_ok=True)
tok = AutoTokenizer.from_pretrained(MODEL); model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=(torch.bfloat16 if args.dtype == "bf16" else torch.float32), device_map="cuda"); model.eval()
n = len(PAN["texts"]); L = model.config.num_hidden_layers + 1; d = model.config.hidden_size
MEAN = np.zeros((L, n, d), np.float32); LAST = np.zeros((L, n, d), np.float32)
with torch.no_grad():
    for i, t in enumerate(PAN["texts"]):
        text = tok.apply_chat_template([{"role": "user", "content": PAN["prompt"](t)}], tokenize=False, add_generation_prompt=True) + PAN["PREFIX"]
        ids = tok(text, add_special_tokens=False, return_tensors="pt").input_ids.to("cuda")
        hs = model(input_ids=ids, output_hidden_states=True).hidden_states
        for l in range(L): h = hs[l][0].float(); MEAN[l, i] = h.mean(0).cpu().numpy(); LAST[l, i] = h[-1].cpu().numpy()
        if (i + 1) % 100 == 0: print(f"{i+1}/{n}", flush=True)
dp = min(args.d_pre, n - 1); mean_r = np.zeros((L, n, dp), np.float32); last_r = np.zeros((L, n, dp), np.float32); expl = np.zeros((L, 2))
for l in range(L):
    for k, (X, R) in enumerate(((MEAN[l], mean_r), (LAST[l], last_r))):
        mu = X.mean(0); U, S, Vt = np.linalg.svd(X - mu, full_matrices=False); R[l] = (X - mu) @ Vt[:dp].T; expl[l, k] = float((S[:dp] ** 2).sum() / (S ** 2).sum())
np.savez(f"{out_dir}/{tag}.npz", mean=mean_r, last=last_r, item_ids=PAN["item_ids"], layers=np.arange(L), explained=expl, model=MODEL, d_pre=dp)
print("saved", f"{out_dir}/{tag}.npz", mean_r.shape, "explained var (mean/last) at mid layer", expl[L // 2].round(3), flush=True)
