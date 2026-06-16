#!/usr/bin/env python3
"""
BAMBU LAB P1S/P2S – MODULLAMPE v2
6 Elemente: 2 Füße + 2 Stiele + 2 Schirme
Gesamthöhe ca. 60 cm (Fuß2 + Stiel2 + Schirm2 = 600 mm)

Bajonett-System (4-Pin, 45°-Vierteldrehung):
  Male (oben): Ø50mm Peg + 4 Pins (→ Ø56mm) bei 0/90/180/270°
  Female (unten): Ø50,5mm Bohrung + 4 J-Schlitze
    – Einführschlitz vertikal (bei 0/90/180/270°)
    – Verriegelungsnut horizontal (bei 45/135/225/315°)
  Kabelkanal: Ø44mm durchgehend durch alle Elemente
"""

import numpy as np
import trimesh
import trimesh.creation as tc
import trimesh.boolean as tb
import os, sys

OUT = "/home/user/WC-Buch/stl"
os.makedirs(OUT, exist_ok=True)

SEG = 64          # Umlauf-Segmente

# ─── Massystem (mm) ───────────────────────────────────────────────────────────
CABLE_R   = 22.0   # Kabelkanal-Radius  → Ø44 mm (Schuko Ø≤19mm)
PEG_R     = 25.0   # Männlicher Stecker  → Ø50 mm
SOCK_R    = 25.3   # Weibliche Buchse    → Ø50,6 mm (0,3 mm Luft pro Seite)
SOCK_WALL = 8.0    # Wanddicke Buchse    → Außen Ø66,6 mm
SOCK_OR   = SOCK_R + SOCK_WALL  # ~33,3 mm Außenradius Buchse
PEG_H     = 14.0   # Höhe Stecker-Peg
SOCK_H    = 14.0   # Tiefe Buchse

PIN_R     = 3.0    # Stärke der Pins (radial über PEG_R)
PIN_ARC   = 12.0   # Breite der Pins (Grad)
PIN_Z     = 5.0    # Z-Position Mitte des Pins (vom unteren Stecker-Ende)
PIN_THICK = 3.0    # Höhe des Pins

CLEARANCE = 0.3    # Druckspiel für PETG

# ─── Basis-Körper via Revolve ──────────────────────────────────────────────────

def revolve(profile_yz, sections=SEG):
    """Profile [[r,z], …] um Z-Achse drehen → Trimesh."""
    pts = np.array(profile_yz, dtype=float)
    n = len(pts); N = sections
    verts = []
    for i in range(N):
        ang = 2 * np.pi * i / N
        c, s = np.cos(ang), np.sin(ang)
        for r, z in pts:
            verts.append([r * c, r * s, z])
    verts = np.array(verts)
    faces = []
    for i in range(N):
        ni = (i + 1) % N
        for j in range(n):
            nj = (j + 1) % n
            a, b = i*n+j, ni*n+j
            c2, d  = ni*n+nj, i*n+nj
            faces += [[a, b, c2], [a, c2, d]]
    m = trimesh.Trimesh(vertices=verts, faces=np.array(faces))
    m.fix_normals()
    return m

def hollow_tube(outer_r, inner_r, height, sections=SEG):
    return revolve([[inner_r,0],[outer_r,0],[outer_r,height],[inner_r,height]], sections)

def hollow_frustum(r_bot, r_top, inner_r, height, sections=SEG):
    return revolve([[inner_r,0],[r_bot,0],[r_top,height],[inner_r,height]], sections)

# ─── Bajonett-Stecker (Male, oben) ────────────────────────────────────────────

def pin_mesh(angle_deg):
    """Ein radialer Pin am Stecker-Peg."""
    a0 = np.radians(angle_deg - PIN_ARC/2)
    a1 = np.radians(angle_deg + PIN_ARC/2)
    r0 = PEG_R - 0.2         # leicht in den Peg eingebettet
    r1 = PEG_R + PIN_R + 0.2 # etwas über Pin-Höhe (für sauberes Boolean)
    z0 = PIN_Z - PIN_THICK/2
    z1 = PIN_Z + PIN_THICK/2
    N = 12
    verts, faces = [], []
    angles = np.linspace(a0, a1, N)
    # 8 Eckpunkte als Sektor-Prisma
    for r in [r0, r1]:
        for z in [z0, z1]:
            for ang in [a0, a1]:
                verts.append([r*np.cos(ang), r*np.sin(ang), z])
    verts = np.array(verts)
    hull = trimesh.convex.convex_hull(verts)
    return hull

