#!/usr/bin/env python3
"""
BAMBU LAB P1S / P2S – BAUHAUS MODULLAMPE
3D-Print Technical Drawing Generator – 7 x A4 landscape SVG sheets.

Build volume Bambu Lab P1S/P2S: 256 x 256 x 256 mm
All elements verified to fit on one plate.
Bayonet: 4-pin, 90 deg quarter-turn, male top / female bottom.
Cable channel: 44 mm dia (Schuko cable + IKEA STRALA E14 pendant).
"""

import math, os

OUT = "/home/user/WC-Buch/lamp_sheets"
os.makedirs(OUT, exist_ok=True)

# ─── Page (A4 landscape at 3 px/mm) ───────────────────────────────────────
PX   = 3            # px per mm
A4W  = 297 * PX    # 891 px
A4H  = 210 * PX    # 630 px

# ─── Colours ──────────────────────────────────────────────────────────────
BG     = "#f8f5ef"
PART   = "#d4c8b0"   # printed plastic (warm grey-beige)
PART_D = "#7a6a50"   # dark edges
GRAIN  = "#bfb09a"   # slight texture
HOLLOW = "#e8e4dc"   # cable channel
RUBBER = "#303030"
RED    = "#b01010"   # dims / centre
BLUE   = "#1a4a80"   # info
BLACK  = "#151208"
GRAY   = "#50483c"
WHITE  = "#ffffff"
GREEN  = "#206020"   # print OK

# ─── Key dimensions (mm) ──────────────────────────────────────────────────
PLATE = 256         # Bambu Lab build plate mm
INNER_R  = 22.0    # cable channel radius → Ø44 mm (Schuko Ø≤19 mm)
BAY_R    = 29.0    # bayonet outer radius → Ø58 mm
BAY_H    = 4.0     # bayonet collar height (each side)
PIN_W    = 5.0     # pin width
PIN_H    = 2.5     # pin height (above collar face)
WALL     = BAY_R - INNER_R   # ~7 mm wall

def p(v):
    """mm → px"""
    return v * PX

# ─── SVG primitives ────────────────────────────────────────────────────────

def hdr(title="", w=A4W, h=A4H):
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{w/PX:.1f}mm" height="{h/PX:.1f}mm" '
            f'viewBox="0 0 {w} {h}">\n'
            f'<!-- {title} -->\n'
            f'<rect width="{w}" height="{h}" fill="{BG}"/>\n')

def defs():
    return f"""<defs>
  <pattern id="pl" x="0" y="0" width="{p(3)}" height="{p(3)}"
           patternUnits="userSpaceOnUse">
    <rect width="{p(3)}" height="{p(3)}" fill="{PART}"/>
    <line x1="0" y1="{p(3)}" x2="{p(3)}" y2="0"
          stroke="{GRAIN}" stroke-width="0.6" opacity="0.6"/>
  </pattern>
  <pattern id="hol" x="0" y="0" width="{p(3)}" height="{p(3)}"
           patternUnits="userSpaceOnUse">
    <rect width="{p(3)}" height="{p(3)}" fill="{HOLLOW}"/>
  </pattern>
</defs>\n"""

def ftr():
    return "</svg>\n"

def rct(x,y,w,h,fill="none",stroke=BLACK,sw=1,rx=0):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" '
            f'width="{w:.1f}" height="{h:.1f}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" rx="{rx}"/>\n')

def ln(x1,y1,x2,y2,stroke=BLACK,sw=1,dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" '
            f'x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{stroke}" stroke-width="{sw}"{d}/>\n')

def ci(cx,cy,r,fill="none",stroke=BLACK,sw=1):
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n')

def pa(d,fill="none",stroke=BLACK,sw=1):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n'

def tx(x,y,s,sz=8,anchor="middle",bold=False,fill=BLACK,
       font="Arial,Helvetica,sans-serif"):
    safe = str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
    fw = "bold" if bold else "normal"
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{sz}" '
            f'text-anchor="{anchor}" font-weight="{fw}" '
            f'fill="{fill}" font-family="{font}">{safe}</text>\n')

def mono(x,y,s,**kw):
    return tx(x,y,s,font="Courier New,Courier,monospace",**kw)

# ─── Dimension helpers ─────────────────────────────────────────────────────

def dh(x1,x2,y,label,above=True,off=p(5)):
    """Horizontal dimension line."""
    sign = -1 if above else 1
    ty = y + sign*(off + p(1))
    out  = ln(x1,y,x2,y,RED,0.6)
    out += ln(x1,y-p(2),x1,y+p(2),RED,0.6)
    out += ln(x2,y-p(2),x2,y+p(2),RED,0.6)
    out += mono((x1+x2)/2, ty + (0 if above else p(4)), label, sz=7, fill=RED)
    return out

def dv(x,y1,y2,label,left=True,off=p(6)):
    """Vertical dimension line."""
    sign = -1 if left else 1
    anchor = "end" if left else "start"
    tx_x = x + sign*(off)
    out  = ln(x,y1,x,y2,RED,0.6)
    out += ln(x-p(2),y1,x+p(2),y1,RED,0.6)
    out += ln(x-p(2),y2,x+p(2),y2,RED,0.6)
    out += mono(tx_x,(y1+y2)/2+p(2),label,sz=7,fill=RED,anchor=anchor)
    return out

