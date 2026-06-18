include <config.scad>

// 60mm bore + chamfers
module _bore_cuts(h) {
    translate([0,0,-EPS]) cylinder(h=h+2*EPS, r=bore_r, $fn=128);
    translate([0,0,-EPS]) cylinder(h=3, r1=bore_r+2, r2=bore_r, $fn=64);
    translate([0,0,h-3]) cylinder(h=3+EPS, r1=bore_r, r2=bore_r+2, $fn=64);
}

// One lug: protrudes outward from bay_spigot_r to bay_lug_r
// bay_lug_arc wide, bay_lug_h tall, lead-in chamfer first 3deg
module bay_lug() {
    chamfer_deg = 3;
    // Main body (after chamfer)
    rotate([0,0, chamfer_deg])
        rotate_extrude(angle=bay_lug_arc - chamfer_deg, $fn=160)
            translate([bay_spigot_r, 0])
                square([bay_lug_depth, bay_lug_h]);
    // Lead-in ramp: 12 thin wedge slices tapering height 0->full
    slices = 12;
    for (s=[0:slices-1]) {
        a0 = s     * chamfer_deg / slices;
        a1 = (s+1) * chamfer_deg / slices;
        hh = bay_lug_h * ((s+1) / slices);
        rotate([0,0, a0])
            rotate_extrude(angle=a1-a0+0.01, $fn=20)
                translate([bay_spigot_r, 0])
                    square([bay_lug_depth, max(hh, 0.2)]);
    }
}

// Male spigot: cylinder r=bay_spigot_r + 3 external lugs
// Place with translate([0,0, module_height]) -- protrudes ABOVE module top
module bay_male_spigot(h=bay_depth) {
    lug_z = h - bay_lug_h - 0.3;  // lugs near top of spigot
    union() {
        difference() {
            cylinder(h=h, r=bay_spigot_r, $fn=96);
            translate([0,0,-EPS]) cylinder(h=h+2*EPS, r=bore_r, $fn=96);
        }
        for (i=[0:bay_n-1])
            rotate([0,0, i*(360/bay_n)])
                translate([0,0, lug_z])
                    bay_lug();
    }
}

// Female socket cuts: entry slots + lock grooves + snap
// Use inside a difference() on a ring of inner=bay_socket_ir, outer=bay_socket_or
module _bay_socket_cuts(h=bay_depth) {
    sw = bay_lug_r + 0.35 - bay_socket_ir;  // slot radial width (~4.0mm)
    groove_h   = bay_lug_h + 0.35;          // lock groove axial height (~3.35mm)
    groove_z   = h - bay_lug_h - 0.3 - 0.35; // groove floor Z in socket frame
    for (i=[0:bay_n-1]) {
        rotate([0,0, i*(360/bay_n)]) {
            // Entry slot: full height
            rotate_extrude(angle=bay_entry_arc, $fn=160)
                translate([bay_socket_ir, 0])
                    square([sw, h+2*EPS]);
            // Lock groove
            rotate([0,0, bay_entry_arc])
                rotate_extrude(angle=bay_lock_arc - snap_ramp_deg, $fn=160)
                    translate([bay_socket_ir, groove_z])
                        square([sw, groove_h]);
            // Snap well (floor drops 0.5mm deeper over last 4deg)
            rotate([0,0, bay_entry_arc + bay_lock_arc - snap_ramp_deg])
                rotate_extrude(angle=snap_ramp_deg, $fn=80)
                    translate([bay_socket_ir, groove_z - snap_step])
                        square([sw, groove_h + snap_step]);
            // Lead-in chamfer at entry slot mouth (top opening)
            rotate_extrude(angle=bay_entry_arc+2, $fn=120)
                translate([bay_socket_ir-1, h-2])
                    polygon([[0,0],[sw+2,2+EPS],[0,2+EPS]]);
        }
    }
}

// Standalone female socket ring (for direct use)
module bay_female_socket(h=bay_depth) {
    difference() {
        cylinder(h=h, r=bay_socket_or, $fn=96);
        translate([0,0,-EPS]) cylinder(h=h+2*EPS, r=bay_socket_ir, $fn=96);
        _bay_socket_cuts(h);
    }
}
