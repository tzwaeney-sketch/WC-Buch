#!/usr/bin/env bash
# Render all 12 v2 parts to READY_TO_PRINT_V2/
set -u
cd "$(dirname "$0")"
OS="xvfb-run -a openscad"
SCAD=openscad
OUT=READY_TO_PRINT_V2
mkdir -p "$OUT"

# name | scad file | part selector
render() {
  local stl="$1" file="$2" sel="$3"
  echo ">>> $stl  ($file part=$sel)"
  $OS -D "part=\"$sel\"" -o "$OUT/$stl" "$SCAD/$file" 2>&1 | grep -iE "error|warning|manifold" | head -3
  local sz=$(stat -c%s "$OUT/$stl" 2>/dev/null || echo 0)
  echo "    -> $sz bytes"
}

render 01_Fuss_Rund.stl            lamp_base_round_v2.scad  round
render 02_Fuss_Design.stl          lamp_base_design_v2.scad design
render 03_Koerper_Kugel.stl        round_modules_v2.scad    sphere
render 04_Koerper_Abgeflacht.stl   round_modules_v2.scad    flat
render 05_Koerper_Organisch.stl    round_modules_v2.scad    organic
render 06_Koerper_Geometrisch.stl  round_modules_v2.scad    geometric
render 07_Koerper_Schmal_Ring.stl  round_modules_v2.scad    ring
render 08_Koerper_Schmal_Gerippt.stl round_modules_v2.scad  ribbed
render 09_Schirm_Klassisch.stl     lamp_shades_v2.scad      classic
render 10_Schirm_Gerippt.stl       lamp_shades_v2.scad      ribbed
render 11_Schirm_Organisch.stl     lamp_shades_v2.scad      organic
render 12_STRALA_Befestigung.stl   strala_holder_v2.scad    holder

echo "=== render_all_v2 done ==="