def cl(cx,y0,y1,ext=p(6)):
    """Red chain centre-line."""
    return ln(cx,y0-ext,cx,y1+ext,RED,0.5,"5,2.5,1.5,2.5")

# ─── 3D-print fill (hatched polygon) ──────────────────────────────────────

def part_rect(x,y,w,h,sw=1.8):
    out  = rct(x,y,w,h,fill="url(#pl)",stroke=PART_D,sw=sw)
    return out

def part_poly(pts,sw=1.8):
    d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x,y in pts) + " Z"
    return pa(d, fill="url(#pl)", stroke=PART_D, sw=sw)

def hole_rect(cx,y,h,r=p(INNER_R)):
    return rct(cx-r, y, r*2, h, fill="url(#hol)", stroke=PART_D, sw=0.7)

# ─── Bayonet collar ────────────────────────────────────────────────────────

def bay_collar(cx, y_face, male=True, scale=1.0):
    """Cross-section: bayonet locking collar (M has pins, F has slots)."""
    W  = p(BAY_R*2) * scale
    H  = p(BAY_H) * scale
    IR = p(INNER_R) * scale
    PW = p(PIN_W) * scale
    PH = p(PIN_H) * scale
    out  = part_rect(cx-W/2, y_face, W, H, sw=1.2)
    out += hole_rect(cx, y_face, H, r=IR)
    for dx in [-W/4, W/4]:
        if male:
            out += rct(cx+dx-PW/2, y_face, PW, PH,
                       fill=PART_D, stroke=PART_D, sw=0.3)
        else:
            out += rct(cx+dx-PW/2, y_face, PW, H,
                       fill=HOLLOW, stroke=PART_D, sw=0.3)
    return out

# ─── Print-bed outline (to show element fits) ─────────────────────────────

def bed_outline(cx, cy, elem_w_mm, elem_h_mm, scale, ok=True):
    """Dashed square showing Bambu Lab build plate vs element footprint."""
    BED = p(PLATE) * scale
    EW  = p(elem_w_mm) * scale
    EH  = p(elem_h_mm) * scale
    col = GREEN if ok else RED
    out  = rct(cx-BED/2, cy-BED/2, BED, BED, fill="none",
               stroke=col, sw=0.7, rx=0)
    out += rct(cx-EW/2, cy-EH/2, EW, EH, fill=col, stroke=col, sw=0, rx=0)
    out  = pa(f"M {cx-BED/2:.1f},{cy-BED/2:.1f} h {BED:.1f} v {BED:.1f} h {-BED:.1f} Z",
              fill="none", stroke=col, sw=0.8)
    out += rct(cx-EW/2, cy-EH/2, EW, EH,
               fill=col.replace("20","80"), stroke=col, sw=0.5, rx=0)
    # labels
    pct_w = elem_w_mm / PLATE * 100
    pct_h = elem_h_mm / PLATE * 100
    out += tx(cx, cy-BED/2-p(2), f"Druckbett 256x256mm", sz=6, fill=col)
    out += tx(cx, cy,
              f"{elem_w_mm:.0f}x{elem_h_mm:.0f}mm ({pct_w:.0f}% Breite)",
              sz=6, fill=col)
    return out

# ─── Top-view (plan) of round element ─────────────────────────────────────

def top_view(cx, cy, outer_r_mm, scale, label="Draufsicht"):
    OR = p(outer_r_mm) * scale
    IR = p(INNER_R) * scale
    BR = p(BAY_R) * scale
    out  = ci(cx, cy, OR, fill="url(#pl)", stroke=PART_D, sw=1.5)
    out += ci(cx, cy, IR, fill="url(#hol)", stroke=PART_D, sw=0.8)
    # bayonet pins
    for a in range(0, 360, 90):
        rad = math.radians(a)
        bx = cx + BR * math.cos(rad)
        by = cy + BR * math.sin(rad)
        out += ci(bx, by, p(PIN_W/2)*scale, fill=PART_D, stroke=PART_D, sw=0.3)
    out += tx(cx, cy+OR+p(6)*scale, label, sz=6.5, fill=GRAY)
    return out

# ═══════════════════════════════════════════════════════════════════════════
# THE 6 ELEMENTS
# All take (cx, cy_mid, s=scale) and return SVG string.
# ═══════════════════════════════════════════════════════════════════════════

def el_A(cx, cy, s=1.4):
    """Fuss 1 – Flache Kreisscheibe  Ø120 x 32 mm  (fits 120x120 on plate)."""
    W=p(120)*s; H=p(32)*s; RH=p(10)*s
    IR=p(INNER_R)*s; BH=p(BAY_H)*s
    x0=cx-W/2; y0=cy-H/2
    out  = part_rect(x0, y0, W, H)
    out += rct(x0, y0+H-RH, W, RH, fill=RUBBER, stroke=PART_D, sw=0.8, rx=p(2)*s)
    out += hole_rect(cx, y0, H, r=IR)
    out += bay_collar(cx, y0-BH, male=True, scale=s)
    out += cl(cx, y0-BH, y0+H)
    out += dh(x0, x0+W, y0+H+p(14)*s, "120 mm", above=False, off=p(4)*s)
    out += dh(cx-IR, cx+IR, y0-BH-p(12)*s, "Kanal 44 mm", above=True, off=p(4)*s)
    out += dv(x0-p(14)*s, y0, y0+H, "32 mm", left=True, off=p(4)*s)
    out += dv(x0-p(8)*s, y0+H-RH, y0+H, "10 mm", left=True, off=p(2)*s)
    return out

