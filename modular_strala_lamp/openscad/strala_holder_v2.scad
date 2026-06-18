include <config.scad>
include <bayonet_v2.scad>

// ============================================================
// strala_holder_v2.scad -- top cap holding the STRALA E27 socket.
// ============================================================

module strala_holder() {
    h_body = 15;
    mount_r = strala_mount_hole_d / 2;  // 13.3mm

    difference() {
        union() {
            cylinder(h=h_body, r=bay_socket_or, $fn=96);
        }
        // Female socket cuts at bottom
        _bay_socket_cuts(bay_depth);
        // Center hole for strala thread
        translate([0,0,-EPS]) cylinder(h=h_body+2*EPS, r=mount_r, $fn=64);
        // Counterbore for shoulder (top side)
        translate([0,0,h_body-3])
            cylinder(h=3+EPS, r=strala_shoulder_d/2, $fn=64);
        // Lead-in chamfer
        translate([0,0,-EPS]) cylinder(h=2, r1=mount_r+1.5, r2=mount_r, $fn=64);
    }
    // Male spigot for shade
    translate([0,0,h_body]) bay_male_spigot(bay_depth);
}

part = "holder";
if (part=="holder") strala_holder();
