"""Stage 6 Amendment 2 (F2): LoRe and a monolithic Bradley–Terry model in LoRe's native PRISM setting — users with >= 6 dialogues split 50/50 seen/unseen,
each user's interactions split half train / few-shot and half test, one (chosen, random other) pair per interaction, 5 random user splits.
Usage: lore_native.py qwen|skywork"""
import os, sys, json, numpy as np, pandas as pd, torch, torch.nn.functional as Fn
HERE = os.path.dirname(os.path.abspath(__file__)); P2 = os.path.abspath(os.path.join(HERE, "..", "paper-2", "phase2")); sys.path.insert(0, P2)
import data_panels
torch.manual_seed(0); torch.set_num_threads(int(os.environ.get("OMP_NUM_THREADS", "4"))); FEAT = sys.argv[1]
u = pd.read_json(f"{data_panels.PRISM_DIR}/utterances.jsonl", lines=True).dropna(subset=["score"]).sort_values("utterance_id").reset_index(drop=True)
if FEAT == "skywork":
    z = np.load(f"{P2}/features/prism_skywork/utterances_Skywork.npz"); pos = {s: j for j, s in enumerate(z["utterance_id"])}; E = z["E"]
else:
    z = np.load(f"{P2}/features/prism/Qwen2.5-7B-Instruct.npz", allow_pickle=True); pos = {str(s): j for j, s in enumerate(z["item_ids"])}; E = z["E_last"]
rng0 = np.random.RandomState(0); pairs = []                               # one pair per interaction: chosen vs one random other
for iid, g in u.groupby("interaction_id", sort=True):
    if len(g) < 2 or g.if_chosen.sum() != 1: continue
    ch = g[g.if_chosen.astype(bool)].iloc[0]; oth = g[~g.if_chosen.astype(bool)]; o = oth.iloc[rng0.randint(len(oth))]
    if str(ch.utterance_id) in pos and str(o.utterance_id) in pos: pairs.append((str(ch.user_id), str(ch.conversation_id), iid, pos[str(ch.utterance_id)], pos[str(o.utterance_id)]))
df = pd.DataFrame(pairs, columns=["user", "conv", "iid", "c", "r"])
ndlg = df.groupby("user").conv.nunique(); users = sorted(ndlg[ndlg >= 6].index); df = df[df.user.isin(users)].reset_index(drop=True)
X = E.astype(np.float32); mu, sd = X.mean(0), X.std(0) + 1e-6; X = torch.tensor((X - mu) / sd)
D = X[torch.tensor(df.c.values)] - X[torch.tensor(df.r.values)]            # chosen − rejected embedding difference
uid = {u_: j for j, u_ in enumerate(users)}; U = torch.tensor(df.user.map(uid).values); NU = len(users)
print(f"{FEAT}: {len(users)} users with >= 6 dialogues, {len(df)} pairs, {len(df) / len(users):.1f} pairs per user", flush=True)
def fit(B, lr, tr, va, epochs=30):
    torch.manual_seed(0); A = torch.nn.Linear(D.shape[1], B, bias=False); W = torch.zeros(NU, B, requires_grad=True); opt = torch.optim.Adam(list(A.parameters()) + [W], lr=lr)
    best = (-1e9, None); bad = 0; rng = np.random.RandomState(0)
    for ep in range(epochs):
        order = torch.tensor(rng.permutation(tr))
        for b0 in range(0, len(order), 256):
            t = order[b0:b0 + 256]; sc = (torch.softmax(W[U[t]], 1) * A(D[t])).sum(1); loss = -Fn.logsigmoid(sc).mean(); opt.zero_grad(); loss.backward(); opt.step()
        with torch.no_grad(): v = float(Fn.logsigmoid((torch.softmax(W[U[va]], 1) * A(D[va])).sum(1)).mean())
        if v > best[0]: best = (v, ({k: x.clone() for k, x in A.state_dict().items()}, W.detach().clone())); bad = 0
        else: bad += 1
        if bad >= 3: break
    A.load_state_dict(best[1][0]); return A, best[1][1], best[0]
res = []
for split in range(5):
    rs = np.random.RandomState(100 + split); perm = rs.permutation(NU); seen = set(perm[: NU // 2]); unseen = set(perm[NU // 2:])
    half = np.zeros(len(df), bool)                                         # per user, half of the interactions are train / few-shot
    for u_, g in df.groupby("user"):
        ii = g.index.values; half[rs.permutation(ii)[: len(ii) // 2]] = True
    is_seen = np.array([uid[x] in seen for x in df.user])
    tr = np.where(is_seen & half)[0]; va = np.where(is_seen & ~half)[0]; fs = np.where(~is_seen & half)[0]; te = np.where(~is_seen & ~half)[0]
    for B in (1, 2, 5, 10, 20, 50):                                       # B = 1: monolithic BT (same linear map)
        for lr in (0.5, 0.05, 0.005):
            A, W, v = fit(B, lr, tr, va); res.append({"split": split, "B": B, "lr": lr, "val": v})
    # select BT (B = 1) and LoRe (B > 1) by validation LL on seen users' held-out pairs
    sel = [r for r in res if r["split"] == split]; bt_cfg = max([r for r in sel if r["B"] == 1], key=lambda r: r["val"]); lo_cfg = max([r for r in sel if r["B"] > 1], key=lambda r: r["val"])
    out = {"split": split, "bt": bt_cfg, "lore": lo_cfg}
    for name, cfg in (("bt", bt_cfg), ("lore", lo_cfg)):
        A, W, _ = fit(cfg["B"], cfg["lr"], tr, va); w0 = W[torch.tensor(sorted(seen))].mean(0)
        with torch.no_grad(): R_te = A(D[torch.tensor(te)]); R_fs = A(D[torch.tensor(fs)])
        acc0 = float(((torch.softmax(w0, 0)[None, :] * R_te).sum(1) > 0).float().mean()); out[f"{name}_acc_k0"] = acc0
        if name == "lore":                                                # few-shot: A frozen, w_u from the seen-user mean, Adam lr 0.1, 100 steps, no regularisation
            Wn = w0.expand(NU, -1).clone().requires_grad_(True); uf = U[torch.tensor(fs)]; o2 = torch.optim.Adam([Wn], lr=0.1)
            for _ in range(100):
                o2.zero_grad(); l = -Fn.logsigmoid((torch.softmax(Wn[uf], 1) * R_fs).sum(1)).sum(); l.backward(); o2.step()
            with torch.no_grad(): out["lore_acc_fs"] = float(((torch.softmax(Wn[U[torch.tensor(te)]], 1) * R_te).sum(1) > 0).float().mean())
    out["n_unseen_users"] = len(unseen); out["fewshot_per_user"] = len(fs) / len(unseen); out["test_pairs"] = len(te); res.append(out); print(json.dumps(out), flush=True)
summ = [r for r in res if "lore_acc_fs" in r]; agg = {k: [float(np.mean([r[k] for r in summ])), float(np.std([r[k] for r in summ]))] for k in ("bt_acc_k0", "lore_acc_k0", "lore_acc_fs")}
print("SUMMARY", FEAT, json.dumps(agg), flush=True)
json.dump({"feat": FEAT, "splits": summ, "summary": agg}, open(f"{HERE}/results/stage6_native_{FEAT}.json", "w"), indent=1)
