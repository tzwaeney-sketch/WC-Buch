include <module_frame.scad>

// ============================================================
// lamp_shades_v2.scad — three thin-wall shades.
// Each is a thin shell (shade_wall_t) with a small mounting
// collar at the bottom carrying a bay_female (clips to the
// strala holder's top male). Ventilation rings near top/bottom.
//   shade_classic : frustum cone
//   shade_ribbed  : frustum + 36 vertical ribs
//   shade_organic : S-curve rotate_extrude profile
// bbox <= 256, watertight single-component shells.
// ============================================================

t        = shade_wall_t;        // 1.6
collar_h = bay_depth + 4;       // mounting collar height (female zone + base)
vent_n   = 12;                  // holes per ring
vent_r   = shade_vent/2;        // 7.5

// radii
br = shade_bot_d/2;             // 120
tr = shade_top_d/2;             // 55

// ----- shade shell as a thin frustum (returns SOLID shell) -----
module _frustum_shell() {
    difference() {
        cylinder(h=shade_h, r1=br, r2=tr, $fn=160);
        // hollow interior, leave wall t, open top and bottom interior
        translate([0,0,-EPS])
            cylinder(h=shade_h+2*EPS, r1=br - t, r2=tr - t, $fn=160);
    }
}

// ----- ventilation hole ring at height z (radial holes) -----
module _vent_ring(z, ring_r) {
    for (i = [0:vent_n-1])
        rotate([0,0, i*360/vent_n + 11])
            translate([0,0,z])
                rotate([0,90,0])
                    cylinder(h=ring_r + 10, r=vent_r, $fn=32);
}

// ----- mounting collar: a small cylinder with bay_female -----
// Built so its outer wall blends to the shade interior. The collar
// sits at the bottom, bore open upward for the bulb/cable.
module _collar() {
    difference() {
        union() {
            cylinder(h=collar_h, r=bay_iface_r, $fn=96);
            // 3 thin webs tying collar out to the shade bottom rim
            for (i=[0:2])
                rotate([0,0,i*120])
                    translate([0,-t/1, 0])
                        cube([br - t + EPS, 2*t, t*2]);
        }
        _bore_cuts(collar_h);
        _bay_female_cuts(bay_depth);
    }
}

module shade_classic() {
    difference() {
        union() {
            _frustum_shell();
            _collar();
        }
        _vent_ring(shade_h - 25, tr);     // near top
        _vent_ring(35, br);               // near bottom (above collar)
    }
}

module shade_ribbed() {
    nrib = 36;
    difference() {
        union() {
            _frustum_shell();
            _collar();
            // vertical ribs on the outside, following the slope
            for (i = [0:nrib-1])
                rotate([0,0, i*360/nrib])
                    hull() {
                        translate([br, 0, 0]) cylinder(h=EPS, r=2, $fn=12);
                        translate([tr, 0, shade_h]) cylinder(h=EPS, r=1.4, $fn=12);
                    }
        }
        _vent_ring(shade_h - 25, tr);
        _vent_ring(35, br);
    }
}

// ----- organic S-curve shell -----
module shade_organic() {
    steps = 60;
    // mean radius follows a smooth S-curve from br to tr with a bulge
    function rmean(z) =
        let(f = z/shade_h)
        // base linear taper plus sinusoidal bulge
        (br + (tr - br)*f) + 12*sin(360*f);
    difference() {
        union() {
            rotate_extrude($fn=160)
                polygon(points = concat(
                    [ for (i=[0:steps]) let(z=i/steps*shade_h)
                        [ max(rmean(z),     tr - t + 1), z ] ],
                    [ for (i=[steps:-1:0]) let(z=i/steps*shade_h)
                        [ max(rmean(z) - t, tr - t),     z ] ]
                ));
            _collar();
        }
        _vent_ring(shade_h - 25, tr + 12);
        _vent_ring(40, br);
    }
}

part = "classic";
if (part == "classic")      shade_classic();
else if (part == "ribbed")  shade_ribbed();
else if (part == "organic") shade_organic();
