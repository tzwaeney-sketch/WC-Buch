#!/usr/bin/env python3
"""
BAMBU LAB MODULLAMPE – STL Generator
Generates 6 x STL files (one per lamp element) for Bambu Lab P1S/P2S.

Key dimensions (mm):
  Cable channel:  Ø 44 mm inner (Schuko + IKEA STRALA E14)
  Bayonet collar: Ø 58 mm outer, 4 pins, 90° quarter-turn
  Wall:           ~7 mm (inner Ø22 → outer Ø29 mm radius)
"""

import numpy as np
import trimesh
import trimesh.creation as tc
import os

OUT = "/home/user/WC-Buch/stl"
os.makedirs(OUT, exist_ok=True)

SEG = 64   # revolution segments (quality)

# ─── Common radii (mm) ───────────────────────────────────────────────────────
INNER_R = 22.0     # cable channel radius (Ø44 mm)
BAY_R   = 29.0     # bayonet outer radius  (Ø58 mm)
BAY_H   = 4.0      # height of bayonet collar on each side
PIN_W   = 5.0      # pin angular width (mm arc)
PIN_H   = 2.5      # pin protrusion height (above collar face)
PIN_D   = BAY_R - 1.5  # pin radial position (just inside outer edge)

# ─── Mesh helpers ─────────────────────────────────────────────────────────────

def revolve_profile(pts_yz, sections=SEG):
    """
    Revolve a 2-D closed profile (Nx2 array of [r, z] points) 360° around Z.
    Returns a watertight trimesh.Trimesh.
    """
    pts = np.asarray(pts_yz, dtype=float)
    n   = len(pts)
    N   = sections
    verts = []
    faces = []

    # Generate vertices
    for i in range(N):
        angle = 2 * np.pi * i / N
        c, s  = np.cos(angle), np.sin(angle)
        for r, z in pts:
            verts.append([r * c, r * s, z])

    verts = np.array(verts)

    # Generate faces (quads → triangles)
    for i in range(N):
        ni = (i + 1) % N
        for j in range(n):
            nj = (j + 1) % n
            a = i  * n + j
            b = ni * n + j
            c = ni * n + nj
            d = i  * n + nj
            faces.append([a, b, c])
            faces.append([a, c, d])

    mesh = trimesh.Trimesh(vertices=verts, faces=np.array(faces))
    mesh.fix_normals()
    return mesh


def hollow_cylinder(outer_r, inner_r, height, sections=SEG):
    """Hollow cylinder (annulus) – open top/bottom closed by walls."""
    # Profile: outer wall → inner wall (counter-clockwise when viewed from outside)
    profile = [
        [inner_r, 0],
        [outer_r, 0],
        [outer_r, height],
        [inner_r, height],
    ]
    return revolve_profile(profile, sections)


def hollow_frustum(r_bot, r_top, inner_r, height, sections=SEG):
    """
    Hollow truncated cone (frustum).
    Outer wall tapers from r_bot (z=0) to r_top (z=height).
    Inner wall stays at inner_r throughout.
    """
    profile = [
        [inner_r, 0],
        [r_bot,   0],
        [r_top,   height],
        [inner_r, height],
    ]
    return revolve_profile(profile, sections)


def bayonet_pin_mesh(angle_deg, r=PIN_D, h_base=0, h_total=BAY_H+PIN_H,
                     arc_w_deg=8.0, radial_d=2.5):
    """
    Single bayonet pin: a small radial protrusion at given angular position.
    Modeled as a box-ish shape using revolve over a narrow angular sector.
    """
    a0 = np.radians(angle_deg - arc_w_deg/2)
    a1 = np.radians(angle_deg + arc_w_deg/2)
    pts = []
    NA = 8
    # outer arc
    for t in np.linspace(a0, a1, NA):
        pts.append([(r + radial_d) * np.cos(t),
                    (r + radial_d) * np.sin(t),
                    h_total])
    # inner arc (reverse)
    for t in np.linspace(a1, a0, NA):
        pts.append([r * np.cos(t), r * np.sin(t), h_total])
    # bottom
    for t in np.linspace(a1, a0, NA):
        pts.append([r * np.cos(t), r * np.sin(t), h_base])
    for t in np.linspace(a0, a1, NA):
        pts.append([(r + radial_d) * np.cos(t),
                    (r + radial_d) * np.sin(t),
                    h_base])

    pts = np.array(pts)
    hull = trimesh.convex.convex_hull(pts)
    return hull


