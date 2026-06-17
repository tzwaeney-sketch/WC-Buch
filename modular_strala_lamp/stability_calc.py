#!/usr/bin/env python3
import math

BASE_RADIUS_MM = 110
BODY_HEIGHT_MM = 616
SHADE_HEIGHT_MM = 212
BASE_HEIGHT = 45

MASS_BASE_PRINTED = 350
MASS_BASE_BALLAST = 300
MASS_MODULES_TOTAL = 400
MASS_STRALA = 150
MASS_SHADE = 120

CoM_BASE = 22
CoM_base_assembly = ((MASS_BASE_PRINTED*CoM_BASE + MASS_BASE_BALLAST*CoM_BASE) /
                     (MASS_BASE_PRINTED + MASS_BASE_BALLAST))
CoM_body  = BASE_HEIGHT + BODY_HEIGHT_MM*0.55
CoM_shade = BASE_HEIGHT + BODY_HEIGHT_MM + SHADE_HEIGHT_MM*0.4
CoM_strala = BASE_HEIGHT + BODY_HEIGHT_MM

total_mass = MASS_BASE_PRINTED+MASS_BASE_BALLAST+MASS_MODULES_TOTAL+MASS_STRALA+MASS_SHADE
CoM_total = ((MASS_BASE_PRINTED+MASS_BASE_BALLAST)*CoM_base_assembly +
             MASS_MODULES_TOTAL*CoM_body + MASS_STRALA*CoM_strala +
             MASS_SHADE*CoM_shade) / total_mass

tip = math.degrees(math.atan(BASE_RADIUS_MM/CoM_total))
print(f"Total mass: {total_mass}g")
print(f"Center of mass height: {CoM_total:.0f}mm")
print(f"Tip angle: {tip:.1f} deg")
print(f"Recommendation: {'OK - safe' if tip>=15 else 'ADD MORE BALLAST'}")
extra = max(0, total_mass*CoM_total/BASE_RADIUS_MM*math.tan(math.radians(15)) - MASS_BASE_BALLAST)
print(f"Min ballast for 15deg: {extra:.0f}g additional")

import json
json.dump({"total_mass_g":total_mass,"com_height_mm":round(CoM_total,1),
           "tip_angle_deg":round(tip,1),"base_radius_mm":BASE_RADIUS_MM,
           "ballast_g":MASS_BASE_BALLAST,"body_height_mm":BODY_HEIGHT_MM,
           "additional_ballast_g":round(extra,0)},
          open("/home/user/WC-Buch/modular_strala_lamp/exports/reports/stability.json","w"), indent=2)
