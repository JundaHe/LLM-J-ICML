"""Stage 6 Amendment 2 (F1): Skywork-Reward-Llama-3.1-8B-v0.2 embeddings (last-layer state at the final token of the chat-formatted user prompt + response) and scalar rewards
for every PRISM utterance; and the PRISM-pairs feature file in the layout vpl_pal.py expects (E_A, E_B; E_P = zeros, unused by LoRe and the D-family's fit is reported only)."""
import os, sys, numpy as np, pandas as pd, torch
HERE = os.path.dirname(os.path.abspath(__file__)); P2 = os.path.abspath(os.path.join(HERE, "..", "paper-2", "phase2")); sys.path.insert(0, P2)
import data_panels
from transformers import AutoTokenizer, AutoModelForSequenceClassification
MODEL = "Skywork/Skywork-Reward-Llama-3.1-8B-v0.2"
tok = AutoTokenizer.from_pretrained(MODEL); model = AutoModelForSequenceClassification.from_pretrained(MODEL, dtype=torch.bfloat16, device_map="cuda", num_labels=1); model.eval()
u = pd.read_json(f"{data_panels.PRISM_DIR}/utterances.jsonl", lines=True).dropna(subset=["score"]).sort_values("utterance_id").reset_index(drop=True)
emb = np.zeros((len(u), 4096), np.float16); rew = np.zeros(len(u), np.float32)
with torch.no_grad():
    for i, r in enumerate(u.itertuples()):
        conv = [{"role": "user", "content": str(r.user_prompt)[:4000]}, {"role": "assistant", "content": str(r.model_response)[:4000]}]
        ids = tok.apply_chat_template(conv, tokenize=True, return_tensors="pt").to("cuda")
        o = model(input_ids=ids, output_hidden_states=True); emb[i] = o.hidden_states[-1][0, -1].float().cpu().numpy(); rew[i] = float(o.logits[0, 0])
        if (i + 1) % 2000 == 0: print(f"{i+1}/{len(u)}", flush=True)
out = f"{P2}/features/prism_skywork"; os.makedirs(out, exist_ok=True); np.savez(f"{out}/utterances_Skywork.npz", E=emb, reward=rew, utterance_id=u.utterance_id.astype(str).to_numpy())
P = data_panels.load("prism_pairs"); pos = {s: j for j, s in enumerate(u.utterance_id.astype(str))}
EA = np.stack([emb[pos[s]] for s in P["utt_A"]]); EB = np.stack([emb[pos[s]] for s in P["utt_B"]])
os.makedirs(f"{P2}/features/prism_pairs", exist_ok=True); np.savez(f"{P2}/features/prism_pairs/pairs_Skywork.npz", E_A=EA, E_B=EB, E_P=np.zeros_like(EA), item_ids=np.asarray(P["item_ids"]).astype(str)); print("saved", EA.shape, flush=True)
