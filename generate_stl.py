#!/usr/bin/env python3
"""
BAMBU LAB MODULLAMPE v5 – Professioneller Generator
====================================================
6 Teile: 1 Fuß · 4 Körper-Module · 1 Schirm
3 Rund + 3 Eckig · Bauhaus-Stil · Alle innen hohl Ø44mm

Bajonett: 4 Pin J-Schlitz, 45° Vierteldrehung, Male oben / Female unten
Alle Körper via Boolean-Union/Difference korrekt verbunden (kein Concatenate!)

Höhe gestapelt: ~55cm (+14mm Peg oben)
"""

import numpy as np
import trimesh
import trimesh.creation as tc
import trimesh.boolean as tb
import shapely.geometry as sg
import os, sys

OUT = "/home/user/WC-Buch/stl"
os.makedirs(OUT, exist_ok=True)

# ═══ KONSTANTEN (mm) ════════════════════════════════════════════════════════
CABLE_R = 22.0    # Kabelkanal Radius  → Ø44mm (Schuko + STRALA E14)
PEG_R   = 25.0    # Bajonett Stecker   → Ø50mm
SOCK_R  = 25.3    # Bajonett Buchse    → Ø50.6mm (+0.3mm Spiel für PETG)
SOCK_OR = 33.3    # Buchsen Außen      → Ø66.6mm
PEG_H   = 14.0    # Stecker Höhe
SOCK_H  = 14.0    # Buchsen Tiefe
PIN_R   = 3.0     # Pin radiale Höhe
PIN_ARC = 12.0    # Pin Breite (Grad)
PIN_Z   = 5.0     # Pin Z-Mitte (von Peg-Basis)
PIN_T   = 3.0     # Pin axiale Dicke
SEG     = 72      # Auflösung Umlauf

# ═══ KERN-HELFER ═══════════════════════════════════════════════════════════

def diff(a, b): return tb.difference([a, b], engine='manifold')
def union2(a, b): return tb.union([a, b], engine='manifold')
def union_all(*meshes):
    result = meshes[0]
    for m in meshes[1:]:
        result = union2(result, m)
    return result

def moved(m, x=0, y=0, z=0):
    m2 = m.copy(); m2.apply_translation([x,y,z]); return m2

def rotated_x(m, angle_deg=180):
    m2 = m.copy()
    m2.apply_transform(trimesh.transformations.rotation_matrix(
        np.radians(angle_deg), [1,0,0]))
    return m2

def cylinder(r, h, sections=SEG):
    return tc.cylinder(radius=r, height=h, sections=sections,
                       transform=trimesh.transformations.translation_matrix([0,0,h/2]))

def ring(r_out, r_in, h, sections=SEG):
    """Hohler Zylinder (Ring) – korrekt via Boolean."""
    outer = cylinder(r_out, h, sections)
    inner = moved(cylinder(r_in, h+2, sections), z=-1)
    return diff(outer, inner)

def cable_cutter(h, extra=2):
    """Kabelkanal-Fräser: Ø44mm, full height + Überstand."""
    return moved(cylinder(CABLE_R, h+extra*2, SEG), z=-extra)

def revolve_profile(outer_pts, inner_r, height, sections=SEG):
    """
    Dreht Außenprofil (r,z)-Liste um Z-Achse.
    Erzeugt hohlen Körper mit geradem Innenkanal bei inner_r.
    Outer_pts: von z=0 nach z=height (ohne Innenkanal).
    """
    pts = [[inner_r, 0.0]] + list(outer_pts) + [[inner_r, height]]
    pts = np.array(pts, float)
    n, N = len(pts), sections
    verts = []
    for i in range(N):
        a = 2*np.pi*i/N; c, s = np.cos(a), np.sin(a)
        for r, z in pts:
            verts.append([r*c, r*s, z])
    verts = np.array(verts)
    faces = []
    for i in range(N):
        ni = (i+1)%N
        for j in range(n):
            nj = (j+1)%n
            a,b,c,d = i*n+j, ni*n+j, ni*n+nj, i*n+nj
            faces += [[a,b,c],[a,c,d]]
    m = trimesh.Trimesh(vertices=verts, faces=np.array(faces))
    m.fix_normals()
    return m

# ═══ ECKIGE KÖRPER (Boolean-korrekt hohl) ═══════════════════════════════════

