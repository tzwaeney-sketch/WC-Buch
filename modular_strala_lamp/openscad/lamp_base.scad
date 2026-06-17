include <config.scad>
include <bayonet_system.scad>

EPS = 0.01;

// ============================================================
// LAMP BASE BODY
// ============================================================
module lamp_base() {
    bore_r  = base_passage_diameter / 2;      // 30mm
    outer_r = base_outer_diameter / 2;         // 110mm
    h       = base_total_height;               // 45mm
    wall    = base_outer_wall;                 // 3.36mm

    cable_exit_r = strala_cable_diameter / 2 + 1.5;  // ~4.5mm radius

    weight_chamber_outer_r = bore_r + wall + 18;
    weight_chamber_h       = h - base_bottom_thickness - 4;

    cable_channel_w = strala_cable_diameter + 4;
    cable_channel_h = strala_cable_diameter + 4;

    difference() {
        union() {
            cylinder(h=h, r=outer_r, $fn=128);
            translate([0,0,h])
                cylinder(h=5, r=bayonet_interface_outer_radius + structural_wall, $fn=64);
        }

        // Central bore (FULL HEIGHT)
        translate([0,0,-EPS])
            cylinder(h=h + 5 + 2*EPS, r=bore_r, $fn=128);
        translate([0,0,-EPS])
            cylinder(h=3, r1=bore_r+3, r2=bore_r, $fn=64);

        // Hollow interior
        translate([0,0,base_bottom_thickness])
            cylinder(h=h - base_bottom_thickness - 4, r=outer_r - wall, $fn=128);

        // Weight chamber pocket (annular, keep bore wall)
        translate([0,0,base_bottom_thickness + 2])
            difference() {
                cylinder(h=weight_chamber_h - 2, r=weight_chamber_outer_r, $fn=64);
                cylinder(h=weight_chamber_h, r=bore_r + wall, $fn=64);
            }

        // Cable channel (rear trough, does NOT cross the bore)
        translate([0, -(cable_channel_w/2), base_bottom_thickness + 2])
            cube([outer_r, cable_channel_w, cable_channel_h]);

        // Side cable exit hole
        translate([outer_r - wall - EPS, 0, base_bottom_thickness + 2 + cable_channel_h/2])
            rotate([0,90,0])
                cylinder(h=wall + 2*EPS, r=cable_exit_r, $fn=32);

        // Rubber foot pockets (4×)
        for(a=[45,135,225,315]) {
            rotate([0,0,a])
                translate([outer_r - 12, 0, -EPS])
                    cylinder(h=base_bottom_thickness + EPS, r=6, $fn=32);
        }

        // Bottom plate screw holes (3 × M3)
        for(a=[0,120,240]) {
            rotate([0,0,a])
                translate([outer_r - 15, 0, -EPS])
                    cylinder(h=base_bottom_thickness + 2*EPS, r=1.6, $fn=16);
        }
    }

    // Male bayonet at top
    translate([0,0,h+5 - (bayonet_working_depth+2)])
        bayonet_male();
}

// ============================================================
// LAMP BASE — DESIGN VARIANT (stepped outer profile)
// Identical interfaces: 60mm bore, same bayonet, same cable
// channel + weight chamber. Only the outer shell differs.
// ============================================================
module lamp_base_design() {
    bore_r  = base_passage_diameter / 2;      // 30mm
    h       = base_total_height;               // 45mm
    wall    = base_outer_wall;
    // 3-step stepped exterior
    step_h  = h/3;
    od0 = 210; od1 = 185; od2 = 160;
    outer_r = od0/2;

    cable_exit_r = strala_cable_diameter / 2 + 1.5;
    weight_chamber_outer_r = bore_r + wall + 18;
    weight_chamber_h       = h - base_bottom_thickness - 4;
    cable_channel_w = strala_cable_diameter + 4;
    cable_channel_h = strala_cable_diameter + 4;

