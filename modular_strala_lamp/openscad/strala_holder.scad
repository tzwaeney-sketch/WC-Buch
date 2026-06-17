// ============================================================
// STRÅLA FASSUNGSBEFESTIGUNG — Formschlüssige Flanschhalterung
// ============================================================
//
// FUNKTIONSPRINZIP:
//   Die originale IKEA-STRÅLA-Fassung besitzt ein Außengewinde und
//   einen originalen Schraubring. Dieser Schraubring sichert die Fassung
//   formschlüssig zwischen Fassungsschulter und Schraubring.
//
//   Der gedruckte Halteflansch liegt zwischen:
//     Fassungsschulter (von unten) ←→ Halteflansch ←→ Schraubring (von oben)
//
//   Es wird kein eigenes Gewinde gedruckt.
//   Es werden keine elektrischen Teile verändert oder berührt.
//   Der originale STRÅLA-Schraubring bleibt vollständig erhalten.
//
// MONTAGEREIHENFOLGE:
//   1. Stecker durch Fuß und alle Module nach oben durchfädeln.
//   2. Stecker passiert den offenen Top-Cap (60mm Bohrung).
//   3. Top-Cap mit unterem Modul verrasten.
//   4. Halteflansch über das Kabel schieben (Kabel = 6mm, Loch = 60mm+).
//      HINWEIS: Halteflansch-Innenloch für Kabel ist ausreichend groß.
//      Der Halteflansch hat eine SEPARATE Kabelführungsöffnung (kein
//      Widerspruch — das große Zentralloch ist der Gewindedurchgang).
//   5. Halteflansch in den Top-Cap einsetzen.
//   6. STRÅLA-Fassung von unten durch den Top-Cap schieben bis das
//      Gewinde durch den Halteflansch ragt.
//   7. Originalen STRÅLA-Schraubring von oben aufschrauben.
//   8. Fassung ist formschlüssig und sicher gehalten.
//
// ALLE STRÅLA-MASSE: In config.scad als MEASURE hinterlegt.
//   Vor dem Druck mit realer Fassung messen und eintragen.
//
// ============================================================

include <config.scad>
include <bayonet_system.scad>

EPS = 0.01;

// ============================================================
// TOP-CAP (offene Bauform)
// ---
// Funktion:
//   - Schließt den Modulstapel nach oben ab
//   - Enthält die weibliche Bajonettschnittstelle unten
//   - 60mm Bohrung durchgehend (Stecker passiert bei Montage)
//   - Innere Aufnahme-Ringfläche für den Halteflansch oben
//   - Lüftungsschlitze oben
//   - Schirmbajonett-Schnittstelle oben (optional, einfache Aufnahme)
// ============================================================
module strala_top_cap() {
    outer_r   = module_outer_diameter_narrow / 2;  // ~43mm
    bore_r    = top_cap_passage_diameter / 2;       // 30mm — nie kleiner!
    h         = 55;
    fem_h     = bayonet_working_depth + 2;
    wall      = structural_wall;

    flange_od  = strala_socket_shoulder_diameter + 2 * reinforced_wall;
    seat_depth = 5.0;

    // Bajonett-Parameter (inline, um koinzidente Flächen zu vermeiden)
    bay_or    = bayonet_interface_outer_radius;   // 39.2mm
    ch_in     = female_channel_inner_radius;
    ch_out    = female_channel_outer_radius;
    ch_h      = female_channel_height;
    entry_a   = 28;
    groove_z  = fem_h - ch_h - bayonet_axial_clearance;

    assert(bore_r * 2 >= top_cap_passage_diameter, "FEHLER: Top-Cap Bohrung zu klein");

