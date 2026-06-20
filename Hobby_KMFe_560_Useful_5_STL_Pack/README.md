# Hobby KMFe 560 – Useful 5 STL-Pack

Fünf speziell für den **Hobby KMFe 560** entwickelte, druckfertige 3D-Bauteile.  
Alle Teile wurden mit CadQuery konstruiert, auf watertight-Mesh geprüft und auf den Bambu Lab P2S abgestimmt.

---

## Grundriss-Referenz Hobby KMFe 560

| Bereich | Details |
|---|---|
| Vorne | Dinette / Umbau-Doppelbett |
| Mitte links | Küche (Herd, Spüle, Kühlschrank Dometic RML 9430) |
| Mitte rechts | Bad (Thetford WC, Dusche, Spiegel) |
| Hinten | Kinderzimmer mit Etagenbett (oben/unten), Trennvorhang |
| Außen | Klappen: CEE-Strom, Gas, Stauraum |

---

## PRODUKT 1 – KMFe-Nachtregal

**Datei:** `01_KMFe_Nachtregal_25mm.stl` / `_30mm.stl` / `_35mm.stl`

### Zweck
Clip-Ablage für das Etagenbett im hinteren Kinderzimmer des KMFe 560.  
Hängt ohne Schrauben oder Kleber über den Sicherungsholm des Oberbetts.  
Bietet Platz für Handy (Schlitz im Boden), Brille, Buch, kleine Wasserflasche.

### Einbauort im KMFe 560
Oberes Etagenbett im Heckabteil. Der horizontale Sicherungsholm läuft quer über die Schlafbreite.

### Maße am Wohnwagen prüfen
- **Holm-Dicke (vertikal):** Mit Messschieber messen → Variante wählen:
  - 25 mm → `_25mm.stl`
  - 30 mm → `_30mm.stl`
  - 35 mm → `_35mm.stl`
- Clip-Spiel: 1,0 mm (hängt rutschfest, trotzdem abnehmbar)
- Holm-Tiefe (horizontal): unkritisch, Haken greift nur 20 mm tief

### Druckmaterial
PETG (empfohlen) oder ASA

### Empfohlene Druckeinstellungen
| Parameter | Wert |
|---|---|
| Schichthöhe | 0,20 mm |
| Perimeter | 3 |
| Infill | 25 % Gyroid |
| Druckrichtung | Regalboden liegt flach auf Druckbett |
| Support | keiner nötig |
| Düse | 0,4 mm |

### Druckzeit (geschätzt)
ca. 3,5–4,0 h (je Variante)

### Montage
1. Richtige Variante (25/30/35 mm) wählen.
2. Clip von der Außenseite des Holms aufsetzen, kurzen Schenkel außen, langer Schenkel innen.
3. Einrasten – der Querriegel unten verhindert Abrutschen.
4. Keine weiteren Schritte erforderlich.

### Benötigte Zusatzteile
Keine.

### Toleranz eingebaut
1,0 mm Spiel auf Holm-Dicke (PETG kann minimal quellen).

---

## PRODUKT 2 – KMFe-KuehlClip

**Datei:** `02_KMFe_KuehlClip_18mm.stl` / `_20mm.stl` / `_22mm.stl`

### Zweck
Fahrtschutz-Clip für die Kühlschranktür (Dometic RML 9430 oder Thetford N-Serie).  
Verhindert das unbeabsichtigte Öffnen der Kühlschranktür durch Fahrvibrationen.  
Wird in Fahrtstellung aufgesteckt, am Stellplatz mit einem Fingerdruck abgenommen.

### Einbauort im KMFe 560
Kühlschrank-Türkante, linker Mittelbereich der Küche.

### Maße am Wohnwagen prüfen
- **Türkantendicke inkl. Dichtlippe (oben oder seitlich):**
  - 18 mm → `_18mm.stl`
  - 20 mm → `_20mm.stl`
  - 22 mm → `_22mm.stl`
