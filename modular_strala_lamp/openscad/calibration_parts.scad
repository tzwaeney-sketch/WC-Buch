// =====================================================================
// calibration_parts.scad - Print-first calibration & gauge parts
// =====================================================================
include <config.scad>;
include <bayonet_system.scad>;

// ---------------------------------------------------------------------
// Single gauge ring with labelled bore.
// ---------------------------------------------------------------------
module plug_gauge_ring(test_diameter = 55) {
    h = 12;
    wall = structural_wall;
    difference() {
        cylinder(h = h, d = test_diameter + 2 * wall + 6, $fn = fn_large_bore);
        translate([0, 0, -1])
            cylinder(h = h + 2, d = test_diameter, $fn = fn_large_bore);
        // Engrave the diameter on top
        translate([0, test_diameter/2 + 1, h - 0.8])
            linear_extrude(1.0)
                text(str(test_diameter), size = 5, halign = "center", valign = "center");
    }
}

// ---------------------------------------------------------------------
// Full gauge set: 44,46,48,50,52,55,58mm laid out in a row.
// ---------------------------------------------------------------------
module plug_gauge_set() {
    dias = [44, 46, 48, 50, 52, 55, 58];
    pitch = 70;
    for (i = [0 : len(dias) - 1])
        translate([i * pitch, 0, 0])
            plug_gauge_ring(dias[i]);
}

// ---------------------------------------------------------------------
// Passage test ring: 20mm tall, exact module inner geometry, 55mm bore.
// ---------------------------------------------------------------------
module passage_test_ring_55mm() {
    h = 20;
    bore = final_plug_passage;
    difference() {
        cylinder(h = h, d = bore + 2 * passage_wall, $fn = fn_large_bore);
        translate([0, 0, -1])
            cylinder(h = h + 2, d = bore, $fn = fn_large_bore);
        // 2mm chamfers both ends
        for (z = [0, h])
            translate([0, 0, z])
                rotate_extrude($fn = fn_large_bore)
                    translate([bore/2, 0])
                        polygon([[0,0],[inner_chamfer,0],[0,(z==0?1:-1)*inner_chamfer]]);
    }
}

// ---------------------------------------------------------------------
// Bayonet tolerance test pair at a given radial clearance.
// (Overrides global clearance locally via re-definition is not possible;
//  instead we scale the female cavity by the requested clearance.)
// ---------------------------------------------------------------------
module bayonet_tolerance_test(clearance = 0.30) {
    // Male
    bayonet_male(h = bayonet_working_depth);
    // Female, shifted aside, cavity widened by (clearance - default)
    delta = clearance - bayonet_radial_clearance;
    translate([bayonet_interface_outer_diameter + 30, 0, 0])
        difference() {
            bayonet_female(h = bayonet_working_depth + 2);
            // Extra cavity widening
            translate([0, 0, -1])
                cylinder(h = bayonet_working_depth + 1,
                         d = bayonet_interface_outer_diameter + 2 * delta,
                         $fn = fn_large_bore);
        }
    // Label
    translate([bayonet_interface_outer_diameter/2 + 10, -45, 0])
        linear_extrude(1.0) text(str(clearance), size = 6, halign = "center");
}

// ---------------------------------------------------------------------
// All 5 clearances in a row: 0.20,0.25,0.30,0.35,0.40mm.
// ---------------------------------------------------------------------
module bayonet_tolerance_set() {
    cls = [0.20, 0.25, 0.30, 0.35, 0.40];
    pitch = bayonet_interface_outer_diameter * 2 + 80;
    for (i = [0 : len(cls) - 1])
        translate([0, i * pitch, 0])
            bayonet_tolerance_test(cls[i]);
}

// ---------------------------------------------------------------------
// STRALA fit test ring (short, minimal material).
// ---------------------------------------------------------------------
module strala_fit_test_ring() {
    socket_d = strala_socket_outer_diameter;  // MEASURE
    h = 10;
    difference() {
        cylinder(h = h, d = socket_d + 2 * minimum_wall, $fn = 64);
        translate([0, 0, -1])
            cylinder(h = h + 2, d = socket_d + general_clearance, $fn = 64);
    }
}

// ---------------------------------------------------------------------
// Cable exit test: several exit-bore sizes.
// ---------------------------------------------------------------------
module cable_exit_test() {
    dias = [6, 7, 8, 9, 10];
    pitch = 22;
    for (i = [0 : len(dias) - 1])
        translate([i * pitch, 0, 0])
            difference() {
                cylinder(h = 14, d = dias[i] + 2 * minimum_wall, $fn = 40);
                translate([0, 0, -1])
                    cylinder(h = 16, d = dias[i] + general_clearance, $fn = 40);
                translate([0, dias[i]/2, 13])
                    linear_extrude(1) text(str(dias[i]), size = 3, halign="center");
            }
}

// ---------------------------------------------------------------------
// Shade wall thickness test: 0.8,1.0,1.2,1.6,2.0mm.
// ---------------------------------------------------------------------
module shade_wall_test() {
    walls = [0.8, 1.0, 1.2, 1.6, 2.0];
    pitch = 26;
    h = 30;
    for (i = [0 : len(walls) - 1])
        translate([i * pitch, 0, 0])
            difference() {
                cylinder(h = h, d = 20, $fn = 64);
                translate([0, 0, -1])
                    cylinder(h = h + 2, d = 20 - 2 * walls[i], $fn = 64);
                translate([0, 10, h - 1])
                    linear_extrude(1) text(str(walls[i]), size = 3, halign="center");
            }
}
