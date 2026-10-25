"""
Constrained target constructions — v3 after Codex round 6: no fallback (optimizer must succeed), one tolerance (1e-6) for simplex / mean / mode, projection-status counters (STATUS). Every restricted target certifies the constraints it claims at ONE tight tolerance,
and callers must hard-fail on any violation (certify_* return counts; `assert_valid_*` raise).

  ordinal_mode_mean(base, z, mu, feasible=None)
      q = argmin KL(q || base)  s.t.  sum q = 1,  E_q[Y] = mu,  q[z] >= q[k] for all k.
      Returns `base` itself if it already satisfies the constraints; otherwise the exponential tilt when its mode is z; otherwise an SLSQP
      KL-projection started from a FEASIBLE point (`feasible`, e.g. the recipient's own histogram, or a constructed one). Raises if no
      solution meets all constraints at tolerance TOL. No heuristic fallback.
  nominal_zc(base, z, c)
      q[z] = c, q[k] <= c for k != z, remaining mass proportional to base over non-modal classes with a persistent-active-set water filling.
      Requires c >= 1/K (otherwise infeasible -> raises).
"""
import numpy as np

TOL = 1e-6
STATUS = {"base": 0, "tilt": 0, "projected": 0, "failed": 0}      # projection-status counters (reset by callers via reset_status()); every target must come from one of the first three
def reset_status():
    for k in STATUS: STATUS[k] = 0

def _kl(q, base): q = np.clip(q, 1e-12, 1); return float(np.sum(q * (np.log(q) - np.log(np.clip(base, 1e-12, 1)))))

def tilt(base, mu, lv):
    lo, hi = -40.0, 40.0
    for _ in range(100):
        lam = (lo + hi) / 2; q = base * np.exp(lam * lv); q /= q.sum()
        if q @ lv < mu: lo = lam
        else: hi = lam
    return q

def _ok_ordinal(q, z, mu, lv):
    return (abs(q.sum() - 1) < TOL and q.min() >= -TOL and abs(q @ lv - mu) < TOL and q[z] >= q.max() - TOL)

def _feasible_point(z, mu, K):
    """A point with mode z and mean mu: mass w at z, the rest spread uniformly over the other classes, w chosen (by bisection) to hit mu; mode guaranteed when w >= 1/K... if the
    uniform remainder cannot hit mu, concentrate the remainder on the class that moves the mean in the right direction."""
    lv = np.arange(K)
    for w in np.linspace(0.999, 1.0 / K + 1e-3, 400):
        rest = (1 - w) / (K - 1); q = np.full(K, rest); q[z] = w
        m = q @ lv
        # shift the remainder toward the end that brings the mean to mu, keeping each non-modal entry <= w
        others = [k for k in range(K) if k != z]
        if m < mu: order = sorted(others, reverse=True)
        else: order = sorted(others)
        for _ in range(50):
            m = q @ lv
            if abs(m - mu) < 1e-7: break
            donor, recv = (order[-1], order[0]) if True else (None, None)
            # move mass from the class farthest on the wrong side to the class farthest on the right side, capped by w
            if m < mu: src, dst = min(others), max(others)
            else: src, dst = max(others), min(others)
            need = (mu - m) / (dst - src) if dst != src else 0
            step = min(abs(need), q[src], w - q[dst])
            if step <= 0: break
            q[src] -= step; q[dst] += step
        if _ok_ordinal(q, z, mu, lv): return q
    raise ValueError(f"no feasible point for mode {z}, mean {mu:.4f}, K={K}")

