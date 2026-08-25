// Hobby Dreholive für Kleiderschrank (silber), Modelljahre 2009-2025
// Nachbau als 3D-Druck-Ersatzteil, parametrisch in OpenSCAD.
//
// WICHTIG - Herkunft der Maße:
// Es lagen keine Konstruktionsdaten vor, nur zwei Produktfotos vom Verkäufer
// (campingplus.de), von denen eines eine bemaßte Nahaufnahme mit einer
// eingezeichneten Messstrecke von 33 mm zeigt (Breite der Öffnung/Olive).
// Dieser einzige belastbare Wert wurde als Referenz genommen; alle übrigen
// Maße sind daraus per Bildproportion abgeschätzt bzw. aus allgemein
// üblichen Werten für Möbel-Dreholiven ("7 mm Vierkant" ist der in der
// Branche gängige Standard für den Betätigungsdorn) übernommen.
// => Vor dem Drucken den vorhandenen (abgebrochenen) Vierkantstift bzw. die
//    Aufnahme im Schrank nachmessen und ggf. shaft_square unten anpassen.

// ---------------------------------------------------------------------
// Parameter (mm)
// ---------------------------------------------------------------------
paddle_width      = 33;    // Breite der Olive / Öffnung (aus Foto vermessen)
paddle_length     = 46;    // Länge der Olive, aus Bildproportion geschätzt
paddle_height     = 13;    // Wölbungshöhe der Olive, aus Bildproportion geschätzt
shell_thickness   = 3;     // Wandstärke der Schale

shaft_square      = 7;     // Vierkant-Maß des Betätigungsdorns (Branchenstandard 7 mm)
shaft_length      = 19;    // Länge des dünnen Vierkant-Abschnitts
shaft_root_size   = 9.5;   // Breite des kurzen, dickeren Ansatzes am Olivenkörper
shaft_root_length = 6;     // Länge dieses Ansatzes
shaft_tip_chamfer = 1.2;   // Fase an der Dornspitze zum leichteren Einführen
shaft_tilt_deg    = 10;    // Neigung des Dorns nach hinten (siehe Foto)
shaft_offset_x    = -8;    // Ansatzpunkt des Dorns, von der Olivenmitte Richtung Heck
dimple_radius     = 14;    // Radius der Kugel für die Mulde (groß = flacher Verlauf)
dimple_depth      = 2.2;   // tatsächliche Einsenktiefe der Mulde

$fn = 64;

module rounded_square(size, r) {
    hull() {
        for (dx = [-1, 1])
            for (dy = [-1, 1])
                translate([dx * (size / 2 - r), dy * (size / 2 - r)])
                    circle(r = r, $fn = 32);
    }
}

// Grundform: aus zwei ungleich großen, in Z flachgedrückten Kugeln gehüllte
// Tropfenform - bildet die außen konvexe, "olivenförmige" Silhouette nach.
module teardrop_dome(length, width, height, heel_r, tip_r) {
    zscale = height / width;
    hull() {
        translate([0, 0, 0])
            scale([1, 1, zscale]) sphere(r = heel_r);
        translate([-(length - heel_r - tip_r), 0, 0])
            scale([1, 1, zscale * (tip_r / heel_r) * 1.6]) sphere(r = tip_r);
    }
}

// Die Olive ist überwiegend massiv (glatte, konvexe Wölbung wie auf dem Foto).
// Nur am Ansatz des Vierkantdorns sitzt eine flache, muldenartige Vertiefung,
// wie sie auf dem Nahaufnahme-Foto zu erkennen ist.
module olive_body() {
    heel_r = paddle_width / 2;
    tip_r  = paddle_width * 0.09;

    difference() {
        translate([0, 0, paddle_height / 2])
            teardrop_dome(paddle_length, paddle_width, paddle_height, heel_r, tip_r);

        // flache Mulde um den Dornansatz: nur die Unterseite der Kugel
        // schneidet ein kleines Stück in die Oberfläche ein
        translate([shaft_offset_x, 0, paddle_height + dimple_radius - dimple_depth])
            scale([1.3, 1, 1])
                sphere(r = dimple_radius);
    }
}

module shaft() {
    root_r = shaft_root_size * 0.18;
    tip_len = shaft_length - shaft_tip_chamfer;

    translate([shaft_offset_x, 0, paddle_height * 0.62])
        rotate([0, shaft_tilt_deg, 0])
        union() {
            // kurzer, etwas dickerer Ansatz direkt an der Olive
            linear_extrude(height = shaft_root_length)
                rounded_square(shaft_root_size, root_r);

            // Vierkant-Betätigungsdorn
            translate([0, 0, shaft_root_length])
                linear_extrude(height = tip_len)
                    rounded_square(shaft_square, shaft_square * 0.12);

            // kleine Fase an der Spitze
            translate([0, 0, shaft_root_length + tip_len])
                cylinder(h = shaft_tip_chamfer, d1 = shaft_square * 1.15, d2 = shaft_square * 0.55, $fn = 4);
        }
}

module dreholive() {
    union() {
        olive_body();
        shaft();
    }
}

dreholive();