- Clip-Länge (Kontaktfläche): 90 mm (passt an jeder Standard-Kühlschranktür)
- Haken-Tiefe: 18 mm (greift hinter Türrahmen-Kante)

### Druckmaterial
PETG (Flex-Effekt für Release-Tab nötig) – **kein ASA** (zu steif für Tab)

### Empfohlene Druckeinstellungen
| Parameter | Wert |
|---|---|
| Schichthöhe | 0,20 mm |
| Perimeter | 4 |
| Infill | 30 % |
| Druckrichtung | Clip-Öffnung zeigt nach oben (liegend) |
| Support | keiner nötig |

### Druckzeit (geschätzt)
ca. 2,0–2,5 h (je Variante)

### Montage
1. Clip auf die Türkante (oben oder seitlich) aufschieben.
2. Oberer Haken hinterhakt am Türrahmen → klemmt sicher.
3. Abnehmen: Tab am unteren Ende mit Daumen nach unten drücken → Clip springt ab.

### Benötigte Zusatzteile
Keine.

### Toleranz eingebaut
0,4 mm Spiel auf Türkantendicke + 18 mm Haken-Tiefe mit 45°-Einführfase.

---

## PRODUKT 3 – KMFe-KlappenArm

**Dateien:** `03a_KMFe_KlappenArm_Wandbuegel.stl` + `03b_KMFe_KlappenArm_Stuetzarm.stl`

### Zweck
Klapp-Stützarm-System für Außenklappen des KMFe 560.  
Klappe öffnet, Arm schwenkt aus der Wandhalterung, hält Klappe dauerhaft bei ~90° offen.  
Beides-Hände-frei beim Kabelanschließen, Wasseranschluss, Staufach-Zugriff.

### Einbauort im KMFe 560
Außenklappen: CEE-Strom-Klappe (vorne links), Gas-Klappe (vorne rechts), Stauraum-Klappen (seitlich).  
Wandbügel wird an der Klappen-Innenzarge montiert.

### Maße am Wohnwagen prüfen
- **Klappen-Zargen-Breite:** Typisch 15–20 mm Alu (Wandbügel-Schrauben passen auf alle gängigen Zargen)
- **Klappen-Öffnungswinkel:** Armlänge 210 mm für ~90°-Stellung ausgelegt
- Haken am Armende: greift 13 mm tief unter Klappenkante (unkritisch, nur Abstützfunktion)

### Druckmaterial
ASA (Außeneinsatz, UV-beständig und wärmeformstabil) oder PETG

### Empfohlene Druckeinstellungen
| Parameter | Wert |
|---|---|
| Schichthöhe | 0,20 mm |
| Perimeter | 4 |
| Infill | 35 % (Stützarm), 40 % (Wandbügel) |
| Druckrichtung | Beide Teile flach auf Druckbett |
| Support | keiner nötig |

### Druckzeit (geschätzt)
Wandbügel: ca. 1,0 h | Stützarm: ca. 1,5 h

### Montage
1. Wandbügel an Klappen-Innenzarge mit 2× Holzschraube 4×20 mm befestigen.
2. Stützarm mit M4-Schraube (25 mm) + Mutter durch Scharnier-Ösen fädeln – leicht anziehen (Arm muss schwenken können).
3. Arm in eingeklappter Stellung hängt flach am Wandbügel.
4. Beim Klappenöffnen: Arm aushaken, Klappe aufstützen, Haken am Armende unter Klappenkante legen.

### Benötigte Zusatzteile
- 2× Holzschraube 4×20 mm (oder 4×25 mm)
- 1× M4-Schraube 25 mm + M4-Mutter + 2× M4-Unterlegscheibe

### Toleranz eingebaut
Scharnier-Öse: Ø 4,4 mm für M4-Bolzen (0,4 mm Spiel für freie Schwenkbewegung).

---

## PRODUKT 4 – KMFe-Schubteiler

