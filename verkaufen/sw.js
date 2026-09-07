/* Service Worker für „Foto → Kleinanzeige“
 * - cached die App-Hülle, damit die App sofort und auch offline startet
 * - nimmt geteilte Fotos (Web Share Target) entgegen und reicht sie an die App weiter
 */
const VERSION = "v2";
const SHELL_CACHE = `verkaufen-shell-${VERSION}`;
const INTAKE_CACHE = "verkaufen-shared-intake";
const SCOPE = "/verkaufen/";
const SHELL = [
  SCOPE,
  `${SCOPE}index.html`,
  `${SCOPE}manifest.webmanifest`,
  `${SCOPE}icon.svg`,
  `${SCOPE}icon-192.png`,
  `${SCOPE}icon-512.png`,
  `${SCOPE}icon-maskable-512.png`,
  `${SCOPE}apple-touch-icon.png`
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(SHELL_CACHE)
      .then((c) => c.addAll(SHELL))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k.startsWith("verkaufen-shell-") && k !== SHELL_CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

// Geteilte Fotos aus dem Android-Teilen-Menü: Formulardaten lesen, im Cache ablegen, zur App umleiten.
async function handleShareTarget(request) {
  try {
    const form = await request.formData();
    const files = form.getAll("photos").filter((f) => f && typeof f === "object" && f.size > 0);
    const cache = await caches.open(INTAKE_CACHE);
    const old = await cache.keys();
    await Promise.all(old.map((k) => cache.delete(k)));
    await Promise.all(files.slice(0, 4).map((file, i) =>
      cache.put(`${SCOPE}_shared/${i}`, new Response(file, { headers: { "content-type": file.type || "image/jpeg", "x-name": encodeURIComponent(file.name || `foto-${i + 1}.jpg`) } }))
    ));
    const text = [form.get("title"), form.get("text")].filter(Boolean).join("\n");
    if (text) await cache.put(`${SCOPE}_shared/text`, new Response(text, { headers: { "content-type": "text/plain; charset=utf-8" } }));
  } catch (e) {
    // Auch bei Fehlern zur App – sie zeigt dann einfach den leeren Startbildschirm.
  }
  return Response.redirect(`${SCOPE}?shared=1`, 303);
}

self.addEventListener("fetch", (event) => {
  const req = event.request;
  const url = new URL(req.url);

  if (req.method === "POST" && url.pathname === `${SCOPE}share-target`) {
    event.respondWith(handleShareTarget(req));
    return;
  }
  if (req.method !== "GET" || url.origin !== self.location.origin) return;
  if (url.pathname.startsWith("/.netlify/")) return; // API immer live

  // Navigation: Netz zuerst, sonst App-Hülle aus dem Cache
  if (req.mode === "navigate") {
    event.respondWith(
      fetch(req).then((res) => {
        const copy = res.clone();
        caches.open(SHELL_CACHE).then((c) => c.put(`${SCOPE}index.html`, copy)).catch(() => {});
        return res;
      }).catch(() => caches.match(`${SCOPE}index.html`))
    );
    return;
  }

  // Übrige Dateien im Scope: Cache zuerst, im Hintergrund aktualisieren
  if (url.pathname.startsWith(SCOPE)) {
    event.respondWith(
      caches.match(req).then((cached) => {
        const net = fetch(req).then((res) => {
          if (res.ok) caches.open(SHELL_CACHE).then((c) => c.put(req, res.clone())).catch(() => {});
          return res;
        }).catch(() => cached);
        return cached || net;
      })
    );
  }
});
