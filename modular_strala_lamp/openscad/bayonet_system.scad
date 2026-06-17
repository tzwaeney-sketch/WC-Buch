// =====================================================================
// bayonet_system.scad - Twist-lock bayonet interface
// =====================================================================
// The bayonet joins modules. The clear bore (final_plug_passage = 55mm)
// is NEVER obstructed. Lugs live in the wall ring between
// bayonet_inner_diameter and bayonet_interface_outer_diameter.
// =====================================================================
include <config.scad>;

// Helper: a rounded-profile lug block placed at the wall radius.
module _bayonet_lug(mid_radius, lug_h, lug_radial, lug_ang) {
    // A lug spanning lug_ang degrees, lug_h tall, projecting lug_radial.
    rotate_extrude(angle = lug_ang, $fn = fn_large_bore)
        translate([mid_radius, 0, 0])
            offset(r = 0.8) offset(delta = -0.8)   // round the corners
                square([lug_radial, lug_h], center = false);
}

// ---------------------------------------------------------------------
// MALE bayonet: lugs project OUTWARD from the interface wall.
// inner_d : clear bore (>= final_plug_passage)
// outer_d : outer diameter of the interface collar
// ---------------------------------------------------------------------
module bayonet_male(h = bayonet_working_depth, inner_d = bayonet_inner_diameter,
                    outer_d = bayonet_interface_outer_diameter) {
    bore = max(inner_d, final_plug_passage);
    // The male collar slides INSIDE the female; reduce its outer size by
    // radial clearance.
    collar_outer = outer_d - 2 * bayonet_radial_clearance;
    lug_mid_r = bore/2 + (collar_outer/2 - bore/2) * 0.5;
    lug_radial = bayonet_lug_radial_depth;

    difference() {
        union() {
            // Collar tube
            difference() {
                cylinder(h = h, d = collar_outer, $fn = fn_large_bore);
                translate([0, 0, -1])
                    cylinder(h = h + 2, d = bore, $fn = fn_large_bore);
            }
            // Lead-in chamfer at top of collar (helps insertion)
            translate([0, 0, h - 1.2])
                difference() {
                    cylinder(h = 1.2, d1 = collar_outer,
                             d2 = collar_outer - 2.0, $fn = fn_large_bore);
                    translate([0,0,-1])
                        cylinder(h = 3, d = bore, $fn = fn_large_bore);
                }
            // Three lugs near the top of the collar
            for (i = [0 : bayonet_lug_count - 1]) {
                rotate([0, 0, i * 360 / bayonet_lug_count])
                    translate([0, 0, h - 2.6])
                        _bayonet_lug(lug_mid_r + lug_radial/2, 1.6,
                                     lug_radial, bayonet_lug_angular_width);
            }
        }
        // Inner chamfer (smooth lead at the bore mouth)
        _inner_chamfer(bore, h);
    }
}

// ---------------------------------------------------------------------
// FEMALE bayonet: receiving cup with L-shaped slots for the lugs.
// ---------------------------------------------------------------------
module bayonet_female(h = bayonet_working_depth + 2, inner_d = bayonet_inner_diameter,
                      outer_d = bayonet_interface_outer_diameter) {
    bore = max(inner_d, final_plug_passage);
    cup_outer = outer_d + 2 * bayonet_outer_wall;
    // Inner cavity that accepts the male collar (with clearance):
    cavity_d = outer_d;
    lug_mid_r = bore/2 + (cavity_d/2 - bore/2) * 0.5;
    slot_radial = bayonet_lug_radial_depth + bayonet_radial_clearance;

    difference() {
        // Outer body
        cylinder(h = h, d = cup_outer, $fn = fn_large_bore);

        // Clear bore through everything
        translate([0, 0, -1])
            cylinder(h = h + 2, d = bore, $fn = fn_large_bore);

        // Receiving cavity for collar (open at the bottom face, z=0)
        translate([0, 0, -1])
            cylinder(h = bayonet_working_depth + 1 + bayonet_axial_clearance,
                     d = cavity_d, $fn = fn_large_bore);

        // L-shaped slots: axial entry + circumferential lock channel
        for (i = [0 : bayonet_lug_count - 1]) {
            rotate([0, 0, i * 360 / bayonet_lug_count]) {
                // Axial entry slot (from bottom face upward)
                translate([0, 0, -1])
                    _bayonet_lug(lug_mid_r, 2.2 + 1,
                                 slot_radial + 0.5, bayonet_lug_angular_width + 4);
                // Circumferential lock channel
                translate([0, 0, bayonet_working_depth - 2.6])
                    rotate([0, 0, -bayonet_lock_angle])
                        _bayonet_lug(lug_mid_r, 2.0,
                                     slot_radial + 0.5,
                                     bayonet_lug_angular_width + bayonet_lock_angle + 4);
            }
        }
        // Inner chamfer at bore mouth (top and bottom)
        _inner_chamfer(bore, h);
        translate([0, 0, h]) mirror([0,0,1]) _inner_chamfer(bore, h);
    }
}

// Inner edge chamfer cutter at z = 0 face, pointing into the part.
module _inner_chamfer(bore, h) {
    translate([0, 0, -0.01])
        rotate_extrude($fn = fn_large_bore)
            polygon(points = [
                [bore/2 - 0.01, -0.01],
                [bore/2 + inner_chamfer, -0.01],
                [bore/2 - 0.01, inner_chamfer]
            ]);
}

// ---------------------------------------------------------------------
// Passage ring: a simple test ring exposing both interfaces.
// Female at bottom, male at top, smooth 55mm bore between.
// ---------------------------------------------------------------------
module bayonet_passage_ring() {
    fh = bayonet_working_depth + 2;
    body_h = 12;
    bore = final_plug_passage;
    union() {
        bayonet_female(h = fh);
        translate([0, 0, fh])
            difference() {
                cylinder(h = body_h, d = bayonet_interface_outer_diameter
                         + 2 * bayonet_outer_wall, $fn = fn_large_bore);
                translate([0,0,-1])
                    cylinder(h = body_h + 2, d = bore, $fn = fn_large_bore);
            }
        translate([0, 0, fh + body_h])
            bayonet_male(h = bayonet_working_depth);
    }
}

// ---------------------------------------------------------------------
// Cross section: cutaway of the passage ring for inspection.
// ---------------------------------------------------------------------
module bayonet_cross_section() {
    difference() {
        bayonet_passage_ring();
        translate([0, -100, -10])
            cube([100, 200, 200]);   // cut away +X half
    }
}

// Quick preview
// bayonet_passage_ring();
