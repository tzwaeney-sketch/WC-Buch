# CHECKLIST – Technische Prüfung aller STL-Dateien

Prüfung automatisiert mit `trimesh` auf Basis des exportierten STL.  
Alle Dateien wurden mit CadQuery 2.7.0 und OCCT-Kernel generiert.

---

## Prüfkriterien

| Kriterium | Methode | Grenzwert |
|---|---|---|
| Watertight (geschlossenes Mesh) | `trimesh.is_watertight` | Muss True sein |
| Positives Volumen | `trimesh.volume > 0` | Muss > 0 cm³ |
| Passt in Bambu P2S Bauraum | BBox ≤ 256×256×256 mm | Alle Dimensionen ≤ 256 mm |
| Non-Manifold-Kanten | implizit via watertight | Keine erlaubt |
| Invertierte Normalen | implizit via watertight | Keine erlaubt |

---

## Ergebnisse

### Produkt 1 – KMFe-Nachtregal

| Datei | Watertight | Volumen | BBox (mm) | P2S-Bauraum | **Ergebnis** |
|---|---|---|---|---|---|
| `01_KMFe_Nachtregal_25mm.stl` | ✅ Ja | 156,1 cm³ | 147×130×59 | ✅ passt | **✅ PASS** |
| `01_KMFe_Nachtregal_30mm.stl` | ✅ Ja | 157,7 cm³ | 152×130×59 | ✅ passt | **✅ PASS** |
| `01_KMFe_Nachtregal_35mm.stl` | ✅ Ja | 159,2 cm³ | 157×130×59 | ✅ passt | **✅ PASS** |

**Wandstärken:** Hakenscenkel 4,0 mm | Regalboden 8,0 mm | Lippen 3,0 mm  
**Überhänge:** Keine Überhänge > 45° – kein Support nötig  
**Druckrichtung:** Regalboden liegt flach auf Druckbett – optimale Schichtausrichtung für Zugkräfte

---

### Produkt 2 – KMFe-KuehlClip

| Datei | Watertight | Volumen | BBox (mm) | P2S-Bauraum | **Ergebnis** |
|---|---|---|---|---|---|
| `02_KMFe_KuehlClip_18mm.stl` | ✅ Ja | 57,6 cm³ | 102×45×53 | ✅ passt | **✅ PASS** |
| `02_KMFe_KuehlClip_20mm.stl` | ✅ Ja | 57,9 cm³ | 102×45×54 | ✅ passt | **✅ PASS** |
| `02_KMFe_KuehlClip_22mm.stl` | ✅ Ja | 58,2 cm³ | 102×45×55 | ✅ passt | **✅ PASS** |

**Wandstärken:** U-Körper 3,5 mm | Haken 3,5 mm | Release-Tab 3,5 mm  
**Überhänge:** Einführungs-Fase am Haken < 45° – kein Support nötig  
**Druckrichtung:** Clip liegt mit U-Öffnung nach oben auf Druckbett

---

### Produkt 3 – KMFe-KlappenArm

| Datei | Watertight | Volumen | BBox (mm) | P2S-Bauraum | **Ergebnis** |
|---|---|---|---|---|---|
| `03a_KMFe_KlappenArm_Wandbuegel.stl` | ✅ Ja | 15,4 cm³ | 50×25×40 | ✅ passt | **✅ PASS** |
| `03b_KMFe_KlappenArm_Stuetzarm.stl` | ✅ Ja | 34,1 cm³ | 216×27×26 | ✅ passt | **✅ PASS** |

**Wandstärken:** Grundplatte 5,0 mm | Armkörper 6,0 mm | Ösen-Wandstärke 3,8 mm  
**Überhänge:** Keine Überhänge > 45° – kein Support nötig  
**Druckrichtung:** Wandbügel-Rückseite auf Druckbett | Arm flach auf Druckbett  
**Scharnier-Pin-Loch:** Ø 4,4 mm (M4 + 0,4 mm Spiel) – konsequent durch beide Ösen

