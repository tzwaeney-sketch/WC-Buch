include <config.scad>
include <bayonet_system.scad>

EPS = 0.01;

// --- Passage test ring (55/58/60/62), self-contained ---
module passage_test_ring(d=60, h=20) {
    bore_r = d/2;
    outer_r = bore_r + structural_wall + 2;
    difference() {
        cylinder(h=h, r=outer_r, $fn=128);
        translate([0,0,-EPS]) cylinder(h=h+2*EPS, r=bore_r, $fn=128);
        translate([0,0,-EPS]) cylinder(h=3, r1=bore_r+3, r2=bore_r, $fn=64);
        translate([0,0,h-3]) cylinder(h=3+EPS, r1=bore_r, r2=bore_r+3, $fn=64);
    }
    translate([0, outer_r - 1, 1])
        rotate([90,0,0]) linear_extrude(1.2)
            text(str(d, "mm"), size=5, halign="center");
}

// --- Long tunnel: 60mm bore, 65mm long ---
module long_tunnel_test() {
    bore_r = final_plug_passage/2;
    outer_r = bore_r + structural_wall + 2;
    h = 65;
    difference() {
        cylinder(h=h, r=outer_r, $fn=128);
        translate([0,0,-EPS]) cylinder(h=h+2*EPS, r=bore_r, $fn=128);
        translate([0,0,-EPS]) cylinder(h=3, r1=bore_r+3, r2=bore_r, $fn=64);
        translate([0,0,h-3]) cylinder(h=3+EPS, r1=bore_r, r2=bore_r+3, $fn=64);
    }
    translate([0, outer_r-1, 1]) rotate([90,0,0])
        linear_extrude(1.2) text("60x65", size=5, halign="center");
}

// --- Bayonet snap test (female + matching male, short) ---
module bayonet_snap_test() {
    bayonet_female(h_total=bayonet_working_depth+2);
    translate([bayonet_interface_outer_radius*2+5,0,0])
        bayonet_male(h_total=bayonet_working_depth+2);
}

// --- Shade wall thickness test (5 thicknesses) ---
module shade_wall_test() {
    // Connecting raft makes the 5 tubes one manifold body.
    // Bores pass fully through the raft -> clean single solid.
    difference() {
        union() {
            translate([-12, -14, 0]) cube([5*22 - 2, 28, 1.2]);
            for(i=[0:4]) {
                t = 0.8 + i*0.2;  // 0.8 .. 1.6
                // wall thickness increases left->right (0.8 .. 1.6 mm)
                translate([i*22,0,0]) cylinder(h=20+1.2, r=8, $fn=48);
            }
        }
        for(i=[0:4]) {
            t = 0.8 + i*0.2;
            translate([i*22,0,-EPS]) cylinder(h=20+1.2+2*EPS, r=8-t, $fn=48);
        }
    }
}

// --- Cable exit test (block with side hole + channel) ---
module cable_exit_test() {
    cable_r = strala_cable_diameter/2 + 1.5;
    difference() {
        cube([40,30,20], center=true);
        rotate([0,90,0]) cylinder(h=42, r=cable_r, center=true, $fn=32);
        translate([0,-15,-cable_r]) cube([cable_r*2,30,cable_r*2], center=false);
    }
}

// Default render: the critical 60mm passage ring
if ($preview) passage_test_ring(60);  // demo: only in GUI preview, skipped on STL export
