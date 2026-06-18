include <config.scad>
include <bayonet_v2.scad>

// ============================================================
// module_frame.scad — shared skeleton for every body module.
//
// Layout (Z):
//   z = 0 .. bay_depth         : FEMALE bayonet zone (bottom)
//   z = bay_depth .. h-bay_depth : central decorative body
//   z = h-bay_depth .. h       : MALE bayonet zone (top, lugs)
//
// The outer decorative shell is passed as children(0). The frame
// adds an inner structural tube, subtracts the 60mm bore + female
// slots in ONE difference block, then adds male lugs on top.
//
// Minimum height: 2*bay_depth + a little body.
// ============================================================
module mod_frame(h, outer_r) {
    inner_tube_r = bay_iface_r + wall_str;   // 42.52
    assert(outer_r >= inner_tube_r - 0.001,
           str("Module too narrow: outer_r=", outer_r, " min=", inner_tube_r));
    assert(h >= 2*bay_depth + 10,
           str("Module too short: h=", h, " min=", 2*bay_depth+10));

    lug_z = h - bay_lug_h - clearance;       // male lugs near top

    difference() {
        union() {
            children(0);                      // outer decorative shell
            cylinder(h=h, r=inner_tube_r, $fn=96);  // structural tube
            // solid bayonet interface rings (so slots/bore cut real walls)
            cylinder(h=bay_depth, r=bay_iface_r, $fn=96);            // bottom (female)
            translate([0,0,h-bay_depth]) cylinder(h=bay_depth, r=bay_iface_r, $fn=96); // top (male base)
        }

        // 60mm through bore + entry/exit chamfers
        _bore_cuts(h);

        // FEMALE slots at the bottom interface zone
        _bay_female_cuts(bay_depth);
    }

    // MALE lugs at the top interface zone (added as solid, sit in wall)
    for (i = [0:bay_n-1])
        rotate([0,0, i*(360/bay_n)])
            translate([0,0, lug_z])
                bay_lug();
}
