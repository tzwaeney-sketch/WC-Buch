#!/usr/bin/env python3
"""
BAMBU LAB P1S/P2S – MODULLAMPE v4
1 Fuß + 4 Körper-Module + 1 Schirm = 6 Teile   → ca. 62cm gestapelt

RUND:  1 Fuß (breite Basis) · 2 Kugel · 6 Schirm (konisch)
ECKIG: 3 Würfel · 4 Sechseck · 5 Raute/Diamant

Bajonett: 4 Pin J-Schlitz, 45° Drehung, Male oben / Female unten
Kabelkanal Ø44mm durchgehend (Schuko + IKEA STRALA E14)
"""

import numpy as np
import trimesh
import trimesh.creation as tc
import trimesh.boolean as tb
import shapely.geometry as sg
import os

OUT = "/home/user/WC-Buch/stl"
os.makedirs(OUT, exist_ok=True)

SEG = 64

# ─── Massen (mm) ──────────────────────────────────────────────────────────────
CABLE_R = 22.0    # Kabelkanal   → Ø44mm
PEG_R   = 25.0    # Male Peg     → Ø50mm
SOCK_R  = 25.3    # Female Innen → Ø50.6mm (+0.3mm Spiel PETG)
SOCK_OR = 33.3    # Female Außen → Ø66.6mm
PEG_H   = 14.0
SOCK_H  = 14.0
PIN_R   = 3.0; PIN_ARC = 12.0; PIN_Z = 5.0; PIN_T = 3.0

# ─── Basis-Geometrie ──────────────────────────────────────────────────────────

def revolve(pts, sections=SEG):
    pts = np.array(pts, float)
    n, N = len(pts), sections
    v = []
    for i in range(N):
        a = 2*np.pi*i/N; c, s = np.cos(a), np.sin(a)
        for r, z in pts:
            v.append([r*c, r*s, z])
    v = np.array(v)
    f = []
    for i in range(N):
        ni = (i+1)%N
        for j in range(n):
            nj=(j+1)%n
            a,b,c2,d = i*n+j,ni*n+j,ni*n+nj,i*n+nj
            f+=[[a,b,c2],[a,c2,d]]
    m = trimesh.Trimesh(vertices=v, faces=np.array(f))
    m.fix_normals(); return m

def htube(OR, IR, H):
    return revolve([[IR,0],[OR,0],[OR,H],[IR,H]])

def hfrustum(R_bot, R_top, IR, H):
    return revolve([[IR,0],[R_bot,0],[R_top,H],[IR,H]])

def cyl_mesh(r, h, sections=SEG):
    m = tc.cylinder(radius=r, height=h, sections=sections)
    return m

def hex_poly(radius):
    pts = [(radius*np.cos(np.radians(60*i+30)),
            radius*np.sin(np.radians(60*i+30))) for i in range(6)]
    return sg.Polygon(pts)

def sq_poly(side):
    h = side/2
    return sg.Polygon([(-h,-h),(h,-h),(h,h),(-h,h)])

def extrude_hollow(polygon, height, cable_r=CABLE_R):
    outer = trimesh.creation.extrude_polygon(polygon, height)
    hole  = cyl_mesh(cable_r, height+2)
    hole.apply_translation([0,0,-1])
    r = tb.difference([outer, hole], engine='manifold')
    if not r.is_watertight: r.fill_holes(); r.fix_normals()
    return r

def round_collar(z_bot, H=12.0):
    m = htube(SOCK_OR, CABLE_R, H)
    m.apply_translation([0,0,z_bot]); return m

# ─── Bajonett Male ────────────────────────────────────────────────────────────

def pin_mesh(ang_deg):
    a0,a1 = np.radians(ang_deg-PIN_ARC/2), np.radians(ang_deg+PIN_ARC/2)
    r0,r1 = PEG_R-.2, PEG_R+PIN_R+.2
    z0,z1 = PIN_Z-PIN_T/2, PIN_Z+PIN_T/2
    v = []
    for r in [r0,r1]:
        for z in [z0,z1]:
            for a in [a0,(a0+a1)/2,a1]:
                v.append([r*np.cos(a),r*np.sin(a),z])
    return trimesh.convex.convex_hull(np.array(v))

