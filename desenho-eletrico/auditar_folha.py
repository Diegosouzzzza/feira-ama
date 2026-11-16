# -*- coding: utf-8 -*-
"""
Auditor geometrico das folhas de interligacao do esp32.html.

Uso:
    python auditar_folha.py wiring-4            (grupo de fios padrao: fios-w4)
    python auditar_folha.py wiring-4 fios-w4

Aplica os transforms (translate/scale/rotate/matrix) de cada elemento e verifica:
  1. XML do SVG bem formado (tags <g> balanceadas)
  2. cores literais (#hex, rgb(), nomes) - so var(--...) e permitido
  3. elementos fora da moldura interna (25 unidades de margem do viewBox)
  4. FIO x TEXTO  : segmento de fio passando sobre texto que nao e o rotulo do proprio fio
  5. FIO x CORPO  : segmento de fio atravessando retangulo (>8x8) de um componente
Itens 4 e 5 ignoram o trecho final de 14 unidades junto a cada ponta do fio
(chegada no pad, onde o numero do terminal fica encostado no fio).
Saida 0 = nenhuma ocorrencia; 1 = ha ocorrencias.
"""
import collections
import html
import math
import os
import re
import sys
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')
SEC = sys.argv[1] if len(sys.argv) > 1 else 'wiring-4'
default_fios = 'fios-pg' if SEC == 'planta-geral' else 'fios-' + SEC.replace('wiring-', 'w')
FIOS = sys.argv[2] if len(sys.argv) > 2 else default_fios
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'esp32.html')
src = open(SRC, encoding='utf-8').read()
a = src.index('<section id="%s"' % SEC)
sec = src[a:src.index('</section>', a)]
svg = sec[sec.index('<svg'):sec.rindex('</svg>') + 6]
problemas = 0

# 1) balanco de <g>
lines, depth, out, extra = svg.split('\n'), 0, [], []
base_line = src[:a + sec.index('<svg')].count('\n') + 1
for k, l in enumerate(lines):
    l2 = re.sub(r'<!--.*?-->', '', l)
    o, c = len(re.findall(r'<g[\s>]', l2)), l2.count('</g>')
    if c and depth + o - c < 0:
        l = l.replace('</g>', '', 1); c -= 1; extra.append(base_line + k)
    depth += o - c; out.append(l)
if extra or depth:
    problemas += 1
    print('XML: </g> sobrando nas linhas', extra, '| <g> sem fechar:', depth)
svg = re.sub(r'&(?!amp;|lt;|gt;|quot;|#)\w+;', ' ', '\n'.join(out))

# 2) cores literais
lit = re.findall(r'(?:fill|stroke|stop-color|color)\s*[=:]\s*"?\s*(#[0-9a-fA-F]{3,8}|rgba?\([^)]*\)|white|black|red|green|blue|yellow|orange|gr[ae]y)\b', sec)
if lit:
    problemas += 1; print('CORES LITERAIS:', collections.Counter(lit))

root = ET.fromstring(svg, parser=ET.XMLParser(target=ET.TreeBuilder(insert_comments=True)))
N = '{http://www.w3.org/2000/svg}'


def mul(A, B):
    a, b, c, d, e, f = A; p, q, r, s, t, u = B
    return [a*p + c*q, b*p + d*q, a*r + c*s, b*r + d*s, a*t + c*u + e, b*t + d*u + f]


def tf(s):
    M = [1, 0, 0, 1, 0, 0]
    for fn, args in re.findall(r'(\w+)\s*\(([^)]*)\)', s or ''):
        v = [float(x) for x in re.split(r'[ ,]+', args.strip()) if x]
        if fn == 'translate': T = [1, 0, 0, 1, v[0], v[1] if len(v) > 1 else 0]
        elif fn == 'scale': T = [v[0], 0, 0, v[1] if len(v) > 1 else v[0], 0, 0]
        elif fn == 'rotate':
            r = math.radians(v[0]); c, s_ = math.cos(r), math.sin(r)
            cx, cy = (v[1], v[2]) if len(v) == 3 else (0, 0)
            T = [c, s_, -s_, c, cx - c*cx + s_*cy, cy - s_*cx - c*cy]
        elif fn == 'matrix': T = v
        else: continue
        M = mul(M, T)
    return M


def ap(M, x, y): return (M[0]*x + M[2]*y + M[4], M[1]*x + M[3]*y + M[5])


def fl(e, k, d=0.0):
    try: return float(e.get(k, d))
    except (TypeError, ValueError): return d


