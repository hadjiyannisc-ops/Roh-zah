#!/usr/bin/env python3
"""Build a Roh-zah study report PDF from a JSON file.

Usage:
    python3 build_report.py report.json output.pdf

Text fields accept light markup:
    **bold**   *italic*   `code`   $inline math$   $$display math$$
    "- " at the start of a line makes a bullet; a blank line starts a new paragraph.
    Write \\$ for a literal dollar sign.

Requires reportlab; matplotlib is optional (used to typeset math).
See SCHEMA at the bottom of this file for the expected JSON fields.
"""

import json
import os
import re
import sys
import tempfile
from datetime import date
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.graphics.shapes import Drawing, Rect, Line
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle,
    KeepTogether, CondPageBreak, PageBreak, Image, Flowable,
)

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")

# ---------------------------------------------------------------- palette ---
INK = colors.HexColor("#16181D")
MUTED = colors.HexColor("#5E6470")
FAINT = colors.HexColor("#9AA0AA")
RULE = colors.HexColor("#DADDE2")
WASH = colors.HexColor("#F4F5F7")
ACCENT = colors.HexColor("#1F3A5F")
ACCENT_SOFT = colors.HexColor("#E7EDF5")
WARN = colors.HexColor("#8A2C2C")
GOOD = colors.HexColor("#2E5E3A")

# ------------------------------------------------------------------ fonts ---
SERIF, SERIF_B, SERIF_I, SERIF_BI = "Times-Roman", "Times-Bold", "Times-Italic", "Times-BoldItalic"
SANS, SANS_M, SANS_B = "Helvetica", "Helvetica", "Helvetica-Bold"
MONO = "Courier"


def _register_fonts():
    global SERIF, SERIF_B, SERIF_I, SERIF_BI, SANS, SANS_M, SANS_B, MONO
    files = {
        "PlexSerif": "IBMPlexSerif-Regular.ttf",
        "PlexSerif-SemiBold": "IBMPlexSerif-SemiBold.ttf",
        "PlexSerif-Italic": "IBMPlexSerif-Italic.ttf",
        "PlexSerif-SemiBoldItalic": "IBMPlexSerif-SemiBoldItalic.ttf",
        "PlexSans": "IBMPlexSans-Regular.ttf",
        "PlexSans-Medium": "IBMPlexSans-Medium.ttf",
        "PlexSans-SemiBold": "IBMPlexSans-SemiBold.ttf",
        "PlexSans-Italic": "IBMPlexSans-Italic.ttf",
        "PlexMono": "IBMPlexMono-Regular.ttf",
    }
    try:
        for name, fn in files.items():
            pdfmetrics.registerFont(TTFont(name, os.path.join(FONT_DIR, fn)))
    except Exception as exc:  # fonts missing: fall back to built-in PDF fonts
        print(f"note: bundled fonts unavailable ({exc}); using built-in fonts", file=sys.stderr)
        return
    from reportlab.pdfbase.pdfmetrics import registerFontFamily
    registerFontFamily("PlexSerif", normal="PlexSerif", bold="PlexSerif-SemiBold",
                       italic="PlexSerif-Italic", boldItalic="PlexSerif-SemiBoldItalic")
    registerFontFamily("PlexSans", normal="PlexSans", bold="PlexSans-SemiBold",
                       italic="PlexSans-Italic", boldItalic="PlexSans-SemiBold")
    SERIF, SERIF_B, SERIF_I, SERIF_BI = "PlexSerif", "PlexSerif-SemiBold", "PlexSerif-Italic", "PlexSerif-SemiBoldItalic"
    SANS, SANS_M, SANS_B = "PlexSans", "PlexSans-Medium", "PlexSans-SemiBold"
    MONO = "PlexMono"


_register_fonts()

# ----------------------------------------------------------------- styles ---
BODY_SIZE = 10


def S(name, **kw):
    base = dict(fontName=SERIF, fontSize=BODY_SIZE, leading=14.6, textColor=INK, spaceAfter=0)
    base.update(kw)
    return ParagraphStyle(name, **base)