def male_peg(z_base):
    """Stecker-Peg mit 4 Pins. z_base = Z-Koordinate Elementoberkante."""
    peg = hollow_tube(PEG_R, CABLE_R, PEG_H)
    peg.apply_translation([0, 0, z_base])
    parts = [peg]
    for a in [0, 90, 180, 270]:
        p = pin_mesh(a)
        p.apply_translation([0, 0, z_base])
        parts.append(p)
    m = trimesh.util.concatenate(parts)
    m.fix_normals()
    return m

# ─── Bajonett-Buchse (Female, unten) ──────────────────────────────────────────

def j_slot_cutter(angle_deg, entry_z_bot=0.0, groove_z_bot=None):
    """
    J-Schlitz-Cutter für eine Position:
      – Einführschlitz (vertikal): von entry_z_bot bis grove_z_bot+PIN_THICK
      – Verriegelungsnut (tangential): 45° Bogensweep ab angle_deg
    Cutter liegt auf dem Zylinder-Innenradius SOCK_R.
    """
    if groove_z_bot is None:
        groove_z_bot = entry_z_bot + 2.0  # Nut sitzt 2mm über Einführung

    ARC_ENTRY = PIN_ARC + 4      # Einführschlitz etwas breiter als Pin
    ARC_LOCK  = 45 + PIN_ARC/2  # Verriegelungsnut 45°-Sweep + Pin-Hälfte

    r0 = SOCK_R - 0.5            # leicht ins Hüllvolumen
    r1 = SOCK_R + PIN_R + 1.5   # über Pin-Höhe

    parts = []

    # 1) Einführschlitz (vertikal)
    a0 = np.radians(angle_deg - ARC_ENTRY/2)
    a1 = np.radians(angle_deg + ARC_ENTRY/2)
    N = 10
    v = []
    for z in [entry_z_bot - 0.5, groove_z_bot + PIN_THICK + 0.5]:
        for r in [r0, r1]:
            for ang in np.linspace(a0, a1, N):
                v.append([r*np.cos(ang), r*np.sin(ang), z])
    hull_e = trimesh.convex.convex_hull(np.array(v))
    parts.append(hull_e)

    # 2) Verriegelungsnut (tangential sweep in Gegenuhrzeiger = -45°)
    a_start = np.radians(angle_deg)
    a_end   = np.radians(angle_deg - ARC_LOCK)   # gegen Uhrzeiger 45°
    N2 = 16
    v2 = []
    for z in [groove_z_bot - 0.5, groove_z_bot + PIN_THICK + 0.5]:
        for r in [r0, r1]:
            for ang in np.linspace(a_start, a_end, N2):
                v2.append([r*np.cos(ang), r*np.sin(ang), z])
    hull_l = trimesh.convex.convex_hull(np.array(v2))
    parts.append(hull_l)

    return trimesh.util.concatenate(parts)

def female_socket(z_top):
    """
    Buchse unten am Element. z_top = Unterseite des Elements.
    Buchse ragt nach UNTEN (negative Z-Richtung).
    """
    z0 = z_top - SOCK_H      # Buchsen-Unterseite
    z1 = z_top               # Buchsen-Oberseite (Flush mit Elementunterseite)

    # Buchsenkörper (Hohlzylinder)
    sock_body = hollow_tube(SOCK_OR, CABLE_R, SOCK_H)
    sock_body.apply_translation([0, 0, z0])

    # 4 J-Schlitze (Einführung bei 0/90/180/270°, Nut dreht −45°)
    cutters = []
    for a in [0, 90, 180, 270]:
        cutter = j_slot_cutter(
            angle_deg   = a,
            entry_z_bot = z0,                  # Einführung von ganz unten
            groove_z_bot= z0 + SOCK_H - PIN_THICK - 3.0  # Nut nahe Oberkante
        )
        cutters.append(cutter)

    cutter_all = trimesh.util.concatenate(cutters)

    # Boolean: Buchse minus Schlitze
    result = tb.difference([sock_body, cutter_all], engine='manifold')
    if not result.is_watertight:
        result.fill_holes()
        result.fix_normals()
    return result

