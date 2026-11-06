"""Tiny SVG drawing helpers shared by build_diagrams.py.

No dependencies. Every diagram gets a white card background so it reads the
same in GitHub's light and dark themes.
"""
from html import escape

FONT = "Segoe UI, Helvetica, Arial, sans-serif"
MONO = "SFMono-Regular, Consolas, Menlo, monospace"

# One colour per topic, plus neutrals. (fill, stroke/text)
ONTO = ("#EFEBFB", "#5B45B0")
GRAPH = ("#E3F4F3", "#0B7477")
SEM = ("#FDEFE3", "#B45309")
EXAMPLE = ("#E7EFFD", "#2557C7")
NEUTRAL = ("#F2F4F7", "#475467")
GOOD = ("#E8F5E9", "#2E7D32")
WARN = ("#FFF8E1", "#9A6700")
LINEAGE = ("#FCE7F0", "#B4235A")
INK = "#1D2939"
MUTED = "#667085"


class Canvas:
    def __init__(self, width: int, height: int, title: str):
        self.w, self.h, self.title = width, height, title
        self.parts: list[str] = []

    # -- primitives ---------------------------------------------------------
    def rect(self, x, y, w, h, fill="#fff", stroke=NEUTRAL[1], rx=10, sw=1.5, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
                          f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def text(self, x, y, s, size=14, weight="normal", anchor="middle", color=INK, mono=False, italic=False, rotate=None):
        fam = MONO if mono else FONT
        st = ' font-style="italic"' if italic else ""
        if rotate is not None:
            st += f' transform="rotate({rotate} {x} {y})"'
        self.parts.append(f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" '
                          f'font-weight="{weight}" text-anchor="{anchor}" fill="{color}"{st}>{escape(s)}</text>')

    def lines(self, x, y, items, size=13, gap=18, anchor="middle", color=INK, mono=False, weight="normal"):
        for i, s in enumerate(items):
            self.text(x, y + i * gap, s, size=size, anchor=anchor, color=color, mono=mono, weight=weight)

    def line(self, x1, y1, x2, y2, color=MUTED, sw=1.6, dash=None, arrow=True, both=False):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        m = ' marker-end="url(#arrow)"' if arrow else ""
        if both:
            m += ' marker-start="url(#arrow-start)"'
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
                          f'stroke-width="{sw}"{d}{m}/>')

    def path(self, d, color=MUTED, sw=1.6, dash=None, arrow=True, fill="none"):
        da = f' stroke-dasharray="{dash}"' if dash else ""
        m = ' marker-end="url(#arrow)"' if arrow else ""
        self.parts.append(f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{sw}"{da}{m}/>')

    def circle(self, cx, cy, r, fill, stroke, sw=1.5):
        self.parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    # -- composites ---------------------------------------------------------
    def box(self, x, y, w, h, title, body=(), colors=NEUTRAL, title_size=15, body_size=12.5,
            body_gap=17, mono_body=False, dash=None):
        fill, stroke = colors
        self.rect(x, y, w, h, fill=fill, stroke=stroke, dash=dash)
        ty = y + 24 if body else y + h / 2 + title_size * 0.35
        self.text(x + w / 2, ty, title, size=title_size, weight="600", color=stroke)
        if body:
            self.lines(x + w / 2, ty + body_gap + 2, body, size=body_size, gap=body_gap, mono=mono_body)

    def label(self, x, y, s, size=12, color=MUTED, anchor="middle", bg=True):
        if bg:
            w = len(s) * size * 0.56 + 10
            ox = {"middle": w / 2, "start": 5, "end": w - 5}[anchor]
            self.parts.append(f'<rect x="{x - ox}" y="{y - size}" width="{w}" height="{size + 7}" '
                              f'rx="4" fill="#ffffff" opacity="0.92"/>')
        self.text(x, y, s, size=size, color=color, anchor=anchor)

    def heading(self, s, sub=None):
        self.text(28, 38, s, size=20, weight="700", anchor="start")
        if sub:
            self.text(28, 60, sub, size=13, anchor="start", color=MUTED)

    # -- output -------------------------------------------------------------
    def svg(self) -> str:
        defs = ('<defs>'
                f'<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
                f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker>'
                f'<marker id="arrow-start" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" '
                f'orient="auto"><path d="M10,0 L0,5 L10,10 z" fill="{MUTED}"/></marker>'
                '</defs>')
        bg = (f'<rect x="1" y="1" width="{self.w - 2}" height="{self.h - 2}" rx="14" fill="#ffffff" '
              f'stroke="#D0D5DD" stroke-width="1"/>')
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
                f'viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{escape(self.title)}">'
                f'<title>{escape(self.title)}</title>{defs}{bg}{"".join(self.parts)}</svg>\n')
