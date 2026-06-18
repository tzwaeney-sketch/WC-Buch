include <module_frame.scad>

// ============================================================
// strala_holder_v2.scad — top cap holding the STRALA E27 socket.
//   bay_female at the BOTTOM (mates topmost body module male)
//   flanged mounting plate, center hole strala_mount_hole_d
//   counterbore recess for strala_shoulder_d
//   bay_male collar at the TOP for the shade
//   60mm bore continuity for the cable
// Single watertight solid.
// ============================================================

inner_tube_r = bay_iface_r + wall_str;   // 42.52

// Z layout
fem_h    = bay_depth;          // bottom female zone
plate_z  = fem_h;              // mounting plate sits above female
plate_t  = 5;                  // mounting plate thickness
cbore_d  = strala_shoulder_d + 1.0;   // shoulder counterbore dia
cbore_t  = 2.5;                // counterbore depth (from top of plate)
collar_z = plate_z + plate_t;  // male collar base
total_h  = collar_z + bay_depth;

module strala_holder() {
    lug_z = total_h - bay_lug_h - clearance;

    difference() {
        union() {
            // bottom female interface ring
            cylinder(h=fem_h, r=bay_iface_r, $fn=96);
            // flanged mounting plate (wider flange) — SOLID, the bore
            // is interrupted here by a web that carries the socket.
            translate([0,0,plate_z])
                cylinder(h=plate_t, r=bay_iface_r + 4, $fn=96);
            // top male collar ring
            translate([0,0,collar_z])
                cylinder(h=bay_depth, r=bay_iface_r, $fn=96);
        }

        // 60mm bore through bottom female zone (cable enters from body)
        translate([0,0,-EPS]) cylinder(h=plate_z+EPS, r=bore_r, $fn=128);
        // 60mm bore through TOP collar (cable space above plate)
        translate([0,0,collar_z-EPS])
            cylinder(h=bay_depth+2*EPS, r=bore_r, $fn=128);

        // FEMALE slots at the bottom interface
        _bay_female_cuts(fem_h);

        // socket thread hole through the mounting plate (cable + thread)
        translate([0,0, plate_z-EPS])
            cylinder(h=plate_t + 2*EPS, r=strala_mount_hole_d/2, $fn=96);

        // counterbore recess for the shoulder on TOP of plate
        translate([0,0, plate_z + plate_t - cbore_t])
            cylinder(h=cbore_t + EPS, r=cbore_d/2, $fn=96);
    }

    // top MALE lugs
    for (i = [0:bay_n-1])
        rotate([0,0, i*(360/bay_n)])
            translate([0,0, lug_z])
                bay_lug();
}

part = "holder";
if (part == "holder") strala_holder();