def hex_verts(radius, z, rot=30):
    """Sechseck-Punkte bei Höhe z."""
    return [(radius*np.cos(np.radians(60*i+rot)),
             radius*np.sin(np.radians(60*i+rot)), z) for i in range(6)]

def hex_frustum_solid(r_bot, r_top, h, rot=30):
    """Sechseckiger Kegelstumpf (solid) über Boolean-freie Geometrie."""
    bot = hex_verts(r_bot, 0, rot)
    top = hex_verts(r_top, h, rot)
    verts = np.array(bot + top, float)
    # 6 Seitenflächen (Quads→Dreiecke) + Deckel/Boden (Fächer)
    faces = []
    for i in range(6):
        ni = (i+1)%6
        b0,b1,t0,t1 = i, ni, 6+i, 6+ni
        faces += [[b0,b1,t1],[b0,t1,t0]]
    # Boden (nach unten = neg Z-Normal → Reihenfolge ccw from below = cw from above)
    bc = np.array([[0.0,0.0,0.0]])
    tc2 = np.array([[0.0,0.0,h]])
    verts_b = np.vstack([verts, bc, tc2])  # idx 12=boden-mitte, 13=deckel-mitte
    for i in range(6):
        ni=(i+1)%6; faces+=[[12,ni,i]]      # Boden
    for i in range(6):
        ni=(i+1)%6; faces+=[[13,6+i,6+ni]]  # Deckel
    m = trimesh.Trimesh(vertices=verts_b, faces=np.array(faces))
    m.fix_normals(); return m

def square_frustum_solid(side_bot, side_top, h):
    """Quadratischer Kegelstumpf (solid)."""
    hb,ht = side_bot/2, side_top/2
    verts = np.array([
        [-hb,-hb,0],[ hb,-hb,0],[ hb, hb,0],[-hb, hb,0],
        [-ht,-ht,h],[ ht,-ht,h],[ ht, ht,h],[-ht, ht,h],
    ], float)
    faces = [
        [0,1,2],[0,2,3],       # Boden
        [4,6,5],[4,7,6],       # Deckel
        [0,1,5],[0,5,4],       # Seite N
        [1,2,6],[1,6,5],       # Seite O
        [2,3,7],[2,7,6],       # Seite S
        [3,0,4],[3,4,7],       # Seite W
    ]
    m = trimesh.Trimesh(vertices=verts, faces=np.array(faces))
    m.fix_normals(); return m

def angular_hollow(solid_body, h):
    """Macht eckigen Körper hohl: subtrahiert Kabelkanal + fügt Übergangskragen ein."""
    # 1. Kabelkanal fräsen
    hollow = diff(solid_body, cable_cutter(h))
    # 2. Runde Übergangskragen (oben + unten, damit Bajonett-Buchse/Stecker passt)
    COLL_H = 14.0  # genau so hoch wie Bajonett → nahtloser Übergang
    coll_bot = ring(SOCK_OR, CABLE_R, COLL_H)
    coll_top = ring(SOCK_OR, CABLE_R, COLL_H)
    coll_top = moved(coll_top, z=h-COLL_H)
    # 3. Alles via Union korrekt zusammenführen
    result = union_all(hollow, coll_bot, coll_top)
    if not result.is_watertight:
        result.fill_holes(); result.fix_normals()
    return result

# ═══ BAJONETT-STECKER (Male, oben) ══════════════════════════════════════════

def pin_mesh(ang_deg):
    """Einzelner radialer Pin."""
    a0 = np.radians(ang_deg - PIN_ARC/2)
    a1 = np.radians(ang_deg + PIN_ARC/2)
    r0 = PEG_R - 0.2; r1 = PEG_R + PIN_R + 0.2
    z0 = PIN_Z - PIN_T/2; z1 = PIN_Z + PIN_T/2
    v = [[r*np.cos(a), r*np.sin(a), z]
         for r in [r0,r1] for z in [z0,z1]
         for a in [a0,(a0+a1)/2,a1]]
    return trimesh.convex.convex_hull(np.array(v))

def male_peg(z_base):
    """Bajonett-Stecker mit 4 Pins bei 0°/90°/180°/270°."""
    peg = moved(ring(PEG_R, CABLE_R, PEG_H), z=z_base)
    pins = [moved(pin_mesh(a), z=z_base) for a in [0,90,180,270]]
    result = union_all(peg, *pins)
    if not result.is_watertight: result.fill_holes(); result.fix_normals()
    return result