ST = {
    "eyebrow": S("eyebrow", fontName=SANS_M, fontSize=7.5, leading=10, textColor=MUTED),
    "title": S("title", fontName=SERIF_B, fontSize=25, leading=30, textColor=INK),
    "meta": S("meta", fontName=SANS, fontSize=8.5, leading=12, textColor=MUTED),
    "lede": S("lede", fontSize=11.2, leading=16.6),
    "body": S("body"),
    "small": S("small", fontSize=8.8, leading=12.4, textColor=MUTED),
    "h_num": S("h_num", fontName=SANS_B, fontSize=8.5, leading=12, textColor=ACCENT),
    "h": S("h", fontName=SANS_B, fontSize=13.5, leading=17, textColor=INK),
    "h_intro": S("h_intro", fontSize=9.4, leading=13.4, textColor=MUTED),
    "item_title": S("item_title", fontName=SERIF_B, fontSize=10.6, leading=14.4),
    "label": S("label", fontName=SANS_M, fontSize=7.2, leading=10, textColor=MUTED),
    "th": S("th", fontName=SANS_M, fontSize=7.2, leading=9.5, textColor=MUTED),
    "td": S("td", fontSize=9.2, leading=12.6),
    "td_sans": S("td_sans", fontName=SANS, fontSize=8.6, leading=11.6, textColor=INK),
    "td_muted": S("td_muted", fontName=SANS, fontSize=8.2, leading=11.2, textColor=MUTED),
    "big_num": S("big_num", fontName=SERIF_B, fontSize=30, leading=32, textColor=ACCENT),
    "card": S("card", fontSize=9.4, leading=13.2),
    "card_num": S("card_num", fontName=SANS_M, fontSize=7.2, leading=10, textColor=FAINT),
}


BRIDGE_TAG = f'&nbsp;&nbsp;<font name="{SANS_M}" size="7" color="#854F0B">BRIDGE</font>'


def spaced(text):
    """Letter-space a short uppercase label."""
    return "&nbsp;".join(escape(text.upper()))


# ------------------------------------------------------------------- math ---
_MATH_DIR = tempfile.mkdtemp(prefix="rohzah_math_")
_math_count = [0]
try:
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib import mathtext
    from matplotlib.font_manager import FontProperties
    HAVE_MPL = True
except Exception:  # pragma: no cover
    HAVE_MPL = False


_MATRIX = re.compile(r"\\begin\{([pbvBV]?)matrix\}(.*?)\\end\{\1matrix\}", re.S)
_DELIMS = {"p": (r"\left(", r"\right)"), "b": (r"\left[", r"\right]"),
           "v": (r"\left|", r"\right|"), "V": (r"\left\Vert", r"\right\Vert"),
           "B": (r"\left\{", r"\right\}"), "": ("", "")}


def _unary_minus(tex):
    # mathtext spaces a leading minus like a binary operator: "(1, -1)" -> "(1, {-}1)"
    return re.sub(r"(^|[(\[{,=&;:])(\s*)-", r"\1\2{-}", tex)


def _matrix_to_mathtext(m):
    """mathtext has no matrix environments: rebuild them from stacks."""
    kind, body = m.group(1), m.group(2)
    rows = [r for r in re.split(r"\\\\", body) if r.strip()]
    cells = [[c.strip() or "{}" for c in r.split("&")] for r in rows]
    ncols = max(len(r) for r in cells)
    cells = [r + ["{}"] * (ncols - len(r)) for r in cells]
    cols = []
    for j in range(ncols):
        col = [cells[i][j] for i in range(len(cells))]
        if len(col) == 1:
            cols.append("{" + col[0] + "}")
        elif len(col) == 2:
            cols.append(r"\genfrac{}{}{0}{0}{" + col[0] + "}{" + col[1] + "}")
        else:
            cols.append(r"\substack{" + r"\\".join(col) + "}")
    left, right = _DELIMS.get(kind, ("", ""))
    return left + r"\ \ ".join(cols) + right


