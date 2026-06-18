include <config.scad>

// ============================================================
// bayonet_v2.scad — Snap bayonet (3 lug)
//
// Male: ring with 3 lugs, lead-in chamfer on leading edge.
// Female: ring with 3 entry slots + lock grooves + snap well.
//
// Mating sequence:
//   1. Axial insert: male lug slides down female ENTRY slot
//   2. Rotate male CW by bay_lock_arc: lug travels under lock groove roof
//   3. Lug climbs snap ramp (deliberate force) then drops into snap well
//   4. Hard end-stop wall prevents over-rotation
//   5. Snap well + ramp resist back-rotation (anti-self-unlock)
// ============================================================

// ------------------------------------------------------------
// Shared bore + chamfers, subtracted from a ring of height h
// ------------------------------------------------------------
module _bore_cuts(h) {
    translate([0,0,-EPS]) cylinder(h=h+2*EPS, r=bore_r, $fn=128);
    // bottom lead-in chamfer for the bore
    translate([0,0,-EPS]) cylinder(h=3, r1=bore_r+2, r2=bore_r, $fn=64);
    // top lead-in chamfer for the bore
    translate([0,0,h-3]) cylinder(h=3+EPS, r1=bore_r, r2=bore_r+2, $fn=64);
}

// ------------------------------------------------------------
// One male lug: arc of bay_lug_arc, with a lead-in ramp on the
// LEADING edge (the edge that enters the lock groove first).
// The lug sits with its base at z=0 here; caller translates.
//
// Cross-section is built as a 2D profile then rotate_extruded.
// To create the lead-in chamfer we taper the *top* of the lug
// over the first snap_ramp-ish degrees using two extrudes:
//   - main body: full height square over (arc - chamfer)
//   - chamfer:   wedge tapering height 0->full over chamfer deg
// ------------------------------------------------------------
module bay_lug(chamfer_deg = 3) {
    // Full-height portion (after the lead-in)
    rotate([0,0, chamfer_deg])
        rotate_extrude(angle = bay_lug_arc - chamfer_deg, $fn=160)
            translate([bay_lug_inner_r, 0])
                square([bay_lug_depth, bay_lug_h]);

    // Lead-in ramp: height grows from a sliver to full over chamfer_deg.
    // Approximate the angular taper with thin angular slices.
    slices = 12;
    for (s = [0:slices-1]) {
        a0 = s     * chamfer_deg / slices;
        a1 = (s+1) * chamfer_deg / slices;
        // height at the END of this slice (so it grows toward full lug)
        hh = bay_lug_h * ((s+1) / slices);
        rotate([0,0, a0])
            rotate_extrude(angle = a1 - a0 + 0.01, $fn=24)
                translate([bay_lug_inner_r, 0])
                    square([bay_lug_depth, max(hh, 0.2)]);
    }
}

// ------------------------------------------------------------
// MALE bayonet ring. Lugs near the TOP of the ring so that when
// this male (on top of a module) is inserted downward into a
// female (on the bottom of the module above), the lug enters.
// ------------------------------------------------------------
module bay_male(h_body = bay_depth) {
    lug_z = h_body - bay_lug_h - clearance;   // lugs near top face

    union() {
        difference() {
            cylinder(h=h_body, r=bay_iface_r, $fn=96);
            _bore_cuts(h_body);
        }
        for (i = [0:bay_n-1])
            rotate([0,0, i*(360/bay_n)])
                translate([0,0, lug_z])
                    bay_lug();
    }
}

// ------------------------------------------------------------
// FEMALE groove cuts (used both here and inside module_frame so
// they live in the SAME difference block as the body).
// Caller must place this so cuts align with male lug_z.
//
// groove_z = floor level of the lock groove (lug rides here).
// ------------------------------------------------------------
module _bay_female_cuts(h_body) {
    groove_inner_r = bay_lug_inner_r - clearance;   // 33.2
    groove_outer_r = bay_lug_outer_r + clearance;   // 37.3
    groove_w       = groove_outer_r - groove_inner_r;
    groove_h       = bay_lug_h + clearance;         // 3.1
    // floor Z of lock groove — matches male lug bottom when mated
    groove_z = h_body - groove_h - clearance;

    for (i = [0:bay_n-1]) {
        rotate([0,0, i*(360/bay_n)]) {
            // (1) Entry slot — full height vertical channel
            rotate_extrude(angle = bay_entry_arc, $fn=160)
                translate([groove_inner_r, 0])
                    square([groove_w, h_body + 2*EPS]);

            // (2) Lock groove — horizontal pocket the lug rotates into.
            //     Spans from end of entry slot through the lock arc.
            //     Stops short of the snap zone (handled below).
            rotate([0,0, bay_entry_arc])
                rotate_extrude(angle = bay_lock_arc - snap_ramp_deg, $fn=160)
                    translate([groove_inner_r, groove_z])
                        square([groove_w, groove_h]);

            // (3) Snap RAMP zone: roof stays, but floor stays at groove_z
            //     and groove height is REDUCED (floor rises) so lug must
            //     squeeze. We model the reduced channel here.
            //     Reduced height = groove_h - snap_step (the bump).
            rotate([0,0, bay_entry_arc + bay_lock_arc - snap_ramp_deg])
                rotate_extrude(angle = snap_ramp_deg, $fn=80)
                    translate([groove_inner_r, groove_z + snap_step])
                        square([groove_w, groove_h - snap_step]);

            // (4) Snap WELL: just past the ramp the floor drops back down
            //     (full groove_h, plus a touch deeper) — the lug DROPS in.
            //     This is the end-stop pocket.
            rotate([0,0, bay_entry_arc + bay_lock_arc])
                rotate_extrude(angle = snap_ramp_deg, $fn=80)
                    translate([groove_inner_r, groove_z - snap_step])
                        square([groove_w, groove_h + snap_step]);

            // (5) Lead-in chamfer at the top mouth of the entry slot
            rotate_extrude(angle = bay_entry_arc, $fn=120)
                translate([groove_inner_r, h_body - 2.5])
                    polygon(points=[
                        [-1.5, 0],
                        [groove_w, 2.5 + EPS],
                        [-1.5, 2.5 + EPS]
                    ]);
        }
    }
}

// ------------------------------------------------------------
// FEMALE bayonet ring (standalone).
// ------------------------------------------------------------
module bay_female(h_body = bay_depth) {
    difference() {
        cylinder(h=h_body, r=bay_iface_r, $fn=96);
        _bore_cuts(h_body);
        _bay_female_cuts(h_body);
    }
}

// ------------------------------------------------------------
// Cross-section validation view
// ------------------------------------------------------------
module bay_section() {
    difference() {
        union() {
            bay_female(h_body=bay_depth);
            translate([0,0, bay_depth + 2]) bay_male(h_body=bay_depth);
        }
        translate([-200, -0.01, -10]) cube([400, 400, 400]);
    }
}

// Preview / export selector
part = "preview";
if (part == "preview") {
    bay_female();
    translate([0,0, bay_depth + 6]) bay_male();
} else if (part == "male") {
    bay_male();
} else if (part == "female") {
    bay_female();
} else if (part == "section") {
    bay_section();
}