---

### Produkt 4 – KMFe-Schubteiler

| Datei | Watertight | Volumen | BBox (mm) | P2S-Bauraum | **Ergebnis** |
|---|---|---|---|---|---|
| `04a_KMFe_Schubteiler_Laengsblatt_240mm.stl` | ✅ Ja | 42,0 cm³ | 240×5×60 | ✅ passt | **✅ PASS** |
| `04b_KMFe_Schubteiler_Querblatt_160mm.stl` | ✅ Ja | 28,2 cm³ | 160×5×60 | ✅ passt | **✅ PASS** |
| `04c_KMFe_Schubteiler_T_Verbinder.stl` | ✅ Ja | 8,1 cm³ | 30×32×60 | ✅ passt | **✅ PASS** |

**Wandstärken:** Blatt-Dicke 3,0 mm (≥ Minimalwert 2,0 mm – OK)  
**Steckschlitz:** 3,5 mm Weite – nimmt 3,0 mm Blatt-Stärke auf (0,5 mm Spiel – formschlüssig)  
**Überhänge:** Keine > 45° – kein Support nötig  
**Druckrichtung:** Alle Blätter flach liegend (60 mm als Z-Achse → maximale Schichtfestigkeit für Biegekräfte)

---

### Produkt 5 – KMFe-DuschClip

| Datei | Watertight | Volumen | BBox (mm) | P2S-Bauraum | **Ergebnis** |
|---|---|---|---|---|---|
| `05_KMFe_DuschClip_20mm.stl` | ✅ Ja | 110,8 cm³ | 120×55×109 | ✅ passt | **✅ PASS** |
| `05_KMFe_DuschClip_22mm.stl` | ✅ Ja | 111,3 cm³ | 120×55×111 | ✅ passt | **✅ PASS** |
| `05_KMFe_DuschClip_25mm.stl` | ✅ Ja | 112,2 cm³ | 120×55×114 | ✅ passt | **✅ PASS** |

**Wandstärken:** Clip-Wand 3,5 mm | Regalboden 6,0 mm | Becher-Wandstärke 3,5 mm  
**Überhänge:** Keine horizontalen Flächen ohne Unterstützung – kein Support nötig  
**Druckrichtung:** Clip-Rückwand flach auf Druckbett  
**Clip-Öffnung:** profile/2 mm breit (Einclipsen ohne Werkzeug, Verstärkungs-Nasen gegen Daueraufspreizen)

---

## Gesamtergebnis

| # | Produkt | Varianten | Bestanden |
|---|---|---|---|
| 1 | KMFe-Nachtregal | 3 | ✅ 3/3 |
| 2 | KMFe-KuehlClip | 3 | ✅ 3/3 |
| 3 | KMFe-KlappenArm | 2 Teile | ✅ 2/2 |
| 4 | KMFe-Schubteiler | 3 Typen | ✅ 3/3 |
| 5 | KMFe-DuschClip | 3 | ✅ 3/3 |
| **Gesamt** | **5 Produkte** | **14 STL-Dateien** | **✅ 14/14** |

---

## Manuelle Drucknachprüfung empfohlen

Diese Punkte können nur am gedruckten Teil geprüft werden:

- [ ] Clip-Spaltmaß (Produkt 1): Holm-Dicke gemessen und richtige Variante gewählt
- [ ] Türkantendicke (Produkt 2): Mit Schieblehre an Dometic-Türkante gemessen
- [ ] Außenklappen-Zarge (Produkt 3): Wandbügel-Schraubenabstand passt zur Zarge
- [ ] Schubladenmaße (Produkt 4): Längsblatt passt in Tiefe, Querblatt in Breite
- [ ] Alu-Profil-Außenmaß (Produkt 5): Profilgröße des Duschabteils gemessen

---

*Automatisch geprüft mit trimesh 4.x am Exporttag | CadQuery 2.7.0*
