include <config.scad>

// Epsilon for avoiding zero-thickness faces
EPS = 0.01;

// ============================================================
// MALE BAYONET INTERFACE
// Adds 3 lugs to the top of a cylinder
// ============================================================
module bayonet_male(h_total = bayonet_working_depth + 2) {
    inner_r = bayonet_bore_radius;
    outer_r = bayonet_interface_outer_radius;
    lug_h   = bayonet_lug_height;
    lug_z   = h_total - lug_h - bayonet_axial_clearance; // lugs near top

    difference() {
        cylinder(h=h_total, r=outer_r, $fn=64);
        translate([0,0,-EPS])
            cylinder(h=h_total+2*EPS, r=inner_r, $fn=128);
        translate([0,0,-EPS])
            cylinder(h=2+EPS, r1=inner_r+2, r2=inner_r, $fn=64);
        translate([0,0,h_total-2])
            cylinder(h=2+EPS, r1=inner_r, r2=inner_r+2, $fn=64);
    }

    // 3 lugs
    for(i=[0:2]) {
        rotate([0,0, i*120]) {
            translate([0,0,lug_z]) {
                rotate_extrude(angle=22, $fn=64)
                    translate([male_lug_inner_radius, 0, 0])
                        square([bayonet_lug_radial_depth, lug_h]);
            }
        }
    }
}

// ============================================================
// FEMALE BAYONET INTERFACE
// ============================================================
module bayonet_female(h_total = bayonet_working_depth + 2) {
    inner_r  = bayonet_bore_radius;
    outer_r  = bayonet_interface_outer_radius;
    ch_inner = female_channel_inner_radius;
    ch_outer = female_channel_outer_radius;
    ch_h     = female_channel_height;

    entry_angle = 28;
    groove_z = h_total - ch_h - bayonet_axial_clearance;

    difference() {
        cylinder(h=h_total, r=outer_r, $fn=64);
        translate([0,0,-EPS])
            cylinder(h=h_total+2*EPS, r=inner_r, $fn=128);
        translate([0,0,-EPS])
            cylinder(h=2+EPS, r1=inner_r+2, r2=inner_r, $fn=64);
        translate([0,0,h_total-2])
            cylinder(h=2+EPS, r1=inner_r, r2=inner_r+2, $fn=64);

        // entry slots
        for(i=[0:2]) {
            rotate([0,0, i*120])
                rotate_extrude(angle=entry_angle, $fn=64)
                    translate([ch_inner, 0, 0])
                        square([ch_outer - ch_inner, h_total + EPS]);
        }

        // lock grooves
        for(i=[0:2]) {
            rotate([0,0, i*120 + entry_angle])
                rotate_extrude(angle=bayonet_lock_angle, $fn=64)
                    translate([ch_inner, groove_z, 0])
                        square([ch_outer - ch_inner, ch_h]);
        }
    }
}

// ============================================================
// COMPLETE BAYONET PAIR
// ============================================================
module bayonet_pair(gap=5) {
    bayonet_female();
    translate([0, 0, bayonet_working_depth + 2 + gap])
        bayonet_male();
}

// ============================================================
// PASSAGE RING — smallest useful module
// ============================================================
module bayonet_passage_ring(h=20) {
    inner_r = bayonet_bore_radius;
    outer_r = bayonet_interface_outer_radius + structural_wall;

    difference() {
        union() {
            cylinder(h=h, r=outer_r, $fn=64);
            bayonet_female(h_total = bayonet_working_depth + 2);
            translate([0,0, h - bayonet_working_depth - 2])
                bayonet_male(h_total = bayonet_working_depth + 2);
        }
        translate([0,0,-EPS])
            cylinder(h=h+2*EPS, r=inner_r, $fn=128);
        translate([0,0,-EPS])
            cylinder(h=3, r1=inner_r+3, r2=inner_r, $fn=64);
        translate([0,0,h-3])
            cylinder(h=3+EPS, r1=inner_r, r2=inner_r+3, $fn=64);
    }
}

// ============================================================
// CROSS-SECTION VIEW
// ============================================================
module bayonet_section_view() {
    difference() {
        bayonet_pair();
        translate([-200, 0, -1])
            cube([200, 200, 100]);
    }
}

// ============================================================
// TOLERANCE TEST PAIR
// ============================================================
module bayonet_tolerance_pair(clearance = 0.30) {
    adj_radial = clearance;
    adj_axial  = clearance * 0.8;

    h = bayonet_working_depth + 4;
    inner_r  = bayonet_bore_radius;
    outer_r  = bayonet_interface_outer_radius;
    ch_inner = male_lug_inner_radius - adj_radial;
    ch_outer = male_lug_outer_radius + adj_radial;
    ch_h     = bayonet_lug_height + adj_axial;
    entry_a  = 28;
    groove_z = h - ch_h - adj_axial;

    // Female part
    difference() {
        cylinder(h=h, r=outer_r, $fn=64);
        translate([0,0,-EPS]) cylinder(h=h+2*EPS, r=inner_r, $fn=128);
        for(i=[0:2]) {
            rotate([0,0,i*120])
                rotate_extrude(angle=entry_a, $fn=64)
                    translate([ch_inner,0]) square([ch_outer-ch_inner, h+EPS]);
            rotate([0,0,i*120+entry_a])
                rotate_extrude(angle=bayonet_lock_angle, $fn=64)
                    translate([ch_inner, groove_z]) square([ch_outer-ch_inner, ch_h]);
        }
    }

    // Male part (offset for printing)
    translate([outer_r*2 + 5, 0, 0]) {
        lug_z = h - bayonet_lug_height - adj_axial;
        difference() {
            cylinder(h=h, r=outer_r, $fn=64);
            translate([0,0,-EPS]) cylinder(h=h+2*EPS, r=inner_r, $fn=128);
        }
        for(i=[0:2]) {
            rotate([0,0,i*120])
                translate([0,0,lug_z])
                    rotate_extrude(angle=22, $fn=64)
                        translate([male_lug_inner_radius,0])
                            square([bayonet_lug_radial_depth, bayonet_lug_height]);
        }
    }

    // Label
    translate([0, outer_r+2, 0])
        linear_extrude(height=1.5)
            text(str(clearance, "mm"), size=4, halign="center");
}