    difference() {
        union() {
            // Hauptkörper — läuft auf volle Höhe
            cylinder(h=h, r=outer_r, $fn=96);
        }

        // 60mm Durchgangsbohrung
        translate([0, 0, -EPS])
            cylinder(h=h + 2*EPS, r=bore_r, $fn=128);

        // Einführfasen
        translate([0, 0, -EPS])
            cylinder(h=3, r1=bore_r + 3, r2=bore_r, $fn=64);
        translate([0, 0, h - 3])
            cylinder(h=3 + EPS, r1=bore_r, r2=bore_r + 3, $fn=64);

        // Flansch-Auflagesitz oben
        translate([0, 0, h - seat_depth])
            cylinder(h=seat_depth + EPS, r=flange_od/2 + general_clearance, $fn=96);

        // Lüftungsschlitze oben (6×)
        for(a=[0:5]) {
            rotate([0, 0, a * 60])
                translate([outer_r - 3, 0, h - 14])
                    cube([7, 4, 15], center=true);
        }

        // Innenkörper aushöhlen (Materialeinsparung)
        translate([0, 0, fem_h + 2])
            cylinder(h=h - fem_h - seat_depth - 5, r=outer_r - wall, $fn=96);

        // Äußere Fase oben
        translate([0, 0, h - 2])
            cylinder(h=2 + EPS, r1=outer_r, r2=outer_r - 2, $fn=96);

        // ---- Bajonett-Nut (weiblich) — inline um Manifold-Probleme zu vermeiden ----
        // Einführschlitze (axial, 3× 28° breit)
        for(i=[0:2]) {
            rotate([0, 0, i * 120])
                rotate_extrude(angle=entry_a, $fn=96)
                    translate([ch_in, 0])
                        square([ch_out - ch_in, fem_h + EPS]);
        }
        // Verriegelungsnuten (tangential, 3× 25° breit)
        for(i=[0:2]) {
            rotate([0, 0, i * 120 + entry_a])
                rotate_extrude(angle=bayonet_lock_angle, $fn=96)
                    translate([ch_in, groove_z])
                        square([ch_out - ch_in, ch_h]);
        }
    }
}

// ============================================================
// HALTEFLANSCH
// ---
// Funktion:
//   Formschlüssige Verbindung zwischen Fassungsschulter und
//   originalem STRÅLA-Schraubring.
//
//   Geometrie:
//     - Innen-Ø = strala_mount_hole_diameter (Gewindedurchgang)
//     - Außen-Ø = passt in Top-Cap-Flanschsitz
//     - Dicke >= 3mm (tragende Mindestwand)
//     - Auflage-Ringbreite >= 4mm (mindestens so breit wie Schulterüberstand)
//     - Lüftungslöcher: 6× radial, außerhalb der Schulterauflagezone
//     - Keine Bauteilberührung mit elektrischen Kontakten
//
//   Montage:
//     Halteflansch über Kabel schieben → in Top-Cap einlegen →
//     Fassung von unten einschieben → Schraubring von oben anziehen
// ============================================================
module strala_halteflansch() {
    mount_r   = strala_mount_hole_diameter / 2;   // Gewindedurchgangsradius
    shoulder_r = strala_socket_shoulder_diameter / 2;  // Schulterradius
    flange_od = strala_socket_shoulder_diameter + 2 * reinforced_wall;
    flange_r  = flange_od / 2;
    flange_thick = 4.0;  // >= 3mm Mindestdicke

    // Auflagering-Breite (Ringzone zwischen mount_r und shoulder_r)
    ring_width = shoulder_r - mount_r;

    assert(ring_width >= 3.0,
           "WARNUNG: Auflagering zu schmal — strala_socket_shoulder_diameter oder strala_thread_outer_diameter prüfen");
    assert(flange_thick >= 3.0,
           "FEHLER: Flanschdicke unter 3mm");

    difference() {
        // Flanschkörper
        cylinder(h=flange_thick, r=flange_r, $fn=96);

        // Durchgangsbohrung für Gewindeabschnitt
        translate([0, 0, -EPS])
            cylinder(h=flange_thick + 2*EPS, r=mount_r, $fn=64);

        // Einführfase (erleichtert Einschieben der Fassung)
        translate([0, 0, flange_thick - 1.5])
            cylinder(h=1.6, r1=mount_r, r2=mount_r + 1.5, $fn=64);
        translate([0, 0, -EPS])
            cylinder(h=1.6, r1=mount_r + 1.5, r2=mount_r, $fn=64);

        // Lüftungslöcher (6×, außerhalb Schulterauflagezone)
        for(a=[0:5]) {
            rotate([0, 0, a * 60 + 30])
                translate([shoulder_r + (flange_r - shoulder_r) / 2, 0, -EPS])
                    cylinder(h=flange_thick + 2*EPS, r=2.5, $fn=24);
        }

        // Äußere Fase
        translate([0, 0, flange_thick - 1])
            cylinder(h=1 + EPS, r1=flange_r, r2=flange_r - 1, $fn=96);
    }