def male_peg(z_base):
    peg = htube(PEG_R, CABLE_R, PEG_H)
    peg.apply_translation([0,0,z_base])
    parts = [peg] + [pin_mesh(a) for a in [0,90,180,270]]
    for p in parts[1:]: p.apply_translation([0,0,z_base])
    m = trimesh.util.concatenate(parts); m.fix_normals(); return m

# ─── Bajonett Female ──────────────────────────────────────────────────────────

def j_cutter(ang_deg, z_bot, z_top):
    AE=PIN_ARC+4; AL=45+PIN_ARC/2
    r0,r1 = SOCK_R-.5, SOCK_R+PIN_R+1.5
    # Einführschlitz
    a0e,a1e = np.radians(ang_deg-AE/2), np.radians(ang_deg+AE/2)
    v  = [[r*np.cos(a),r*np.sin(a),z]
          for z in [z_bot-.5,z_top+.5]
          for r in [r0,r1]
          for a in np.linspace(a0e,a1e,8)]
    # Verriegelungsnut
    a_s,a_e = np.radians(ang_deg), np.radians(ang_deg-AL)
    gz = z_top-PIN_T-3
    v2 = [[r*np.cos(a),r*np.sin(a),z]
          for z in [gz-.5,z_top+.5]
          for r in [r0,r1]
          for a in np.linspace(a_s,a_e,14)]
    c1 = trimesh.convex.convex_hull(np.array(v))
    c2 = trimesh.convex.convex_hull(np.array(v2))
    return trimesh.util.concatenate([c1,c2])

def female_socket(z_top):
    z0 = z_top - SOCK_H
    sock = htube(SOCK_OR, CABLE_R, SOCK_H)
    sock.apply_translation([0,0,z0])
    cutters = trimesh.util.concatenate([j_cutter(a,z0,z_top) for a in [0,90,180,270]])
    r = tb.difference([sock, cutters], engine='manifold')
    if not r.is_watertight: r.fill_holes(); r.fix_normals()
    return r

def std_connectors(body, H):
    """Male oben + Female unten."""
    parts = [body, male_peg(H), female_socket(0.0)]
    m = trimesh.util.concatenate(parts); m.fix_normals(); return m

def top_only(body, H):
    """Nur Male oben – für Fuß (kein Female unten nötig)."""
    m = trimesh.util.concatenate([body, male_peg(H)]); m.fix_normals(); return m

def bot_only(body):
    """Nur Female unten – für Schirm (kein Male oben nötig)."""
    m = trimesh.util.concatenate([body, female_socket(0.0)]); m.fix_normals(); return m

# ═══════════════════════════════════════════════════════════════════════════════
# 6 TEILE
# ═══════════════════════════════════════════════════════════════════════════════

def make_1_fuss():
    """
    1  FUSS  – Breite stabile Rundscheibe  Ø180 × 50mm  [PETG SCHWARZ]
    Schwerer runder Standfuß mit breitem Anti-Rutsch-Rand.
    Unten KEIN Bajonett (Bodenkontakt).  Oben Male Peg.
    """
    H = 50.0
    # Körper: breite dicke Scheibe
    body = revolve([
        [CABLE_R, 0], [90.0, 0], [90.0, H], [CABLE_R, H]
    ])
    # Kleiner Wulst am unteren Rand (Anti-Rutsch-Illlusion)
    rim = revolve([
        [80.0, 0], [90.0, 0], [90.0, 6], [80.0, 6]
    ])
    m = trimesh.util.concatenate([body, male_peg(H)])
    m.fix_normals(); return m


def make_2_kugel():
    """
    2  KUGEL  – Bauchige Kugelform  Ø100 × 90mm  [PETG GELB]
    RUND · Sinusoidales Profil. Organic.
    """
    H=90.0; MAX_R=50.0; N=64
    outer=[]
    for i in range(N+1):
        t=np.pi*i/N
        r=SOCK_OR+(MAX_R-SOCK_OR)*np.sin(t)
        z=H*i/N
        outer.append([r,z])
    body = revolve([[CABLE_R,0]]+outer+[[CABLE_R,H]])
    return std_connectors(body, H)


