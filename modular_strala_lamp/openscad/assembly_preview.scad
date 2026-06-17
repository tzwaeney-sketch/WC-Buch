include <config.scad>
include <bayonet_system.scad>
include <round_modules.scad>
include <geometric_modules.scad>
include <organic_modules.scad>
include <utility_modules.scad>
include <lamp_base.scad>

// NOTE: included module files have trailing demo calls; suppress by
// rendering only the requested config module. The trailing calls render
// at origin but the preview modules translate the real stack upward, so
// for clean previews render with the specific config module only.

overlap = bayonet_working_depth;  // modules overlap by lug depth when locked

// Stack helper: place a sequence of [module-height] at increasing z.
// We simply translate each part; real assembly interlocks via bayonet.

module _show(label, total) {
    echo(str("CONFIG ", label, " total body height = ", total, " mm"));
}

// Config 1 — Soft Round
module config_soft_round() {
    lamp_base();
    translate([0,0,base_total_height+5-overlap]) {
        mod_sphere(h=75);
        translate([0,0,75-overlap]) mod_disc(h=35);
        translate([0,0,75+35-2*overlap]) mod_oblate_sphere(h=45);
        translate([0,0,75+35+45-3*overlap]) mod_ring_module(h=40);
        translate([0,0,75+35+45+40-4*overlap]) mod_soft_cylinder(h=65);
        translate([0,0,75+35+45+40+65-5*overlap]) mod_sphere(h=75);
        translate([0,0,75+35+45+40+65+75-6*overlap]) mod_top_cap();
    }
    _show("1 SoftRound", 75+35+45+40+65+75 - 6*overlap);
}

// Config 2 — Geometric
module config_geometric() {
    translate([0,0,base_total_height+5-overlap]) {
        mod_cube_rounded(h=70);
        translate([0,0,70-overlap]) mod_diamond_faceted(h=80);
        translate([0,0,150-2*overlap]) mod_hexagon(h=65);
        translate([0,0,215-3*overlap]) mod_frustum(h=60);
        translate([0,0,275-4*overlap]) mod_stepped_geometric(h=75);
        translate([0,0,350-5*overlap]) mod_cube_rounded(h=70);
        translate([0,0,420-6*overlap]) mod_top_cap();
    }
    lamp_base();
    _show("2 Geometric", 420-6*overlap);
}

// Config 3 — Organic
module config_organic() {
    translate([0,0,base_total_height+5-overlap]) {
        mod_teardrop(h=75);
        translate([0,0,75-overlap]) mod_vase(h=85);
        translate([0,0,160-2*overlap]) mod_pumpkin(h=65);
        translate([0,0,225-3*overlap]) mod_wave(h=60);
        translate([0,0,285-4*overlap]) mod_organic_diamond(h=80);
        translate([0,0,365-5*overlap]) mod_top_cap();
    }
    lamp_base();
    _show("3 Organic", 365-5*overlap);
}

// Config 4 — Minimal
module config_minimal() {
    translate([0,0,base_total_height+5-overlap]) {
        mod_sphere(h=120, outer_d=130);
        translate([0,0,120-overlap]) mod_top_cap();
    }
    lamp_base();
    _show("4 Minimal", 120-overlap);
}

// Config 5 — Mixed
module config_mixed() {
    translate([0,0,base_total_height+5-overlap]) {
        mod_sphere(h=75);
        translate([0,0,75-overlap]) mod_narrow_shadow_ring(h=25);
        translate([0,0,100-2*overlap]) mod_cube_rounded(h=70);
        translate([0,0,170-3*overlap]) mod_narrow_ribbed_ring(h=30);
        translate([0,0,200-4*overlap]) mod_vase(h=85);
        translate([0,0,285-5*overlap]) mod_top_cap();
    }
    lamp_base();
    _show("5 Mixed", 285-5*overlap);
}

if ($preview) config_soft_round();  // demo: only in GUI preview