# ─── Hilfsfunktionen ──────────────────────────────────────────────────────────

def combine(*meshes):
    m = trimesh.util.concatenate(list(meshes))
    m.fix_normals()
    return m

def element_check(mesh, name):
    wt = mesh.is_watertight
    vol = mesh.volume if wt else float('nan')
    bb = mesh.bounding_box.extents
    print(f"  {name:35s}  watertight={wt}  "
          f"vol={vol/1000:.1f}cm³  "
          f"bbox={bb[0]:.0f}x{bb[1]:.0f}x{bb[2]:.0f}mm")
    return mesh

# ═══════════════════════════════════════════════════════════════════════════════
# 6 VERSCHIEDENE STIEL-MODULE – Bauhaus Stil
#
# Alle verbindbar via Bajonett (M oben, F unten).
# Komplett-Stack alle 6: ~620 mm → ca. 62 cm
# + IKEA STRALA E14 Fassung oben einhängen.
#
# 1  SCHEIBE    – Flache breite Disc  Ø160 × 25mm   (Abschluss/Schirm/Trennring)
# 2  KUGEL      – Bauchige Kugelform  Ø90  × 75mm   (dekorativ, Mitte)
# 3  PYRAMIDE ↑ – Kegel nach oben    Ø58→Ø110×80mm  (öffnend)
# 4  PYRAMIDE ↓ – Kegel nach unten  Ø110→Ø58×80mm   (schließend)
# 5  STAB KURZ  – Schlankes Rohr    Ø58   × 130mm
# 6  STAB LANG  – Hohes Rohr        Ø58   × 300mm
#
# Beispiel-Konfigurationen (Höhe ≈ ohne Überlappung):
#   Komplett:    1+2+3+4+5+6 = 25+75+80+80+130+300 = 690mm = 69cm
#   Standard:    6+3+1       = 300+80+25            = 405mm = 41cm + Schirm
#   Klassisch:   6+2+1       = 300+75+25            = 400mm = 40cm
#   Bauhaus-Turm:6+5+4+3+1  = 300+130+80+80+25     = 615mm = 62cm ← ~60cm
# ═══════════════════════════════════════════════════════════════════════════════

def profile_body(outer_pts, inner_r, height, sections=SEG):
    """
    Beliebige Außenkontur (Liste von [r,z] von z=0 bis z=height),
    kombiniert mit geradem Innenkanal bei inner_r.
    Ergibt ein geschlossenes Hohlkörper-Profil.
    """
    # Profil: innen unten → außen unten → außenkontur → außen oben → innen oben → zurück
    profile = [[inner_r, 0.0]] + list(outer_pts) + [[inner_r, height]]
    return revolve(profile, sections)

# ─── 6 FORMEN ──────────────────────────────────────────────────────────────────

def make_1_scheibe():
    """
    1 SCHEIBE – Breite Disc  Ø160 × 30mm  [ROT]
    Wie eine breite Scheibe / Abschluss-Cap / Schirm-Ersatz.
    Flache Platte mit kurzem Randwulst für Stabilität.
    """
    H = 30.0; OR = 80.0
    # Außenkontur: flach mit leichtem Randwulst
    outer = [
        [OR,   0.0],
        [OR,   H],
    ]
    body = profile_body(outer, CABLE_R, H)
    male = male_peg(z_base=H)
    fem  = female_socket(z_top=0.0)
    return combine(body, male, fem)

def make_2_kugel():
    """
    2 KUGEL – Bauchiger Kugelkörper  Ø100 × 90mm  [GELB]
    Runde Bauchform, Kugel-ähnlich. Dekoratives Mittelelement.
    Sinusoidales Profil: eng-breit-eng.
    """
    H = 90.0; MAX_R = 50.0; N = 48
    outer = []
    for i in range(N+1):
        t = np.pi * i / N        # 0 → π
        r = SOCK_OR + (MAX_R - SOCK_OR) * np.sin(t)
        z = H * i / N
        outer.append([r, z])
    body = profile_body(outer, CABLE_R, H)
    male = male_peg(z_base=H)
    fem  = female_socket(z_top=0.0)
    return combine(body, male, fem)

