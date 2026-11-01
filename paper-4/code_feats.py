"""Stage 10 Am. 2 (PROTOCOL_STAGE10.md): 22 per-snippet code-readability attributes (after Buse & Weimer, 2010), standardised over snippets."""
import re, numpy as np
NAMES = ["mean line length", "max line length", "mean identifier length", "max identifier length", "identifiers per line", "mean indentation", "max indentation",
         "max brace depth", "keywords per line", "numbers per line", "comment-line fraction", "blank-line fraction", "periods per line", "commas per line",
         "spaces per line", "parentheses per line", "arithmetic ops per line", "comparison ops per line", "assignments per line", "branches per line", "loops per line", "log lines"]
KW = set("abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import "
         "instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try "
         "void volatile while and as async await def del elif except False from global in is lambda None nonlocal not or pass raise True with yield auto bool constexpr "
         "delete extern friend inline mutable namespace nullptr operator register sizeof struct template typedef typename union unsigned using virtual __global__ __device__ "
         "__shared__ __host__".split())
IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*"); NUM = re.compile(r"\b\d+(\.\d+)?\b"); COMMENT = re.compile(r"^\s*(//|#|/\*|\*|\"\"\"|''')")
def attrs(code):
    lines = code.replace("\t", "    ").split("\n"); nl = max(1, len(lines)); ne = [l for l in lines if l.strip()]; nn = max(1, len(ne))
    ids = [t for t in IDENT.findall(code) if t not in KW]; ind = [len(l) - len(l.lstrip(" ")) for l in ne] or [0]
    depth = mx = 0
    for ch in code:
        if ch == "{": depth += 1; mx = max(mx, depth)
        elif ch == "}": depth = max(0, depth - 1)
    per = lambda pat: len(re.findall(pat, code)) / nn
    return np.array([np.mean([len(l) for l in ne]) if ne else 0.0, max([len(l) for l in lines] or [0]), np.mean([len(t) for t in ids]) if ids else 0.0, max([len(t) for t in ids] or [0]),
                     len(ids) / nn, np.mean(ind), max(ind), mx, sum(t in KW for t in IDENT.findall(code)) / nn, len(NUM.findall(code)) / nn,
                     sum(bool(COMMENT.match(l)) for l in ne) / nn, (nl - len(ne)) / nl, code.count(".") / nn, code.count(",") / nn, code.count(" ") / nn,
                     (code.count("(") + code.count(")")) / nn, per(r"(?<![+\-*/%=<>!&|^])[+\-*/%](?![=+\-])"), per(r"==|!=|<=|>=|(?<![<>=-])[<>](?![<>=])"),
                     per(r"(?<![=!<>+\-*/%&|^])=(?!=)|[+\-*/%]="), per(r"\b(if|else|switch|case|elif)\b"), per(r"\b(for|while|do)\b"), np.log(nl)], float)
def code_G(texts):
    D = np.stack([attrs(str(t)) for t in texts]); sd = D.std(0); sd[sd == 0] = 1.0; return (D - D.mean(0)) / sd