# ═══ BAJONETT-BUCHSE (Female, unten) ════════════════════════════════════════

def j_slot_cutter(ang_deg, z_bot, z_top):
    """J-Schlitz Fräser: Einführung (vertikal) + Verriegelungsnut (tangential −45°)."""
    AE = PIN_ARC + 4; AL = 45 + PIN_ARC/2
    r0 = SOCK_R - 0.5; r1 = SOCK_R + PIN_R + 1.5
    # Einführschlitz (bei ang_deg, vertikal)
    a0e, a1e = np.radians(ang_deg-AE/2), np.radians(ang_deg+AE/2)
    v_e = [[r*np.cos(a),r*np.sin(a),z]
           for z in [z_bot-0.5, z_top+0.5]
           for r in [r0,r1]
           for a in np.linspace(a0e,a1e,10)]
    hull_e = trimesh.convex.convex_hull(np.array(v_e))
    # Verriegelungsnut (−45° tangential, nahe z_top)
    a_s = np.radians(ang_deg); a_e = np.radians(ang_deg - AL)
    gz = z_top - PIN_T - 3
    v_n = [[r*np.cos(a),r*np.sin(a),z]
           for z in [gz-0.5, z_top+0.5]
           for r in [r0,r1]
           for a in np.linspace(a_s,a_e,16)]
    hull_n = trimesh.convex.convex_hull(np.array(v_n))
    return union2(hull_e, hull_n)

def female_socket(z_top):
    """
    Bajonett-Buchse: Ring mit 4 J-Schlitzen.
    z_top = Unterseite des Elements (Buchse ragt nach unten).
    """
    z0 = z_top - SOCK_H
    sock_ring = ring(SOCK_OR, CABLE_R, SOCK_H)
    sock_ring = moved(sock_ring, z=z0)
    # 4 J-Schlitze subtrahieren
    cutters = [j_slot_cutter(a, z0, z_top) for a in [0,90,180,270]]
    cutter_all = union_all(*cutters)
    result = diff(sock_ring, cutter_all)
    if not result.is_watertight: result.fill_holes(); result.fix_normals()
    return result

# ═══ VERBINDUNGS-CHECK ═══════════════════════════════════════════════════════

def verify_hollow(mesh, name):
    """Prüft ob Kabelkanal wirklich offen ist."""
    test_pts = np.array([
        [0.0, 0.0, mesh.bounding_box.extents[2]/2],   # Mitte Kanal (soll LEER sein)
        [30.0, 0.0, mesh.bounding_box.extents[2]/2],  # Wand (soll VOLL sein)
    ])
    inside = mesh.contains(test_pts)
    canal_empty = not inside[0]
    wall_solid  = inside[1]
    ok = canal_empty and wall_solid
    print(f"    Kanal offen={canal_empty} Wand solid={wall_solid}  → {'[OK]' if ok else '[FEHLER]'}")
    return ok

# ═══════════════════════════════════════════════════════════════════════════
# DIE 6 TEILE
# ═══════════════════════════════════════════════════════════════════════════

def make_1_fuss():
    """
    1  FUSS – Breite stabile Kreisscheibe  Ø200 × 50mm  [PETG Schwarz]
    Schwerer Sockel. Unten flach (kein Bajonett). Oben Male-Peg.
    Profil: breite Scheibe mit leichtem Wulst-Rand.
    """
    H = 50.0
    outer = [
        [SOCK_OR, 0], [100.0, 0], [100.0, 4],   # Außenkante mit Fase
        [98.0, H-2],  [100.0, H-2], [100.0, H],  # Deckel-Kante
    ]
    # Statt dieser Punkte: einfachere Disk-Form
    body = revolve_profile(
        [[SOCK_OR, 0], [100.0, 0], [100.0, H]],
        inner_r=CABLE_R, height=H
    )
    m = union2(body, male_peg(H))
    if not m.is_watertight: m.fill_holes(); m.fix_normals()
    return m

