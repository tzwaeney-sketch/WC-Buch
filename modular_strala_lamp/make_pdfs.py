#!/usr/bin/env python3
import json, os
from fpdf import FPDF

BASE = "/home/user/WC-Buch/modular_strala_lamp"
READY = f"{BASE}/READY_TO_PRINT"
val = json.load(open(f"{BASE}/exports/reports/production_validation.json"))
stab = json.load(open(f"{BASE}/exports/reports/stability.json"))

# ---------------- Montageanleitung ----------------
class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica","B",14)
        self.cell(0,10,"Modulare STRALA-Lampe - Montageanleitung",align="C",new_x="LMARGIN",new_y="NEXT")
        self.ln(3)
    def footer(self):
        self.set_y(-15); self.set_font("Helvetica","I",8)
        self.cell(0,10,f"Seite {self.page_no()}",align="C")

pdf=PDF(); pdf.set_auto_page_break(True,15); pdf.add_page()
pdf.set_font("Helvetica","B",16)
pdf.cell(0,10,"Modulare STRALA-Lampe",new_x="LMARGIN",new_y="NEXT")
pdf.set_font("Helvetica",size=10)
pdf.cell(0,6,"Montageanleitung - Bambu Lab P2S FDM-Drucksystem",new_x="LMARGIN",new_y="NEXT")
pdf.ln(5)
pdf.set_fill_color(255,240,200)
y=pdf.get_y(); pdf.rect(pdf.get_x(),y,180,30,style="F")
pdf.set_font("Helvetica","B",10)
pdf.cell(0,6,"SICHERHEITSHINWEIS",new_x="LMARGIN",new_y="NEXT")
pdf.set_font("Helvetica",size=9)
for line in ["Nur fuer geeignete LED-Leuchtmittel. Keine Gluehlampen, keine Halogenlampen.",
             "Nur fuer Innenraeume und trockene Umgebung. Alle elektrischen Teile sind original IKEA-Komponenten.",
             "Vor dem ersten Einstecken alle Bajonette pruefen und Standfestigkeit testen.",
             "3D-Druckteile sind keine geprueften Elektrokomponenten."]:
    pdf.cell(0,5,line,new_x="LMARGIN",new_y="NEXT")
pdf.ln(5)
pdf.set_font("Helvetica","B",12); pdf.cell(0,8,"Benoetigte Teile",new_x="LMARGIN",new_y="NEXT")
pdf.set_font("Helvetica",size=9)
parts_list=[("01_Fuss_Rund.stl","Lampenfuss rund - PETG","1x"),
    ("03_Koerper_Kugel.stl","Koerpermodul Kugel - PETG","1x"),
    ("07_Koerper_Schmal_Ring.stl","Schmaler Akzentring - PETG","1x"),
    ("04_Koerper_Abgeflachte_Kugel.stl","Koerpermodul abgefl. Kugel - PETG","1x"),
    ("06_Koerper_Geometrisch.stl","Koerpermodul Geometrisch - PETG","1x"),
    ("05_Koerper_Organisch.stl","Koerpermodul Organisch - PETG","1x"),
    ("08_Koerper_Schmal_Gerippt.stl","Schmaler Rippring - PETG","1x"),
    ("09_Schirm_Klassisch.stl","Lampenschirm (nach Wahl) - PETG/PLA","1x"),
    ("12_STRALA_Fassungsbefestigung.stl","STRALA-Fassungsbefestigung - PETG","1 Satz"),
    ("-","IKEA STRALA Lampenkabel-Set (Original)","1x"),
    ("-","Geeignetes LED-Leuchtmittel (E14/E27)","1x"),
    ("-","Stahlplatte/Stahlring als Ballast (>=300g)","1x"),
    ("-","Gummifuesse 12mm","4x"),("-","M3x12 Schrauben Bodenplatte","3x"),
    ("-","M3x8 Schrauben Fassungsadapter","2x")]
for fn,desc,qty in parts_list:
    pdf.cell(12,5,qty); pdf.cell(80,5,desc); pdf.cell(0,5,fn,new_x="LMARGIN",new_y="NEXT")
