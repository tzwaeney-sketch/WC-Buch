// =====================================================================
// organic_modules.scad - Organic / flowing decorative modules
// =====================================================================
include <config.scad>
include <bayonet_system.scad>
include <round_modules.scad>   // reuse _module_frame

// ---------------------------------------------------------------------
// Teardrop, h ~ 75mm.
// ---------------------------------------------------------------------
module mod_teardrop() {
    h = 75;
    od = 96;
    _module_frame(h)
        rotate_extrude($fn = 96)
            polygon(points = [
                [final_plug_passage/2 + structural_wall, 0],
                [od/2, h * 0.30],
                [od/2 * 0.85, h * 0.55],
                [od/2 * 0.45, h * 0.85],
                [final_plug_passage/2 + structural_wall, h],
            ]);
}

// ---------------------------------------------------------------------
// Vase with waist, h ~ 85mm.
// ---------------------------------------------------------------------
module mod_vase() {
    h = 85;
    _module_frame(h)
        rotate_extrude($fn = 96)
            offset(r = 5) offset(delta = -5)
                polygon(points = [
                    [final_plug_passage/2 + 2, 0],
                    [48, 0],
                    [40, h * 0.25],
                    [28, h * 0.50],     // waist
                    [42, h * 0.78],
                    [38, h],
                    [final_plug_passage/2 + 2, h],
                ]);
}

// ---------------------------------------------------------------------
// Asymmetric gentle bulge, h ~ 70mm.
// ---------------------------------------------------------------------
module mod_asymmetric_soft() {
    h = 70;
    _module_frame(h)
        rotate_extrude($fn = 96)
            offset(r = 8) offset(delta = -8)
                polygon(points = [
                    [final_plug_passage/2 + 2, 0],
                    [46, 0],
                    [54, h * 0.40],     // bulge
                    [40, h * 0.75],
                    [44, h],
                    [final_plug_passage/2 + 2, h],
                ]);
}

// ---------------------------------------------------------------------
// Pumpkin / gourd with vertical ribs, h ~ 65mm.
// ---------------------------------------------------------------------
module mod_pumpkin() {
    h = 65;
    od = 110;
    ribs = 12;
    _module_frame(h)
        union() {
            // Core squashed sphere
            intersection() {
                scale([1, 1, h / od])
                    translate([0, 0, od/2]) sphere(d = od, $fn = 96);
                cylinder(h = h, d = od + 6, $fn = 96);
            }
            // Rib lobes
            for (i = [0 : ribs - 1])
                rotate([0, 0, i * 360 / ribs])
                    translate([od/2 - 6, 0, h/2])
                        scale([1, 1, h / (od*0.9)])
                            sphere(d = 14, $fn = 32);
            // central support tube to the bore wall
            cylinder(h = h, d = final_plug_passage + 2 * structural_wall, $fn = fn_large_bore);
        }
}

// ---------------------------------------------------------------------
// Undulating wave cylinder, h ~ 60mm.
// ---------------------------------------------------------------------
module mod_wave() {
    h = 60;
    base_r = 48;
    waves = 4;
    amp = 6;
    inner_x = final_plug_passage/2 + 2;
    outer_pts = [ for (i = [0 : 40])
        let (z = h * i / 40,
             r = base_r + amp * sin(360 * waves * i / 40))
        [max(inner_x, r), z] ];
    _module_frame(h)
        rotate_extrude($fn = 120)
            polygon(points = concat(
                [[inner_x, 0]],
                outer_pts,
                [[inner_x, h]]
            ));
}

// ---------------------------------------------------------------------
// Soft organic diamond, h ~ 80mm.
// ---------------------------------------------------------------------
module mod_organic_diamond() {
    h = 80;
    od = 100;
    _module_frame(h)
        rotate_extrude($fn = 96)
            offset(r = 10) offset(delta = -10)
                polygon(points = [
                    [final_plug_passage/2 + 2, 0],
                    [od/2 * 0.5, 0],
                    [od/2, h * 0.5],     // widest mid
                    [od/2 * 0.4, h],
                    [final_plug_passage/2 + 2, h],
                ]);
}
