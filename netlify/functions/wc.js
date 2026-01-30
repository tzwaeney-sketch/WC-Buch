export async function handler(event) {
  const GAS_URL = "https://script.google.com/macros/s/AKfycbzWz7x15X29gld5hR8qVBhW4AvMAhR0fNkEGyt1FwPWiKmGD51rk4E9QGFPktGr9AT5/exec";

  try {
    const method = event.httpMethod || "GET";

    if (method === "GET") {
      const qs = event.rawQuery || "";
      const res = await fetch(qs ? `${GAS_URL}?${qs}` : GAS_URL, { method: "GET" });
      const text = await res.text();
      return {
        statusCode: res.status,
        headers: { "content-type": "application/json; charset=utf-8" },
        body: text
      };
    }

    if (method === "POST") {
      const res = await fetch(GAS_URL, {
        method: "POST",
        headers: { "content-type": "application/json; charset=utf-8" },
        body: event.body || "{}"
      });
      const text = await res.text();
      return {
        statusCode: res.status,
        headers: { "content-type": "application/json; charset=utf-8" },
        body: text
      };
    }

    return { statusCode: 405, body: JSON.stringify({ ok:false, error:"Method not allowed" }) };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ ok:false, error: String(err?.message || err) }) };
  }
}