def make_3_kegel_auf():
    """
    3 KEGEL AUF – Kegel öffnet nach oben  Ø66→Ø120 × 100mm  [BLAU]
    Wie ein Trichter: unten schmal, oben weit. Licht-Diffusor.
    """
    H = 100.0; R_BOT = SOCK_OR; R_TOP = 60.0
    body = hollow_frustum(r_bot=R_BOT, r_top=R_TOP, inner_r=CABLE_R, height=H)
    male = male_peg(z_base=H)
    fem  = female_socket(z_top=0.0)
    return combine(body, male, fem)

def make_4_kegel_ab():
    """
    4 KEGEL AB – Kegel schließt nach oben  Ø120→Ø66 × 100mm  [SCHWARZ]
    Wie ein umgekehrter Trichter: unten breit, oben schmal. Gegenpart zu Kegel Auf.
    """
    H = 100.0; R_BOT = 60.0; R_TOP = SOCK_OR
    body = hollow_frustum(r_bot=R_BOT, r_top=R_TOP, inner_r=CABLE_R, height=H)
    male = male_peg(z_base=H)
    fem  = female_socket(z_top=0.0)
    return combine(body, male, fem)

def make_5_sanduhr():
    """
    5 SANDUHR – Doppelkegel / Stundenglasfigur  Ø110→Ø58→Ø110 × 140mm  [WEISS]
    Unten breit, Mitte eng, oben breit. Zwei Kegel Rücken an Rücken.
    """
    H = 140.0; R_WIDE = 55.0; R_NARROW = SOCK_OR; N = 48
    outer = []
    for i in range(N+1):
        t = np.pi * i / N        # 0 → π : cos(0)=1, cos(π)=-1
        # r breit bei t=0 und t=π, schmal bei t=π/2
        r = R_NARROW + (R_WIDE - R_NARROW) * abs(np.cos(t))
        z = H * i / N
        outer.append([r, z])
    body = profile_body(outer, CABLE_R, H)
    male = male_peg(z_base=H)
    fem  = female_socket(z_top=0.0)
    return combine(body, male, fem)

def make_6_kelch():
    """
    6 KELCH – Kelchform / Vase  Ø66→Ø90→Ø66→Ø100 × 160mm  [ROT-DUNKEL]
    Kelch-Silhouette: schmal unten, bauchig in der Mitte, wieder eng,
    dann ausladend am Rand oben. Wie ein Weinglas.
    """
    H = 160.0; N = 60
    # Stützpunkte des Kelch-Profils (r, z) von unten nach oben
    knots = [
        (SOCK_OR,  0.0),      # Fuß-Ansatz (schmal)
        (SOCK_OR + 2, H*0.05),
        (42.0,  H * 0.20),   # erster Bauch
        (44.0,  H * 0.35),   # Bauch-Maximum
        (38.0,  H * 0.50),   # Taille einziehen
        (36.0,  H * 0.60),   # engste Stelle (Stiel des Kelchs)
        (40.0,  H * 0.70),   # öffnet wieder
        (50.0,  H * 0.85),   # Rand öffnet weit
        (55.0,  H * 1.00),   # Oberkante
    ]
    # Hermite-ähnliche Interpolation via numpy
    import numpy as np
    zk = np.array([k[1] for k in knots])
    rk = np.array([k[0] for k in knots])
    z_dense = np.linspace(0, H, N+1)
    r_dense = np.interp(z_dense, zk, rk)
    outer = list(zip(r_dense, z_dense))
    body = profile_body(outer, CABLE_R, H)
    male = male_peg(z_base=H)
    fem  = female_socket(z_top=0.0)
    return combine(body, male, fem)

# ═══════════════════════════════════════════════════════════════════════════════
# VERBINDUNGS-CHECK
# ═══════════════════════════════════════════════════════════════════════════════

