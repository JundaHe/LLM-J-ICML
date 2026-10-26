"""
ask_disagreement — G3 predictor (iii): ask the frozen LLM directly how much annotators would disagree about each item (1 = everyone agrees … 5 = strongly divided), read the
expected value from the score-token distribution (decoding-free). Writes paper-3/results/ask/<panel>.npz with `disagree` (n,) and `pmf` (n,5), aligned with the paper-2 panel rows.
Usage: python ask_disagreement.py --panel dices [--model Qwen/Qwen2.5-7B-Instruct]
"""
import argparse, os, sys, numpy as np, torch
HERE = os.path.dirname(os.path.abspath(__file__)); P2 = os.path.abspath(os.path.join(HERE, "..", "paper-2", "phase2")); sys.path.insert(0, P2)
import data_panels
from transformers import AutoTokenizer, AutoModelForCausalLM
ap = argparse.ArgumentParser(); ap.add_argument("--panel", required=True); ap.add_argument("--model", default=None); args = ap.parse_args()
PAN = data_panels.load(args.panel); MODEL = args.model or PAN["model"]
tok = AutoTokenizer.from_pretrained(MODEL); model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.bfloat16, device_map="cuda"); model.eval()
ids5 = torch.tensor([tok.encode(str(k), add_special_tokens=False)[0] for k in range(1, 6)], device="cuda")
HEAD = ("Several human annotators will each rate the item below (the original rating instruction is quoted first). Do NOT rate the item yourself. Instead, estimate how much the annotators "
        "will DISAGREE with each other: 1 = virtually everyone will give the same rating, 2 = minor spread, 3 = moderate spread, 4 = clearly divided, 5 = strongly divided (ratings all over the scale).\n"
        "Respond ONLY with JSON:\n{\n\"disagreement\": \"1-5\"\n}\n\n--- Original rating instruction and item ---\n")
out = np.zeros((len(PAN["texts"]), 5))
with torch.no_grad():
    for i, t in enumerate(PAN["texts"]):
        prompt = HEAD + PAN["prompt"](t)
        text = tok.apply_chat_template([{"role": "user", "content": prompt}], tokenize=False, add_generation_prompt=True) + '```json\n{\n"disagreement": "'
        ids = tok(text, add_special_tokens=False, return_tensors="pt").input_ids.to("cuda"); lg = model(input_ids=ids).logits[0, -1][ids5].float(); out[i] = torch.softmax(lg, -1).cpu().numpy()
        if (i + 1) % 200 == 0: print(f"{i+1}/{len(out)}", flush=True)
os.makedirs(f"{HERE}/results/ask", exist_ok=True); np.savez(f"{HERE}/results/ask/{args.panel}.npz", pmf=out, disagree=out @ np.arange(1, 6), item_ids=PAN["item_ids"], model=MODEL)
print("saved", args.panel, "mean predicted disagreement", (out @ np.arange(1, 6)).mean().round(3), flush=True)
