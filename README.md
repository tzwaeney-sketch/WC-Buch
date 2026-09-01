# WC-Buch – Familie Albrecht

Statische Netlify-Seite mit zwei Teilen:

| Seite | Zweck |
|---|---|
| `index.html` | WC-Gästebuch (Einträge landen über `netlify/functions/wc.js` in einem Google-Apps-Script) |
| `verkaufen.html` | **Foto → Kleinanzeige**: Foto machen, KI erkennt den Artikel, schreibt Titel + Beschreibung, wählt Kategorie/Zustand und schätzt den Preis. Danach teilen/kopieren und bei Kleinanzeigen einstellen. |

## Foto → Kleinanzeige einrichten

Die Analyse läuft in der Netlify-Funktion `netlify/functions/analyze.js` über die Anthropic-API (Claude). Damit sie funktioniert:

1. API-Key unter <https://console.anthropic.com/> anlegen.
2. In Netlify: **Site configuration → Environment variables → Add a variable**
   - `ANTHROPIC_API_KEY` = `sk-ant-…`
3. Neu deployen (Deploys → Trigger deploy). Netlify installiert dabei `@anthropic-ai/sdk` aus der `package.json`.

Optionale Variablen:

| Variable | Standard | Bedeutung |
|---|---|---|
| `ANALYZE_MODEL` | `claude-opus-5` | Modell für die Bildanalyse |
| `ANALYZE_EFFORT` | `medium` | `low` ist schneller und günstiger, `high` gründlicher. Wenn Netlify die Funktion nach 10 s abbricht (Fehler 502/504), auf `low` stellen. |

Kosten: pro Anzeige mit 1–2 Fotos grob 3–6 Cent (Opus 5). Die Funktion schickt bei einer Sicherheits-Ablehnung die Anfrage automatisch an ein Ersatzmodell (`fallbacks: "default"`), damit möglichst immer ein Ergebnis kommt.

## Ablauf auf dem Handy

1. `…/verkaufen.html` öffnen (im Gästebuch oben rechts „🏷️ Verkaufen“). Am besten zum Startbildschirm hinzufügen.
2. Foto aufnehmen (bis zu 4), optional Hinweise wie Neupreis/Alter/Mängel eintippen, **Anzeige erstellen**.
3. Ergebnis prüfen und ggf. anpassen (alles editierbar, Zeichenlimits von Kleinanzeigen werden eingehalten).
4. **Fotos + Text an Kleinanzeigen-App teilen** (Android: Kleinanzeigen als Ziel wählen, Fotos landen direkt in der neuen Anzeige; Text liegt in der Zwischenablage) oder **Alles kopieren** + **Kleinanzeigen öffnen**.
5. In der Kleinanzeigen-App einfügen, Kategorie/Zustand wie angezeigt wählen, **Anzeige aufgeben**.

Warum nicht vollautomatisch? Kleinanzeigen bietet keine öffentliche Schnittstelle zum Einstellen von Anzeigen, und automatisiertes Bedienen der App/Website verstößt gegen deren Nutzungsbedingungen. Der letzte Schritt (Einfügen + „Anzeige aufgeben“) bleibt deshalb bei dir.

## Lokal entwickeln

```bash
npm install
npx netlify-cli dev      # startet Seite + Functions unter http://localhost:8888
```

Dabei muss `ANTHROPIC_API_KEY` in der Umgebung gesetzt sein (`export ANTHROPIC_API_KEY=sk-ant-…`).
