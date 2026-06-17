# Standfestigkeits-Analyse — Modulare STRÅLA-Lampe

> Vereinfachte statische Kippanalyse. Ersetzt keinen realen Kipptest.

## Annahmen

| Größe | Wert |
|-------|------|
| Gesamthöhe Korpus | 600 mm |
| Schirmhöhe | 200 mm |
| Gesamthöhe (mit Schirm) | ~800 mm |
| Gesamtmasse | ~1200 g (Module ~500 g + Schirm ~200 g + STRÅLA ~100 g + Basis ~400 g) |
| Schwerpunkt (CoM) Höhe | ~400 mm |
| Basisradius | 110 mm |

## Kippwinkel (Ausgangszustand)

Der statische Kippwinkel ist der Winkel, um den die Lampe gekippt werden kann,
bevor der Schwerpunkt über die Standkante hinauswandert:

```
tip_angle = atan(base_radius / CoM_height)
          = atan(110 / 400)
          = 15.4°
```

15,4° ist grenzwertig — eine kopflastige Lampe sollte mehr Reserve haben.

## Empfehlung: Ballast

Erhöht man die Basismasse auf ~600 g (z. B. Stahlring im Gewichtskammer-Pocket),
sinkt der Schwerpunkt auf ~340 mm:

```
tip_angle = atan(110 / 340) = 17.9° (~18°)
```

- **Empfohlener Ballast:** Stahlring 200 g im `lamp_base_weight_insert`-Pocket.
- **Empfohlener maximaler Schirmdurchmesser:** 280 mm.
- Bei größeren/höheren Konfigurationen Basisgewicht weiter erhöhen.

## Sicherheitsmargen

| Zustand | Kippwinkel | Bewertung |
|---------|-----------|-----------|
| Ohne Ballast | 15,4° | grenzwertig |
| Mit 200 g Ballast | ~18° | akzeptabel |
| Ziel | >= 20° | empfohlen für hohe Konfigurationen |

## Noch erforderlich (real)

1. Reale Massen aller gedruckten Teile wiegen.
2. Realen Schwerpunkt durch Auswiegen / Balancieren bestimmen.
3. Kipptest mit montiertem größtem Schirm durchführen.
4. Standfläche / Gummifüße auf rutschfesten Halt prüfen.
