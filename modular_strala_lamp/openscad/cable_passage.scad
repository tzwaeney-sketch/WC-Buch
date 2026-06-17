// =====================================================================
// cable_passage.scad - Cable channels, plug test bodies, exit fittings
// =====================================================================
include <config.scad>

// ---------------------------------------------------------------------
// Smooth internal cable/plug guide channel of given length.
// Bore is always >= final_plug_passage. Walls = structural_wall.
// ---------------------------------------------------------------------
module cable_guide_channel(length = 40) {
    bore = final_plug_passage;
    difference() {
        cylinder(h = length, d = bore + 2 * structural_wall, $fn = fn_large_bore);
        translate([0, 0, -1])
            cylinder(h = length + 2, d = bore, $fn = fn_large_bore);
        // Chamfer both mouths for snag-free passage
        for (z = [0, length])
            translate([0, 0, z])
                rotate_extrude($fn = fn_large_bore)
                    translate([bore/2, 0])
                        polygon([[0,0],[inner_chamfer, 0],[0, (z==0?1:-1)*inner_chamfer]]);
    }
}

// ---------------------------------------------------------------------
// Solid test plug at real Schuko plug dimensions. Use for collision
// checks: import a module, subtract this, confirm it passes through.
// Rounded box approximating the Schuko body + a cylindrical pin region.
// ---------------------------------------------------------------------
module plug_test_body() {
    r = 6;
    // Main body
    hull() {
        for (x = [-1, 1], y = [-1, 1])
            translate([x * (actual_plug_width/2 - r),
                       y * (actual_plug_height/2 - r), 0])
                cylinder(h = actual_plug_length * 0.55, r = r, $fn = 32);
    }
    // Pin region (narrower cylindrical nose)
    translate([0, 0, actual_plug_length * 0.55])
        cylinder(h = actual_plug_length * 0.45, d = 28, $fn = 48);
}

// ---------------------------------------------------------------------
// Plug clearance test body: a plain 55mm x 115mm cylinder. If a part
// can have this pushed straight through, the clearance is verified.
// ---------------------------------------------------------------------
module plug_clearance_test_body() {
    color("red", 0.4)
        cylinder(h = 115, d = plug_clear_passage_diameter, $fn = fn_large_bore);
}

// ---------------------------------------------------------------------
// Side cable exit fitting. Tube with smooth bore for the cable to leave
// the base sideways. cable_d is the cable diameter; bore adds clearance.
// ---------------------------------------------------------------------
module cable_exit_fitting(cable_d = 8) {
    bore = cable_d + general_clearance * 2;
    len = 18;
    difference() {
        union() {
            cylinder(h = len, d = bore + 2 * structural_wall, $fn = 48);
            // Flared mouth
            translate([0, 0, len - 3])
                cylinder(h = 3, d1 = bore + 2 * structural_wall,
                         d2 = bore + 2 * structural_wall + 4, $fn = 48);
        }
        translate([0, 0, -1])
            cylinder(h = len + 5, d = bore, $fn = 48);
        // Rounded internal lip to avoid cable chafing
        translate([0, 0, len])
            rotate_extrude($fn = 48)
                translate([bore/2, 0]) circle(r = 1.2, $fn = 24);
    }
}