def _prepare_tex(tex):
    tex = _MATRIX.sub(_matrix_to_mathtext, tex)
    tex = tex.replace(r"\dfrac", r"\frac").replace(r"\tfrac", r"\frac")
    tex = re.sub(r"\\text\{([^}]*)\}", r"\\mathrm{\1}", tex)
    return _unary_minus(tex)


def _plain_tex(tex):
    """Last-resort readable fallback when mathtext can't parse something."""
    t = re.sub(r"\\(left|right|mathrm|mathbf|mathcal|operatorname|text)\b", "", tex)
    t = re.sub(r"\\([a-zA-Z]+)", r"\1", t)
    return re.sub(r"[{}]", "", t).replace("\\\\", "; ").strip()


def render_math(tex, size, display=False):
    """Render TeX to a PNG. Returns (path, width_pt, height_pt, depth_pt) or None."""
    if not HAVE_MPL:
        return None
    tex = _prepare_tex(tex)
    _math_count[0] += 1
    path = os.path.join(_MATH_DIR, f"m{_math_count[0]}.png")
    dpi = 600
    try:
        depth = mathtext.math_to_image(
            f"${tex}$", path,
            prop=FontProperties(size=size * (1.15 if display else 1.0), math_fontfamily="stix"),
            dpi=dpi, format="png", color="#16181D",
        )
        from PIL import Image as PILImage
        w_px, h_px = PILImage.open(path).size
    except Exception:
        return None
    return path, w_px / dpi * 72, h_px / dpi * 72, float(depth or 0)


# ----------------------------------------------------------------- markup ---
_MATH_SPLIT = re.compile(r"(\$\$.+?\$\$|(?<!\\)\$[^$\n]+?(?<!\\)\$)", re.S)


def _inline_markup(raw):
    t = escape(raw).replace("\\$", "$")
    t = re.sub(r"`([^`]+)`", lambda m: f'<font name="{MONO}" size="{BODY_SIZE * 0.9:.1f}">{m.group(1)}</font>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", t)
    return t


def rich(text, size=BODY_SIZE):
    """Convert one paragraph of light markup to ReportLab paragraph XML."""
    if text is None:
        return ""
    out = []
    for part in _MATH_SPLIT.split(str(text)):
        if not part:
            continue
        if part.startswith("$$") and part.endswith("$$") and len(part) > 4:
            part = "$" + part[2:-2] + "$"
        if part.startswith("$") and part.endswith("$") and len(part) > 2 and not part.startswith("\\$"):
            tex = part[1:-1].strip()
            r = render_math(tex, size)
            if r:
                path, w, h, depth = r
                out.append(f'<img src="{path}" width="{w:.2f}" height="{h:.2f}" valign="{-depth:.2f}"/>')
            else:
                out.append(f"<i>{escape(_plain_tex(tex))}</i>")
        else:
            out.append(_inline_markup(part))
    return "".join(out)


def blocks(text, style=None, bullet_style=None):
    """Turn multi-paragraph markup into flowables (paragraphs, bullets, display math)."""
    style = style or ST["body"]
    if not text:
        return []
    if isinstance(text, list):
        text = "\n".join(f"- {x}" for x in text)
    flow = []
    for para in re.split(r"\n\s*\n", str(text).strip()):
        para = para.strip()
        if not para:
            continue
        m = re.fullmatch(r"\$\$(.+?)\$\$", para, re.S)
        if m:
            r = render_math(m.group(1).strip(), style.fontSize, display=True)
            if r:
                path, w, h, _ = r
                img = Image(path, width=w, height=h)
                img.hAlign = "CENTER"
                flow += [Spacer(1, 3), img, Spacer(1, 5)]
                continue
        lines = para.split("\n")
        if all(l.strip().startswith(("- ", "• ")) for l in lines):
            bstyle = ParagraphStyle("b", parent=style, leftIndent=11, bulletIndent=0, spaceAfter=2.5)
            for l in lines:
                flow.append(Paragraph(rich(l.strip()[2:], style.fontSize), bstyle,
                                      bulletText="–"))
            flow.append(Spacer(1, 3))
        else:
            flow.append(Paragraph(rich(" ".join(l.strip() for l in lines), style.fontSize), style))
            flow.append(Spacer(1, 5))
    if flow and isinstance(flow[-1], Spacer):
        flow.pop()
    return flow


# ------------------------------------------------------------- flowables ---
class Rule(Flowable):
    def __init__(self, width=None, color=RULE, thickness=0.6, space_before=0, space_after=0):
        super().__init__()
        self.w, self.color, self.t = width, color, thickness
        self.sb, self.sa = space_before, space_after

    def wrap(self, aw, ah):
        self.width = self.w or aw
        return self.width, self.sb + self.sa + self.t

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.t)
        self.canv.line(0, self.sa, self.width, self.sa)