def bayonet_collar_male(z_offset=0):
    """
    Male bayonet collar: annular ring + 4 outward pins.
    Sits on top of the element (pins face upward).
    """
    # Base collar ring
    collar = hollow_cylinder(BAY_R, INNER_R, BAY_H + PIN_H)
    collar.apply_translation([0, 0, z_offset])

    # 4 pins at 45°, 135°, 225°, 315°
    parts = [collar]
    for a in [45, 135, 225, 315]:
        pin = bayonet_pin_mesh(a, r=BAY_R-1, h_base=z_offset,
                                h_total=z_offset + BAY_H + PIN_H,
                                arc_w_deg=9, radial_d=3)
        parts.append(pin)

    combined = trimesh.util.concatenate(parts)
    combined.fix_normals()
    return combined


def bayonet_collar_female(z_offset=0):
    """
    Female bayonet collar: annular ring with 4 slots cut in (simplified as full ring).
    Slots are at 0°, 90°, 180°, 270° – just slightly thinner ring (visual only for now).
    The actual slot is a J-slot: for printing, the male pins slide in from a gap.
    """
    collar = hollow_cylinder(BAY_R, INNER_R, BAY_H)
    collar.apply_translation([0, 0, z_offset])
    return collar


def combine(*meshes):
    result = trimesh.util.concatenate(list(meshes))
    result.fix_normals()
    return result

# ═══════════════════════════════════════════════════════════════════════════════
# 6 LAMP ELEMENTS
# ═══════════════════════════════════════════════════════════════════════════════

def make_A():
    """Fuss 1 – Scheiben-Basis  Ø120 × 32 mm  (Male Bajonett oben)."""
    body   = hollow_cylinder(outer_r=60, inner_r=INNER_R, height=32)
    collar = bayonet_collar_male(z_offset=32)
    return combine(body, collar)


def make_B():
    """Fuss 2 – Konus-Dreifuss  Ø140→Ø58 × 55 mm  (Male Bajonett oben)."""
    body   = hollow_frustum(r_bot=70, r_top=BAY_R, inner_r=INNER_R, height=55)
    collar = bayonet_collar_male(z_offset=55)
    return combine(body, collar)


def make_C():
    """Schirm 1 – Bauhaus Disc  Ø180 × 25 mm  (Male oben, Female unten)."""
    body    = hollow_cylinder(outer_r=90, inner_r=INNER_R, height=25)
    col_top = bayonet_collar_male(z_offset=25)
    col_bot = bayonet_collar_female(z_offset=-BAY_H)
    return combine(body, col_top, col_bot)


def make_D():
    """Schirm 2 – Konus-Schirm  Ø200→Ø58 × 75 mm  (Male Bajonett oben, offen unten)."""
    body   = hollow_frustum(r_bot=100, r_top=BAY_R, inner_r=INNER_R, height=75)
    collar = bayonet_collar_male(z_offset=75)
    return combine(body, collar)


