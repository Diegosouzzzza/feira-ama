# -*- coding: utf-8 -*-
"""
Camada de override do TEMA CLARO para os desenhos SVG.

As folhas foram desenhadas para fundo preto e carregam cores fixas nos
atributos de apresentacao (fill="#18261e", stroke="#00e676", ...). Reescrever
esses ~300 atributos a mao em 6 arquivos seria frageil e esconderia erros no
code review, entao aqui o markup ja montado e varrido e cada cor encontrada e
classificada por luminancia/matiz para gerar a regra CSS equivalente.

Funciona porque atributo de apresentacao do SVG perde para qualquer regra CSS:
nenhum componente do esquema eletrico e tocado, so a cor com que ele e pintado.
O tema escuro continua identico — toda regra emitida sai sob `body.theme-light`.

Regra geral da traducao:
  - todo TEXTO vira escuro  (legibilidade sobre branco)
  - todo FUNDO de forma vira claro
  - ACENTOS mantem o matiz, trocando neon por tom com contraste AA
"""

import colorsys
import re

# Matiz -> cor de acento com contraste AA sobre branco.
# Espelha a paleta de barramentos ja definida em css_styles.py (body.theme-light)
# para que o desenho e a legenda flutuante falem a mesma lingua.
_ACCENT_BY_HUE = [
    (15,  "#c0392b"),  # vermelho — +12V
    (45,  "#d35400"),  # laranja  — +6V servo
    (70,  "#9a7d0a"),  # amarelo  — +5V
    (100, "#5f7d1f"),  # lima     — PE
    (165, "#1e8449"),  # verde    — GND
    (200, "#0e7490"),  # ciano    — info
    (255, "#2471a3"),  # azul     — AC neutro
    (295, "#6c3483"),  # violeta  — +3V3 / sinais
    (335, "#8e24aa"),  # magenta
    (361, "#c0547a"),  # rosa     — AC fase
]

_INK_TEXT = "#15211a"      # texto principal sobre branco
_INK_STROKE = "#2a3a31"    # traco que era branco no escuro
_MUTED_TEXT = "#41554a"    # texto secundario (AA sobre branco)
_MUTED_STROKE = "#9db0a4"  # separador de peso medio
_FAINT_STROKE = "#c7d4cc"  # grade / separador discreto

_COLOR_ATTR_RE = re.compile(r'\b(fill|stroke)="(#[0-9a-fA-F]{3,6})"')


def _to_rgb(value):
    """'#abc' ou '#aabbcc' -> (r, g, b) em 0..1."""
    h = value.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def _to_hex(r, g, b):
    return "#%02x%02x%02x" % tuple(max(0, min(255, round(c * 255))) for c in (r, g, b))


def _hsl(value):
    r, g, b = _to_rgb(value)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h * 360.0, s, l


def _accent_for_hue(hue):
    for limit, color in _ACCENT_BY_HUE:
        if hue < limit:
            return color
    return _ACCENT_BY_HUE[-1][1]


def _tint_for_hue(hue, sat):
    """Fundo claro que preserva o matiz do acento (badge, LED, borne)."""
    r, g, b = colorsys.hls_to_rgb(hue / 360.0, 0.90, min(max(sat, 0.35), 0.55))
    return _to_hex(r, g, b)


def _surface_for(hue, sat, lig):
    """
    Painel escuro -> faixa clara mantendo a ordem de profundidade.
    No escuro, quanto mais fundo o painel, mais escuro ele e; no claro
    esses mesmos niveis viram brancos levemente mais acinzentados.
    """
    out_l = 0.985 - (lig * 0.50)
    r, g, b = colorsys.hls_to_rgb(hue / 360.0, max(0.88, min(out_l, 0.99)), min(sat, 0.10))
    return _to_hex(r, g, b)


def _classify(value):
    """Devolve (cor_para_texto, cor_para_forma, cor_para_traco)."""
    hue, sat, lig = _hsl(value)

    if sat >= 0.45:
        accent = _accent_for_hue(hue)
        return accent, _tint_for_hue(hue, sat), accent

    if lig >= 0.72:
        # Era texto/traco claro sobre fundo preto.
        return _INK_TEXT, "#f7faf8", _INK_STROKE

    if lig <= 0.22:
        # Era painel de fundo. Texto preto continua preto; forma vira clara.
        return _INK_TEXT, _surface_for(hue, sat, lig), _FAINT_STROKE

    return _MUTED_TEXT, "#dce5e0", _MUTED_STROKE


def build_light_overrides(markup):
    """
    Varre o markup montado e devolve o bloco CSS do tema claro.
    Emite, por cor encontrada, no maximo tres regras disjuntas.
    """
    fills, strokes = set(), set()
    for attr, color in _COLOR_ATTR_RE.findall(markup):
        (fills if attr == "fill" else strokes).add(color.lower())

    linhas = [
        "/* ═══════════════════════════════════════════════════════",
        "   Traducao das cores fixas dos SVGs para fundo claro.",
        "   Gerado em build por light_mode_map.py a partir do markup real.",
        "   Atributo de apresentacao perde para CSS, entao nenhum",
        "   componente do esquema eletrico precisou ser reescrito.",
        "   ═══════════════════════════════════════════════════════ */",
    ]

    for color in sorted(fills):
        texto, forma, _ = _classify(color)
        linhas.append(
            'body.theme-light text[fill="%s"],\n'
            'body.theme-light tspan[fill="%s"] { fill: %s; }' % (color, color, texto)
        )
        linhas.append(
            'body.theme-light [fill="%s"]:not(text):not(tspan) { fill: %s; }'
            % (color, forma)
        )

    for color in sorted(strokes):
        _, _, traco = _classify(color)
        linhas.append('body.theme-light [stroke="%s"] { stroke: %s; }' % (color, traco))

    return "\n".join(linhas)
