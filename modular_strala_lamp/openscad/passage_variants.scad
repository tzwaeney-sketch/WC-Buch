// Three passage test rings for physical fit testing
// Print all three and test with real Schuko plug

include <config.scad>
include <bayonet_system.scad>

// Test ring: 20mm tall, with chamfers, full bayonet interface
module passage_test_ring(bore_diameter, label_text) {
    wall = structural_wall;
    h = 20;
    outer_d = bore_diameter + 2*wall + 2*bayonet_lug_radial_depth + 2*bayonet_outer_wall;

    difference() {
        // outer body
        cylinder(h=h, d=outer_d, $fn=64);
        // bore
        translate([0,0,-1])
            cylinder(h=h+2, d=bore_diameter, $fn=128);
        // top chamfer
        translate([0,0,h-2])
            cylinder(h=3, d1=bore_diameter, d2=bore_diameter+4, $fn=64);
        // bottom chamfer
        translate([0,0,-1])
            cylinder(h=3, d1=bore_diameter+4, d2=bore_diameter, $fn=64);
    }
    // label
    translate([0, outer_d/2 - 1, h/2])
        rotate([90,0,0])
            linear_extrude(height=1.5)
                text(label_text, size=4, halign="center", valign="center");
}

// 55mm variant (minimum required)
translate([0, 0, 0])
    passage_test_ring(55, "55mm");

// 58mm variant
translate([80, 0, 0])
    passage_test_ring(58, "58mm");

// 60mm variant
translate([160, 0, 0])
    passage_test_ring(60, "60mm");