def el_B(cx, cy, s=1.4):
    """Fuss 2 – Konus-Dreifuss  Ø140 (unten) → Ø58 (oben) x 55 mm."""
    W_top=p(58)*s; W_bot=p(140)*s; H=p(55)*s
    IR=p(INNER_R)*s; BH=p(BAY_H)*s
    y0=cy-H/2; y1=cy+H/2
    pts=[(cx-W_top/2,y0),(cx+W_top/2,y0),(cx+W_bot/2,y1),(cx-W_bot/2,y1)]
    out  = part_poly(pts)
    d = (f"M {cx-IR:.1f},{y0:.1f} L {cx+IR:.1f},{y0:.1f} "
         f"L {cx+IR:.1f},{y1:.1f} L {cx-IR:.1f},{y1:.1f} Z")
    out += pa(d, fill="url(#hol)", stroke=PART_D, sw=0.7)
    out += ln(cx-W_bot/2, y1, cx+W_bot/2, y1, PART_D, 2)
    # rubber feet
    for dx in [-W_bot/2+p(12)*s, W_bot/2-p(12)*s]:
        out += ci(cx+dx, y1+p(5)*s, p(5)*s, fill=RUBBER, stroke=PART_D, sw=0.8)
    out += bay_collar(cx, y0-BH, male=True, scale=s)
    out += cl(cx, y0-BH, y1+p(6)*s)
    out += dh(cx-W_bot/2, cx+W_bot/2, y1+p(16)*s, "140 mm", above=False, off=p(4)*s)
    out += dh(cx-W_top/2, cx+W_top/2, y0-BH-p(12)*s, "58 mm", above=True, off=p(4)*s)
    out += dv(cx+W_bot/2+p(14)*s, y0, y1, "55 mm", left=False, off=p(4)*s)
    return out

def el_C(cx, cy, s=1.4):
    """Schirm 1 – Bauhaus Disc  Ø180 x 25 mm  (M+F Bajonett)."""
    W=p(180)*s; H=p(25)*s
    IR=p(INNER_R)*s; BH=p(BAY_H)*s
    x0=cx-W/2; y0=cy-H/2
    out  = part_rect(x0, y0, W, H)
    out += hole_rect(cx, y0, H, r=IR)
    out += bay_collar(cx, y0-BH, male=True, scale=s)    # top M
    out += bay_collar(cx, y0+H,  male=False, scale=s)   # bottom F
    out += cl(cx, y0-BH, y0+H+BH)
    out += dh(x0, x0+W, y0+H+BH+p(14)*s, "180 mm", above=False, off=p(4)*s)
    out += dh(cx-IR, cx+IR, y0-BH-p(12)*s, "Kanal 44 mm", above=True, off=p(4)*s)
    out += dv(x0-p(14)*s, y0, y0+H, "25 mm", left=True, off=p(4)*s)
    # M/F label
    out += tx(cx+W/2+p(20)*s, y0-BH/2, "M (Stecker)", sz=7, fill=BLUE, anchor="start")
    out += tx(cx+W/2+p(20)*s, y0+H+BH/2, "F (Buchse)", sz=7, fill=BLUE, anchor="start")
    return out

def el_D(cx, cy, s=1.4):
    """Schirm 2 – Konus-Schirm (down)  Ø200 unten, Ø58 oben, H=75 mm."""
    W_top=p(58)*s; W_bot=p(200)*s; H=p(75)*s
    IR=p(INNER_R)*s; BH=p(BAY_H)*s
    y0=cy-H/2; y1=cy+H/2
    pts=[(cx-W_top/2,y0),(cx+W_top/2,y0),(cx+W_bot/2,y1),(cx-W_bot/2,y1)]
    out  = part_poly(pts)
    d = (f"M {cx-IR:.1f},{y0:.1f} L {cx+IR:.1f},{y0:.1f} "
         f"L {cx+IR:.1f},{y1:.1f} L {cx-IR:.1f},{y1:.1f} Z")
    out += pa(d, fill="url(#hol)", stroke=PART_D, sw=0.7)
    out += ln(cx-W_bot/2, y1, cx+W_bot/2, y1, PART_D, 2)
    out += bay_collar(cx, y0-BH, male=True, scale=s)
    out += cl(cx, y0-BH, y1+p(4)*s)
    out += dh(cx-W_bot/2, cx+W_bot/2, y1+p(14)*s, "200 mm", above=False, off=p(4)*s)
    out += dh(cx-W_top/2, cx+W_top/2, y0-BH-p(12)*s, "58 mm", above=True, off=p(4)*s)
    out += dv(cx+W_bot/2+p(16)*s, y0, y1, "75 mm", left=False, off=p(4)*s)
    out += tx(cx, y1+p(26)*s, "offen (Licht nach unten)", sz=7, fill=GRAY)
    return out

