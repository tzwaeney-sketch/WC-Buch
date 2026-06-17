include <config.scad>

EPS = 0.01;

// Single passage test ring with bore diameter d, height h, label.
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
        rotate([90,0,0])
            linear_extrude(height=1.2)
                text(str(d, "mm"), size=5, halign="center");
}

// Three reference rings 55 / 58 / 60
module passage_variants() {
    passage_test_ring(55);
    translate([70,0,0]) passage_test_ring(58);
    translate([140,0,0]) passage_test_ring(60);
}

if ($preview) passage_variants();  // demo: only in GUI preview, skipped on STL export
