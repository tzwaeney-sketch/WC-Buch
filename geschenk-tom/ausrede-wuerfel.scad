// Tom's Ausrede-Würfel – Geburtstagsgeschenk
// Würfeln, wenn Tom eine Ausrede braucht.
size  = 45;     // Kantenlänge in mm
r     = 4;      // Kantenrundung
depth = 1.0;    // Gravurtiefe
font  = "DejaVu Sans:style=Bold";
maxw  = size - 10;   // nutzbare Textbreite

faces = [
  ["BIN IM",     "MEETING"],
  ["WLAN",       "KAPUTT"],
  ["MORGEN",     "VIELLEICHT"],
  ["ERST",       "KAFFEE"],
  ["NICHT MEIN", "PROJEKT"],
  ["HAPPY",      "BDAY TOM!"]
];

module label(l) {
  linear_extrude(depth + 0.01)
    for (i = [0:1])
      translate([0, i == 0 ? 4.5 : -6.5])
        resize([min(maxw, len(l[i]) * 4.6), 0], auto = true)
          text(l[i], size = 6.5, font = font, halign = "center", valign = "center");
}

// Ausrichtung je Fläche: Text liegt auf der Fläche, von außen lesbar
rots = [[0,0,0],[180,0,0],[90,0,0],[90,0,180],[90,0,90],[90,0,-90]];

// part = "body" (Würfel mit Gravur) | "text" (Einlage für 2. Farbe/AMS) | "all"
part = "all";

module rohling() { minkowski() { cube(size - 2*r, center = true); sphere(r, $fn = 32); } }
module texte() { for (k = [0:5]) rotate(rots[k]) translate([0, 0, size/2 - depth]) label(faces[k]); }

if (part == "body" || part == "all") difference() { rohling(); texte(); }
if (part == "text" || part == "all") color("black") intersection() { rohling(); texte(); }