def el_E(cx, cy, s=1.4):
    """Schirm 3 – Dom-Schirm (up/ambient)  Ø190 x 60 mm."""
    W_BASE=p(58)*s; W_DOME=p(190)*s; H=p(60)*s; H_SK=p(15)*s
    IR=p(INNER_R)*s; BH=p(BAY_H)*s
    y_bot=cy+H/2; y_sk=y_bot-H_SK; y_ap=y_bot-H
    RX=W_DOME/2; RY=H-H_SK

    d_out=(f"M {cx-W_BASE/2:.1f},{y_bot:.1f} "
           f"L {cx-W_DOME/2:.1f},{y_sk:.1f} "
           f"A {RX:.1f} {RY:.1f} 0 0 1 {cx+W_DOME/2:.1f},{y_sk:.1f} "
           f"L {cx+W_BASE/2:.1f},{y_bot:.1f} Z")
    out  = pa(d_out, fill="url(#pl)", stroke=PART_D, sw=1.8)
    out += hole_rect(cx, y_bot-H_SK, H_SK, r=IR)
    d_in=(f"M {cx-IR:.1f},{y_bot:.1f} L {cx-IR:.1f},{y_sk:.1f} "
          f"A {IR:.1f} {RY*0.3:.1f} 0 0 1 {cx+IR:.1f},{y_sk:.1f} "
          f"L {cx+IR:.1f},{y_bot:.1f} Z")
    out += pa(d_in, fill="url(#hol)", stroke=PART_D, sw=0.7)
    out += bay_collar(cx, y_bot, male=False, scale=s)
    out += cl(cx, y_ap-p(4)*s, y_bot+BH)
    out += dh(cx-W_DOME/2, cx+W_DOME/2, y_sk+p(8)*s, "190 mm", above=False, off=p(3)*s)
    out += dh(cx-W_BASE/2, cx+W_BASE/2, y_bot+BH+p(12)*s, "58 mm", above=False, off=p(4)*s)
    out += dv(cx+W_DOME/2+p(16)*s, y_ap, y_bot, "60 mm", left=False, off=p(4)*s)
    out += dv(cx-W_DOME/2-p(14)*s, y_sk, y_bot, "15 mm", left=True, off=p(4)*s)
    out += tx(cx, y_ap-p(8)*s, "Licht nach oben / Ambient", sz=7, fill=BLUE)
    return out

def el_F(cx, cy, s=1.4):
    """Stiel / Verbinder  Ø58 x 100 mm  (M oben, F unten, stapelbar)."""
    W=p(58)*s; H=p(100)*s
    IR=p(INNER_R)*s; BH=p(BAY_H)*s
    x0=cx-W/2; y0=cy-H/2
    out  = part_rect(x0, y0, W, H)
    out += hole_rect(cx, y0, H, r=IR)
    out += bay_collar(cx, y0-BH, male=True, scale=s)
    out += bay_collar(cx, y0+H,  male=False, scale=s)
    out += cl(cx, y0-BH, y0+H+BH)
    out += dv(x0-p(14)*s, y0, y0+H, "100 mm", left=True, off=p(4)*s)
    out += dh(x0, x0+W, y0+H+BH+p(12)*s, "58 mm", above=False, off=p(4)*s)
    out += dh(cx-IR, cx+IR, y0-BH-p(12)*s, "Kanal 44 mm", above=True, off=p(4)*s)
    out += tx(cx+W/2+p(20)*s, cy-p(8), "Stapelbar:", sz=7, fill=BLUE, anchor="start", bold=True)
    out += tx(cx+W/2+p(20)*s, cy+p(2), "2 Stiels = 200 mm",
              sz=7, fill=BLUE, anchor="start")
    out += tx(cx+W/2+p(20)*s, cy+p(10), "3 Stiels = 300 mm",
              sz=7, fill=GRAY, anchor="start")
    return out

# ═══════════════════════════════════════════════════════════════════════════
# TITLE BLOCK
# ═══════════════════════════════════════════════════════════════════════════

def title_block(eid, ename, scale="1:1.4", sheet="1/7"):
    TH = p(18); y = A4H - TH
    out  = rct(0, y, A4W, TH, fill="#f0ece0", stroke=BLACK, sw=1)
    # verticals
    for xd in [p(55), p(145), p(220), A4W-p(18)]:
        out += ln(xd, y, xd, A4H, BLACK, 0.5)
    # content
    out += mono(p(27.5), y+p(6.5), "BAMBU LAB P1S / P2S", sz=8, bold=True)
    out += mono(p(27.5), y+p(13), "Bauhaus Modullampe", sz=7, fill=GRAY)
    out += mono(p(100), y+p(7.5), f"Element {eid}: {ename}", sz=10, bold=True)
    out += mono(p(182.5), y+p(6.5), f"Massstab: {scale}", sz=8, fill=GRAY)
    out += mono(p(182.5), y+p(13), "Masse in mm", sz=7, fill=GRAY)
    out += mono(p(238), y+p(6.5), f"Blatt {sheet}", sz=8, fill=GRAY)
    out += mono(p(238), y+p(13), "Druck: A4 quer", sz=7, fill=GRAY)
    return out, y

def border():
    m = p(4)
    return rct(m, m, A4W-2*m, A4H-2*m, fill="none", stroke=BLACK, sw=1)

# ═══════════════════════════════════════════════════════════════════════════
# INFO PANEL (right column of each sheet)
# ═══════════════════════════════════════════════════════════════════════════

