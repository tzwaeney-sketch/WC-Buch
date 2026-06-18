include <module_frame.scad>

// ============================================================
// lamp_base_design_v2.scad — stepped (3-step) lamp base
// Same interfaces as round base: 60mm bore, bay_male on top,
// feet, cable trough, weight chamber. Exterior = 3 stacked
// cylinders 220 -> 180 -> 140. Single watertight solid.
// ============================================================

foot_r       = 6;
foot_depth   = 3;
foot_radius  = 90;
trough_w     = 7;
inner_tube_r = bay_iface_r + wall_str;   // 42.52

module lamp_base_design() {
    h3 = base_h/3;
    d0 = 220; d1 = 180; d2 = 140;
    lug_z = base_h - bay_lug_h - clearance;

    difference() {
        union() {
            // 3 stacked steps (EPS overlap to fuse)
            cylinder(h=h3 + EPS,      r=d0/2, $fn=128);
            translate([0,0,h3])     cylinder(h=h3 + EPS, r=d1/2, $fn=128);
            translate([0,0,2*h3])   cylinder(h=base_h-2*h3, r=d2/2, $fn=128);
            // male bayonet ring at top
            translate([0,0, base_h - bay_depth])
                cylinder(h=bay_depth, r=bay_iface_r, $fn=96);
            cylinder(h=base_h, r=inner_tube_r, $fn=96);
        }

        _bore_cuts(base_h);

        // Weight chamber (annular cavity from bottom)
        translate([0,0, base_bot])
            difference() {
                cylinder(h=base_h - base_bot - 4, r=d2/2 - wall_str, $fn=128);
                translate([0,0,-EPS])
                    cylinder(h=base_h, r=inner_tube_r + 1.5, $fn=96);
            }

        // Cable exit: radial groove in the BOTTOM face only.
        // Cable runs down through the 60mm bore and exits laterally
        // at the base of the foot. Groove width = cable dia + 2mm
        // clearance, depth = base_bot (5mm) — top stays closed.
        translate([-EPS, -(strala_cable_d/2 + 1), -EPS])
            cube([d0/2 + 2*EPS, strala_cable_d + 2, base_bot + EPS]);

        // foot pockets
        for (i = [0:3])
            rotate([0,0, i*90])
                translate([foot_radius, 0, -EPS])
                    cylinder(h=foot_depth + EPS, r=foot_r, $fn=48);
    }

    for (i = [0:bay_n-1])
        rotate([0,0, i*(360/bay_n)])
            translate([0,0, lug_z])
                bay_lug();
}

part = "design";
if (part == "design") lamp_base_design();
