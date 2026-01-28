exports.handler = async (event) => {
  const EXEC_URL = "https://script.google.com/macros/s/AKfycbxjY97auBg9rHnzcSbVFXvJ5iKpMDDkQauvZ6IckKJppMjeCowfjS_FSXmmCmf/exec";

  const cors = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
  };

  if (event.httpMethod === "OPTIONS") {
    return { statusCode: 204, headers: cors, body: "" };
  }

  try {
    if (event.httpMethod === "GET") {
      const qs =
        event.rawQuery ||
        (event.queryStringParameters
          ? new URLSearchParams(event.queryStringParameters).toString()
          : "");
      const upstreamUrl = EXEC_URL + (qs ? `?${qs}` : "");
      const r = await fetch(upstreamUrl);
      const body = await r.text();
      return {
        statusCode: r.status,
        headers: { ...cors, "Content-Type": "application/json; charset=utf-8" },
        body,
      };
    }

    if (event.httpMethod === "POST") {
      const r = await fetch(EXEC_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: event.body || "{}",
      });
      const body = await r.text();
      return {
        statusCode: r.status,
        headers: { ...cors, "Content-Type": "application/json; charset=utf-8" },
        body,
      };
    }

    return {
      statusCode: 405,
      headers: cors,
      body: JSON.stringify({ ok: false, error: "Method not allowed" }),
    };
  } catch (e) {
    return {
      statusCode: 500,
      headers: cors,
      body: JSON.stringify({ ok: false, error: String(e.message || e) }),
    };
  }
};
