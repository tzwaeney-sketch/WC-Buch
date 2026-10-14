# 🎲 Toms Ausrede-Würfel – Geburtstagsgeschenk

Ein 45-mm-Würfel für alle Lebenslagen im Büro. Tom wird gefragt, ob er was erledigt? **Würfeln!**

| Seite | Text |
|---|---|
| 1 | BIN IM MEETING |
| 2 | WLAN KAPUTT |
| 3 | MORGEN VIELLEICHT |
| 4 | ERST KAFFEE |
| 5 | NICHT MEIN PROJEKT |
| 6 | HAPPY BDAY TOM! (der Joker) |

Dateien:
- **`ausrede-wuerfel-2farbig.3mf` – alles in einer Datei (Körper + Schrift als Teile) → einfach öffnen**
- `wuerfel-koerper.stl` – Würfel mit 1 mm tiefer Gravur (alleine = einfarbige Version)
- `wuerfel-text.stl` – Schrift-Einlage, füllt die Gravur exakt (2. Farbe)
- `ausrede-wuerfel.scad` – Quelle; Texte/Größe änderbar (`part = "body"` / `"text"`)

## 🎨 Zweifarbig mit AMS (Bambu Studio)
1. `ausrede-wuerfel-2farbig.3mf` öffnen – Körper und Text sind schon ein Objekt mit zwei Teilen.
   (Alternativ beide STLs zusammen importieren und „als ein Objekt mit mehreren Teilen laden?" mit **Ja** beantworten.)
2. Falls Bambu Studio fragt, ob es eine Datei eines anderen Slicers ist: nur Geometrie laden ist okay.
3. In der Objektliste: Körper → Filament 1 (z. B. **Gelb/Orange**), Text → Filament 2 (**Schwarz**).
4. Würfel nicht drehen/neu ausrichten – liegt bereits richtig („BIN IM MEETING" oben).
5. Einstellungen zum Sparen von Zeit und Abfall:
   - **Prime Tower**: an (Breite 35 mm)
   - **Spülen in Infill des Objekts**: an („Flush into objects' infill")
   - **Spülmengen**: Bambu-Automatik, dann Multiplikator **0,8**
   - Helle Körperfarbe + dunkle Schrift wählen – von Schwarz zurück auf Hell spülen kostet sonst viel.
6. Farbwechsel passieren nur im Textbereich (mittleres Drittel der Höhe + erste/letzte 6 Schichten).
   Rechne mit ca. **5–6 h** Druckzeit und ca. **15–25 g** Abfall statt 3 h einfarbig.
   Tipp: Schichthöhe **0,2 mm** statt 0,16 spart ca. 20 % Farbwechsel; Schrift bleibt trotzdem gut lesbar.

Das Ausmalen mit Farbe (siehe unten) entfällt bei der AMS-Version.

## Druckeinstellungen (PLA, z. B. Bambu/Prusa/Creality)

| Einstellung | Wert |
|---|---|
| Material | PLA (Tipp: Gelb/Orange + Schwarz, oder Silk-Gold + Schwarz) |
| Düse | 0,4 mm |
| Schichthöhe | 0,16 mm (Gravur wird sauberer als bei 0,2) |
| Erste Schicht | 0,2 mm |
| Wände/Perimeter | 3 |
| Ober-/Unterschichten | 5 / 4 |
| Infill | 15 % Gyroid |
| Düsentemperatur | 210 °C |
| Betttemperatur | 60 °C |
| Geschwindigkeit | 60 mm/s außen, 100 mm/s innen |
| Kühlung | 100 % ab Schicht 3 |
| Stützstrukturen | **keine** |
| Haftung | keine (Brim nur bei schlechter Betthaftung, 3 mm) |
| Naht | „Hinten" / Ausgerichtet an Kante |
| Ausrichtung | flach auf eine Seite legen (z. B. „HAPPY BDAY TOM!" nach oben) |

Druckzeit ca. 3–3,5 h, ca. 35–40 g Filament.

## Finish für die einfarbige Version
1. Gravuren (1 mm tief) mit Acrylfarbe in Kontrastfarbe ausmalen (schwarz auf gold, weiß auf orange).
2. Sofort mit einem Tuch/Küchenpapier mit etwas Spiritus flach über die Oberfläche wischen → Farbe bleibt nur in den Buchstaben.
3. Optional: Klarlack drüber.

## Verpackung-Idee
Kleine Karte dazu: *„Für alle Fragen, auf die du keine Lust hast. Alles Gute, Tom! 🎂"*