**Dateien:**
- `04a_KMFe_Schubteiler_Laengsblatt_240mm.stl` (2× drucken)
- `04b_KMFe_Schubteiler_Querblatt_160mm.stl` (2× drucken)
- `04c_KMFe_Schubteiler_T_Verbinder.stl` (4× drucken)

### Zweck
Modulare Küchen-Schubladenorganisation für die Hobby-KMFe-560-Küche.  
Steckbares System ohne Klebstoff – Blätter + T-Verbinder ergeben beliebige Raster.  
Anti-Rutsch-Noppen auf der Unterkante halten das System in der Schublade.

### Einbauort im KMFe 560
Küchenschubladen (Besteck, Gewürze, Küchenhelfer). Typische KMFe-560-Schubladenmaße innen: ~350×260×65 mm.

### Maße am Wohnwagen prüfen
- **Schubladen-Innentiefe:** Längsblatt 240 mm muss mit 5–10 mm Luft passen (ggf. kürzen oder Länge vor Druck anpassen)
- **Schubladen-Innenbreite:** Querblatt 160 mm muss quer passen (mehrere drucken für komplettes Raster)
- **Schubladen-Innenhöhe:** Blatt-Höhe 60 mm (5 mm Luft bei 65 mm Schrankfach)

### Druckmaterial
PETG (lebensmittelnahe Umgebung, hitzeformstabil bei Küchentemperaturen)

### Empfohlene Druckeinstellungen
| Parameter | Wert |
|---|---|
| Schichthöhe | 0,20 mm |
| Perimeter | 3 |
| Infill | 20 % (Blätter sind ohnehin dünnwandig) |
| Druckrichtung | Alle Teile flach (60 mm Höhe als Z-Achse) |
| Support | keiner nötig |

### Druckzeit (geschätzt)
Längsblatt: ca. 1,2 h | Querblatt: ca. 0,8 h | T-Verbinder: ca. 0,5 h

### Montage
1. Längsblätter parallel in die Schublade stellen (entlang der Schubladenachse).
2. Querblatt durch die Schlitze der Längsblätter stecken.
3. T-Verbinder bei Kreuzungspunkten einstecken – Zahn rastet hörbar ein.
4. Anti-Rutsch-Noppen liegen auf Schubladen-Boden auf.

### Benötigte Zusatzteile
Keine.

### Toleranz eingebaut
Schlitz-Weite 3,5 mm / Blatt-Stärke 3,0 mm → 0,5 mm Spiel. Leichter Klemmsitz über Zahn-Rastnase am T-Verbinder.

---

## PRODUKT 5 – KMFe-DuschClip

**Datei:** `05_KMFe_DuschClip_20mm.stl` / `_22mm.stl` / `_25mm.stl`

### Zweck
Duschregal-Clip für das Bad-Duschabteil des KMFe 560.  
Klemmt werkzeuglos auf das quadratische Alu-Rahmenprofil der Duschwand.  
Trägt ein Regal mit 2 runden Fächern (Ø 44 mm) für Shampoo und Seife.  
Kein Bohren, kein Kleben, kein Beschädigen der Wohnwand.

### Einbauort im KMFe 560
Alu-Senkrecht-Profil an der Duschwandecke oder am seitlichen Duschabtrennrahmen (Bad, rechte Mittelzone).

### Maße am Wohnwagen prüfen
- **Alu-Profil-Außenmaß (Vierkant):**
  - 20 mm → `_20mm.stl` (häufigste Variante bei Hobby-Modellen)
  - 22 mm → `_22mm.stl`
  - 25 mm → `_25mm.stl`
- Clip-Höhe (Kontaktlänge am Profil): 40 mm
- Öffnungsschlitz: profile/2 mm (Einclipsen durch seitliches Aufdrücken)

### Druckmaterial
PETG (leichter Flex für Clip-Öffnung, feuchtigkeitsbeständig)  
**Kein ASA im Innenbereich nötig.**

### Empfohlene Druckeinstellungen
| Parameter | Wert |
|---|---|
| Schichthöhe | 0,20 mm |
| Perimeter | 4 |
| Infill | 30 % |
| Druckrichtung | Clip-Rückwand liegt auf Druckbett (nach Rotation: flach) |
| Support | keiner nötig |

