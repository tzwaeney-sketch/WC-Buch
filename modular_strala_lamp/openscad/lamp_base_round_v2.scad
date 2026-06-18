include <config.scad>
include <bayonet_v2.scad>

// ============================================================
// lamp_base_round_v2.scad -- round lamp base
// ============================================================

foot_r       = 6;
foot_depth   = 3;
foot_radius  = 90;
inner_tube_r = bay_socket_or;   // 43mm

module lamp_base_round() {
    or = base_d/2;          // 110

    difference() {
        union() {
            cylinder(h=base_h, r=or, $fn=128);
            cylinder(h=base_h, r=inner_tube_r, $fn=96);
        }

        // 60mm through bore + chamfers
        _bore_cuts(base_h);

        // Hollow interior (open at bottom -- no enclosed void)
        translate([0,0, base_bot])
            cylinder(h=base_h, r=or - wall_str, $fn=128);

        // Cable exit: radial groove in the BOTTOM face only
        translate([-EPS, -(strala_cable_d/2 + 1), -EPS])
            cube([or + 2*EPS, strala_cable_d + 2, base_bot + EPS]);

        // 4 rubber foot pockets on the bottom
        for (i = [0:3])
            rotate([0,0, i*90])
                translate([foot_radius, 0, -EPS])
                    cylinder(h=foot_depth + EPS, r=foot_r, $fn=48);
    }

    // Male spigot on TOP: protrudes above base
    translate([0,0, base_h]) bay_male_spigot(bay_depth);
}

part = "round";
if (part == "round") lamp_base_round();