def info_panel(x, y, w, elem_data):
    rows = [
        ("BAMBU LAB P1S/P2S", None, BLACK, True),
        ("Druckbett:", "256 x 256 x 256 mm", GRAY, False),
        ("", "", GRAY, False),
        ("MATERIAL", None, BLACK, True),
        ("Empfehlung:", "PLA-CF / PETG-CF", GRAY, False),
        ("", "oder Bambu-PLA Matte", GRAY, False),
        ("Schichthoehe:", "0.2 mm", GRAY, False),
        ("Wandlinien:", "4 (min.)", GRAY, False),
        ("Fuellung:", "25-40 %  Gyroid", GRAY, False),
        ("Stuetzstruktur:", elem_data.get("support", "Nein"), GRAY, False),
        ("Druckausricht.:", elem_data.get("orient", "Flach auf Bett"), GRAY, False),
        ("", "", GRAY, False),
        ("ELEMENT", None, BLACK, True),
        ("Breite:", f"{elem_data['w']} mm", GRAY, False),
        ("Tiefe:", f"{elem_data['d']} mm", GRAY, False),
        ("Hoehe:", f"{elem_data['h']} mm", GRAY, False),
        ("Kabelkanal:", "Ø 44 mm", GRAY, False),
        ("Bajonett:", "Ø 58 mm  4-Pin", GRAY, False),
        ("", "", GRAY, False),
        ("IKEA STRALA", None, BLUE, True),
        ("Fassung:", "E14 Pendelleuchte", BLUE, False),
        ("Kabel:", "laeuft durch Kanal", BLUE, False),
        ("", "", GRAY, False),
        ("HINWEIS", None, BLACK, True),
    ]
    if elem_data.get("note"):
        for ln_txt in elem_data["note"].split("\n"):
            rows.append(("", ln_txt, GRAY, False))

    row_h = p(8.5)
    total_h = len(rows) * row_h + p(6)
    out  = rct(x, y, w, total_h, fill=WHITE, stroke=BLACK, sw=0.7, rx=p(2))
    for i, (k, v, col, bold) in enumerate(rows):
        yy = y + p(5) + i*row_h
        if v is None:
            out += tx(x+w/2, yy, k, sz=7.5, bold=True, fill=col)
            out += ln(x+p(3), yy+p(1.5), x+w-p(3), yy+p(1.5), col, 0.4)
        else:
            out += mono(x+p(3), yy, k, sz=7, bold=bold, fill=col, anchor="start")
            out += mono(x+p(38), yy, v or "", sz=7, fill=col, anchor="start")
    return out, y + total_h + p(4)

def bay_detail_panel(x, y, w):
    """Bayonet cross-section detail."""
    h = p(55)
    out = rct(x, y, w, h, fill="#fffae8", stroke="#a07000", sw=0.7, rx=p(2))
    out += tx(x+w/2, y+p(6), "BAJONETT-DETAIL (Querschnitt)", sz=7.5, bold=True, fill="#6a4800")
    out += ln(x+p(3), y+p(9), x+w-p(3), y+p(9), "#a07000", 0.4)
    # draw cross-section at scale 1:1
    cx2 = x + w/2; cy2 = y + p(28)
    BW = p(BAY_R*2)*0.55; BH2 = p(BAY_H)*0.9; IR2 = p(INNER_R)*0.55
    # male top
    out += part_rect(cx2-BW/2, cy2-BH2*2-p(2), BW, BH2, sw=0.8)
    out += hole_rect(cx2, cy2-BH2*2-p(2), BH2, r=IR2)
    pins_w = p(PIN_W)*0.55; pins_h = p(PIN_H)*0.55
    for dx in [-BW/4, BW/4]:
        out += rct(cx2+dx-pins_w/2, cy2-BH2*2-p(2), pins_w, pins_h,
                   fill=PART_D, stroke=PART_D, sw=0.2)
    # gap
    out += ln(cx2-BW/2-p(3), cy2-p(1), cx2+BW/2+p(3), cy2-p(1), "#aaa", 0.4, "2,2")
    # female bottom
    out += part_rect(cx2-BW/2, cy2+p(1), BW, BH2, sw=0.8)
    out += hole_rect(cx2, cy2+p(1), BH2, r=IR2)
    for dx in [-BW/4, BW/4]:
        out += rct(cx2+dx-pins_w/2, cy2+p(1), pins_w, BH2,
                   fill=HOLLOW, stroke=PART_D, sw=0.2)
    # arrow 90 deg
    ax = cx2+BW/2+p(5); ay = cy2-p(5)
    out += pa(f"M {ax:.1f} {ay:.1f} A {p(6):.1f} {p(6):.1f} 0 0 1 {ax+p(6):.1f} {ay+p(6):.1f}",
              fill="none", stroke=RED, sw=0.8)
    out += tx(ax+p(8), ay+p(3), "90 Grad", sz=6.5, fill=RED, anchor="start")
    out += tx(ax+p(8), ay+p(10), "Verriegelt", sz=6, fill=RED, anchor="start")
    # labels
    out += tx(cx2-BW/2-p(3), cy2-BH2-p(2), "M", sz=7, fill=BLUE, anchor="end", bold=True)
    out += tx(cx2-BW/2-p(3), cy2+p(5), "F", sz=7, fill=BLUE, anchor="end", bold=True)
    return out

