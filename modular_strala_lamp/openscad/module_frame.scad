include <config.scad>
include <bayonet_v2.scad>

module mod_frame(h, outer_r) {
    inner_tube_r = bay_socket_or;   // 43mm
    assert(outer_r >= inner_tube_r - 0.001,
           str("Module too narrow: outer_r=", outer_r, " min=", inner_tube_r));
    assert(h >= 2*bay_depth + 10,
           str("Module too short: h=", h));

    difference() {
        union() {
            children(0);                                    // outer decorative body
            cylinder(h=h, r=inner_tube_r, $fn=96);         // structural tube
        }
        _bore_cuts(h);                                      // 60mm bore
        _bay_socket_cuts(bay_depth);                        // female slots at bottom
    }

    // Male spigot on TOP: protrudes above the module
    translate([0,0, h]) bay_male_spigot(bay_depth);
}
