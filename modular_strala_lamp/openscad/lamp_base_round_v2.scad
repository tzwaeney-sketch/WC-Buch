include <module_frame.scad>

// ============================================================
// lamp_base_round_v2.scad — round lamp base
// Outer dia base_d=220, height base_h=45.
// Through 60mm bore, bay_male on top, cable trough, weight
// chamber, 4 rubber foot pockets. Single watertight solid.
// ============================================================

foot_r       = 6;     // foot pocket radius (dia 12)
foot_depth   = 3;
foot_radius  = 90;    // placement radius
trough_w     = 7;     // cable trough width
inner_tube_r = bay_iface_r + wall_str;   // 42.52

module lamp_base_round() {
    or = base_d/2;          // 110
    lug_z = base_h - bay_lug_h - clearance;

    difference() {
        union() {
            // main body
            cylinder(h=base_h, r=or, $fn=128);
            // solid male bayonet ring at top (cuts share difference)
            translate([0,0, base_h - bay_depth])
                cylinder(h=bay_depth, r=bay_iface_r, $fn=96);
            // structural tube around bore (already inside body, harmless)
            cylinder(h=base_h, r=inner_tube_r, $fn=96);
        }

        // 60mm through bore + chamfers
        _bore_cuts(base_h);

        // Weight chamber: annular cavity in the base body, hollowed
        // from the bottom, leaving base_bot floor and outer/inner walls.
        translate([0,0, base_bot])
            difference() {
                cylinder(h=base_h - base_bot - 4, r=or - wall_str, $fn=128);
                // keep clear of bore tube
                translate([0,0,-EPS])
                    cylinder(h=base_h, r=inner_tube_r + 1.5, $fn=96);
            }

        // Cable trough: open vertical slot through the side wall,
        // connecting outer surface to the bore region. Above the
        // weight chamber floor so it stays a clean channel.
        translate([0,0, base_bot + 6])
            translate([0, -trough_w/2, 0])
                cube([or + EPS, trough_w, base_h]);

        // 4 rubber foot pockets on the bottom
        for (i = [0:3])
            rotate([0,0, i*90])
                translate([foot_radius, 0, -EPS])
                    cylinder(h=foot_depth + EPS, r=foot_r, $fn=48);
    }

    // MALE lugs on top (solid, sit in the ring wall)
    for (i = [0:bay_n-1])
        rotate([0,0, i*(360/bay_n)])
            translate([0,0, lug_z])
                bay_lug();
}

part = "round";
if (part == "round") lamp_base_round();
