"""Stage 7 Am. 3 (PROTOCOL_STAGE7.md): semantic injection axes for MultiPref pairs — (s1) markdown formatting lines, (s2) hedging / refusal phrases; log(1 + B) − log(1 + A)."""
import re, numpy as np
LIST = re.compile(r"^\s*([-*+•]|\d+[.)]|#+)\s", re.M)
PHR = ("i'm sorry", "i am sorry", "i apologize", "i cannot", "i can't", "i'm not able", "i am not able", "as an ai", "i don't have", "however", "it's important to", "it is important to", "please consult", "it depends", "may vary")
def fmt_lines(t): return len(LIST.findall(t))
def hedge(t): t = t.lower().replace("’", "'"); return sum(t.count(p) for p in PHR)
def sem_G(raw):
    A = [str(r["completion_a"]) for r in raw]; B = [str(r["completion_b"]) for r in raw]
    s1 = np.log1p([fmt_lines(b) for b in B]) - np.log1p([fmt_lines(a) for a in A]); s2 = np.log1p([hedge(b) for b in B]) - np.log1p([hedge(a) for a in A])
    G = np.stack([s1, s2], 1).astype(np.float64); return (G - G.mean(0)) / G.std(0)
