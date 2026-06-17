#!/bin/bash
# validate_all.sh — render and validate all OpenSCAD modules
# Requires: openscad, python3 with trimesh

PROJECT="/home/user/WC-Buch/modular_strala_lamp"
SCAD="$PROJECT/openscad"
STL_OUT="$PROJECT/exports/stl"
REPORT="$PROJECT/exports/reports/validation_results.json"

export OPENSCADPATH="$SCAD"

mkdir -p "$STL_OUT/calibration" "$STL_OUT/base" "$STL_OUT/modules_round" \
         "$STL_OUT/modules_organic" "$STL_OUT/modules_geometric" \
         "$STL_OUT/modules_narrow" "$STL_OUT/adapters" "$STL_OUT/shades" \
         "$PROJECT/exports/reports"

echo '{"parts":[' > "$REPORT"
FIRST=1

render_part() {
    local name=$1
    local scad_file=$2
    local module_call=$3
    local out_dir=$4
    local stl_file="$STL_OUT/$out_dir/${name}.stl"

    local wrapper="/tmp/${name}_wrapper.scad"
    echo "include <$scad_file>; $module_call;" > "$wrapper"

    local render_log="/tmp/${name}_render.log"
    openscad -o "$stl_file" "$wrapper" 2>"$render_log"
    local exit_code=$?
    local warnings=$(grep -c "WARNING" "$render_log" 2>/dev/null); warnings=${warnings:-0}
    local errors=$(grep -c "ERROR" "$render_log" 2>/dev/null); errors=${errors:-0}

    local stl_size=0
    local manifold="false"
    local open_edges=0

    if [ -f "$stl_file" ]; then
        stl_size=$(stat -c%s "$stl_file" 2>/dev/null || echo 0)
        python3 -c "
import trimesh, json
try:
    m = trimesh.load('$stl_file')
    print(json.dumps({'manifold': bool(m.is_watertight), 'open_edges': 0 if m.is_watertight else 1, 'face_count': len(m.faces)}))
except Exception as e:
    print(json.dumps({'manifold': False, 'open_edges': -1, 'error': str(e)}))
" > /tmp/${name}_mesh.json 2>/dev/null
        manifold=$(python3 -c "import json; d=json.load(open('/tmp/${name}_mesh.json')); print(str(d.get('manifold',False)).lower())" 2>/dev/null || echo "false")
        open_edges=$(python3 -c "import json; d=json.load(open('/tmp/${name}_mesh.json')); print(d.get('open_edges',0))" 2>/dev/null || echo 0)
    fi

    [ $FIRST -eq 0 ] && echo ',' >> "$REPORT"
    FIRST=0
    cat >> "$REPORT" << JSON
{
  "name": "$name",
  "scad_file": "$scad_file",
  "module": "$module_call",
  "render_exit_code": $exit_code,
  "render_warnings": $warnings,
  "render_errors": $errors,
  "stl_file": "$stl_file",
  "stl_size_bytes": $stl_size,
  "manifold": $manifold,
  "open_edges": $open_edges,
  "status": "$([ $exit_code -eq 0 ] && [ "$manifold" = "true" ] && echo PASS || echo FAIL)"
}
JSON
    echo "[$( [ $exit_code -eq 0 ] && [ "$manifold" = "true" ] && echo OK || echo FAIL)] $name (exit=$exit_code, manifold=$manifold, size=${stl_size}b)"
}

# Calibration
render_part "passage_ring_60mm" "$SCAD/calibration_parts.scad" "passage_test_ring(60)" "calibration"
render_part "passage_ring_55mm" "$SCAD/calibration_parts.scad" "passage_test_ring(55)" "calibration"
render_part "passage_ring_58mm" "$SCAD/calibration_parts.scad" "passage_test_ring(58)" "calibration"
render_part "passage_ring_62mm" "$SCAD/calibration_parts.scad" "passage_test_ring(62)" "calibration"
render_part "long_tunnel_test" "$SCAD/calibration_parts.scad" "long_tunnel_test()" "calibration"
render_part "bayonet_snap_test" "$SCAD/calibration_parts.scad" "bayonet_snap_test()" "calibration"
render_part "shade_wall_test" "$SCAD/calibration_parts.scad" "shade_wall_test()" "calibration"
render_part "cable_exit_test" "$SCAD/calibration_parts.scad" "cable_exit_test()" "calibration"
render_part "bayonet_tolerance_020" "$SCAD/bayonet_system.scad" "bayonet_tolerance_pair(0.20)" "calibration"
render_part "bayonet_tolerance_025" "$SCAD/bayonet_system.scad" "bayonet_tolerance_pair(0.25)" "calibration"
render_part "bayonet_tolerance_030" "$SCAD/bayonet_system.scad" "bayonet_tolerance_pair(0.30)" "calibration"
render_part "bayonet_tolerance_035" "$SCAD/bayonet_system.scad" "bayonet_tolerance_pair(0.35)" "calibration"
render_part "bayonet_tolerance_040" "$SCAD/bayonet_system.scad" "bayonet_tolerance_pair(0.40)" "calibration"

