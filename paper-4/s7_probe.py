"""Stage 7 S7-1 (PROTOCOL_STAGE7.md): cross-fitted ridge probes of the injected content features g1 (log length ratio) and g2 (random whitened
pair-difference direction), computed exactly as make_synth.py, from each learner's input space; out-of-fold R² over the paper's prompt-group item folds."""
import os, sys, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); P2 = os.path.join(os.path.dirname(HERE), "paper-2", "phase2"); sys.path.insert(0, P2)
import data_panels
PAN = data_panels.load("multipref_overall"); H = PAN["H"]; n = H.shape[0]
Gp = np.asarray(PAN["groups"]); ug = np.unique(Gp); perm = np.random.RandomState(0).permutation(len(ug)); gf = {g_: perm[j] % 5 for j, g_ in enumerate(ug)}; ifold = np.array([gf[g_] for g_ in Gp])
# ---- g1, g2 exactly as make_synth.py
raw = [json.loads(l) for l in open(data_panels.MULTIPREF)]; assert [r["comparison_id"] for r in raw] == list(PAN["item_ids"])
g1 = np.log(np.array([max(1, len(str(r["completion_b"]))) for r in raw]) / np.array([max(1, len(str(r["completion_a"]))) for r in raw]))
Fp = np.load(f"{P2}/features/multipref_overall/pairs_Qwen2.5-7B-Instruct.npz"); assert np.array_equal(Fp["item_ids"], np.asarray(PAN["item_ids"]).astype(str))
Dd = (Fp["E_B"] - Fp["E_A"]).astype(np.float64); Dd -= Dd.mean(0); U2, S2, _ = np.linalg.svd(Dd, full_matrices=False); Z = U2[:, :256] * S2[:256]; Z /= Z.std(0)
ymean = H.mean(1); w = np.linalg.solve(Z.T @ Z + 1000.0 * np.eye(256), Z.T @ (ymean - ymean.mean())); w /= np.linalg.norm(w)
u = np.random.RandomState(0).randn(256); u -= (u @ w) * w; u /= np.linalg.norm(u); g2 = Z @ u
T = {"g1": (g1 - g1.mean()) / g1.std(), "g2": (g2 - g2.mean()) / g2.std()}
SEMP = len(sys.argv) > 1 and sys.argv[1] == "sem"                              # Stage 7 Am. 3: probe the semantic axes instead
if SEMP:
    from sem_feats import sem_G; Gs = sem_G(raw); T = {"g1": Gs[:, 0], "g2": Gs[:, 1]}
# ---- input spaces
EA, EB, EP = (Fp[k].astype(np.float32) for k in ("E_A", "E_B", "E_P")); allE = np.concatenate([EA, EB, EP]); mu = allE.mean(0)
_, _, Vt = np.linalg.svd(allE[::3] - mu, full_matrices=False); W = Vt[:256].T                    # vpl_pal.py --pca 256
XA, XB, XP = ((E - mu) @ W for E in (EA, EB, EP)); sd = np.concatenate([XA, XB, XP]).std(0) + 1e-6; XA, XB, XP = XA / sd, XB / sd, XP / sd
sdf = allE.std(0) + 1e-6                                                                          # vpl_pal.py --pca 0 (full, standardised)
F_ = np.load(f"{P2}/features/multipref_overall/Qwen2.5-7B-Instruct.npz", allow_pickle=True); assert np.array_equal(F_["item_ids"].astype(str), np.asarray(PAN["item_ids"]).astype(str))
E = F_["E_last"].astype(np.float64); E -= E.mean(0); U, S, _ = np.linalg.svd(E, full_matrices=False); X = U[:, :256] * S[:256]; X /= X.std(0)   # factorised_rm.py
SP = {"VPL/PAL PCA-256 [xA,xB,xP]": np.concatenate([XA, XB, XP], 1), "VPL/PAL PCA-256 xB-xA": XB - XA,
      "VPL/PAL full xB-xA": (EB - EA) / sdf, "D/DL/DFs joint PCA-256": X, "generator basis Z (reference)": Z}
LAMS = 10.0 ** np.arange(-2, 6)
def ridge_pred(Xtr, ytr, Xte, lams):                                      # dual/primal ridge via SVD of centred Xtr, for all λ at once
    mx, my = Xtr.mean(0), ytr.mean(); Uq, s, Vq = np.linalg.svd(Xtr - mx, full_matrices=False); a = Uq.T @ (ytr - my)
    return {l: my + ((Xte - mx) @ Vq.T) @ (s / (s ** 2 + l) * a) for l in lams}
def probe(Xs, y):
    oof = np.zeros(n); lam_sel = []
    for f in range(5):
        tr, te = ifold != f, ifold == f; itr = np.where(tr)[0]; inner = np.random.RandomState(f).permutation(len(itr)) % 5; sse = {l: 0.0 for l in LAMS}
        for g in range(5):
            a, b = itr[inner != g], itr[inner == g]; P = ridge_pred(Xs[a], y[a], Xs[b], LAMS)
            for l in LAMS: sse[l] += float(((P[l] - y[b]) ** 2).sum())
        l = min(sse, key=sse.get); lam_sel.append(float(l)); oof[te] = ridge_pred(Xs[tr], y[tr], Xs[te], [l])[l]
    return 1 - ((oof - y) ** 2).sum() / ((y - y.mean()) ** 2).sum(), lam_sel
res = {}
for name, Xs in SP.items():
    Xs = Xs.astype(np.float64)
    for t, y in T.items():
        r2, ls = probe(Xs, y); res[f"{name} | {t}"] = {"R2": float(r2), "lambda": ls}; print(f"{name:34s} {t}: R² = {r2:.3f}  λ = {ls}", flush=True)
read = lambda r: "available" if r >= 0.5 else ("largely unavailable" if r < 0.2 else "partly available")
L = ["# Stage 7 S7-1 — out-of-fold linear-probe R² of the injected features from each learner's inputs", "", "| input space | R²(g1, log length ratio) | R²(g2, random direction) |", "|---|---|---|"]
L += [f"| {s} | {res[f'{s} | g1']['R2']:.3f} ({read(res[f'{s} | g1']['R2'])}) | {res[f'{s} | g2']['R2']:.3f} ({read(res[f'{s} | g2']['R2'])}) |" for s in SP]
sfx = "_sem" if SEMP else ""; L[0] = L[0] + (" (semantic axes: g1 = formatting, g2 = hedging / refusal)" if SEMP else "")
json.dump(res, open(f"{HERE}/results/stage7_probe{sfx}.json", "w"), indent=1); open(f"{HERE}/results/stage7_probe{sfx}.md", "w").write("\n".join(L) + "\n"); print("\n".join(L))
