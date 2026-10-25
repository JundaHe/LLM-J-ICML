"""Smoke test: local Qwen2.5-7B-Instruct judge, read next-token probabilities over score levels for What/Why."""
import sys, time, json, torch, numpy as np
sys.path.insert(0, "/mnt/hdd2/jundahe/LLM-J/paper-2/idea-stage/pilot")
import cm_data
from transformers import AutoTokenizer, AutoModelForCausalLM
MODEL = "Qwen/Qwen2.5-Coder-7B-Instruct"
tok = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.bfloat16, device_map="cuda")
model.eval()
d = cm_data.load("developer").head(int(sys.argv[1]) if len(sys.argv) > 1 else 8)
level_ids = [tok.encode(str(l), add_special_tokens=False)[0] for l in cm_data.LEVELS]
print("level token ids", level_ids, flush=True)

def score(prompt):
    out = {}
    for key, prefix in [("what", '```json\n{\n    "What": '), ("why", None)]:
        msgs = [{"role": "user", "content": prompt}]
        text = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
        if key == "what":
            text += prefix
        else:
            text += '```json\n{\n    "What": %d,\n    "Why": ' % out["what_argmax"]
        ids = tok(text, return_tensors="pt").to("cuda")
        with torch.no_grad():
            logits = model(**ids).logits[0, -1]
        p = torch.softmax(logits[level_ids].float(), 0).cpu().numpy()
        out[f"{key}_p"] = p.tolist(); out[f"{key}_argmax"] = int(np.argmax(p)); out[f"{key}_mean"] = float((p * np.arange(5)).sum())
        out["n_tokens"] = int(ids.input_ids.shape[1])
    return out

t0 = time.time()
for i, row in d.iterrows():
    r = score(row.prompt)
    H_what = cm_data.H(d, "what")[i].tolist(); H_why = cm_data.H(d, "why")[i].tolist()
    print(json.dumps({"i": int(i), "n_tok": r["n_tokens"], "what_p": [round(x, 3) for x in r["what_p"]], "H_what": H_what,
                      "why_p": [round(x, 3) for x in r["why_p"]], "H_why": H_why}), flush=True)
print("elapsed per item (s):", round((time.time() - t0) / len(d), 2), "max mem GB:", round(torch.cuda.max_memory_allocated() / 1e9, 2))