# ═══════════════════════════════════════════════════════════════════════════
# GENERATE INDIVIDUAL SHEET
# ═══════════════════════════════════════════════════════════════════════════

def make_sheet(eid, ename, draw_fn, elem_data, sheet_n):
    svg  = hdr(f"Bambu Lab Lampe Element {eid}: {ename}")
    svg += defs()
    svg += border()

    # Drawing area
    DX = p(5); DY = p(5)
    DW = p(193); DH = p(175)
    svg += rct(DX, DY, DW, DH, fill=WHITE, stroke=BLACK, sw=0.8, rx=p(1.5))
    svg += tx(DX+DW/2, DY+p(9), f"Element {eid}  –  {ename}",
              sz=12, bold=True, fill=BLACK)
    svg += ln(DX+p(5), DY+p(12), DX+DW-p(5), DY+p(12), BLACK, 0.6)

    # Scale label
    svg += mono(DX+p(5), DY+DH-p(4), "Massstab 1:1.4  |  Alle Masse in mm  |  Druckbett 256x256mm",
                sz=6.5, fill=GRAY, anchor="start")

    # Main element drawing (centred in drawing area)
    cx = DX + DW/2; cy = DY + DH/2 + p(8)
    svg += draw_fn(cx, cy)

    # Top view (small, bottom-right of drawing area)
    tv_cx = DX+DW-p(30); tv_cy = DY+DH-p(28)
    outer_r = elem_data.get("outer_r_for_topview", 29)
    svg += top_view(tv_cx, tv_cy, outer_r, scale=0.5)

    # Bayonet 90-deg indicator (bottom-left of drawing area)
    bx = DX+p(20); by = DY+DH-p(38)
    svg += rct(bx-p(2), by-p(6), p(52), p(40),
               fill="#fffae8", stroke="#a07000", sw=0.5, rx=p(1.5))
    svg += tx(bx+p(24), by-p(1), "Bajonett – 90 Grad", sz=6.5, bold=True, fill="#6a4800")
    # top view bay
    bcirc = p(BAY_R)*0.5; bcx = bx+p(14); bcy = by+p(17)
    svg += ci(bcx, bcy, bcirc, fill="url(#pl)", stroke=PART_D, sw=0.8)
    svg += ci(bcx, bcy, p(INNER_R)*0.5, fill="url(#hol)", stroke=PART_D, sw=0.6)
    for a in range(0, 360, 90):
        r = math.radians(a)
        svg += ci(bcx+bcirc*math.cos(r), bcy+bcirc*math.sin(r),
                  p(PIN_W)*0.25, fill=PART_D, stroke=PART_D, sw=0.2)
    # arc arrow
    svg += pa(f"M {bcx+bcirc:.1f} {bcy:.1f} "
              f"A {bcirc:.1f} {bcirc:.1f} 0 0 1 {bcx:.1f} {bcy+bcirc:.1f}",
              fill="none", stroke=RED, sw=0.8)
    svg += tx(bcx+bcirc+p(2), bcy+bcirc-p(2), "90 Grad", sz=6, fill=RED, anchor="start")

    # Right info column
    IX = DX+DW+p(4); IY = p(5); IW = A4W-IX-p(4)

    # Colour swatch for this element
    col_hex, col_name, txt_col = ELEM_COLORS.get(eid, ("#888","?","#fff"))
    svg += rct(IX, IY, IW, p(16), fill=col_hex, stroke=BLACK, sw=0.8, rx=p(2))
    svg += tx(IX+IW/2, IY+p(6.5), f"PETG: {col_name}", sz=8,
              bold=True, fill=txt_col)
    svg += tx(IX+IW/2, IY+p(13), "Bambu Lab Filament", sz=6.5, fill=txt_col)

    nxt_y = IY + p(19)
    info_out, nxt_y = info_panel(IX, nxt_y, IW, elem_data)
    svg += info_out

    svg += bay_detail_panel(IX, nxt_y, IW)

    # Title block
    tb, _ = title_block(eid, ename, sheet=sheet_n)
    svg += tb

    svg += ftr()
    return svg

# ═══════════════════════════════════════════════════════════════════════════
# OVERVIEW SHEET
# ═══════════════════════════════════════════════════════════════════════════

def bauhaus_color_strip(x, y, w):
    """Horizontal Bauhaus PETG colour legend."""
    H = p(22)
    out = rct(x, y, w, H, fill=WHITE, stroke=BLACK, sw=0.7, rx=p(1.5))
    out += tx(x+w/2, y+p(6.5), "BAUHAUS FARBKONZEPT – PETG Filament",
              sz=7.5, bold=True, fill=BLACK)
    eids = ["A","B","C","D","E","F"]
    enames = ["Fuss 1","Fuss 2","Schirm 1","Schirm 2","Schirm 3","Stiel"]
    sw_w = (w - p(6)) / len(eids)
    for i,(eid,enm) in enumerate(zip(eids,enames)):
        col_hex, col_name, txt_col = ELEM_COLORS[eid]
        sx = x + p(3) + i*sw_w
        out += rct(sx, y+p(9), sw_w-p(2), p(10),
                   fill=col_hex, stroke="#888", sw=0.5, rx=p(1))
        out += tx(sx+sw_w/2-p(1), y+p(15.5), f"{eid}: {col_name}", sz=6,
                  fill=txt_col, bold=True)
    return out