### Druckzeit (geschätzt)
ca. 3,5–4,0 h (je Variante)

### Montage
1. Clip-Öffnung an Alu-Profil ansetzen.
2. Mit gleichmäßigem Druck aufdrücken – Clip schnappt ein.
3. Regal in gewünschter Höhe positionieren.
4. Fächer aufstellen: Shampoo / Seife / Rasierer.
5. Abnehmen: Clip-Öffnung mit Daumen auseinanderdrücken, abziehen.

### Benötigte Zusatzteile
Keine.

### Toleranz eingebaut
Clip-Innenlichtmaß = Profil + 0,3 mm (PETG-Untermaß für Klemmsitz).  
Verstärkungs-Nasen an der Öffnungskante verhindern dauerhaftes Aufspreizen.

---

## Dateiübersicht

| Datei | Produkt | Variante | Druckzeit | Material |
|---|---|---|---|---|
| `01_KMFe_Nachtregal_25mm.stl` | Nachtregal | Holm 25 mm | ~3,5 h | PETG |
| `01_KMFe_Nachtregal_30mm.stl` | Nachtregal | Holm 30 mm | ~3,5 h | PETG |
| `01_KMFe_Nachtregal_35mm.stl` | Nachtregal | Holm 35 mm | ~3,5 h | PETG |
| `02_KMFe_KuehlClip_18mm.stl` | KuehlClip | Tür 18 mm | ~2,0 h | PETG |
| `02_KMFe_KuehlClip_20mm.stl` | KuehlClip | Tür 20 mm | ~2,0 h | PETG |
| `02_KMFe_KuehlClip_22mm.stl` | KuehlClip | Tür 22 mm | ~2,0 h | PETG |
| `03a_KMFe_KlappenArm_Wandbuegel.stl` | KlappenArm | Wandbügel | ~1,0 h | ASA |
| `03b_KMFe_KlappenArm_Stuetzarm.stl` | KlappenArm | Stützarm | ~1,5 h | ASA |
| `04a_KMFe_Schubteiler_Laengsblatt_240mm.stl` | Schubteiler | Längsblatt 240 mm | ~1,2 h | PETG |
| `04b_KMFe_Schubteiler_Querblatt_160mm.stl` | Schubteiler | Querblatt 160 mm | ~0,8 h | PETG |
| `04c_KMFe_Schubteiler_T_Verbinder.stl` | Schubteiler | T-Verbinder | ~0,5 h | PETG |
| `05_KMFe_DuschClip_20mm.stl` | DuschClip | Profil 20 mm | ~3,5 h | PETG |
| `05_KMFe_DuschClip_22mm.stl` | DuschClip | Profil 22 mm | ~3,5 h | PETG |
| `05_KMFe_DuschClip_25mm.stl` | DuschClip | Profil 25 mm | ~3,5 h | PETG |

---

## Wichtige Hinweise vor dem Druck

1. **Variante messen:** Jedes Maß am echten Wohnwagen mit Messschieber prüfen, dann passende STL wählen.
2. **Bambu Studio:** STL öffnen → automatische Druckausrichtung sollte bereits korrekt sein (Teile wurden so ausgerichtet exportiert).
3. **Erstdruck:** Empfohlen zuerst eine Testversion in PLA drucken um Passgenauigkeit zu verifizieren, danach in PETG/ASA.
4. **ASA außen:** Für alle Außenteile (Produkt 3) ASA verwenden – PETG verliert bei Dauertemperaturen >60°C (Sommer, Sonneneinstrahlung) die Form.
5. **Keine sicherheitskritischen Teile:** Alle Produkte sind Komfort-Zubehör ohne Funktion an Fahrwerk, Bremse, Gas, 230 V oder tragender Struktur.

---

*Konstruiert mit CadQuery 2.7.0 | Validiert mit trimesh | Spezifisch für Hobby KMFe 560*