def path_segs(d):
    toks = re.findall(r'[A-Za-z]|-?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?', d)
    NARG = {'M': 2, 'L': 2, 'H': 1, 'V': 1, 'C': 6, 'S': 4, 'Q': 4, 'T': 2, 'A': 7, 'Z': 0}
    segs, cur, start, i, cmd = [], (0.0, 0.0), (0.0, 0.0), 0, 'M'
    while i < len(toks):
        if re.match(r'[A-Za-z]', toks[i]): cmd = toks[i]; i += 1
        U, rel = cmd.upper(), cmd.islower(); n = NARG.get(U, 0)
        if U == 'Z': segs.append((cur, start)); cur = start; continue
        if i + n > len(toks): break
        v = [float(t) for t in toks[i:i + n]]; i += n
        if U == 'H': pt = (v[0] + (cur[0] if rel else 0), cur[1])
        elif U == 'V': pt = (cur[0], v[0] + (cur[1] if rel else 0))
        else: pt = (v[-2] + (cur[0] if rel else 0), v[-1] + (cur[1] if rel else 0))
        if U == 'M': start = cur = pt; cmd = 'l' if rel else 'L'; continue
        segs.append((cur, pt)); cur = pt
    return segs


vb_init = [float(v) for v in re.split(r'[ ,]+', root.get('viewBox', '0 0 1400 900').strip())]
VB_W, VB_H = vb_init[2], vb_init[3]
items = []  # (tipo, bbox, info, grupo_topo, nome_fio)


def walk(e, M, top, wname):
    t = e.tag if isinstance(e.tag, str) else 'comment'
    t = t.replace(N, '')
    if t == 'comment':
        return
    M2 = mul(M, tf(e.get('transform')))
    if t in ('g', 'svg'):
        cur = wname
        for c in e:
            if not isinstance(c.tag, str):
                m = re.match(r'\s*(W\d{3})\b', c.text or '')
                if m: cur = m.group(1)
                continue
            walk(c, M2, top or e.get('id'), cur)
        return
    if t in ('defs', 'pattern', 'marker', 'title'):
        return
    cls = e.get('class', '')
    if t == 'rect':
        x, y, w, h = fl(e, 'x'), fl(e, 'y'), fl(e, 'width'), fl(e, 'height')
        if w >= VB_W - 60: return
        p, q = ap(M2, x, y), ap(M2, x + w, y + h)
        items.append(('rect', (min(p[0], q[0]), min(p[1], q[1]), max(p[0], q[0]), max(p[1], q[1])), cls, top, wname))
    elif t in ('circle', 'ellipse'):
        c = ap(M2, fl(e, 'cx'), fl(e, 'cy')); r = max(fl(e, 'r'), fl(e, 'rx'), fl(e, 'ry')) * abs(M2[0])
        items.append(('circle', (c[0] - r, c[1] - r, c[0] + r, c[1] + r), cls, top, wname))
    elif t == 'text':
        x, y, fs = fl(e, 'x'), fl(e, 'y'), fl(e, 'font-size', 6)
        txt = html.unescape(''.join(e.itertext())).strip()
        w = len(txt) * fs * 0.56; x0 = {'start': x, 'middle': x - w/2, 'end': x - w}[e.get('text-anchor', 'start')]
        p, q = ap(M2, x0, y - fs*0.72), ap(M2, x0 + w, y + fs*0.18)
        items.append(('text', (min(p[0], q[0]), min(p[1], q[1]), max(p[0], q[0]), max(p[1], q[1])), txt, top, wname))
    elif t in ('path', 'line', 'polyline', 'polygon'):
        if t == 'path': segs = path_segs(e.get('d', ''))
        elif t == 'line': segs = [((fl(e, 'x1'), fl(e, 'y1')), (fl(e, 'x2'), fl(e, 'y2')))]
        else:
            v = [float(x) for x in re.split(r'[ ,]+', e.get('points', '').strip()) if x]
            P = list(zip(v[::2], v[1::2])); segs = list(zip(P, P[1:]))
        segs = [(ap(M2, *s[0]), ap(M2, *s[1])) for s in segs]
        if segs:
            xs = [p[0] for s in segs for p in s]; ys = [p[1] for s in segs for p in s]
            items.append(('path', (min(xs), min(ys), max(xs), max(ys)), (cls, segs), top, wname))


walk(root, [1, 0, 0, 1, 0, 0], None, None)

# 3) fora da moldura
vb = [float(v) for v in re.split(r'[ ,]+', root.get('viewBox', '0 0 1400 900').strip())]
X1, Y1 = vb[0] + vb[2] - 25, vb[1] + vb[3] - 25
fora = [(k, [round(v) for v in bb], str(info)[:30], g) for k, bb, info, g, _ in items
        if (bb[0] < 25 or bb[1] < 25 or bb[2] > X1 or bb[3] > Y1) and not (k == 'rect' and bb[0] <= 25 and bb[1] <= 25)]
