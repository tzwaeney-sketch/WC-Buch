// Netlify Function: Foto(s) -> fertige Kleinanzeigen-Anzeige (Titel, Beschreibung, Preis ...)
//
// Erwartet POST mit JSON:
//   { images: [{ media_type: "image/jpeg", data: "<base64>" }, ...], hints: "optionaler Freitext" }
// Antwortet mit JSON:
//   { ok: true, listing: {...}, model: "..." }  bzw.  { ok: false, error: "..." }
//
// Benötigt die Umgebungsvariable ANTHROPIC_API_KEY (in Netlify: Site settings -> Environment variables).

import Anthropic from "@anthropic-ai/sdk";

const MODEL = process.env.ANALYZE_MODEL || "claude-opus-5";
const EFFORT = process.env.ANALYZE_EFFORT || "medium"; // low | medium | high
const MAX_IMAGES = 4;
const MAX_IMAGE_B64_CHARS = 5.5 * 1024 * 1024; // ~4 MB Bild
const ALLOWED_TYPES = new Set(["image/jpeg", "image/png", "image/webp", "image/gif"]);

const CONDITIONS = ["Neu mit Etikett", "Neu", "Sehr Gut", "Gut", "In Ordnung", "Defekt"];
const PRICE_TYPES = ["VB", "Festpreis", "Zu verschenken"];

// Ausgabeformat – wird als JSON-Schema erzwungen (Structured Outputs).
const LISTING_SCHEMA = {
  type: "object",
  additionalProperties: false,
  required: [
    "title", "description", "category", "subcategory", "condition",
    "brand", "model", "price", "shipping", "attributes", "keywords",
    "confidence", "seller_notes", "open_questions"
  ],
  properties: {
    title: { type: "string", description: "Anzeigentitel, max. 65 Zeichen, deutsch, ohne Preis." },
    description: { type: "string", description: "Fertiger Anzeigentext auf Deutsch, 400-1200 Zeichen, Absätze mit Zeilenumbrüchen, keine Emojis-Flut, kein Preis im Text." },
    category: { type: "string", description: "Kleinanzeigen-Hauptkategorie, z.B. 'Elektronik', 'Haus & Garten', 'Mode & Beauty', 'Familie, Kind & Baby', 'Freizeit, Hobby & Nachbarschaft', 'Auto, Rad & Boot', 'Musik, Filme & Bücher', 'Haustiere'." },
    subcategory: { type: "string", description: "Passende Unterkategorie bei Kleinanzeigen, z.B. 'Handy & Telefon', 'Wohnzimmer', 'Damenschuhe'." },
    condition: { type: "string", enum: CONDITIONS },
    brand: { anyOf: [{ type: "string" }, { type: "null" }], description: "Marke, falls erkennbar, sonst null." },
    model: { anyOf: [{ type: "string" }, { type: "null" }], description: "Modellbezeichnung / Typ, falls erkennbar, sonst null." },
    price: {
      type: "object",
      additionalProperties: false,
      required: ["suggested", "min", "max", "type", "reasoning"],
      properties: {
        suggested: { type: "integer", description: "Empfohlener Angebotspreis in Euro (ganze Zahl)." },
        min: { type: "integer", description: "Realistischer Mindestpreis in Euro." },
        max: { type: "integer", description: "Realistischer Höchstpreis in Euro." },
        type: { type: "string", enum: PRICE_TYPES },
        reasoning: { type: "string", description: "1-3 Sätze: warum dieser Preis (Neupreis, Alter, Zustand, Gebrauchtmarkt)." }
      }
    },
    shipping: {
      type: "object",
      additionalProperties: false,
      required: ["possible", "note"],
      properties: {
        possible: { type: "boolean", description: "true = Versand sinnvoll möglich, false = nur Abholung." },
        note: { type: "string", description: "Kurzer Hinweis, z.B. 'Paket bis 5 kg, ca. 6 € Versand' oder 'Sperrgut, nur Abholung'." }
      }
    },
    attributes: {
      type: "array",
      description: "Erkennbare Eigenschaften wie Farbe, Größe, Material, Maße, Speicher.",
      items: {
        type: "object",
        additionalProperties: false,
        required: ["name", "value"],
        properties: { name: { type: "string" }, value: { type: "string" } }
      }
    },
    keywords: { type: "array", items: { type: "string" }, description: "5-10 Suchbegriffe, nach denen Käufer suchen würden." },
    confidence: { type: "number", description: "0 bis 1: wie sicher ist die Erkennung des Artikels." },
    seller_notes: { type: "string", description: "Kurze Hinweise an den Verkäufer: was er vor dem Einstellen prüfen/ergänzen sollte." },
    open_questions: { type: "array", items: { type: "string" }, description: "Fragen, die aus dem Foto nicht beantwortbar sind und den Preis beeinflussen." }
  }
};

