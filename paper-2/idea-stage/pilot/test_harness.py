"""M0 harness unit tests (R000): AUROC ties, ordinal alpha, 9-rater strata, z_i tie rule, max-matching certificate. Run: python test_harness.py"""
import sys, os, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import csje_eval as E
from support_audit import z_label, random_max_matching
from collections import Counter
def test_auroc_ties(): assert abs(E.auroc(np.zeros(10), np.array([1,0]*5)) - 0.5) < 1e-9; assert E.auroc(np.array([0,0,1,1]), np.array([0,0,1,1])) == 1.0
def test_alpha():
    a = np.array([1,2,3,3,4,2,1,5,4,3]); assert abs(E.kripp_alpha_ordinal(a, a) - 1.0) < 1e-9
    b = np.array([1,2,3,4,4,2,2,5,4,3]); al = E.kripp_alpha_ordinal(a, b); assert 0.9 < al < 1.0, al
def test_strata9():
    H = np.array([[3,3,3,3,3,4,2,3,5],[1,5,2,4,3,1,5,2,4],[2,2,3,3,3,4,4,5,1]]); st = E.strata(H); assert list(st) == ["High","Low","Partial"], st
def test_z_rule():
    assert z_label(np.array([2,2,3,1,0])) == 2; assert z_label(np.array([1,1,3,3,0])) == 1 or z_label(np.array([1,1,3,3,0])) == 3
    r = np.array([1,1,3,3,4]); assert z_label(r) == 3           # tie 1 vs 3 → closest to median 3
    r = np.array([1,1,3,3,2]); assert z_label(r) == 1           # tie, equidistant from median 2 → lower
def test_matching():
    rng = np.random.RandomState(0); hist = [(1,2,0,0,0)]*5 + [(0,3,0,0,0)]*1; items = list(range(6))
    m = random_max_matching(items, hist, rng); assert len(m) == 2 and all(hist[a] != hist[b] for a, b in m.items())      # min(N, 2(N−M)) = 2
    hist = [(1,2,0,0,0)]*3 + [(0,3,0,0,0)]*3; m = random_max_matching(items, hist, rng); assert len(m) == 6 and sorted(m) == sorted(m.values())
    hist = [(1,2,0,0,0)]*6; assert random_max_matching(items, hist, rng) == {}
for t in [test_auroc_ties, test_alpha, test_strata9, test_z_rule, test_matching]:
    t(); print("ok", t.__name__)