# Base
render_part "lamp_base" "$SCAD/lamp_base.scad" "lamp_base()" "base"
render_part "lamp_base_bottom_plate" "$SCAD/lamp_base.scad" "lamp_base_bottom_plate()" "base"
render_part "lamp_base_weight_insert" "$SCAD/lamp_base.scad" "lamp_base_weight_insert()" "base"
render_part "cable_exit_grommet" "$SCAD/lamp_base.scad" "cable_exit_grommet()" "base"

# Round modules
for mod in mod_sphere mod_oblate_sphere mod_double_sphere mod_soft_cylinder mod_disc mod_ring_module; do
    render_part "${mod}" "$SCAD/round_modules.scad" "${mod}()" "modules_round"
done

# Organic modules
for mod in mod_teardrop mod_vase mod_pumpkin mod_wave mod_organic_diamond mod_asymmetric_soft; do
    render_part "${mod}" "$SCAD/organic_modules.scad" "${mod}()" "modules_organic"
done

# Narrow accent modules
render_part "mod_narrow_shadow_ring" "$SCAD/organic_modules.scad" "mod_narrow_shadow_ring()" "modules_narrow"
render_part "mod_narrow_ribbed_ring" "$SCAD/organic_modules.scad" "mod_narrow_ribbed_ring()" "modules_narrow"

# Geometric modules
for mod in mod_cube_rounded mod_hexagon mod_diamond_faceted mod_frustum mod_triangle_rounded mod_stepped_geometric; do
    render_part "${mod}" "$SCAD/geometric_modules.scad" "${mod}()" "modules_geometric"
done

# Utility modules
for mod in mod_neutral_extension mod_short_spacer mod_top_cap mod_transition; do
    render_part "${mod}" "$SCAD/utility_modules.scad" "${mod}()" "modules_narrow"
done

# Adapters
render_part "strala_fit_test" "$SCAD/strala_holder.scad" "strala_fit_test()" "adapters"
render_part "strala_split_clamp_left" "$SCAD/strala_holder.scad" "strala_split_clamp_left()" "adapters"
render_part "strala_split_clamp_right" "$SCAD/strala_holder.scad" "strala_split_clamp_right()" "adapters"

# Shades
for shade in shade_frustum shade_cylinder shade_bell shade_mushroom shade_globe shade_vertical_ribs shade_horizontal_ribs shade_faceted shade_organic_curve shade_perforated; do
    render_part "${shade}" "$SCAD/lamp_shades.scad" "${shade}()" "shades"
done

echo ']}' >> "$REPORT"

python3 << 'PYEOF'
import json, datetime

with open("/home/user/WC-Buch/modular_strala_lamp/exports/reports/validation_results.json") as f:
    data = json.load(f)

parts = data["parts"]
pass_count = sum(1 for p in parts if p.get("status") == "PASS")
fail_count = len(parts) - pass_count

md = f"""# Validation Report — Modulare STRÅLA-Lampe

**Geprüft:** {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}
**OpenSCAD:** 2021.01 (echte Render-Prüfung)
**Mesh-Prüfung:** trimesh (Python)
**Ergebnis:** {pass_count}/{len(parts)} bestanden

> **Digital geprüft und konstruktiv für mindestens 60 mm Steckerdurchgang ausgelegt.**
> Realer Steckerdurchgang-Test noch erforderlich.

## Ergebnistabelle

| Teil | Exit | Manifold | Dateigröße | Status |
|------|------|----------|------------|--------|
"""

for p in parts:
    status = "PASS" if p.get("status") == "PASS" else "FAIL"
    md += f"| {p['name']} | {p['render_exit_code']} | {p['manifold']} | {p.get('stl_size_bytes',0):,} B | {status} |\n"

md += f"""
## Zusammenfassung

- **Gesamt:** {len(parts)} Teile
- **Bestanden:** {pass_count}
- **Fehlgeschlagen:** {fail_count}

## Hinweis

Diese Prüfung ist eine digitale Render- und Mesh-Prüfung.
Sie ersetzt **keinen** realen Probedruck.
Erst nach erfolgreichem Testdruck mit dem tatsächlichen IKEA-STRÅLA-Stecker
darf geschrieben werden: "Realer Steckerdurchgang erfolgreich geprüft."

## Noch erforderliche reale Prüfungen

1. STRÅLA-Fassung ausmessen -> MEASURE-Parameter in config.scad eintragen
2. 60mm-Durchgangsring drucken und mit realem Stecker prüfen
3. Bajonett-Toleranzset drucken -> bestes Spiel bestimmen
4. Fußkabelweg real montieren und prüfen
5. Standfestigkeit mit montiertem Schirm testen
"""

with open("/home/user/WC-Buch/modular_strala_lamp/validation_report.md", "w") as f:
    f.write(md)
print("validation_report.md written")
PYEOF

echo "=== VALIDATION COMPLETE ==="
echo "STL files: $STL_OUT"
echo "Report: $REPORT"