def level_bar(level, target, segments=5, seg_w=9.5, seg_h=6.5, gap=2):
    d = Drawing(segments * (seg_w + gap), seg_h + 2)
    for i in range(segments):
        x = i * (seg_w + gap)
        filled = i < round(level)
        d.add(Rect(x, 1, seg_w, seg_h, strokeColor=None,
                   fillColor=ACCENT if filled else colors.HexColor("#E3E6EA")))
        if i == int(target) - 1:
            d.add(Line(x + seg_w + gap / 2, 0, x + seg_w + gap / 2, seg_h + 2,
                       strokeColor=INK, strokeWidth=0.9))
    return d


def section(num, title, intro=None):
    items = [
        CondPageBreak(60 * mm),
        Spacer(1, 16),
        Paragraph(f"{num:02d}", ST["h_num"]),
        Spacer(1, 1),
        Paragraph(escape(title), ST["h"]),
        Spacer(1, 5),
        Rule(color=INK, thickness=0.8),
        Spacer(1, 9),
    ]
    if intro:
        items += [Paragraph(rich(intro, 9.4), ST["h_intro"]), Spacer(1, 9)]
    return items


def labelled(label, text, color=MUTED, style=None):
    style = style or ST["body"]
    lab = ParagraphStyle("lab", parent=ST["label"], textColor=color)
    return [Paragraph(spaced(label), lab), Spacer(1, 1.5)] + blocks(text, style) + [Spacer(1, 6)]


def clean_table(data, col_widths, header=True, zebra=False, valign="TOP", pad=5):
    t = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
    cmds = [
        ("VALIGN", (0, 0), (-1, -1), valign),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), pad),
        ("BOTTOMPADDING", (0, 0), (-1, -1), pad + 1),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, RULE),
    ]
    if header:
        cmds += [("LINEBELOW", (0, 0), (-1, 0), 0.8, INK), ("BOTTOMPADDING", (0, 0), (-1, 0), 4)]
    t.setStyle(TableStyle(cmds))
    return t


# ------------------------------------------------------------ page chrome ---
class NumberedCanvas(rl_canvas.Canvas):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._saved = []

    def showPage(self):
        self._saved.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._saved)
        for state in self._saved:
            self.__dict__.update(state)
            self._footer(total)
            super().showPage()
        super().save()

    def _footer(self, total):
        w, _ = A4
        self.setFont(SANS, 7.5)
        self.setFillColor(FAINT)
        self.drawString(22 * mm, 12 * mm, getattr(self, "_rz_footer", "Roh-zah study report"))
        self.drawRightString(w - 22 * mm, 12 * mm, f"{self._pageNumber} / {total}")
        self.setStrokeColor(RULE)
        self.setLineWidth(0.5)
        self.line(22 * mm, 16 * mm, w - 22 * mm, 16 * mm)


# ----------------------------------------------------------------- build ---
def as_list(x):
    if x is None:
        return []
    return x if isinstance(x, list) else [x]


