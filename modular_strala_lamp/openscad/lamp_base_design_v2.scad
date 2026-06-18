include <config.scad>
include <bayonet_v2.scad>

// ============================================================
// lamp_base_design_v2.scad -- stepped (3-step) lamp base
// ============================================================

foot_r       = 6;
foot_depth   = 3;
foot_radius  = 90;
inner_tube_r = bay_socket_or;   // 43mm

module lamp_base_design() {
    h3 = base_h/3;
    d0 = 220; d1 = 180; d2 = 140;

    difference() {
        union() {
            cylinder(h=h3 + EPS,      r=d0/2, $fn=128);
            translate([0,0,h3])     cylinder(h=h3 + EPS, r=d1/2, $fn=128);
            translate([0,0,2*h3])   cylinder(h=base_h-2*h3, r=d2/2, $fn=128);
            cylinder(h=base_h, r=inner_tube_r, $fn=96);
        }

        _bore_cuts(base_h);

        // Weight chamber
        translate([0,0, base_bot])
            difference() {
                cylinder(h=base_h - base_bot - 4, r=d2/2 - wall_str, $fn=128);
                translate([0,0,-EPS])
                    cylinder(h=base_h, r=inner_tube_r + 1.5, $fn=96);
            }

        // Cable exit trough
        translate([-EPS, -(strala_cable_d/2 + 1), -EPS])
            cube([d0/2 + 2*EPS, strala_cable_d + 2, base_bot + EPS]);

        // foot pockets
        for (i = [0:3])
            rotate([0,0, i*90])
                translate([foot_radius, 0, -EPS])
                    cylinder(h=foot_depth + EPS, r=foot_r, $fn=48);
    }

    // Male spigot on TOP
    translate([0,0, base_h]) bay_male_spigot(bay_depth);
}

part = "design";
if (part == "design") lamp_base_design();
