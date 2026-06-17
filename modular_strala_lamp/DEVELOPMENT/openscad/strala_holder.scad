include <config.scad>

EPS = 0.01;

// ============================================================
// SPLIT CLAMP ADAPTER FOR IKEA STRÅLA
// Two half-shells that clamp around the STRÅLA socket body.
// All STRÅLA dimensions marked MEASURE in config.scad.
// ============================================================

clamp_od    = strala_socket_outer_diameter + 6; // MEASURE dependent
clamp_id    = strala_socket_outer_diameter;      // MEASURE
clamp_h     = 25;

module strala_split_clamp_half(side = "left") {
    clamp_r  = clamp_od / 2;
    socket_r = clamp_id / 2;
    clip = side == "left" ? 1 : -1;

    intersection() {
        difference() {
            cylinder(h=clamp_h, r=clamp_r, $fn=64);
            translate([0,0,-EPS])
                cylinder(h=clamp_h+2*EPS, r=socket_r + general_clearance, $fn=64);
            for(z=[clamp_h*0.3, clamp_h*0.7]) {
                translate([0, -clamp_r-EPS, z])
                    rotate([-90,0,0])
                        cylinder(h=clamp_od+2*EPS, r=1.6, $fn=16);
            }
            translate([0, socket_r, clamp_h/2 - 1])
                cube([4, 3, 2], center=true);
        }
        translate([0, clip > 0 ? -EPS : -(clamp_od+2)+EPS, -EPS])
            cube([clamp_od+2, clamp_od+2, clamp_h+2], center=false);
    }
}

module strala_split_clamp_left() {
    strala_split_clamp_half("left");
}

module strala_split_clamp_right() {
    strala_split_clamp_half("right");
}

// Fit test ring set (print first to check STRÅLA socket diameter)
module strala_fit_test() {
    for(i=[0:4]) {
        d = strala_socket_outer_diameter + i * 0.5;
        translate([i * 20, 0, 0]) {
            difference() {
                cylinder(h=8, r=d/2 + 3, $fn=32);
                translate([0,0,-EPS])
                    cylinder(h=10, r=d/2 + general_clearance, $fn=32);
            }
            translate([0, d/2+4, 0])
                linear_extrude(height=1)
                    text(str("+", i*0.5), size=2.5, halign="center");
        }
    }
}

if ($preview) strala_fit_test();  // demo: only in GUI preview, skipped on STL export