def build(data, out_path):
    W, H = A4
    margin_x = 22 * mm
    frame = Frame(margin_x, 22 * mm, W - 2 * margin_x, H - 20 * mm - 22 * mm, id="f",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    course = data.get("course") or "Course"
    footer = f"{course}  ·  Study report"

    def on_page(c, doc):
        c._rz_footer = footer

    doc = BaseDocTemplate(out_path, pagesize=A4, title=f"{course}: study report",
                          author=data.get("learner") or "Roh-zah", subject="Study report")
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=on_page)])
    tw = W - 2 * margin_x
    f = []

    # ---- header
    f += [Paragraph(spaced("Roh-zah") + "&nbsp;&nbsp;&nbsp;·&nbsp;&nbsp;&nbsp;" + spaced("Study report"),
                    ST["eyebrow"]), Spacer(1, 7)]
    f += [Paragraph(escape(course), ST["title"]), Spacer(1, 6)]
    exam = data.get("exam") or {}
    meta = []
    if data.get("learner"):
        meta.append(escape(data["learner"]))
    if exam.get("date") or exam.get("format"):
        meta.append("Exam " + escape(" · ".join(x for x in [exam.get("date"), exam.get("format")] if x)))
    meta.append("Report " + escape(data.get("date") or date.today().isoformat()))
    if data.get("sessions"):
        meta.append(f"{escape(str(data['sessions']))} sessions")
    f += [Paragraph("&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;".join(meta), ST["meta"])]
    if data.get("materials"):
        f += [Spacer(1, 2), Paragraph("Materials: " + escape(", ".join(as_list(data["materials"]))), ST["meta"])]
    f += [Spacer(1, 12), Rule(color=INK, thickness=1.1), Spacer(1, 12)]
    f += blocks(data.get("summary"), ST["lede"])

    n = 0
    # ---- 01 readiness
    skills = as_list(data.get("skills"))
    if skills:
        n += 1
        f += section(n, "Exam readiness",
                     "Levels: 0 unaware · 1 heard of it · 2 can follow · 3 can do with help · "
                     "4 can do independently · 5 can teach it. The vertical tick marks your target.")
        tgt_default = data.get("target_level", 4)
        core = [s for s in skills if not s.get("bridge")] or skills
        ratios = [min(float(s.get("level", 0)), float(s.get("target", tgt_default))) /
                  max(float(s.get("target", tgt_default)), 1) for s in core]
        overall = round(100 * sum(ratios) / len(ratios))
        rows = [[Paragraph(spaced("Topic"), ST["th"]), Paragraph(spaced("Level"), ST["th"]), "",
                 Paragraph(spaced("Next review"), ST["th"]), Paragraph(spaced("Note"), ST["th"])]]
        for s in skills:
            lvl = float(s.get("level", 0))
            tgt = int(s.get("target", tgt_default))
            name_xml = rich(s.get("name", ""), 9.2)
            if s.get("bridge"):
                name_xml += BRIDGE_TAG
            rows.append([
                Paragraph(name_xml, ST["td"]),
                level_bar(lvl, tgt),
                Paragraph(f"{lvl:g}/5", ST["td_sans"]),
                Paragraph(escape(str(s.get("next_review", "") or "")), ST["td_muted"]),
                Paragraph(rich(s.get("note", ""), 8.2), ST["td_muted"]),
            ])
        table = clean_table(rows, [tw * 0.31, 58, 26, tw * 0.15, None], valign="MIDDLE")
        head = Table([[Paragraph(f"{overall}%", ST["big_num"]),
                       Paragraph("<b>Overall readiness</b><br/>Average progress toward your target level "
                                 "across all topics from your material (bridges excluded).", ST["small"])]],
                     colWidths=[30 * mm, None])
        head.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                                  ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
        f += [head, Spacer(1, 10), table]

    # ---- 02 covered
    covered = as_list(data.get("covered"))
    if covered:
        n += 1
        f += section(n, "What we covered")
        for i, c in enumerate(covered, 1):
            title = f'<font name="{SANS_M}" color="#9AA0AA" size="8">{i:02d}</font>&nbsp;&nbsp;' + rich(c.get("title", ""), 10.6)
            if c.get("bridge"):
                title += BRIDGE_TAG
            if c.get("source"):
                title += f'&nbsp;&nbsp;<font name="{SANS}" color="#9AA0AA" size="7.5">{escape(c["source"])}</font>'
            item = [Paragraph(title, ST["item_title"]), Spacer(1, 3)]
            item += blocks(c.get("summary"), ST["body"])
            if c.get("points"):
                item += [Spacer(1, 2)] + blocks(as_list(c["points"]), ST["body"])
            f += [KeepTogether(item), Spacer(1, 10)]

    # ---- strengths
    strengths = as_list(data.get("strengths"))
    if strengths:
        n += 1
        f += section(n, "Strengths", "What you have demonstrated reliably, with the evidence.")
        rows = []
        for s in strengths:
            rows.append([Paragraph('<font color="#2E5E3A">+</font>', S("plus", fontName=SANS_B, fontSize=11, leading=13)),
                         [Paragraph(rich(s.get("title", ""), 10.6), ST["item_title"]), Spacer(1, 2)]
                         + blocks(s.get("evidence"), ST["small"])])
        f.append(clean_table(rows, [14, None], header=False, pad=6))

    # ---- weaknesses
    weaknesses = as_list(data.get("weaknesses"))
    if weaknesses:
        n += 1
        f += section(n, "Weaknesses to fix",
                     "Each one: the wrong model you held, the correct model, and what to do about it.")
        for w in weaknesses:
            inner = [Paragraph(rich(w.get("title", ""), 10.6), ST["item_title"]), Spacer(1, 6)]
            if w.get("misconception"):
                inner += labelled("What you thought", w["misconception"], WARN)
            if w.get("correction"):
                inner += labelled("What is actually true", w["correction"], GOOD)
            if w.get("action"):
                inner += labelled("What to do", w["action"], ACCENT)
            box = Table([[inner]], colWidths=[tw])
            box.setStyle(TableStyle([
                ("LINEBEFORE", (0, 0), (0, -1), 2, WARN),
                ("BACKGROUND", (0, 0), (-1, -1), WASH),
                ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]))
            f += [KeepTogether([box]), Spacer(1, 9)]

    # ---- redo problems
    redo = as_list(data.get("redo"))
    if redo:
        n += 1
        f += section(n, "Problems to redo",
                     "Problems you missed or needed heavy hints on. Try them again cold, without notes. "
                     "Solutions are in the appendix.")
        for i, p in enumerate(redo, 1):
            tag = " · ".join(x for x in [p.get("topic"), p.get("miss_type")] if x)
            head = f'<font name="{SANS_B}" color="#1F3A5F">Problem {i}</font>'
            if tag:
                head += f'&nbsp;&nbsp;<font name="{SANS}" color="#9AA0AA" size="7.8">{escape(tag)}</font>'
            item = [Paragraph(head, S("ph", fontName=SANS_B, fontSize=9.5, leading=13)), Spacer(1, 4)]
            item += blocks(p.get("problem"), ST["body"]) + [Spacer(1, 7)]
            if p.get("your_answer"):
                item += labelled("Your answer", p["your_answer"], MUTED, ST["small"])
            if p.get("what_went_wrong"):
                item += labelled("Where it went wrong", p["what_went_wrong"], WARN, ST["small"])
            if p.get("hint"):
                item += labelled("Hint, only if stuck", p["hint"], ACCENT, ST["small"])
            f += [KeepTogether(item), Rule(space_before=2, space_after=10)]

    # ---- flashcards
    cards = as_list(data.get("flashcards"))
    if cards:
        n += 1
        f += section(n, "Flashcards",
                     "Fold the page along the dashed line, or cover the right column, and answer each card "
                     "out loud before checking.")
        rows = [[Paragraph(spaced("Front"), ST["th"]), Paragraph(spaced("Back"), ST["th"])]]
        for i, c in enumerate(cards, 1):
            front = [Paragraph(f"{i:02d}" + (f"&nbsp;&nbsp;·&nbsp;&nbsp;{escape(c['topic'])}" if c.get("topic") else ""),
                               ST["card_num"]), Spacer(1, 2)] + blocks(c.get("front"), ST["card"])
            back = [Paragraph("&nbsp;", ST["card_num"]), Spacer(1, 2)] + blocks(c.get("back"), ST["card"])
            rows.append([front, back])
        t = Table(rows, colWidths=[tw / 2, tw / 2], repeatRows=1)
        t.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (0, -1), 0), ("RIGHTPADDING", (0, 0), (0, -1), 14),
            ("LEFTPADDING", (1, 0), (1, -1), 14), ("RIGHTPADDING", (1, 0), (1, -1), 0),
            ("TOPPADDING", (0, 1), (-1, -1), 7), ("BOTTOMPADDING", (0, 1), (-1, -1), 9),
            ("LINEBELOW", (0, 0), (-1, 0), 0.8, INK),
            ("LINEBELOW", (0, 1), (-1, -1), 0.5, RULE),
            ("LINEAFTER", (0, 1), (0, -1), 0.7, FAINT, None, (2, 2.5)),
        ]))
        f.append(t)

    # ---- plan
    schedule = as_list(data.get("review_schedule"))
    next_steps = data.get("next_steps")
    if schedule or next_steps:
        n += 1
        plan = []
        if schedule:
            rows = [[Paragraph(spaced("When"), ST["th"]), Paragraph(spaced("What to review"), ST["th"])]]
            for r in schedule:
                rows.append([Paragraph(escape(str(r.get("date", ""))), ST["td_sans"]),
                             Paragraph(rich(", ".join(as_list(r.get("items"))), 9.2), ST["td"])])
            plan += [clean_table(rows, [32 * mm, None]), Spacer(1, 12)]
        if next_steps:
            plan += [Paragraph(spaced("Next steps"), ST["label"]), Spacer(1, 3)]
            plan += blocks(as_list(next_steps), ST["body"])
        sec = section(n, "Plan until the exam")
        f += sec[:1] + [KeepTogether(sec[1:] + plan)]

    # ---- appendix: solutions
    sols = [(i, p) for i, p in enumerate(redo, 1) if p.get("solution")]
    if sols:
        f += [PageBreak(), Paragraph(spaced("Appendix"), ST["h_num"]), Spacer(1, 1),
              Paragraph("Solutions to the redo problems", ST["h"]), Spacer(1, 5),
              Rule(color=INK, thickness=0.8), Spacer(1, 9),
              Paragraph("Read these only after a genuine attempt.", ST["h_intro"]), Spacer(1, 9)]
        for i, p in sols:
            item = [Paragraph(f'<font name="{SANS_B}" color="#1F3A5F">Problem {i}</font>',
                              S("sh", fontName=SANS_B, fontSize=9.5, leading=13)), Spacer(1, 4)]
            item += blocks(p.get("solution"), ST["body"])
            f += [KeepTogether(item), Rule(space_before=4, space_after=10)]

    f += [Spacer(1, 18), Paragraph("Generated with Roh-zah.", ST["small"])]
    doc.build(f, canvasmaker=NumberedCanvas)
    return out_path


