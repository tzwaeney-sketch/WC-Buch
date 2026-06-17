// =====================================================================
// strala_holder.scad - Adapters for IKEA STRALA socket/shade hardware
// =====================================================================
// All STRALA dimensions are PLACEHOLDERS marked // MEASURE.
// Re-measure your specific STRALA part and update config.scad before
// printing the final adapters. Use the test/measurement modules first.
// =====================================================================
include <config.scad>;
include <bayonet_system.scad>;

// ---------------------------------------------------------------------
// Clamp adapter: a split ring that grips the STRALA socket body.
// ---------------------------------------------------------------------
module strala_clamp_adapter() {
    grip_d = strala_socket_outer_diameter;          // MEASURE
    len    = strala_socket_total_length * 0.6;
    wall   = structural_wall;
    difference() {
        cylinder(h = len, d = grip_d + 2 * wall, $fn = 64);
        // Gripping bore (slight interference, +clearance)
        translate([0, 0, -1])
            cylinder(h = len + 2, d = grip_d + general_clearance, $fn = 64);
        // Split slot so the clamp can flex
        translate([-1, 0, -1]) cube([2, grip_d, len + 2]);
        // Two M3 clamp-screw holes across the slot
        for (z = [len * 0.3, len * 0.7])
            translate([0, grip_d/2 + wall, z])
                rotate([90, 0, 0]) cylinder(h = grip_d + 2*wall + 2, d = 3.2, $fn = 24);
    }
}

// ---------------------------------------------------------------------
// Shade ring adapter: slides over the STRALA shade mounting ring.
// ---------------------------------------------------------------------
module strala_shade_ring_adapter() {
    ring_od = strala_shade_ring_outer_diameter;     // MEASURE
    ring_id = strala_shade_ring_inner_diameter;     // MEASURE
    len = 14;
    wall = structural_wall;
    difference() {
        cylinder(h = len, d = ring_od + 2 * wall, $fn = 64);
        // Recess that captures the shade ring
        translate([0, 0, 2])
            cylinder(h = len, d = ring_od + general_clearance, $fn = 64);
        // Through passage (keeps cable/socket clear)
        translate([0, 0, -1])
            cylinder(h = len + 2, d = ring_id - 2 * wall, $fn = 64);
    }
}

// ---------------------------------------------------------------------
// Top cap: female bayonet below to join the module stack, STRALA socket
// holder above. This is the terminal piece of every lamp configuration.
// ---------------------------------------------------------------------
module strala_top_cap() {
    fh = bayonet_working_depth + 2;
    deck = base_wall;
    holder_len = strala_socket_total_length;        // MEASURE
    thread_d = strala_thread_outer_diameter;        // MEASURE
    socket_d = strala_socket_outer_diameter;        // MEASURE
    bore = final_plug_passage;

    union() {
        // Female bayonet to receive the module below
        bayonet_female(h = fh);
        // Transition deck (still keeps the 55mm bore clear!)
        translate([0, 0, fh])
            difference() {
                cylinder(h = deck, d = bayonet_interface_outer_diameter
                         + 2 * bayonet_outer_wall, $fn = fn_large_bore);
                translate([0, 0, -1])
                    cylinder(h = deck + 2, d = bore, $fn = fn_large_bore);
            }
        // STRALA socket holder tube above
        translate([0, 0, fh + deck])
            difference() {
                cylinder(h = holder_len, d = socket_d + 2 * structural_wall, $fn = 64);
                // Socket bore (MEASURE)
                translate([0, 0, -1])
                    cylinder(h = holder_len + 2, d = socket_d + general_clearance, $fn = 64);
                // Thread relief at top (MEASURE)
                translate([0, 0, holder_len - strala_thread_length])
                    cylinder(h = strala_thread_length + 1, d = thread_d + general_clearance, $fn = 64);
                // Cable side-entry near base of holder (MEASURE cable dia)
                translate([0, socket_d/2, holder_len * 0.25])
                    rotate([90, 0, 0])
                        cylinder(h = socket_d + 4,
                                 d = strala_cable_diameter + general_clearance, $fn = 32);
            }
    }
}

// ---------------------------------------------------------------------
// Test adapter: minimal short ring for fit testing the STRALA socket.
// ---------------------------------------------------------------------
module strala_test_adapter() {
    socket_d = strala_socket_outer_diameter;        // MEASURE
    len = 12;
    difference() {
        cylinder(h = len, d = socket_d + 2 * minimum_wall, $fn = 64);
        translate([0, 0, -1])
            cylinder(h = len + 2, d = socket_d + general_clearance, $fn = 64);
    }
}

// ---------------------------------------------------------------------
// Measurement guide: a flat plate carrying labelled dimension arrows so
// you know exactly which value to capture. Rendered as engraved text.
// ---------------------------------------------------------------------
module strala_measurement_guide() {
    difference() {
        cube([120, 90, 3], center = true);
        for (i = [0:6]) {
            txt = [
                "socket_outer_diameter",
                "socket_total_length",
                "shade_ring_outer_diameter",
                "shade_ring_inner_diameter",
                "thread_outer_diameter",
                "thread_length",
                "cable_diameter"
            ][i];
            translate([-55, 35 - i * 11, 1.0])
                linear_extrude(1.2)
                    text(str("[MEASURE] ", txt), size = 3.2, font = "Liberation Sans");
        }
    }
}

// Preview
// strala_top_cap();