const SYSTEM_PROMPT = `Du bist ein erfahrener Verkäufer auf kleinanzeigen.de (ehemals eBay Kleinanzeigen) in Deutschland.
Du bekommst ein oder mehrere Fotos eines Gegenstands sowie optionale Hinweise des Verkäufers und erstellst daraus eine fertige, sofort einstellbare Anzeige.

Regeln:
- Alles auf Deutsch, Du-Form vermeiden, neutral und ehrlich. Nichts erfinden: Was auf dem Foto nicht erkennbar ist, nicht als Fakt behaupten.
- Titel: max. 65 Zeichen, präzise, mit Marke/Modell wenn erkennbar, ohne Preis, ohne Sonderzeichen-Spam.
- Beschreibung: 400-1200 Zeichen. Aufbau: 1) Was ist es (Marke, Modell, Wichtigstes), 2) Zustand & Besonderheiten (auch sichtbare Gebrauchsspuren ehrlich nennen), 3) Lieferumfang / was ist dabei, 4) Abholung/Versand, 5) Standard-Schlusssatz "Privatverkauf, daher keine Garantie oder Rücknahme." Keine Preisangabe im Text.
- Zustand nach den Kleinanzeigen-Stufen: Neu mit Etikett, Neu, Sehr Gut, Gut, In Ordnung, Defekt. Bei Unsicherheit eher eine Stufe konservativer.
- Preis: Schätze den realistischen Gebrauchtmarktpreis in Deutschland (Kleinanzeigen-Niveau, nicht Neupreis, nicht eBay-Auktions-Ausreißer). Gib Spanne min/max und einen konkreten Vorschlag. Bei typischen Gebrauchtwaren "VB" empfehlen, bei sehr günstigen Kleinteilen (unter ca. 10 Euro) Festpreis, bei wertlosen Dingen "Zu verschenken". Hinweise des Verkäufers (Neupreis, Alter, Rechnung, Mängel) unbedingt in die Schätzung einbeziehen.
- Kategorie und Unterkategorie so wählen, wie sie bei kleinanzeigen.de heißen.
- Versand: "possible" true, wenn der Artikel realistisch per Paket verschickt werden kann.
- seller_notes: 1-3 kurze Sätze, was der Verkäufer vor dem Einstellen prüfen sollte (z.B. Seriennummer, Funktionstest, Zubehör).
- open_questions: nur Dinge, die den Preis oder die Beschreibung wirklich ändern würden.`;

function json(statusCode, body) {
  return {
    statusCode,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
    body: JSON.stringify(body)
  };
}

function validateImages(images) {
  if (!Array.isArray(images) || images.length === 0) return "Mindestens ein Foto wird benötigt.";
  if (images.length > MAX_IMAGES) return `Maximal ${MAX_IMAGES} Fotos pro Anzeige.`;
  for (const img of images) {
    if (!img || typeof img !== "object") return "Ungültiges Bildobjekt.";
    if (!ALLOWED_TYPES.has(img.media_type)) return `Bildformat ${img.media_type || "?"} wird nicht unterstützt (JPEG, PNG, WebP, GIF).`;
    if (typeof img.data !== "string" || img.data.length < 100) return "Bilddaten fehlen.";
    if (img.data.length > MAX_IMAGE_B64_CHARS) return "Ein Foto ist zu groß. Bitte kleiner aufnehmen (die Seite verkleinert normalerweise automatisch).";
  }
  return null;
}

function buildUserContent(images, hints) {
  const content = images.map((img) => ({
    type: "image",
    source: { type: "base64", media_type: img.media_type, data: img.data.replace(/\s+/g, "") }
  }));

  let text = `Erstelle aus ${images.length === 1 ? "diesem Foto" : `diesen ${images.length} Fotos`} eine fertige Kleinanzeigen-Anzeige.`;
  const cleanHints = String(hints || "").trim().slice(0, 2000);
  if (cleanHints) {
    text += `\n\nHinweise des Verkäufers (haben Vorrang vor dem, was du auf dem Foto vermutest):\n${cleanHints}`;
  } else {
    text += "\n\nDer Verkäufer hat keine weiteren Angaben gemacht.";
  }
  content.push({ type: "text", text });
  return content;
}

