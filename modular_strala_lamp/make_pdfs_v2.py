#!/usr/bin/env python3
"""Generate Pruefbericht_V2.pdf and Montageanleitung_V2.pdf from validation_v2.json."""
import json, os
from fpdf import FPDF

BASE = os.path.dirname(os.path.abspath(__file__))
OUT  = f"{BASE}/READY_TO_PRINT_V2"
val  = json.load(open(f"{BASE}/validation_v2.json"))
parts = val["parts"]

# ---- bayonet summary (from config) ----
BAY = {
    "lug_inner_r": 33.5, "lug_outer_r": 37.0, "interface_d": 80.0,
    "lock_arc_deg": 25, "entry_arc_deg": 30, "lug_arc_deg": 22,
    "lug_axial_h": 2.8, "snap_step_mm": 0.5, "snap_ramp_deg": 4,
    "clearance_mm": 0.30, "lug_count": 3,
}

# ---- stability estimate ----
# rough PLA density ~1.24 g/cm3 = 0.00124 g/mm3, infill ~20% effective
DENS = 0.00124
INFILL = 0.30
def mass_g(v): return v*DENS*INFILL
total_mass = sum(mass_g(p.get("volume_mm3",0)) for p in parts)
# base mass dominates CoM low; estimate CoM at ~ 35% of stack height
stack_h = 45 + 80 + 70 + 200  # base + 1-2 bodies + shade approx
com_h = stack_h*0.38
base_radius = 110.0
import math
tip_angle = math.degrees(math.atan(base_radius/com_h))

def status_color(pdf, s):
    pdf.set_text_color(0,120,0) if s=="PASS" else pdf.set_text_color(180,0,0)

# ================= Pruefbericht =================
class RP(FPDF):
    def header(self):
        self.set_font("Helvetica","B",13)
        self.cell(0,9,"Modulare STRALA-Lampe V2 - Pruefbericht",align="C",new_x="LMARGIN",new_y="NEXT")
        self.set_font("Helvetica","",8); self.set_text_color(90,90,90)
        self.cell(0,5,"Snap-Bajonett System | Bambu Lab P2S | Stand 2026-06-18",align="C",new_x="LMARGIN",new_y="NEXT")
        self.set_text_color(0,0,0); self.ln(2)
    def footer(self):
        self.set_y(-12); self.set_font("Helvetica","I",7)
        self.cell(0,8,f"Seite {self.page_no()}",align="C")

pdf=RP(); pdf.set_auto_page_break(True,14); pdf.add_page()

pdf.set_font("Helvetica","B",10)
pdf.cell(0,7,f"Gesamtergebnis: {'ALLE BESTANDEN' if val['all_pass'] else 'FEHLER VORHANDEN'}  ({val['count']} Teile)",
         new_x="LMARGIN",new_y="NEXT")
pdf.ln(1)

for p in parts:
    pdf.set_font("Helvetica","B",10); pdf.set_text_color(0,0,0)
    pdf.cell(0,6,p["file"],new_x="LMARGIN",new_y="NEXT")
    pdf.set_font("Helvetica","",8)
    rows = [
        ("Dateigroesse", f"{p.get('size_bytes',0):,} B"),
        ("Faces", f"{p.get('faces','-')}"),
        ("Bounding Box (XYZ)", f"{p.get('bbox_mm','-')} mm"),
        ("Volumen", f"{p.get('volume_mm3','-')} mm3"),
        ("Wasserdicht", "JA" if p.get('watertight') else "NEIN"),
        ("Komponenten", f"{p.get('components','-')}"),
        ("Durchgang >=60mm bestaetigt", "JA" if p.get('bore_passage_ok') else "NEIN"),
        ("Bajonett Snap vorhanden", "JA" if p.get('bayonet_snap_present') else "NEIN"),
        ("Passt P2S (256mm)", "JA" if p.get('fits_P2S') else "NEIN"),
    ]
    for k,v in rows:
        pdf.cell(70,5,f"  {k}",border=0)
        pdf.cell(0,5,str(v),new_x="LMARGIN",new_y="NEXT")
    pdf.set_font("Helvetica","B",9); status_color(pdf,p["status"])
    pdf.cell(0,6,f"  STATUS: {p['status']}",new_x="LMARGIN",new_y="NEXT")
    pdf.set_text_color(0,0,0); pdf.ln(1)

# Bayonet summary table
pdf.add_page(); pdf.set_font("Helvetica","B",11)
pdf.cell(0,8,"Bajonett-Spezifikation",new_x="LMARGIN",new_y="NEXT"); pdf.ln(1)
pdf.set_font("Helvetica","",9)
for k,v in BAY.items():
    pdf.cell(80,6,k,border=1); pdf.cell(40,6,str(v),border=1,new_x="LMARGIN",new_y="NEXT")