def make_overview():
    svg  = hdr("Bambu Lab Modullampe – Uebersicht")
    svg += defs()
    svg += border()

    # Title
    svg += tx(A4W/2, p(13), "BAMBU LAB MODULLAMPE  –  BAUHAUS STIL",
              sz=14, bold=True, fill=BLACK)
    svg += tx(A4W/2, p(20), "6 Bajonett-Elemente  |  Bambu Lab P1S / P2S  |  IKEA STRALA E14",
              sz=8, fill=GRAY)
    svg += ln(p(5), p(23), A4W-p(5), p(23), BLACK, 0.8)

    # 3x2 grid of elements (small scale)
    fns   = [el_A,el_B,el_C,el_D,el_E,el_F]
    names = ["A: Fuss 1\nScheiben-Basis 120mm",
             "B: Fuss 2\nKonus-Basis 140mm",
             "C: Schirm 1\nBauhaus-Disc 180mm",
             "D: Schirm 2\nKonus 200mm",
             "E: Schirm 3\nDom-Schirm 190mm",
             "F: Stiel\nVerbinder Ø58 100mm"]
    CW = p(82); CH = p(76)
    OX = p(5);  OY = p(26)

    for i,(fn,nm) in enumerate(zip(fns,names)):
        col=i%3; row=i//3
        ccx=OX+col*CW+CW/2; ccy=OY+row*CH+CH/2
        svg += rct(OX+col*CW+p(1), OY+row*CH+p(1), CW-p(2), CH-p(2),
                   fill=WHITE, stroke="#bbb", sw=0.5, rx=p(1.5))
        svg += fn(ccx, ccy+p(4), s=0.55)
        nl = nm.split("\n")
        svg += tx(ccx, OY+row*CH+p(7), nl[0], sz=7.5, bold=True, fill=BLACK)
        svg += tx(ccx, OY+row*CH+p(13), nl[1], sz=6, fill=GRAY)

    # Vertical divider
    DIV = OX + 3*CW + p(2)
    svg += ln(DIV, p(24), DIV, A4H-p(22), BLACK, 0.8)

    # Right: assembly diagram
    RX = DIV+p(4); RW = A4W-RX-p(5)
    svg += tx(RX+RW/2, p(31), "Montage-Beispiel", sz=9, bold=True, fill=BLACK)
    svg += tx(RX+RW/2, p(39), "Fuss 2 + Stiel + Schirm 2", sz=7, fill=GRAY)
    svg += ln(RX, p(42), RX+RW, p(42), BLACK, 0.5)

    # Assembly stack (Schirm2 top → Stiel → Fuss2 bottom)
    S2 = 0.45   # assembly scale
    acx = RX+RW/2
    # STRALA above
    asy = p(50)
    svg += ln(acx, asy, acx, asy+p(8), "#888", 1.5)
    svg += rct(acx-p(6), asy-p(10), p(12), p(10), fill="#ddd", stroke="#888", sw=0.7, rx=p(1))
    svg += tx(acx+p(10), asy-p(5), "STRALA E14", sz=6, fill=GRAY, anchor="start")
    # Schirm 2
    svg += el_D(acx, asy+p(58)*S2*1.2, s=S2)
    jy1 = asy+p(58)*S2*1.2 + p(75)*S2/2 + p(4)*S2
    # Bajonett joint 1
    svg += ln(acx+p(20), jy1, acx+RW/2-p(2), jy1, RED, 0.6, "3,2")
    svg += tx(acx+RW/2, jy1+p(2), "Bajonett 1", sz=6, fill=RED, anchor="end")
    # Stiel
    svg += el_F(acx, jy1+p(100)*S2/2+p(4)*S2, s=S2)
    jy2 = jy1 + p(100)*S2 + p(8)*S2
    svg += ln(acx+p(20), jy2, acx+RW/2-p(2), jy2, RED, 0.6, "3,2")
    svg += tx(acx+RW/2, jy2+p(2), "Bajonett 2", sz=6, fill=RED, anchor="end")
    # Fuss 2
    svg += el_B(acx, jy2+p(55)*S2/2+p(4)*S2, s=S2)
    # Schuko cable below
    cby = jy2 + p(55)*S2 + p(10)*S2
    svg += ln(acx, cby, acx, cby+p(10), "#888", 1.5)
    svg += ci(acx, cby+p(15), p(8), fill="#ddd", stroke="#888", sw=0.8)
    svg += tx(acx, cby+p(25), "Schuko-Kabel", sz=6, fill=GRAY)
    svg += tx(acx, cby+p(32), "Ø 44 mm Kanal", sz=6, fill=GRAY)

    # Bauhaus colour strip
    svg += bauhaus_color_strip(p(5), A4H-p(62), A4W-p(10))

    # Notes strip at bottom
    ny = A4H-p(38)
    svg += ln(p(5), ny, A4W-p(5), ny, BLACK, 0.5)
    notes = [
        "Kabelkanal Ø 44 mm: Schuko-Kabel (Ø max.19 mm Stecker) laeuft durch alle Elemente sicher hindurch.",
        "Bajonett Ø 58 mm: 4 Pins, 90 Grad Vierteldrehung zum Verriegeln. Male oben (M), Female unten (F).",
        "Druckmaterial: PLA-CF / PETG-CF / Bambu Matte PLA | Infill: 25-40 % Gyroid | Schichthoehe: 0.2 mm",
        "Alle Masse in mm | Massstab Uebersicht ca. 1:2.8 | Einzelblaetter Elemente A-F: Massstab 1:1.4",
    ]
    for i,n in enumerate(notes):
        svg += mono(p(8), ny+p(7)+i*p(7.5), n, sz=6.5, fill=GRAY, anchor="start")

    # Footer / title bar
    TH = p(16); ty = A4H-TH
    svg += rct(0, ty, A4W, TH, fill="#f0ece0", stroke=BLACK, sw=1)
    for xd in [p(55),p(180),A4W-p(18)]:
        svg += ln(xd, ty, xd, A4H, BLACK, 0.5)
    svg += mono(p(27.5), ty+p(6), "BAMBU LAB P1S / P2S", sz=7, bold=True)
    svg += mono(p(27.5), ty+p(12), "Bauhaus Modullampe", sz=6.5, fill=GRAY)
    svg += mono(p(117), ty+p(8), "Uebersicht – alle 6 Elemente", sz=9, bold=True)
    svg += mono(p(238), ty+p(8), "Blatt 1 / 7", sz=8, fill=GRAY)

    svg += ftr()
    return svg

