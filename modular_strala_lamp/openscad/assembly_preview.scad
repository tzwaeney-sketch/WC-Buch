// =====================================================================
// assembly_preview.scad - Stacked configuration previews
// =====================================================================
include <config.scad>;
include <bayonet_system.scad>;
include <cable_passage.scad>;
include <lamp_base.scad>;
include <strala_holder.scad>;
include <round_modules.scad>;
include <geometric_modules.scad>;
include <organic_modules.scad>;
include <lamp_shades.scad>;

// Each module overlaps the previous by bayonet_working_depth when stacked.
overlap = bayonet_working_depth;

// Optional translucent 55mm clearance rod down the centre.
module _clearance_overlay(total_h) {
    if (show_plug_clearance_test)
        color("red", 0.35)
            cylinder(h = total_h + 20, d = plug_clear_passage_diameter, $fn = fn_large_bore);
}

// ---------------------------------------------------------------------
// Soft round configuration: base + sphere + disc + ring + ribbed shade.
// ---------------------------------------------------------------------
module config_soft_round() {
    z = 0;
    lamp_base();
    z1 = base_total_height + bayonet_working_depth - overlap;
    translate([0, 0, z1]) mod_sphere();
    z2 = z1 + (bayonet_working_depth + 2 + 70 + bayonet_working_depth) - overlap;
    translate([0, 0, z2]) mod_disc();
    z3 = z2 + (bayonet_working_depth + 2 + 35 + bayonet_working_depth) - overlap;
    translate([0, 0, z3]) mod_ring_module();
    z4 = z3 + (bayonet_working_depth + 2 + 40 + bayonet_working_depth) - overlap;
    translate([0, 0, z4]) shade_vertical_ribs();
    total = z4 + 14 + shade_height;
    echo(str("config_soft_round total height ~ ", total, " mm, parts = 6 (base, sphere, disc, ring, shade, +feet)"));
    _clearance_overlay(total);
}

// ---------------------------------------------------------------------
// Geometric configuration: base + cube + diamond + hex + faceted shade.
// ---------------------------------------------------------------------
module config_geometric() {
    lamp_base();
    z1 = base_total_height + bayonet_working_depth - overlap;
    translate([0, 0, z1]) mod_cube_rounded();
    z2 = z1 + (bayonet_working_depth + 2 + 70 + bayonet_working_depth) - overlap;
    translate([0, 0, z2]) mod_diamond_faceted();
    z3 = z2 + (bayonet_working_depth + 2 + 80 + bayonet_working_depth) - overlap;
    translate([0, 0, z3]) mod_hexagon();
    z4 = z3 + (bayonet_working_depth + 2 + 65 + bayonet_working_depth) - overlap;
    translate([0, 0, z4]) shade_faceted();
    total = z4 + 14 + shade_height;
    echo(str("config_geometric total height ~ ", total, " mm, parts = 5"));
    _clearance_overlay(total);
}

// ---------------------------------------------------------------------
// Minimal: short base + one large sphere + cylinder shade.
// ---------------------------------------------------------------------
module config_minimal() {
    lamp_base();
    z1 = base_total_height + bayonet_working_depth - overlap;
    translate([0, 0, z1]) mod_sphere(scale_z = 1.2);
    z2 = z1 + (bayonet_working_depth + 2 + 70*1.2 + bayonet_working_depth) - overlap;
    translate([0, 0, z2]) shade_cylinder();
    total = z2 + 14 + shade_height;
    echo(str("config_minimal total height ~ ", total, " mm, parts = 3"));
    _clearance_overlay(total);
}

// ---------------------------------------------------------------------
// Organic: base + teardrop + vase + mushroom shade.
// ---------------------------------------------------------------------
module config_organic() {
    lamp_base();
    z1 = base_total_height + bayonet_working_depth - overlap;
    translate([0, 0, z1]) mod_teardrop();
    z2 = z1 + (bayonet_working_depth + 2 + 75 + bayonet_working_depth) - overlap;
    translate([0, 0, z2]) mod_vase();
    z3 = z2 + (bayonet_working_depth + 2 + 85 + bayonet_working_depth) - overlap;
    translate([0, 0, z3]) shade_mushroom();
    total = z3 + 14 + shade_bottom_diameter * 0.55;
    echo(str("config_organic total height ~ ", total, " mm, parts = 4"));
    _clearance_overlay(total);
}

// ---------------------------------------------------------------------
// Mixed: base + sphere + cube + frustum + bell shade.
// ---------------------------------------------------------------------
module config_mixed() {
    lamp_base();
    z1 = base_total_height + bayonet_working_depth - overlap;
    translate([0, 0, z1]) mod_sphere();
    z2 = z1 + (bayonet_working_depth + 2 + 70 + bayonet_working_depth) - overlap;
    translate([0, 0, z2]) mod_cube_rounded();
    z3 = z2 + (bayonet_working_depth + 2 + 70 + bayonet_working_depth) - overlap;
    translate([0, 0, z3]) mod_frustum();
    z4 = z3 + (bayonet_working_depth + 2 + 60 + bayonet_working_depth) - overlap;
    translate([0, 0, z4]) shade_bell();
    total = z4 + 14 + shade_height;
    echo(str("config_mixed total height ~ ", total, " mm, parts = 5"));
    _clearance_overlay(total);
}

// Default render
config_soft_round();
