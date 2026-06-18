include <module_frame.scad>

collar_h = bay_depth + 3;   // collar height including socket

module _shade_collar() {
    difference() {
        cylinder(h=collar_h, r=bay_socket_or, $fn=96);
        translate([0,0,-EPS]) cylinder(h=collar_h+2*EPS, r=bay_socket_ir, $fn=96);
        _bay_socket_cuts(bay_depth);
    }
}

module shade_classic(h=shade_h, bot_d=shade_bot_d, top_d=shade_top_d) {
    union() {
        _shade_collar();
        translate([0,0, collar_h])
            difference() {
                cylinder(h=h, r1=bot_d/2, r2=top_d/2, $fn=128);
                translate([0,0,-EPS])
                    cylinder(h=h+2*EPS, r1=bot_d/2-shade_wall_t, r2=top_d/2-shade_wall_t, $fn=128);
                // Top vent opening
                translate([0,0, h-shade_vent])
                    cylinder(h=shade_vent+EPS, r=top_d/2+EPS, $fn=64);
            }
    }
}

module shade_ribbed(h=shade_h, bot_d=shade_bot_d, top_d=shade_top_d) {
    n_ribs = 24;
    union() {
        _shade_collar();
        translate([0,0, collar_h]) {
            difference() {
                union() {
                    cylinder(h=h, r1=bot_d/2, r2=top_d/2, $fn=128);
                    for (i=[0:n_ribs-1])
                        rotate([0,0, i*(360/n_ribs)])
                            hull() {
                                translate([bot_d/2-1, 0, 0]) cylinder(h=EPS, r=2, $fn=8);
                                translate([top_d/2-1, 0, h]) cylinder(h=EPS, r=1.5, $fn=8);
                            }
                }
                translate([0,0,-EPS])
                    cylinder(h=h+2*EPS, r1=bot_d/2-shade_wall_t, r2=top_d/2-shade_wall_t, $fn=128);
                translate([0,0, h-shade_vent])
                    cylinder(h=shade_vent+EPS, r=top_d/2+EPS, $fn=64);
            }
        }
    }
}

module shade_organic(h=shade_h, bot_d=shade_bot_d, top_d=shade_top_d) {
    union() {
        _shade_collar();
        translate([0,0, collar_h]) {
            difference() {
                hull() {
                    cylinder(h=EPS, r=bot_d/2, $fn=128);
                    translate([0,0, h*0.5]) cylinder(h=EPS, r=bot_d/2*1.05, $fn=128);
                    translate([0,0, h]) cylinder(h=EPS, r=top_d/2, $fn=128);
                }
                translate([0,0,-EPS]) hull() {
                    cylinder(h=EPS, r=bot_d/2-shade_wall_t, $fn=128);
                    translate([0,0, h*0.5]) cylinder(h=EPS, r=bot_d/2*1.05-shade_wall_t, $fn=128);
                    translate([0,0, h]) cylinder(h=EPS, r=top_d/2-shade_wall_t, $fn=128);
                }
                translate([0,0, h-shade_vent])
                    cylinder(h=shade_vent+EPS, r=top_d/2+EPS, $fn=64);
            }
        }
    }
}

part = "classic";
if      (part == "classic")  shade_classic();
else if (part == "ribbed")   shade_ribbed();
else if (part == "organic")  shade_organic();
