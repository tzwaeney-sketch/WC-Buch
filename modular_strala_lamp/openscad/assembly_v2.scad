include <config.scad>
include <round_modules_v2.scad>

// ============================================================
// assembly_v2.scad — full stack preview for the .3mf bundle.
// Stacks base + a few bodies + holder spacing (visual only).
// Each interface offset by bay_depth so lugs visually nest.
// ============================================================
$fn = 48;

z = 0;
// base placeholder (cylinder) — real base in lamp_base_round_v2
color("dimgray") cylinder(h=base_h, r=base_d/2, $fn=96);
z1 = base_h;
translate([0,0,z1]) color("lightblue") body_sphere();
z2 = z1 + 80;
translate([0,0,z2]) color("lightgreen") body_flat();
z3 = z2 + 70;
translate([0,0,z3]) color("khaki") body_narrow_ring();
