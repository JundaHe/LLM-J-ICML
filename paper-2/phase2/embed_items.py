"""
Frozen item representations for the Stage-A (small-head) experiments.
For each panel, run the base LLM once over the bare task prompt of every item and store
  E_last  (n_items x d)  hidden state of the last prompt token at the final layer  (= the state that would emit the score token)
  E_mean  (n_items x d)  mean over prompt tokens at the final layer
  Q0      (n_items x K)  the frozen model's own zero-shot score pmf (for a no-training baseline)
Usage: python embed_items.py --panel dices [--model Qwen/Qwen2.5-7B-Instruct] [--layer -1]
Writes phase2/features/{panel}/{model_tag}.npz
"""
import argparse, os, sys, numpy as np, torch
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import data_panels
from transformers import AutoTokenizer, AutoModelForCausalLM
p = argparse.ArgumentParser(); p.add_argument("--panel", required=True); p.add_argument("--model", default=None); p.add_argument("--layer", type=int, default=-1); p.add_argument("--device", default="cuda"); p.add_argument("--dtype", default="bf16")
args = p.parse_args(); PAN = data_panels.load(args.panel); MODEL = args.model or PAN["model"]; tag = MODEL.split("/")[-1]
out_dir = f"{HERE}/features/{args.panel}"; os.makedirs(out_dir, exist_ok=True)
tok = AutoTokenizer.from_pretrained(MODEL); DEV = args.device; model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=(torch.bfloat16 if args.dtype == "bf16" else torch.float32), device_map=DEV); model.eval()
level_ids = torch.tensor([tok.encode(s, add_special_tokens=False)[0] for s in PAN["LEVEL_STRS"]], device=DEV)
E_last, E_mean, Q0 = [], [], []
with torch.no_grad():
    for i, t in enumerate(PAN["texts"]):
        text = tok.apply_chat_template([{"role": "user", "content": PAN["prompt"](t)}], tokenize=False, add_generation_prompt=True) + PAN["PREFIX"]
        ids = tok(text, add_special_tokens=False, return_tensors="pt").input_ids.to(DEV)
        o = model(input_ids=ids, output_hidden_states=True); h = o.hidden_states[args.layer][0].float()
        E_last.append(h[-1].cpu().numpy()); E_mean.append(h.mean(0).cpu().numpy())
        Q0.append(torch.softmax(o.logits[0, -1][level_ids].float(), -1).cpu().numpy())
        if (i + 1) % 50 == 0: print(f"{i+1}/{len(PAN['texts'])}", flush=True)
np.savez(f"{out_dir}/{tag}.npz", E_last=np.array(E_last), E_mean=np.array(E_mean), Q0=np.array(Q0), item_ids=PAN["item_ids"], model=MODEL, layer=args.layer)
print("saved", f"{out_dir}/{tag}.npz", np.array(E_last).shape, "zero-shot mean pmf", np.array(Q0).mean(0).round(3))
