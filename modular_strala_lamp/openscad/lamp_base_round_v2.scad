include <module_frame.scad>

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

        _bore_cuts(base_h);

        // Weight chamber
        translate([0,0, base_bot])
            difference() {
                cylinder(h=base_h - base_bot - 4, r=or - wall_str, $fn=128);
                translate([0,0,-EPS])
                    cylinder(h=base_h, r=inner_tube_r + 1.5, $fn=96);
            }

        // Cable exit: radial groove in BOTTOM face only
        translate([-EPS, -(strala_cable_d/2 + 1), -EPS])
            cube([or + 2*EPS, strala_cable_d + 2, base_bot + EPS]);

        // 4 rubber foot pockets
        for (i = [0:3])
            rotate([0,0, i*90])
                translate([foot_radius, 0, -EPS])
                    cylinder(h=foot_depth + EPS, r=foot_r, $fn=48);
    }

    // Male spigot protrudes above top
    translate([0,0, base_h]) bay_male_spigot(bay_depth);
}

part = "round";
if (part == "round") lamp_base_round();