pdf.ln(4); pdf.set_font("Helvetica","B",11)
pdf.cell(0,8,"Standsicherheit (Schaetzung)",new_x="LMARGIN",new_y="NEXT"); pdf.set_font("Helvetica","",9)
for k,v in [("Geschaetzte Gesamtmasse",f"{total_mass:.0f} g"),
            ("Geschaetzte Stapelhoehe",f"{stack_h:.0f} mm"),
            ("Geschaetzte Schwerpunkthoehe",f"{com_h:.0f} mm"),
            ("Basisradius",f"{base_radius:.0f} mm"),
            ("Kippwinkel",f"{tip_angle:.1f} deg (Anforderung >=15 deg: {'OK' if tip_angle>=15 else 'FAIL'})")]:
    pdf.cell(80,6,k,border=1); pdf.cell(60,6,v,border=1,new_x="LMARGIN",new_y="NEXT")

pdf.output(f"{OUT}/Pruefbericht_V2.pdf")
print("wrote Pruefbericht_V2.pdf")

# ================= Montageanleitung =================
class MA(FPDF):
    def header(self):
        self.set_font("Helvetica","B",13)
        self.cell(0,9,"Modulare STRALA-Lampe V2 - Montageanleitung",align="C",new_x="LMARGIN",new_y="NEXT")
        self.ln(2)
    def footer(self):
        self.set_y(-12); self.set_font("Helvetica","I",7)
        self.cell(0,8,f"Seite {self.page_no()}",align="C")

steps = [
    "Alle 12 Teile auf Vollstaendigkeit und Druckqualitaet pruefen. Bohrung (60mm) muss frei sein.",
    "Bajonett-Flaechen entgraten. Lugs (Nocken) und Nuten muessen sauber sein.",
    "Vier Gummifuesse in die Taschen an der Unterseite des Fusses (01 oder 02) eindruecken.",
    "STRALA-Kabel von oben durch den Fuss fuehren - durch die 60mm Bohrung.",
    "Gewuenschte Gewichte in die Gewichtskammer des Fusses einlegen (Standsicherheit).",
    "Bodenplatte des Fusses montieren (falls separat) - Kabel im offenen Kabelkanal verlegen.",
    "Erstes Koerpermodul waehlen. Kabel durch dessen Bohrung fuehren.",
    "Bajonett verbinden: Modul AXIAL aufsetzen, bis die Nocken in die Einfuehrnuten gleiten.",
    "Die Einfuehr-Fase (Lead-in) zentriert die Teile automatisch - nicht verkanten.",
    "Modul im Uhrzeigersinn drehen (~25 Grad) bis der Endanschlag erreicht ist.",
    "Kurz vor dem Anschlag spuerbarer Widerstand (Snap-Rampe) - mit Nachdruck weiterdrehen.",
    "Hoerbarer/fuehlbarer KLICK = Nocke ist in die Snap-Mulde eingerastet. Verriegelt.",
    "Verriegelung pruefen: leichtes Zurueckdrehen muss spuerbar blockiert sein (Anti-Loesung).",
    "Weitere Koerpermodule nach gleichem Schema stapeln (Kabel jeweils mitfuehren).",
    "Gesamthoehe pruefen (Zielbereich ca. 570-630 mm Korpus).",
    "STRALA-Halterung (12) oben aufsetzen: axial einfuehren, drehen bis Snap-Klick.",
    "E27-Fassung von unten durch das Montageloch (26.6mm) der Halterung schieben.",
    "Fassungsschulter liegt an der Flansch-Unterseite an; Original-Schraubring von oben sichern.",
    "Leuchtmittel (E27) eindrehen. KEIN Kontakt zum Schirm sicherstellen.",
    "Schirm (09/10/11) auf den oberen Bajonett-Kragen der Halterung setzen und einrasten.",
]
pdf=MA(); pdf.set_auto_page_break(True,14); pdf.add_page()
pdf.set_font("Helvetica","",9)
pdf.multi_cell(0,5,"Hinweis zum Snap-Bajonett: Jede Verbindung hat Einfuehr-Fase, axialen "
    "Einfuehrweg, ca. 25 Grad Drehung, Endanschlag und eine Snap-Rastung gegen "
    "selbsttaetiges Loesen. Verbinden: Aufsetzen -> Drehen bis Klick.")
pdf.ln(2)
for i,s in enumerate(steps,1):
    pdf.set_font("Helvetica","B",10); pdf.set_text_color(20,20,120)
    pdf.cell(10,6,f"{i}.",new_x="RIGHT",new_y="TOP")
    pdf.set_font("Helvetica","",10); pdf.set_text_color(0,0,0)
    pdf.multi_cell(0,6,s)
    pdf.ln(0.5)
pdf.output(f"{OUT}/Montageanleitung_V2.pdf")
print("wrote Montageanleitung_V2.pdf")