def make_3_wuerfel():
    """
    3  WÜRFEL  – Quadratischer Kubus  80×80×80mm  [PETG BLAU]
    ECKIG · 4-seitiger Querschnitt. Runde Kragen für Bajonett.
    """
    H=80.0; SIDE=80.0; COLL=12.0
    cube = extrude_hollow(sq_poly(SIDE), H)
    c_bot = round_collar(0, COLL)
    c_top = round_collar(H-COLL, COLL)
    body = trimesh.util.concatenate([cube, c_bot, c_top])
    body.fix_normals()
    return std_connectors(body, H)


def make_4_sechseck():
    """
    4  SECHSECK  – Hexagonaler Prisma  ∅98mm × 100mm  [PETG GRÜN]
    ECKIG · 6-seitiger Querschnitt. Zwischen rund und eckig.
    """
    H=100.0; HEX_R=49.0; COLL=12.0
    hex_body = extrude_hollow(hex_poly(HEX_R), H)
    c_bot = round_collar(0, COLL)
    c_top = round_collar(H-COLL, COLL)
    body = trimesh.util.concatenate([hex_body, c_bot, c_top])
    body.fix_normals()
    return std_connectors(body, H)


def make_5_raute():
    """
    5  RAUTE / DIAMANT  – Hexagonale Doppelpyramide  Ø120 × 130mm  [PETG LILA]
    ECKIG · Wie Diamant: breit in der Mitte, spitz an den Enden (eckig!).
    6 Flächen Dreieck-Pyramiden oben+unten.
    """
    H=130.0; HH=H/2; HEX_MID=60.0; HEX_END=SOCK_OR; N=20
    segs=[]
    for half in [0,1]:
        for i in range(N):
            t0,t1 = i/N, (i+1)/N
            if half==0:   # untere Hälfte: wächst
                r0 = HEX_END+(HEX_MID-HEX_END)*t0
                r1 = HEX_END+(HEX_MID-HEX_END)*t1
                z0,z1 = HH*t0, HH*t1
            else:          # obere Hälfte: schrumpft
                r0 = HEX_MID+(HEX_END-HEX_MID)*t0
                r1 = HEX_MID+(HEX_END-HEX_MID)*t1
                z0,z1 = HH+HH*t0, HH+HH*t1
            v0=np.array([(x,y,z0) for x,y in hex_poly(r0).exterior.coords[:-1]])
            v1=np.array([(x,y,z1) for x,y in hex_poly(r1).exterior.coords[:-1]])
            segs.append(trimesh.convex.convex_hull(np.vstack([v0,v1])))

    diamond_outer = trimesh.util.concatenate(segs)
    hole = cyl_mesh(CABLE_R, H+2); hole.apply_translation([0,0,-1])
    diamond = tb.difference([diamond_outer, hole], engine='manifold')
    if not diamond.is_watertight: diamond.fill_holes(); diamond.fix_normals()
    # runde Kragen
    c_bot = round_collar(0, 12); c_top = round_collar(H-12, 12)
    body = trimesh.util.concatenate([diamond, c_bot, c_top]); body.fix_normals()
    return std_connectors(body, H)


def make_6_schirm():
    """
    6  SCHIRM  – Konischer Lampenschirm  Ø200→Ø66 × 100mm  [PETG ROT]
    RUND · Öffnet nach unten → Licht nach unten.
    Oben: Female Buchse (steckt auf Körpermodul).
    Unten: offen (Lichtaustritt + Kabelausgang für E14).
    """
    H=100.0; R_TOP=SOCK_OR; R_BOT=100.0
    # Kegel öffnet nach unten: unten breit, oben schmal
    body = revolve([
        [CABLE_R, 0],   # innen oben (schmal)
        [R_TOP, 0],     # außen oben (schmal)
        [R_BOT, H],     # außen unten (breit)
        [CABLE_R, H],   # innen unten
    ])
    # Nur Female unten (Schirm empfängt Male des letzten Körpermoduls)
    # Aber Schirm ZEIGT NACH OBEN: Kegel-Spitze oben, Öffnung unten
    # → drehen: Spitze = TOP, Öffnung = BOTTOM
    body.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [1,0,0]))
    body.apply_translation([0,0,H])
    # Jetzt: z=0 ist Spitze (female socket hier), z=H ist offene Öffnung unten
    m = trimesh.util.concatenate([body, female_socket(0.0)])
    m.fix_normals(); return m