    difference() {
        union() {
            // stepped outer body
            cylinder(h=step_h+EPS, r=od0/2, $fn=128);
            translate([0,0,step_h]) cylinder(h=step_h+EPS, r=od1/2, $fn=128);
            translate([0,0,2*step_h]) cylinder(h=step_h, r=od2/2, $fn=128);
            translate([0,0,h])
                cylinder(h=5, r=bayonet_interface_outer_radius + structural_wall, $fn=64);
        }
        // Central bore (FULL HEIGHT)
        translate([0,0,-EPS])
            cylinder(h=h + 5 + 2*EPS, r=bore_r, $fn=128);
        translate([0,0,-EPS])
            cylinder(h=3, r1=bore_r+3, r2=bore_r, $fn=64);
        // Hollow interior
        translate([0,0,base_bottom_thickness])
            cylinder(h=h - base_bottom_thickness - 4, r=od2/2 - wall, $fn=128);
        // Weight chamber pocket
        translate([0,0,base_bottom_thickness + 2])
            difference() {
                cylinder(h=weight_chamber_h - 2, r=weight_chamber_outer_r, $fn=64);
                cylinder(h=weight_chamber_h, r=bore_r + wall, $fn=64);
            }
        // Cable channel
        translate([0, -(cable_channel_w/2), base_bottom_thickness + 2])
            cube([od0/2, cable_channel_w, cable_channel_h]);
        // Side cable exit hole
        translate([od2/2 - wall - EPS, 0, base_bottom_thickness + 2 + cable_channel_h/2])
            rotate([0,90,0])
                cylinder(h=wall + 2*EPS, r=cable_exit_r, $fn=32);
        // Rubber foot pockets (4×)
        for(a=[45,135,225,315])
            rotate([0,0,a])
                translate([od0/2 - 12, 0, -EPS])
                    cylinder(h=base_bottom_thickness + EPS, r=6, $fn=32);
        // Bottom plate screw holes (3 × M3)
        for(a=[0,120,240])
            rotate([0,0,a])
                translate([od0/2 - 15, 0, -EPS])
                    cylinder(h=base_bottom_thickness + 2*EPS, r=1.6, $fn=16);
    }
    // Male bayonet at top
    translate([0,0,h+5 - (bayonet_working_depth+2)])
        bayonet_male();
}

// ============================================================
// BOTTOM PLATE
// ============================================================
module lamp_base_bottom_plate() {
    bore_r  = base_passage_diameter / 2;
    outer_r = base_outer_diameter / 2;

    difference() {
        cylinder(h=base_bottom_thickness - 0.5, r=outer_r - general_clearance, $fn=128);
        translate([0,0,-EPS])
            cylinder(h=base_bottom_thickness + 2*EPS, r=bore_r, $fn=128);
        translate([-(strala_cable_diameter/2 + 2), -(outer_r), -EPS])
            cube([strala_cable_diameter + 4, outer_r, base_bottom_thickness + 2*EPS]);
        for(a=[0,120,240]) {
            rotate([0,0,a])
                translate([outer_r - 15, 0, -EPS]) {
                    cylinder(h=base_bottom_thickness - 1.5 + EPS, r=3.2, $fn=16);
                    translate([0,0,base_bottom_thickness - 1.5])
                        cylinder(h=1.6, r1=3.2, r2=1.6, $fn=16);
                }
        }
        for(a=[45,135,225,315]) {
            rotate([0,0,a])
                translate([outer_r - 12, 0, -EPS])
                    cylinder(h=base_bottom_thickness + 2*EPS, r=5.5, $fn=32);
        }
        translate([0,0,-EPS])
            cylinder(h=3, r1=bore_r+3, r2=bore_r, $fn=64);
    }
}

// ============================================================
// WEIGHT INSERT (steel ring placeholder)
// ============================================================
module lamp_base_weight_insert() {
    bore_r  = base_passage_diameter / 2;
    weight_outer_r = bore_r + base_wall + 17;
    difference() {
        cylinder(h=8, r=weight_outer_r - 0.5, $fn=64);
        translate([0,0,-EPS])
            cylinder(h=10, r=bore_r + base_wall + 0.5, $fn=64);
    }
}

// ============================================================
// CABLE EXIT GROMMET
// ============================================================
module cable_exit_grommet() {
    cable_r = strala_cable_diameter / 2 + 1.5;
    difference() {
        cylinder(h=base_outer_wall + 2, r=cable_r + structural_wall, $fn=32);
        translate([0,0,-EPS])
            cylinder(h=base_outer_wall + 4, r=cable_r, $fn=32);
        translate([0,0,-EPS])
            cylinder(h=2, r1=cable_r+2, r2=cable_r, $fn=32);
    }
}

if ($preview) lamp_base();  // demo: only in GUI preview, skipped on STL export
