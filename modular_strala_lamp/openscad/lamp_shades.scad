include <config.scad>

EPS = 0.01;

mount_r      = shade_mount_diameter / 2;
mount_wall   = reinforced_wall;
mount_h      = 15;

// Shared mounting ring — all shades use this
module shade_mounting_ring() {
    difference() {
        cylinder(h=mount_h, r=mount_r + mount_wall, $fn=64);
        translate([0,0,-EPS])
            cylinder(h=mount_h+2*EPS, r=mount_r, $fn=64);
        for(a=[0:5]) {
            rotate([0,0,a*60])
                translate([mount_r + mount_wall/2, 0, mount_h/2])
                    cube([mount_wall+2, 4, mount_h*0.6], center=true);
        }
    }
}

// Generic shade body from a rotate_extrude profile (children = profile polygon)
module _shade_body(h) {
    union() {
        shade_mounting_ring();
        translate([0,0,mount_h]) children();
    }
}

// hollow frustum/cone helper
module _hollow_cone(h, bot_r, top_r, w) {
    difference() {
        cylinder(h=h, r1=bot_r, r2=top_r, $fn=128);
        translate([0,0,-EPS])
            cylinder(h=h+2*EPS, r1=bot_r-w, r2=top_r-w, $fn=128);
        // top ventilation opening
        translate([0,0,h-shade_ventilation_gap])
            cylinder(h=shade_ventilation_gap+EPS, r=top_r+1, $fn=64);
    }
}

// 1. Frustum
module shade_frustum() {
    _shade_body(shade_height)
        _hollow_cone(shade_height, shade_bottom_diameter/2, shade_top_diameter/2, shade_wall);
}

// 2. Straight cylinder
module shade_cylinder() {
    r = shade_bottom_diameter/2 * 0.7;
    _shade_body(shade_height)
        _hollow_cone(shade_height, r, r, shade_wall);
}

// 3. Bell curve
module shade_bell() {
    h=shade_height;
    _shade_body(h)
        rotate_extrude($fn=128)
            difference() {
                polygon([for(i=[0:1:24])
                    let(t=i/24, rad = shade_top_diameter/2 + (shade_bottom_diameter/2 - shade_top_diameter/2)*pow(1-t,1.8))
                    [rad, t*h]
                ]);
                polygon([for(i=[0:1:24])
                    let(t=i/24, rad = shade_top_diameter/2 + (shade_bottom_diameter/2 - shade_top_diameter/2)*pow(1-t,1.8) - shade_wall)
                    [max(0.1,rad), t*h]
                ]);
            }
}

// 4. Mushroom cap
module shade_mushroom() {
    h=shade_height*0.7;
    _shade_body(h)
        difference() {
            resize([shade_bottom_diameter, shade_bottom_diameter, h*2])
                sphere(r=shade_bottom_diameter/2,$fn=96);
            resize([shade_bottom_diameter-2*shade_wall, shade_bottom_diameter-2*shade_wall, h*2-2*shade_wall])
                sphere(r=shade_bottom_diameter/2,$fn=96);
            translate([0,0,-h]) cylinder(h=h,r=shade_bottom_diameter,$fn=64);
            cylinder(h=h*2, r=shade_top_diameter/2, $fn=64); // top vent
        }
}

// 5. Globe (sphere segment)
module shade_globe() {
    h=shade_height*0.8;
    _shade_body(h)
        difference() {
            resize([shade_bottom_diameter,shade_bottom_diameter,h]) sphere(r=shade_bottom_diameter/2,$fn=96);
            resize([shade_bottom_diameter-2*shade_wall,shade_bottom_diameter-2*shade_wall,h-2*shade_wall]) sphere(r=shade_bottom_diameter/2,$fn=96);
            cylinder(h=h, r=shade_top_diameter/2, $fn=64);
        }
}

// 6. Vertical ribs
module shade_vertical_ribs() {
    h=shade_height;
    _shade_body(h) {
        _hollow_cone(h, shade_bottom_diameter/2, shade_top_diameter/2, shade_wall);
        for(a=[0:360/shade_rib_count:359])
            rotate([0,0,a])
                translate([shade_bottom_diameter/2 - 1, 0, 0])
                    cylinder(h=h-shade_ventilation_gap, r1=shade_rib_depth, r2=shade_rib_depth*0.5, $fn=8);
    }
}

// 7. Horizontal ribs
module shade_horizontal_ribs() {
    h=shade_height;
    _shade_body(h) {
        _hollow_cone(h, shade_bottom_diameter/2, shade_top_diameter/2, shade_wall);
        for(z=[10:18:h-shade_ventilation_gap]) {
            t = z/h;
            rr = shade_bottom_diameter/2 + (shade_top_diameter/2 - shade_bottom_diameter/2)*t;
            translate([0,0,z])
                rotate_extrude($fn=128)
                    translate([rr,0]) circle(r=shade_rib_depth,$fn=8);
        }
    }
}

// 8. Faceted polygon shade
module shade_faceted() {
    h=shade_height;
    _shade_body(h)
        difference() {
            cylinder(h=h, r1=shade_bottom_diameter/2, r2=shade_top_diameter/2, $fn=10);
            translate([0,0,-EPS])
                cylinder(h=h+2*EPS, r1=shade_bottom_diameter/2-shade_wall, r2=shade_top_diameter/2-shade_wall, $fn=10);
            translate([0,0,h-shade_ventilation_gap])
                cylinder(h=shade_ventilation_gap+EPS, r=shade_top_diameter/2+2, $fn=64);
        }
}

// 9. Organic S-curve
module shade_organic_curve() {
    h=shade_height;
    botr=shade_bottom_diameter/2; topr=shade_top_diameter/2;
    _shade_body(h)
        rotate_extrude($fn=128)
            difference() {
                polygon([for(i=[0:1:30])
                    let(t=i/30, rad = topr + (botr-topr)*(0.5+0.5*cos(180*t)))
                    [rad, t*h]
                ]);
                polygon([for(i=[0:1:30])
                    let(t=i/30, rad = topr + (botr-topr)*(0.5+0.5*cos(180*t)) - shade_wall)
                    [max(0.1,rad), t*h]
                ]);
            }
}

// 10. Perforated frustum
module shade_perforated() {
    h=shade_height;
    _shade_body(h)
        difference() {
            _hollow_cone(h, shade_bottom_diameter/2, shade_top_diameter/2, shade_wall);
            for(z=[25:30:h-30])
                for(a=[0:30:330])
                    rotate([0,0,a + (z/30)*15]) {
                        t=z/h;
                        rr = shade_bottom_diameter/2 + (shade_top_diameter/2 - shade_bottom_diameter/2)*t;
                        translate([rr,0,z]) rotate([0,90,0]) cylinder(h=20,r=5,center=true,$fn=24);
                    }
        }
}

if ($preview) shade_frustum();  // demo: only in GUI preview, skipped on STL export