if fora:
    problemas += 1; print('FORA DA MOLDURA:'); [print('  ', f) for f in fora[:20]]

wires = [(info[1], wn or '(sem ID)') for k, bb, info, g, wn in items
         if k == 'path' and g == FIOS and 'wire' in str(info[0])]
orphan_wires = [wn or '(sem ID)' for k, bb, info, g, wn in items
                if k == 'path' and g is None and 'wire' in str(info[0])]
if orphan_wires:
    problemas += 1; print('FIOS SOLTOS FORA DE <g>:', len(orphan_wires), orphan_wires[:10])
texts = [(bb, info, g, wn) for k, bb, info, g, wn in items if k == 'text']
bodies = [(bb, g) for k, bb, info, g, wn in items
          if k == 'rect' and g and g not in (FIOS, 'bloco-protoboard-e26') and 'wire-tag' not in str(info)
          and (bb[2]-bb[0]) > 8 and (bb[3]-bb[1]) > 8]
tag_rects = [(bb, wn or g or 'tag') for k, bb, info, g, wn in items
             if k == 'rect' and 'wire-tag' in str(info)]
for idx_a in range(len(tag_rects)):
    b1, n1 = tag_rects[idx_a]
    for idx_b in range(idx_a + 1, len(tag_rects)):
        b2, n2 = tag_rects[idx_b]
        if max(b1[0], b2[0]) < min(b1[2], b2[2]) - 0.5 and max(b1[1], b2[1]) < min(b1[3], b2[3]) - 0.5:
            problemas += 1; print('TAG x TAG SOBREPOSTA: %s %s x %s %s' % (n1, [round(v, 1) for v in b1], n2, [round(v, 1) for v in b2]))


def trim(s, ends, d=14.0):
    (x1, y1), (x2, y2) = s
    L = math.hypot(x2 - x1, y2 - y1)
    if L == 0: return None
    ux, uy = (x2 - x1)/L, (y2 - y1)/L
    a0 = d if (round(x1, 1), round(y1, 1)) in ends else 0
    b0 = d if (round(x2, 1), round(y2, 1)) in ends else 0
    if L - a0 - b0 <= 0: return None
    return ((x1 + ux*a0, y1 + uy*a0), (x2 - ux*b0, y2 - uy*b0))


def hits(s, bb, pad=0.4):
    (x1, y1), (x2, y2) = s
    if abs(x1 - x2) < 1e-6:
        return bb[0] + pad < x1 < bb[2] - pad and max(min(y1, y2), bb[1]) < min(max(y1, y2), bb[3]) - pad
    if abs(y1 - y2) < 1e-6:
        return bb[1] + pad < y1 < bb[3] - pad and max(min(x1, x2), bb[0]) < min(max(x1, x2), bb[2]) - pad
    n = 20
    return any(bb[0] + pad < x1 + (x2-x1)*i/n < bb[2] - pad and bb[1] + pad < y1 + (y2-y1)*i/n < bb[3] - pad for i in range(n + 1))


rel_t, rel_b = collections.defaultdict(set), collections.defaultdict(set)
for segs, nm in wires:
    pts = collections.Counter((round(p[0], 1), round(p[1], 1)) for s in segs for p in s)
    ends = {p for p, c in pts.items() if c == 1}
    segs2 = [x for x in (trim(s, ends) for s in segs) if x]
    for bb, txt, g, wn in texts:
        if g == FIOS and wn == nm: continue           # rotulo do proprio fio
        if any(hits(s, bb) for s in segs2): rel_t[nm].add('%s [%s]' % (txt[:30], g))
    for bb, g in bodies:
        if any(hits(s, bb, 1.0) for s in segs2): rel_b[nm].add('%s %s' % (g, [round(v) for v in bb]))
if rel_t:
    problemas += 1; print('\nFIO x TEXTO:')
    for nm in sorted(rel_t): print('  %-9s' % nm, '; '.join(sorted(rel_t[nm])))
if rel_b:
    problemas += 1; print('\nFIO x CORPO DE COMPONENTE:')
    for nm in sorted(rel_b): print('  %-9s' % nm, '; '.join(sorted(rel_b[nm])))
print('\nfios analisados: %d | elementos: %d | %s' % (len(wires), len(items), 'OK' if not problemas else 'HA OCORRENCIAS'))
sys.exit(1 if problemas else 0)