def ordinal_mode_mean(base, z, mu, feasible=None):
    """Deterministic KKT active-set KL projection onto {sum q = 1, E[Y] = mu, q_z >= q_k}, constraint- and optimality-certified to numerical tolerance,
    relative to the 1e-9-floored base distribution (Codex rounds 7-8).
    KKT: q_k = s b_k e^{lam k} (untied), q_j = c = s G(lam) for the mode and the tied set A, G = geometric mean of the tied classes' tilted bases;
    lam solves (F1 + G J)/(F0 + nT G) = mu; tied j != z need b_j e^{lam j} >= G, untied need <= G. All tie sets are enumerated. Roots at lam = +-inf
    (mu equal to the limiting mean of the surviving components) are handled analytically. No fallback: if no KKT-consistent tie set exists, raise.
    `feasible` is accepted for API compatibility (unused)."""
    import itertools
    K = len(base); lv = np.arange(K, dtype=float); base = np.asarray(base, float)
    if _ok_ordinal(base / base.sum(), z, mu, lv): STATUS["base"] += 1; return base / base.sum()
    b = np.clip(base, 1e-9, None); b = b / b.sum(); lb = np.log(b)
    q0 = tilt(b, mu, lv)
    if _ok_ordinal(q0, z, mu, lv): STATUS["tilt"] += 1; return q0
    others = [k for k in range(K) if k != z]; cands = []
    for r in range(len(others) + 1):
        for A in itertools.combinations(others, r):
            tied = sorted(set(A) | {z}); free = [k for k in range(K) if k not in tied]; nT = len(tied); J = float(sum(tied)); mT = J / nT
            def logparts(lam):
                logG = float(np.mean(lb[tied] + lam * lv[tied])); lf = (lb[free] + lam * lv[free]) if free else None
                return logG, lf
            def R(lam):
                logG, lf = logparts(lam); m = max(logG, float(lf.max()) if free else -np.inf)
                F0 = float(np.sum(np.exp(lf - m))) if free else 0.0; F1 = float(np.sum(lv[free] * np.exp(lf - m))) if free else 0.0; G = np.exp(logG - m)
                return (F1 + G * J) / (F0 + nT * G) - mu
            q = None; kkt = None
            if not free:
                if abs(mT - mu) > TOL: continue
                logq = np.full(K, -np.inf); logq[tied] = lb[tied] / 1.0          # all tied: q = uniform over tied (lam irrelevant); KKT needs lb_j >= mean(lb_tied) for j != z
                qq = np.zeros(K); qq[tied] = 1.0 / nT; q = qq; kkt = all(lb[j] >= float(np.mean(lb[tied])) - 1e-9 for j in A)
            else:
                lo, hi = -200.0, 200.0; rlo, rhi = R(lo), R(hi)
                if rlo * rhi <= 0:
                    for _b in range(400):
                        mid = (lo + hi) / 2; rm = R(mid)
                        if rm * rlo <= 0: hi = mid
                        else: lo, rlo = mid, rm
                    lam_sol = (lo + hi) / 2; logG, lf = logparts(lam_sol); logq = np.empty(K)
                    for k in free: logq[k] = lb[k] + lam_sol * lv[k]
                    for j in tied: logq[j] = logG
                    q = np.exp(logq - logq.max()); q = q / q.sum(); tv = lb + lam_sol * lv
                    kkt = all(tv[k] <= logG + 1e-9 for k in free) and all(tv[j] >= logG - 1e-9 for j in A)
                else:
                    # root at lam -> +inf (mu equals the limiting mean r* = max(k_max_free, mT)) or lam -> -inf (r* = min(k_min_free, mT))
                    for sign in (+1, -1):
                        rstar = max(max(free), mT) if sign > 0 else min(min(free), mT)
                        if abs(rstar - mu) > TOL: continue
                        comp = {}                                                     # surviving components: free class with index == rstar, tied block if mT == rstar
                        for k in free:
                            if abs(k - rstar) < 1e-12: comp[k] = lb[k]
                        tied_survives = abs(mT - rstar) < 1e-12
                        if tied_survives:
                            logG_inf = float(np.mean(lb[tied]))
                            for j in tied: comp[j] = logG_inf
                        if not comp: continue
                        logq = np.full(K, -np.inf)
                        for k, v in comp.items(): logq[k] = v
                        q = np.exp(logq - max(comp.values())); q = q / q.sum()
                        if not tied_survives: continue                                # the mode would vanish -> infeasible for this tie set
                        # KKT at the limit: untied k survives only if index == rstar and then needs lb_k <= logG_inf; tied j != z: index beyond mT in the sign direction -> ok,
                        # index short of mT -> multiplier negative -> inconsistent; index == mT -> needs lb_j >= logG_inf
                        ok = True
                        for k in free:
                            if abs(k - rstar) < 1e-12 and lb[k] > logG_inf + 1e-9: ok = False
                        for j in A:
                            d = (j - mT) * sign
                            if d < -1e-12 or (abs(d) < 1e-12 and lb[j] < logG_inf - 1e-9): ok = False
                        kkt = ok; break
                    if q is None: continue
            if q is None or not _ok_ordinal(q, z, mu, lv): continue
            cands.append((bool(kkt), _kl(q, b), q))
    exact = [c for c in cands if c[0]]
    if not exact:
        STATUS["failed"] += 1; raise ValueError(f"KKT-certified KL projection not found for mode {z}, mean {mu:.6f} (feasible candidates: {len(cands)})")
    STATUS["projected"] += 1; return min(exact, key=lambda c: c[1])[2]