SCHEMA = """
{
  "course": "Thermodynamics I",                      // required
  "learner": "Name (optional)",
  "date": "2026-11-16",
  "exam": {"date": "2026-12-12", "format": "Written, 3 hours"},
  "materials": ["Lecture slides 1-9.pdf"],
  "sessions": 4,
  "target_level": 4,
  "summary": "Two or three sentences on where the learner stands.",
  "skills": [{"name": "...", "level": 3, "target": 4, "next_review": "2026-11-20", "note": "..."}],
  "covered": [{"title": "...", "source": "Slides 4-9", "summary": "...", "points": ["...", "..."]}],
  "strengths": [{"title": "...", "evidence": "..."}],
  "weaknesses": [{"title": "...", "misconception": "...", "correction": "...", "action": "..."}],
  "redo": [{"problem": "...", "topic": "...", "miss_type": "wrong idea chosen",
            "your_answer": "...", "what_went_wrong": "...", "hint": "...", "solution": "..."}],
  "flashcards": [{"front": "...", "back": "...", "topic": "..."}],
  "review_schedule": [{"date": "2026-11-20", "items": ["...", "..."]}],
  "next_steps": ["...", "..."]
}
"""

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        print("JSON schema:", SCHEMA)
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as fh:
        payload = json.load(fh)
    print(build(payload, sys.argv[2]))