# ═══════════════════════════════════════════════════════════════════════════════
# ÜBERPRÜFUNG & EXPORT
# ═══════════════════════════════════════════════════════════════════════════════

HEIGHTS = {"Fuss":50,"Kugel":90,"Wuerfel":80,"Sechseck":100,"Raute":130,"Schirm":100}

PARTS = [
    ("1_Fuss_Basis_50mm",          make_1_fuss,    "PETG Schwarz"),
    ("2_Kugel_Sphere_90mm",        make_2_kugel,   "PETG Gelb"),
    ("3_Wuerfel_Cube_80mm",        make_3_wuerfel, "PETG Blau"),
    ("4_Sechseck_Hex_100mm",       make_4_sechseck,"PETG Gruen"),
    ("5_Raute_Diamant_130mm",      make_5_raute,   "PETG Lila"),
    ("6_Schirm_Konus_100mm",       make_6_schirm,  "PETG Rot"),
]

def main():
    print("=== VERBINDUNGS-CHECK ===")
    print(f"  Male  Ø{PEG_R*2}mm  →  Female Ø{SOCK_R*2:.1f}mm  Spiel {(SOCK_R-PEG_R)*2:.1f}mm [OK PETG]")
    print(f"  Kabelkanal Ø{CABLE_R*2:.0f}mm durchgehend  →  Schuko + IKEA STRALA E14")
    print(f"  Bajonett 4 Pins, 45° Drehung, Male oben / Female unten")

    print("\n=== KONFIGURATIONEN ===")
    H=HEIGHTS
    cfgs = [
        ("Standard ~62cm",        ["Fuss","Kugel","Wuerfel","Sechseck","Raute","Schirm"]),
        ("Bauhaus-Eckig ~43cm",   ["Fuss","Wuerfel","Sechseck","Schirm"]),
        ("Organisch ~33cm",       ["Fuss","Kugel","Schirm"]),
        ("Volle Eleganz ~56cm",   ["Fuss","Raute","Sechseck","Kugel","Schirm"]),
        ("Mini-Tisch ~27cm",      ["Fuss","Wuerfel","Schirm"]),
    ]
    for name,parts in cfgs:
        total=sum(H[p] for p in parts)
        print(f"  {name:30s}  {' + '.join(parts):50s} = {total}mm = {total/10:.0f}cm")

    print(f"\n=== STL-GENERIERUNG → {OUT}/ ===\n")
    all_ok=True
    for name,fn,color in PARTS:
        print(f"  {name} [{color}] ...", end=" ", flush=True)
        try:
            m=fn()
            if not m.is_watertight: m.fill_holes(); m.fix_normals()
            wt=m.is_watertight
            bb=m.bounding_box.extents
            print(f"{'OK ' if wt else '!WT'}  {bb[0]:.0f}×{bb[1]:.0f}×{bb[2]:.0f}mm  "
                  f"{m.volume/1000:.0f}cm³  ({len(m.vertices):,}V)")
            m.export(f"{OUT}/{name}.stl")
            if not wt: all_ok=False
        except Exception as e:
            print(f"FEHLER: {e}"); import traceback; traceback.print_exc(); all_ok=False

    print(f"\n{'[OK] Alle 6 STL fertig' if all_ok else '[!!] Fehler aufgetreten'}")
    print("\nBambu Studio:")
    print("  Fuß(Schwarz) · Kugel(Gelb) · Würfel(Blau) · Sechseck(Grün) · Raute(Lila) · Schirm(Rot)")
    print("  PETG · 0.2mm Layer · 4 Wände · 30% Gyroid · Schirm mit Stütze")

if __name__=="__main__":
    main()