function sanitizeListing(listing) {
  const out = { ...listing };
  out.title = String(out.title || "").trim().slice(0, 65);
  out.description = String(out.description || "").trim().slice(0, 4000);
  if (!CONDITIONS.includes(out.condition)) out.condition = "Gut";
  const p = out.price || {};
  const num = (v, fallback) => (Number.isFinite(Number(v)) ? Math.max(0, Math.round(Number(v))) : fallback);
  const suggested = num(p.suggested, 0);
  let min = num(p.min, suggested);
  let max = num(p.max, suggested);
  if (min > max) [min, max] = [max, min];
  out.price = {
    suggested,
    min,
    max,
    type: PRICE_TYPES.includes(p.type) ? p.type : (suggested === 0 ? "Zu verschenken" : "VB"),
    reasoning: String(p.reasoning || "").trim()
  };
  out.shipping = {
    possible: Boolean(out.shipping && out.shipping.possible),
    note: String((out.shipping && out.shipping.note) || "").trim()
  };
  out.attributes = Array.isArray(out.attributes) ? out.attributes.filter((a) => a && a.name && a.value).slice(0, 12) : [];
  out.keywords = Array.isArray(out.keywords) ? out.keywords.map(String).slice(0, 12) : [];
  out.open_questions = Array.isArray(out.open_questions) ? out.open_questions.map(String).slice(0, 6) : [];
  out.confidence = Math.min(1, Math.max(0, Number(out.confidence) || 0));
  out.seller_notes = String(out.seller_notes || "").trim();
  out.brand = out.brand ? String(out.brand) : null;
  out.model = out.model ? String(out.model) : null;
  return out;
}

export async function handler(event) {
  if ((event.httpMethod || "GET") !== "POST") {
    return json(405, { ok: false, error: "Nur POST erlaubt." });
  }
  if (!process.env.ANTHROPIC_API_KEY) {
    return json(500, { ok: false, error: "ANTHROPIC_API_KEY ist in Netlify nicht gesetzt (Site settings → Environment variables)." });
  }

  let payload;
  try {
    payload = JSON.parse(event.body || "{}");
  } catch {
    return json(400, { ok: false, error: "Ungültiges JSON." });
  }

  const problem = validateImages(payload.images);
  if (problem) return json(400, { ok: false, error: problem });

  const client = new Anthropic({ maxRetries: 1, timeout: 55_000 });

  try {
    const response = await client.beta.messages.create({
      model: MODEL,
      max_tokens: 4000,
      betas: ["server-side-fallback-2026-07-01"],
      fallbacks: "default",
      thinking: { type: "adaptive" },
      output_config: {
        effort: EFFORT,
        format: { type: "json_schema", schema: LISTING_SCHEMA }
      },
      system: SYSTEM_PROMPT,
      messages: [{ role: "user", content: buildUserContent(payload.images, payload.hints) }]
    });

    if (response.stop_reason === "refusal") {
      const why = response.stop_details && response.stop_details.explanation;
      return json(422, { ok: false, error: `Die Analyse wurde abgelehnt${why ? `: ${why}` : "."}` });
    }
    if (response.stop_reason === "max_tokens") {
      return json(502, { ok: false, error: "Antwort wurde abgeschnitten. Bitte noch einmal versuchen." });
    }

    const text = response.content.filter((b) => b.type === "text").map((b) => b.text).join("");
    let listing;
    try {
      listing = JSON.parse(text);
    } catch {
      return json(502, { ok: false, error: "Die Antwort konnte nicht gelesen werden. Bitte noch einmal versuchen." });
    }

    return json(200, {
      ok: true,
      listing: sanitizeListing(listing),
      model: response.model,
      usage: {
        input_tokens: response.usage && response.usage.input_tokens,
        output_tokens: response.usage && response.usage.output_tokens
      }
    });
  } catch (err) {
    if (err instanceof Anthropic.AuthenticationError) {
      return json(500, { ok: false, error: "Der Anthropic API-Key ist ungültig." });
    }
    if (err instanceof Anthropic.RateLimitError) {
      return json(429, { ok: false, error: "Zu viele Anfragen. Bitte kurz warten und erneut versuchen." });
    }
    if (err instanceof Anthropic.BadRequestError) {
      return json(400, { ok: false, error: `Anfrage abgelehnt: ${err.message}` });
    }
    if (err instanceof Anthropic.APIError) {
      return json(502, { ok: false, error: `API-Fehler ${err.status || ""}: ${err.message}` });
    }
    return json(500, { ok: false, error: String((err && err.message) || err) });
  }
}