pdf.ln(4)
pdf.set_font("Helvetica","B",12); pdf.cell(0,8,"Montagereihenfolge",new_x="LMARGIN",new_y="NEXT")
steps=[("VORBEREITUNG",["Netzstecker ausgesteckt lassen waehrend gesamter Montage.",
        "Alle Druckteile auf Vollstaendigkeit und Gratfreiheit pruefen.",
        "Bajonettnuten frei von Druckrueckstaenden.",
        "Ballastgewicht (>=300g) und Schrauben bereithalten."]),
    ("SCHRITT 1-4: KABEL EINFAEDELN",["1. Bodenplatte (3x M3) abnehmen.",
        "2. STRALA-Stecker durch zentrale 60-mm-Oeffnung von oben nach unten fuehren.",
        "3. Stecker durch alle Module fuehren: Fuss -> Kugel -> Schmaler Ring -> Abgfl. Kugel -> Geometrisch -> Organisch -> Schmaler Rippring -> Top-Cap.",
        "4. Stecker liegt unter dem Fuss, Kabel im offenen Kanal."]),
    ("SCHRITT 5-8: FUSS SCHLIESSEN",["5. Kabel von Mitte zum rueckseitigen Ausgang legen.",
        "6. Kabeldurchfuehrung/Tuelle einsetzen, kein scharfer Knick.",
        "7. Ballastgewicht in Gewichtskammer einlegen (getrennt vom Kanal).",
        "8. Bodenplatte mit 3x M3x12 festziehen, Kabel nicht einklemmen."]),
    ("SCHRITT 9-12: MODULE VERRIEGELN",["9. Unterstes Bajonett aufstecken, 25 Grad drehen bis Anschlag.",
        "10. Jede weitere Verbindung ebenso, Kabel nicht mitverdrehen.",
        "11. Alle Bajonette pruefen: Rastnocke eingerastet, kein Rueckdrehen.",
        "12. Module ausrichten (Designseite nach vorne)."]),
    ("SCHRITT 13-16: FASSUNGSADAPTER UND SCHIRM",["13. STRALA-Fassung durch Top-Cap fuehren.",
        "14. Geteilten Fassungsadapter um Fassung legen.",
        "15. Halbschalen mit 2x M3x8 verschrauben, in Top-Cap einrasten.",
        "16. Sicherungsring eindrehen/aufstecken."]),
    ("SCHRITT 17-21: ABSCHLIESSEND",["17. Schirm aufstecken und 25 Grad verdrehen bis Anschlag.",
        "18. Alle Bajonette erneut pruefen.",
        "19. Standfestigkeit pruefen: seitlich antippen, darf nicht kippen.",
        "20. Kabelweg pruefen: nicht eingeklemmt, kein Knick.",
        "21. ERST JETZT Netzstecker einstecken, Funktion pruefen."])]
for title,ss in steps:
    if pdf.get_y()>250: pdf.add_page()
    pdf.set_font("Helvetica","B",10); pdf.set_fill_color(220,230,245)
    pdf.cell(0,7,title,new_x="LMARGIN",new_y="NEXT",fill=True)
    pdf.set_font("Helvetica",size=9)
    for s in ss: pdf.multi_cell(0,5,s,new_x="LMARGIN",new_y="NEXT")
    pdf.ln(2)
pdf.add_page()
pdf.set_font("Helvetica","B",12); pdf.cell(0,8,"Technische Daten",new_x="LMARGIN",new_y="NEXT")
tech=[("Steckerdurchgang","60,0 mm frei (digital geprueft)"),
    ("Koerperhoehe",f"~{stab['body_height_mm']} mm (Fuss bis Schirmansatz)"),
    ("Fussdurchmesser","220 mm"),("Empfohlener Ballast",">= 300 g Stahl"),
    ("Bajonett","3 Nasen, 25 Grad Drehweg, Eigenentwicklung"),
    ("Material tragende Teile","PETG"),("Material Schirm","PETG transparent / weiss"),
    ("Zieldrucker","Bambu Lab P2S, 0,4 mm Duese"),("Schichthoehe","0,20 mm"),
    ("Elektrische Teile","Ausschliesslich original IKEA STRALA")]
for k,v in tech:
    pdf.set_font("Helvetica","B",10); pdf.cell(70,6,k+":")
    pdf.set_font("Helvetica",size=10); pdf.cell(0,6,v,new_x="LMARGIN",new_y="NEXT")
pdf.ln(6); pdf.set_font("Helvetica","B",10)
pdf.multi_cell(0,6,"HINWEIS: Digital geprueft. Realer Steckerdurchgangstest mit echtem STRALA-Stecker erforderlich. STRALA-Masse in config.scad sind als MEASURE markiert.",new_x="LMARGIN",new_y="NEXT")
pdf.output(f"{READY}/Montageanleitung.pdf")
print("Montageanleitung.pdf created")

