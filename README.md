# WC-Buch – Familie Albrecht

Statische Netlify-Seite mit zwei Teilen:

| Seite | Zweck |
|---|---|
| `index.html` | WC-Gästebuch (Einträge landen über `netlify/functions/wc.js` in einem Google-Apps-Script) |
| `verkaufen/` | **Foto → Kleinanzeige** (eigenständige, installierbare App / PWA): Foto machen, KI erkennt den Artikel, schreibt Titel + Beschreibung, wählt Kategorie/Zustand und schätzt den Preis. Danach teilen/kopieren und bei Kleinanzeigen einstellen. |

## Foto → Kleinanzeige einrichten

Die Analyse läuft in der Netlify-Funktion `netlify/functions/analyze.js` über die Anthropic-API (Claude). Damit sie funktioniert:

1. API-Key unter <https://console.anthropic.com/> anlegen.
2. In Netlify: **Site configuration → Environment variables → Add a variable**
   - `ANTHROPIC_API_KEY` = `sk-ant-…`
3. Neu deployen (Deploys → Trigger deploy). Netlify installiert dabei `@anthropic-ai/sdk` aus der `package.json`.
4. Beim nächsten Öffnen der App aktualisiert sich der Service Worker automatisch.

Optionale Variablen:

| Variable | Standard | Bedeutung |
|---|---|---|
| `ANALYZE_MODEL` | `claude-opus-5` | Modell für die Bildanalyse |
| `ANALYZE_EFFORT` | `medium` | `low` ist schneller und günstiger, `high` gründlicher. Wenn Netlify die Funktion nach 10 s abbricht (Fehler 502/504), auf `low` stellen. |

Kosten: pro Anzeige mit 1–2 Fotos grob 3–6 Cent (Opus 5). Die Funktion schickt bei einer Sicherheits-Ablehnung die Anfrage automatisch an ein Ersatzmodell (`fallbacks: "default"`), damit möglichst immer ein Ergebnis kommt.

## Die App aufs Handy bringen

`https://<deine-netlify-adresse>/verkaufen/` öffnen.

- **Android (Chrome):** Banner „App installieren“ antippen (oder Menü ⋮ → „App installieren“). Danach hat die App ein eigenes Icon, startet ohne Browserleiste und erscheint im **Teilen-Menü der Kamera-App**: Foto machen → Teilen → „Verkaufen“ → die Anzeige wird vorbereitet.
- **iPhone (Safari):** Teilen-Symbol → „Zum Home-Bildschirm“.

Die App startet offline (App-Hülle wird gecacht), nur die Analyse braucht Internet. Alle erstellten Anzeigen liegen unter „Meine Anzeigen“ lokal auf dem Gerät (IndexedDB), inklusive Status „Entwurf“ / „Eingestellt“.

## Ablauf

1. App öffnen oder Foto direkt aus der Kamera-App teilen.
2. Foto aufnehmen (bis zu 4), optional Hinweise wie Neupreis/Alter/Mängel eintippen, **Anzeige erstellen**. Unter ⚙️ Einstellungen kannst du Abholort und einen Standardzusatz hinterlegen, die in jede Anzeige einfließen.
3. Ergebnis prüfen und ggf. anpassen (alles editierbar, Zeichenlimits von Kleinanzeigen werden eingehalten).
4. **Fotos + Text an Kleinanzeigen-App teilen** (Android: Kleinanzeigen als Ziel wählen, Fotos landen direkt in der neuen Anzeige; Text liegt in der Zwischenablage) oder **Alles kopieren** + **Kleinanzeigen öffnen**.
5. In der Kleinanzeigen-App einfügen, Kategorie/Zustand wie angezeigt wählen, **Anzeige aufgeben**. Danach „Als eingestellt markieren“.

Warum nicht vollautomatisch? Kleinanzeigen bietet keine öffentliche Schnittstelle zum Einstellen von Anzeigen, und automatisiertes Bedienen der App/Website verstößt gegen deren Nutzungsbedingungen. Der letzte Schritt (Einfügen + „Anzeige aufgeben“) bleibt deshalb bei dir.

## Lokal entwickeln

```bash
npm install
npx netlify-cli dev      # startet Seite + Functions unter http://localhost:8888
```

Dabei muss `ANTHROPIC_API_KEY` in der Umgebung gesetzt sein (`export ANTHROPIC_API_KEY=sk-ant-…`).