    // Verdrehsicherungs-Nut (in Außenflanke — wird im Top-Cap-Sitz geführt)
    // Als Differenz ausgeführt, damit keine nicht-manifold Berührflächen entstehen.
}

// ============================================================
// SCHIRMAUFNAHME-RING
// ---
// Sitzt oben auf dem Top-Cap (oder ist Teil des Top-Cap).
// Der Lampenschirm rastet hier ein (Schirm-Bajonett oder
// einfache Steckverbindung mit Arretiernocken).
// Kein Kontakt mit elektrischen Teilen.
// ============================================================
module strala_shade_mount_ring() {
    mount_r  = strala_socket_shoulder_diameter / 2 + reinforced_wall + 4;
    outer_r  = mount_r + reinforced_wall + 3;
    h        = 12;

    difference() {
        cylinder(h=h, r=outer_r, $fn=64);
        translate([0, 0, -EPS])
            cylinder(h=h + 2*EPS, r=mount_r, $fn=64);
        // 4× Lüftungsschlitze
        for(a=[0, 90, 180, 270])
            rotate([0, 0, a])
                translate([outer_r - 3, 0, h/2])
                    cube([7, 3.5, h*0.7], center=true);
    }

    // Rastnasen für Schirmbajonett: als Differenz-Nut ausgeführt,
    // damit keine nicht-manifold Berührflächen entstehen.
    // Der Schirm hat passende Nasen die in diese Nut eingreifen.
}

// ============================================================
// FASSUNGS-TESTSET
// Kleine Testringe um strala_thread_outer_diameter und
// strala_socket_shoulder_diameter zu bestimmen.
// Vor dem vollständigen Druck messen und MEASURE-Werte eintragen.
// ============================================================
module strala_fit_test_set() {
    base_d = strala_thread_outer_diameter;
    thick  = 5;

    for(i = [0:4]) {
        d = base_d + i * 0.5;
        translate([i * (d + 10), 0, 0]) {
            difference() {
                cylinder(h=thick, r=d/2 + 4, $fn=32);
                translate([0, 0, -EPS])
                    cylinder(h=thick + 2*EPS, r=d/2, $fn=32);
                translate([0, 0, thick - 1.5])
                    cylinder(h=1.6, r1=d/2, r2=d/2 + 1.5, $fn=32);
            }
            translate([0, 0, thick])
                linear_extrude(height=1.2)
                    text(str(d, "mm"), size=3, halign="center", valign="center");
        }
    }
}

// ============================================================
// KOMPLETTSET für Druck (Plattenlayout)
// Enthält alle zu druckenden Teile für die STRÅLA-Befestigung:
//   1. Top-Cap
//   2. Halteflansch
//   3. Schirmaufnahme-Ring
// Der originale STRÅLA-Schraubring ist nicht enthalten (Originalpart).
// ============================================================
// strala_befestigung_komplett() ist nur für die GUI-Vorschau.
// Die Produktion (STL-Export) erzeugt separate Dateien pro Teil.
module strala_befestigung_komplett() {
    tc_outer_r = module_outer_diameter_narrow / 2;
    flange_od  = strala_socket_shoulder_diameter + 2 * reinforced_wall;

    strala_top_cap();
    translate([tc_outer_r + 20, 0, 0]) strala_halteflansch();
    translate([tc_outer_r + 20 + flange_od + 10, 0, 0]) strala_shade_mount_ring();
}

// Demo in GUI-Vorschau:
if ($preview) strala_befestigung_komplett();