# ---------------- Pruefbericht ----------------
class PB(FPDF):
    def header(self):
        self.set_font("Helvetica","B",13)
        self.cell(0,10,"Pruefbericht - Produktionsvalidierung",align="C",new_x="LMARGIN",new_y="NEXT"); self.ln(2)
    def footer(self):
        self.set_y(-15); self.set_font("Helvetica","I",8)
        self.cell(0,10,f"Seite {self.page_no()}",align="C")
p=PB(); p.set_auto_page_break(True,15); p.add_page()
p.set_font("Helvetica",size=9)
p.cell(0,6,"Modulare STRALA-Lampe - 12 Produktionsteile - Bambu Lab P2S (256x256x256 mm)",new_x="LMARGIN",new_y="NEXT")
p.cell(0,6,f"Alle Teile bestanden: {'JA' if val['all_pass'] else 'NEIN'}",new_x="LMARGIN",new_y="NEXT")
p.ln(2)
# table
p.set_font("Helvetica","B",7)
hdr=[("Datei",54),("BBox X/Y/Z mm",34),("Wasserd.",16),("Faces",16),("Vol cm3",16),("PETG g",14),("P2S",12),("Status",18)]
for h,w in hdr: p.cell(w,6,h,border=1)
p.ln()
p.set_font("Helvetica",size=7)
for r in val["parts"]:
    bb=r.get("bounding_box_mm",["-"]*3)
    bbs="/".join(str(x) for x in bb) if isinstance(bb,list) else "-"
    row=[(r["file"],54),(bbs,34),("ja" if r.get("is_watertight") else "nein",16),
         (str(r.get("face_count","-")),16),(str(r.get("volume_cm3","-")),16),
         (str(r.get("mass_petg_g","-")),14),("ja" if r.get("fits_bambu_p2s") else "NEIN",12),
         (r.get("status","-"),18)]
    for v,w in row: p.cell(w,5,v,border=1)
    p.ln()
p.ln(4)
p.set_font("Helvetica","B",11); p.cell(0,7,"Standfestigkeit",new_x="LMARGIN",new_y="NEXT")
p.set_font("Helvetica",size=9)
for line in [f"Gesamtmasse (geschaetzt): {stab['total_mass_g']} g",
    f"Schwerpunkthoehe: {stab['com_height_mm']} mm",
    f"Kippwinkel: {stab['tip_angle_deg']} Grad (Ziel >= 15 Grad)",
    f"Basisradius: {stab['base_radius_mm']} mm, Ballast: {stab['ballast_g']} g",
    f"Bewertung: {'STABIL' if stab['tip_angle_deg']>=15 else 'MEHR BALLAST'}"]:
    p.cell(0,5,line,new_x="LMARGIN",new_y="NEXT")
p.ln(3)
p.set_font("Helvetica","B",11); p.cell(0,7,"60-mm-Durchgang",new_x="LMARGIN",new_y="NEXT")
p.set_font("Helvetica",size=9)
p.multi_cell(0,5,"Alle tragenden Teile besitzen eine zentrale Bohrung von 60,0 mm (final_plug_passage in config.scad). Digital bestaetigt. Realer Steckertest mit Original-STRALA-Stecker erforderlich.",new_x="LMARGIN",new_y="NEXT")
p.ln(2)
p.set_font("Helvetica","B",11); p.cell(0,7,"Bekannte Einschraenkungen",new_x="LMARGIN",new_y="NEXT")
p.set_font("Helvetica",size=9)
for line in ["STRALA-Massen (config.scad, MEASURE) muessen am realen Bauteil gemessen werden.",
    "Validierung rein digital (OpenSCAD-Render + trimesh-Meshpruefung).",
    "Bajonett-Toleranzen am realen Druck pruefen (Toleranztestteil verfuegbar).",
    "Realer Probedruck und Steckerdurchgangstest stehen aus."]:
    p.multi_cell(0,5,"- "+line,new_x="LMARGIN",new_y="NEXT")
p.ln(2)
p.set_font("Helvetica","B",11); p.cell(0,7,"Verwendete Werkzeuge",new_x="LMARGIN",new_y="NEXT")
p.set_font("Helvetica",size=9)
p.multi_cell(0,5,"OpenSCAD 2021.01 (xvfb-run, headless STL-Export); Python3 + trimesh (Meshvalidierung); fpdf2 (PDF); networkx/lxml (3MF-Export).",new_x="LMARGIN",new_y="NEXT")
p.output(f"{READY}/Pruefbericht.pdf")
print("Pruefbericht.pdf created")