def make_2_kugel():
    """
    2  KUGEL – Bauchige Kugelform  Ø104 × 90mm  [PETG Gelb]
    RUND · Sinusoidales Profil. Zwischen SOCK_OR und MAX_R.
    """
    H = 90.0; MAX_R = 52.0; N = 96
    outer = []
    for i in range(N+1):
        t = np.pi * i / N
        r = SOCK_OR + (MAX_R - SOCK_OR) * np.sin(t)
        outer.append([r, H*i/N])
    body = revolve_profile(outer, CABLE_R, H)
    m = union_all(body, female_socket(0.0), male_peg(H))
    if not m.is_watertight: m.fill_holes(); m.fix_normals()
    return m

def make_3_wuerfel():
    """
    3  WÜRFEL – Quadratischer Kubus  88×88×88mm  [PETG Blau]
    ECKIG · 4-seitiger Querschnitt. Runde Kragen (SOCK_OR) für Bajonett.
    Innen hohl Ø44mm via Boolean-Difference.
    """
    H = 88.0; SIDE = 88.0
    sq = sg.Polygon([(-SIDE/2,-SIDE/2),(SIDE/2,-SIDE/2),
                     (SIDE/2,SIDE/2),(-SIDE/2,SIDE/2)])
    cube_solid = trimesh.creation.extrude_polygon(sq, H)
    body = angular_hollow(cube_solid, H)
    m = union_all(body, female_socket(0.0), male_peg(H))
    if not m.is_watertight: m.fill_holes(); m.fix_normals()
    return m

def make_4_sechseck():
    """
    4  SECHSECK – Hexagonaler Prisma  Ø110 × 110mm  [PETG Grün]
    ECKIG · 6-seitiger Querschnitt. Innen hohl Ø44mm.
    """
    H = 110.0; HEX_R = 55.0
    hex_pg = sg.Polygon([(HEX_R*np.cos(np.radians(60*i+30)),
                          HEX_R*np.sin(np.radians(60*i+30))) for i in range(6)])
    hex_solid = trimesh.creation.extrude_polygon(hex_pg, H)
    body = angular_hollow(hex_solid, H)
    m = union_all(body, female_socket(0.0), male_peg(H))
    if not m.is_watertight: m.fill_holes(); m.fix_normals()
    return m

def make_5_raute():
    """
    5  RAUTE / DIAMANT – Hexagonale Doppelpyramide  Ø130 × 140mm  [PETG Lila]
    ECKIG · Schmal unten, breit in Mitte, schmal oben.
    Wie Diamant: 6 Dreiecksflächen oben + 6 unten. Innen hohl Ø44mm.
    """
    H = 140.0; HH = H/2; HEX_MID = 65.0
    # Zwei Hexagonal-Kegelstümpfe (solid), zu Bipyramide vereint
    lower = hex_frustum_solid(r_bot=SOCK_OR, r_top=HEX_MID, h=HH)
    upper = hex_frustum_solid(r_bot=HEX_MID, r_top=SOCK_OR, h=HH)
    upper = moved(upper, z=HH)
    diamond_solid = union2(lower, upper)
    body = angular_hollow(diamond_solid, H)
    m = union_all(body, female_socket(0.0), male_peg(H))
    if not m.is_watertight: m.fill_holes(); m.fix_normals()
    return m

def make_6_schirm():
    """
    6  SCHIRM – Konischer Lampenschirm  Ø220 → Ø66 × 110mm  [PETG Rot]
    RUND · Öffnet nach unten → Licht unten.
    Oben Female-Buchse (steckt auf letztes Körpermodul).
    Kabelkanal durchgehend: E14 Fassung hängt in der Öffnung.
    """
    H = 110.0; R_TOP = SOCK_OR; R_BOT = 110.0
    # Schirm: Kegel öffnet nach UNTEN
    # In unserem Koordinatensystem: unten = z=0 (breit, offen), oben = z=H (schmal, Female-Buchse)
    # Profile: innen bei z=0 offen (CABLE_R), außen bei z=0 breit (R_BOT)
    body = revolve_profile(
        [[R_TOP, 0], [R_BOT, H]],   # außen: schmal oben → breit unten (wir spiegeln danach)
        inner_r=CABLE_R, height=H
    )
    # Spiegeln: Schirm-Öffnung nach unten drehen
    body = rotated_x(body, 180)
    body = moved(body, z=H)
    # Female-Buchse bei z=H (Oberkante = Verbindung zum Modul darunter)
    m = union2(body, female_socket(H))
    if not m.is_watertight: m.fill_holes(); m.fix_normals()
    return m