def make_E():
    """
    Schirm 3 – Dom-Schirm / Uplighter  Ø190 × 60 mm  (Female Bajonett unten).

    Cross-section profile (revolved 360°):
    - Skirt: vertical wall from base to spring line (INNER_R → W_DOME)
    - Dome shell: elliptic arc with wall thickness WALL_T
    - Closed profile avoids degenerate apex (inner dome stops at small flat cap)
    """
    SKIRT_H = 15.0
    DOME_H  = 45.0
    W_DOME  = 95.0   # outer radius at spring line
    WALL_T  = 7.0    # shell wall thickness
    APEX_R  = 3.0    # small flat cap at dome apex (avoids r=0 singularity)
    N_ARC   = 40

    # Build outer arc: (W_DOME, SKIRT_H) → (APEX_R, SKIRT_H+DOME_H)
    outer_arc = []
    for i in range(N_ARC + 1):
        t = np.pi/2 * i / N_ARC
        r = APEX_R + (W_DOME - APEX_R) * np.cos(t)
        z = SKIRT_H + DOME_H * np.sin(t)
        outer_arc.append([r, z])

    # Inner arc: slightly smaller ellipse (wall thickness inward and downward)
    W_IN = W_DOME - WALL_T
    DH_IN = DOME_H - WALL_T
    inner_arc = []
    for i in range(N_ARC + 1):
        t = np.pi/2 * i / N_ARC
        r = APEX_R + (W_IN - APEX_R) * np.cos(t)
        z = SKIRT_H + DH_IN * np.sin(t)
        inner_arc.append([r, z])

    # Full closed profile (counter-clockwise looking from +r side):
    # Start at bottom inner (INNER_R, 0)
    # → up inner wall to skirt top (INNER_R, SKIRT_H)
    # → along inner dome arc from (W_IN, SKIRT_H) to (APEX_R, SKIRT_H+DH_IN)
    # → flat inner cap at apex z (APEX_R → APEX_R)
    # → up tiny wall to outer apex (APEX_R, SKIRT_H+DOME_H)
    # → back along outer dome arc (APEX_R, SKIRT_H+DOME_H) → (W_DOME, SKIRT_H)
    # → down outer skirt wall to base (W_DOME, 0)
    # → close along base (W_DOME → INNER_R at z=0)

    profile = []
    profile.append([INNER_R, 0.0])
    profile.append([INNER_R, SKIRT_H])
    # transition from inner skirt to inner dome
    profile.append([W_IN, SKIRT_H])
    # inner dome arc (index 0 starts at spring, N_ARC ends at apex)
    for r, z in inner_arc[1:]:
        profile.append([r, z])
    # flat inner apex cap: from inner apex to outer apex (same z, APEX_R radius)
    profile.append([APEX_R, SKIRT_H + DOME_H])
    # outer dome arc reversed (from apex back to spring line)
    for r, z in reversed(outer_arc[:-1]):
        profile.append([r, z])
    # down outer skirt
    profile.append([W_DOME, 0.0])
    # close at base
    # (the revolve_profile closes back to start)

    dome_mesh = revolve_profile(profile, sections=SEG)

    # Female collar below (z_offset=-BAY_H so it sits under the base)
    collar = bayonet_collar_female(z_offset=-BAY_H)
    return combine(dome_mesh, collar)


def make_F():
    """Stiel – Modularer Verbinder  Ø58 × 100 mm  (Male oben, Female unten, stapelbar)."""
    body    = hollow_cylinder(outer_r=BAY_R, inner_r=INNER_R, height=100)
    col_top = bayonet_collar_male(z_offset=100)
    col_bot = bayonet_collar_female(z_offset=-BAY_H)
    return combine(body, col_top, col_bot)

# ═══════════════════════════════════════════════════════════════════════════════
# EXPORT
# ═══════════════════════════════════════════════════════════════════════════════

PARTS = [
    ("A_Fuss1_Scheiben-Basis",   make_A),
    ("B_Fuss2_Konus-Dreifuss",   make_B),
    ("C_Schirm1_Bauhaus-Disc",   make_C),
    ("D_Schirm2_Konus-Schirm",   make_D),
    ("E_Schirm3_Dom-Schirm",     make_E),
    ("F_Stiel_Verbinder",        make_F),
]

def main():
    print(f"Generating STL files → {OUT}/\n")
    for name, fn in PARTS:
        print(f"  Building {name} ...", end=" ", flush=True)
        mesh = fn()

        # Verify mesh
        if not mesh.is_watertight:
            mesh.fill_holes()
            mesh.fix_normals()

        vols = mesh.volume if mesh.is_watertight else float('nan')
        path = f"{OUT}/{name}.stl"
        mesh.export(path)
        print(f"OK  ({len(mesh.vertices):,} verts, vol≈{vols:.0f} mm³) → {name}.stl")

    print(f"\nDone – {len(PARTS)} STL files in {OUT}/")
    print("\nBambu Lab slicer settings:")
    print("  Material:  PETG (or PETG-CF for strength)")
    print("  Layer:     0.2 mm")
    print("  Walls:     4 perimeters")
    print("  Infill:    25-40 %  Gyroid")
    print("  Cable channel: Ø44 mm – NO supports inside channel")

if __name__ == "__main__":
    main()