# ═══════════════════════════════════════════════════════════════════════════
# ELEMENT METADATA
# ═══════════════════════════════════════════════════════════════════════════

# Bauhaus PETG colour per element  (html, name, text-colour)
ELEM_COLORS = {
    "A": ("#1c1c1c", "Schwarz",  "#ffffff"),   # Fuss 1
    "B": ("#f0f0f0", "Weiss",    "#1a1a1a"),   # Fuss 2
    "C": ("#c0201a", "Rot",      "#ffffff"),   # Schirm 1 – Bauhaus red
    "D": ("#e8a800", "Gelb",     "#1a1a1a"),   # Schirm 2 – Bauhaus yellow
    "E": "#1a3e8a,Blau,#ffffff".split(","),     # Schirm 3 – Bauhaus blue
    "F": ("#1c1c1c", "Schwarz",  "#ffffff"),   # Stiel
}
# Fix list-style for E
ELEM_COLORS["E"] = ("#1a3e8a", "Blau", "#ffffff")

ELEMENTS = [
    ("A", "Fuss 1 – Scheiben-Basis", el_A,
     {"w":120,"d":120,"h":32,"outer_r_for_topview":60,
      "support":"Nein","orient":"Flach auf Bett",
      "petg_color": "PETG Schwarz",
      "note":"Breite Standbasis.\nGummi-Pad unten drucken\n(weiches TPU, 10mm)."}),

    ("B", "Fuss 2 – Konus-Dreifuss", el_B,
     {"w":140,"d":140,"h":55,"outer_r_for_topview":70,
      "support":"Ja (Boden)","orient":"Spitze oben",
      "petg_color": "PETG Weiss",
      "note":"Dreifuss-Kegel.\n3 Gummifuesse TPU\nam Boden (Ø10mm)."}),

    ("C", "Schirm 1 – Bauhaus Disc", el_C,
     {"w":180,"d":180,"h":25,"outer_r_for_topview":90,
      "support":"Nein","orient":"Flach auf Bett",
      "petg_color": "PETG Rot",
      "note":"Bauhaus-Scheibe.\nBeidseitig Bajonett.\nBesonders flach."}),

    ("D", "Schirm 2 – Konus-Schirm", el_D,
     {"w":200,"d":200,"h":75,"outer_r_for_topview":100,
      "support":"Ja (Rand)","orient":"Oeffnung nach oben",
      "petg_color": "PETG Gelb",
      "note":"Kegel-Schirm, Licht\nnach unten. Groesstes\nElement auf Platte."}),

    ("E", "Schirm 3 – Dom-Schirm", el_E,
     {"w":190,"d":190,"h":60,"outer_r_for_topview":95,
      "support":"Ja (Kuppel)","orient":"Dom nach unten",
      "petg_color": "PETG Blau",
      "note":"Uplighter / Ambient.\nKuppel liegt auf Bett.\nWeicher Lichtkegel."}),

    ("F", "Stiel – Modularer Verbinder", el_F,
     {"w":58,"d":58,"h":100,"outer_r_for_topview":29,
      "support":"Nein","orient":"Hochkant / stehend",
      "petg_color": "PETG Schwarz",
      "note":"Stapelbar. Ideal 1,\n2 oder 3 Stueck.\n100 / 200 / 300 mm."}),
]

# ═══════════════════════════════════════════════════════════════════════════

def main():
    # Overview
    path = f"{OUT}/00_Uebersicht.svg"
    with open(path,"w",encoding="utf-8") as f:
        f.write(make_overview())
    print(f"OK  {path}")

    # Individual sheets
    for i,(eid,ename,fn,data) in enumerate(ELEMENTS,start=2):
        svg = make_sheet(eid, ename, fn, data, f"{i}/7")
        safe = ename.replace(" ","_").replace("/","_").replace("–","")
        path = f"{OUT}/{i:02d}_{eid}_{safe}.svg"
        with open(path,"w",encoding="utf-8") as f:
            f.write(svg)
        print(f"OK  {path}")

    print(f"\n7 SVG-Blaetter gespeichert in {OUT}/")

if __name__ == "__main__":
    main()