def certify_ordinal(Q, Z, MU):
    Q = np.asarray(Q, float); lv = np.arange(Q.shape[1]); idx = np.arange(len(Q)); Z = np.asarray(Z); MU = np.asarray(MU)
    return dict(mode_violations=int(np.sum(Q[idx, Z] < Q.max(1) - TOL)), mean_violations=int(np.sum(np.abs(Q @ lv - MU) > TOL)),
                simplex_violations=int(np.sum((np.abs(Q.sum(1) - 1) > TOL) | (Q.min(1) < -TOL))))
def assert_valid_ordinal(Q, Z, MU, what=""):
    c = certify_ordinal(Q, Z, MU)
    if any(v for v in c.values()): raise AssertionError(f"invalid ordinal targets {what}: {c}")
    return c

def nominal_zc(base, z, c):
    K = len(base); base = np.clip(np.asarray(base, float), 1e-9, None)
    if c < 1.0 / K - 1e-12: raise ValueError(f"modal mass {c:.4f} < 1/K: infeasible")
    q = np.zeros(K); free = [k for k in range(K) if k != z]; remaining = 1.0 - c
    while free:
        scale = remaining / base[free].sum(); over = [k for k in free if scale * base[k] > c + 1e-12]
        if not over:
            for k in free: q[k] = scale * base[k]
            break
        for k in over: q[k] = c
        remaining -= c * len(over); free = [k for k in free if k not in over]
    q[z] = c
    return q

def certify_nominal(Q, Z, C):
    Q = np.asarray(Q, float); idx = np.arange(len(Q)); Z = np.asarray(Z); C = np.asarray(C)
    return dict(mass_violations=int(np.sum(np.abs(Q[idx, Z] - C) > TOL)), mode_violations=int(np.sum(Q.max(1) > Q[idx, Z] + TOL)),
                simplex_violations=int(np.sum((np.abs(Q.sum(1) - 1) > TOL) | (Q.min(1) < -TOL))))
def assert_valid_nominal(Q, Z, C, what=""):
    c = certify_nominal(Q, Z, C)
    if any(v for v in c.values()): raise AssertionError(f"invalid nominal targets {what}: {c}")
    return c

if __name__ == "__main__":
    # regression (Codex round 8): boundary root at lam -> +inf; the min-KL fallback used to return (0,0,1/3,1/3,1/3) with KL .20923
    bb = np.array([.05997, .06751, .42366, .16359, .28527]); qq = ordinal_mode_mean(bb, 2, 3.0)
    assert abs(qq @ np.arange(5) - 3.0) < TOL and qq[2] >= qq.max() - TOL and _kl(qq, bb / bb.sum()) < 0.1522 + 1e-4, (qq, _kl(qq, bb / bb.sum()))
    print("regression boundary case ok:", qq.round(5), "KL", round(_kl(qq, bb / bb.sum()), 5))
    rng = np.random.RandomState(0)
    for K in (3, 4, 5):
        lv = np.arange(K); Qs, Zs, Ms = [], [], []
        for _ in range(3000):
            h = rng.randint(0, K, size=rng.choice([4, 6, 9, 97])); p = np.bincount(h, minlength=K) / len(h); z = int(np.argmax(p)); mu = h.mean()
            base = np.clip(p + 0.3 * rng.rand(K), 1e-6, None); base /= base.sum()
            q = ordinal_mode_mean(base, z, mu, feasible=p)          # raises on failure: the self-test must complete all cases
            Qs.append(q); Zs.append(z); Ms.append(mu)
        assert len(Qs) == 3000 and STATUS["failed"] == 0, STATUS
        c = certify_ordinal(np.array(Qs), Zs, Ms); assert not any(c.values()), c
        print(f"ordinal K={K}: {c} over {len(Qs)} cases; status {dict(STATUS)}"); reset_status()
        Qs, Zs, Cs = [], [], []
        for _ in range(20000):
            p = rng.dirichlet(np.ones(K)); z = int(np.argmax(p)); c = float(p[z]); base = rng.dirichlet(np.ones(K))
            Qs.append(nominal_zc(base, z, c)); Zs.append(z); Cs.append(c)
        print(f"nominal K={K}: {certify_nominal(np.array(Qs), Zs, Cs)} over 20000 cases")