def check_connection():
    """
    Prüft geometrisch ob Male-Peg in Female-Buchse passt.
    Gibt Abstände und Spielmaße aus.
    """
    print("\n=== VERBINDUNGS-CHECK ===")
    print(f"  Male  Peg    Außen: Ø{PEG_R*2:.1f}mm")
    print(f"  Female Buchse Innen: Ø{SOCK_R*2:.1f}mm")
    print(f"  Radiales Spiel:      {(SOCK_R-PEG_R)*2:.2f}mm total  → {SOCK_R-PEG_R:.2f}mm je Seite")
    print(f"  Pin-Höhe:            {PIN_R:.1f}mm radial, {PIN_THICK:.1f}mm axial")
    print(f"  J-Schlitz gesamt:    ~{PIN_R+1.5:.1f}mm radial, {PIN_THICK+0.5:.1f}mm axial")
    print(f"  Drehwinkel:          45° zum Verriegeln")
    print(f"  Kabelkanal:          Ø{CABLE_R*2:.0f}mm → Schuko + STRALA E14 OK")
    pin_to_wall = SOCK_OR - PEG_R - PIN_R
    print(f"  Wanddicke Buchse:    {SOCK_WALL:.1f}mm  (Peg-Außen bis Buchsen-Außen: {pin_to_wall:.1f}mm)")
    if SOCK_R >= PEG_R + CLEARANCE:
        print(f"  [OK] Spiel {(SOCK_R-PEG_R):.2f}mm/Seite – perfekt fuer PETG-Druck (0.2–0.4mm Empfehlung)")
    else:
        print("  [!!] Spiel zu gering – bitte SOCK_R erhoehen!")

def height_check():
    print("\n=== HÖHENCHECK (Konfigurationen) ===")
    H = {
        "Scheibe":30, "Kugel":90, "Kegel-auf":100,
        "Kegel-ab":100, "Sanduhr":140, "Kelch":160,
    }
    configs = [
        ("Komplett-Stack ~62cm",    ["Scheibe","Kugel","Kegel-auf","Kegel-ab","Sanduhr","Kelch"]),
        ("Bauhaus-Turm ~60cm",      ["Kelch","Sanduhr","Kegel-auf","Scheibe"]),
        ("Organisch-Rund ~53cm",    ["Kelch","Kugel","Sanduhr","Kegel-ab"]),
        ("Schlank ~33cm",           ["Kegel-auf","Kegel-ab","Sanduhr"]),
        ("Mini-Tisch ~22cm",        ["Kugel","Scheibe","Kegel-auf"]),
        ("Maximal ~59cm",           ["Kelch","Sanduhr","Kugel","Kegel-auf","Kegel-ab"]),
    ]
    for name, parts in configs:
        total = sum(H[p] for p in parts)
        print(f"  {name:30s}  {' + '.join(parts):55s}  = {total}mm = {total/10:.1f}cm")

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

PARTS = [
    ("1_Scheibe_Disc_30mm",       make_1_scheibe,    "PETG Rot"),
    ("2_Kugel_Sphere_90mm",       make_2_kugel,      "PETG Gelb"),
    ("3_Kegel-Auf_100mm",         make_3_kegel_auf,  "PETG Blau"),
    ("4_Kegel-Ab_100mm",          make_4_kegel_ab,   "PETG Schwarz"),
    ("5_Sanduhr_140mm",           make_5_sanduhr,    "PETG Weiss"),
    ("6_Kelch_Vase_160mm",        make_6_kelch,      "PETG Dunkelrot"),
]

def main():
    check_connection()
    height_check()

    print(f"\n=== STL-GENERIERUNG → {OUT}/ ===\n")
    all_ok = True
    for name, fn, color in PARTS:
        print(f"  Baue {name} ({color}) ...", end=" ", flush=True)
        try:
            mesh = fn()
            if not mesh.is_watertight:
                mesh.fill_holes()
                mesh.fix_normals()
            wt   = mesh.is_watertight
            bb   = mesh.bounding_box.extents
            vol  = mesh.volume if wt else float('nan')
            path = f"{OUT}/{name}.stl"
            mesh.export(path)
            status = "OK " if wt else "!WT"
            print(f"{status}  {bb[0]:.0f}x{bb[1]:.0f}x{bb[2]:.0f}mm  "
                  f"vol={vol/1000:.1f}cm³  ({len(mesh.vertices):,}V)")
            if not wt:
                all_ok = False
        except Exception as e:
            print(f"FEHLER: {e}")
            all_ok = False

    print(f"\n{'Alle 6 STL OK' if all_ok else 'Achtung: nicht alle OK'}")
    print("\nBambu Studio Einstellungen:")
    print("  Material:      PETG")
    print("  Schichthoehe:  0.2 mm")
    print("  Wandlinien:    4 min.")
    print("  Infill:        30 % Gyroid")
    print("  Stuetzen:      Nur fuer Fuß2 und Schirm2 noetig")
    print("  Kabelkanal:    Ø44mm – KEIN Support im Kanal!")

if __name__ == "__main__":
    main()