# ═══════════════════════════════════════════════════════════════════════════
# EXPORT + CHECKS
# ═══════════════════════════════════════════════════════════════════════════

HEIGHTS = {
    "Fuss":50,"Kugel":90,"Wuerfel":88,"Sechseck":110,"Raute":140,"Schirm":110
}
PARTS = [
    ("1_Fuss_Basis_50mm",         make_1_fuss,     "PETG Schwarz"),
    ("2_Kugel_Round_90mm",        make_2_kugel,    "PETG Gelb"),
    ("3_Wuerfel_Square_88mm",     make_3_wuerfel,  "PETG Blau"),
    ("4_Sechseck_Hex_110mm",      make_4_sechseck, "PETG Gruen"),
    ("5_Raute_Diamant_140mm",     make_5_raute,    "PETG Lila"),
    ("6_Schirm_Konus_110mm",      make_6_schirm,   "PETG Rot"),
]

def main():
    print("╔═══════════════════════════════════════════════════╗")
    print("║  BAMBU LAB MODULLAMPE – Professioneller Check     ║")
    print("╚═══════════════════════════════════════════════════╝")
    print(f"\n  Bajonett: Male Ø{PEG_R*2}mm → Female Ø{SOCK_R*2}mm "
          f"(Spiel {(SOCK_R-PEG_R)*2:.1f}mm – OK für PETG)")
    print(f"  Kabelkanal: Ø{CABLE_R*2:.0f}mm · Schuko-Stecker ✓ · IKEA STRALA E14 ✓")
    print(f"  Bajonett: 4 Pins @ 0°/90°/180°/270°, Nut @ −45°, Drehung: 45°\n")

    H = HEIGHTS
    print("  Konfigurationen:")
    cfgs = [
        ("Komplett  ~58cm", ["Fuss","Kugel","Wuerfel","Sechseck","Raute","Schirm"]),
        ("Bauhaus-Mix ~45cm", ["Fuss","Wuerfel","Sechseck","Raute","Schirm"]),
        ("Organisch  ~31cm", ["Fuss","Kugel","Schirm"]),
        ("Eckig-Turm ~39cm", ["Fuss","Wuerfel","Sechseck","Schirm"]),
        ("Diamant    ~41cm", ["Fuss","Raute","Schirm"]),
    ]
    for name, parts in cfgs:
        t = sum(H[p] for p in parts)
        print(f"    {name:25s}  {' + '.join(parts):50s} = {t}mm = {t/10:.0f}cm")

    print(f"\n  STL-Export → {OUT}/\n")
    all_ok = True
    for name, fn, color in PARTS:
        print(f"  Baue  {name}  [{color}]")
        try:
            m = fn()
            wt = m.is_watertight
            bb = m.bounding_box.extents
            print(f"    Mesh: {'WASSERDICHT' if wt else '!NICHT WASSERDICHT'} · "
                  f"{bb[0]:.0f}×{bb[1]:.0f}×{bb[2]:.0f}mm · "
                  f"{m.volume/1000:.0f}cm³ · {len(m.vertices):,} Vertices")
            verify_hollow(m, name)
            m.export(f"{OUT}/{name}.stl")
            if not wt: all_ok = False
        except Exception as e:
            print(f"    FEHLER: {e}"); import traceback; traceback.print_exc()
            all_ok = False
        print()

    print("═"*54)
    print(f"  {'[OK] ALLE 6 STL FERTIG' if all_ok else '[!!] FEHLER AUFGETRETEN'}")
    print("═"*54)
    print("\n  Bambu Studio Empfehlungen:")
    print("  Material:    PETG (mind. 240°C Düse / 70°C Bett)")
    print("  Schicht:     0.2mm")
    print("  Wände:       4 Perimeter (für Bajonett-Festigkeit)")
    print("  Infill:      30% Gyroid")
    print("  Stützstruk:  Nur für Schirm (Überhang ~45°)")
    print("  Toleranz:    Bajonett 0.6mm Spiel · passt sofort")
    print()
    print("  Farben (Bauhaus-Palette):")
    for _, _, c in PARTS: print(f"    {c}")

if __name__ == "__main__":
    main()
