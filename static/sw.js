const STATIC_CACHE = 'pwa-static-v2';
const PRECACHE = [
  '/',                     // se il tuo form è in home
  '/static/async-forms.js',
  '/static/manifest.webmanifest'
];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(STATIC_CACHE).then(c => c.addAll(PRECACHE)));
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(self.clients.claim());
});

// Navigazioni: network con fallback cache
self.addEventListener('fetch', (e) => {
  if (e.request.mode === 'navigate') {
    e.respondWith((async () => {
      try {
        const res = await fetch(e.request);
        const copy = res.clone();
        const cache = await caches.open(STATIC_CACHE);
        cache.put(e.request, copy);
        return res;
      } catch {
        return (await caches.match(e.request)) || (await caches.match('/'));
      }
    })());
  }
});