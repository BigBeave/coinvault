const CACHE_NAME = 'coinvault-v2';
const ASSETS_TO_CACHE = [
  './',
  'index.html',
  'manifest.json',
  '/manifest.json',
  'static/css/app.css',
  '/static/css/app.css',
  'static/js/coin-engine.js',
  '/static/js/coin-engine.js',
  'static/js/app.js',
  '/static/js/app.js',
  'static/icons/icon-192.png',
  '/static/icons/icon-192.png',
  'static/icons/icon-512.png',
  '/static/icons/icon-512.png',
  'COINVAULT_STANDALONE_GUIDE.html',
  '/COINVAULT_STANDALONE_GUIDE.html',
  'COINVAULT_GUIDE.html',
  '/COINVAULT_GUIDE.html'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(async (cache) => {
      // Cache each asset individually so a single 404 does not fail installation
      for (const asset of ASSETS_TO_CACHE) {
        try {
          await cache.add(asset);
        } catch (e) {
          // Path might not exist in current host config, continue
        }
      }
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // If API call, try network first; if network unreachable (PC off), return JSON error
  if (url.pathname.includes('/api/')) {
    event.respondWith(
      fetch(event.request).catch(() => {
        return new Response(
          JSON.stringify({
            error: 'Backend server unreachable. Falling back to Standalone iOS Engine.',
            standalone_fallback: true
          }),
          {
            status: 503,
            headers: { 'Content-Type': 'application/json' }
          }
        );
      })
    );
    return;
  }

  // Static assets & navigation: Cache First with Network Fallback
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        // Fetch in background to revalidate cache if online and GET
        if (event.request.method === 'GET' && event.request.url.startsWith('http')) {
          fetch(event.request).then((networkResponse) => {
            if (networkResponse && networkResponse.status === 200) {
              const resClone = networkResponse.clone();
              caches.open(CACHE_NAME).then((cache) => cache.put(event.request, resClone));
            }
          }).catch(() => {});
        }
        return cachedResponse;
      }

      return fetch(event.request).then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200 && event.request.method === 'GET' && event.request.url.startsWith('http')) {
          const resClone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, resClone));
        }
        return networkResponse;
      }).catch(async () => {
        // If navigation request failed while offline, return cached index
        if (event.request.mode === 'navigate') {
          const cachedIndex = (await caches.match('index.html')) ||
                              (await caches.match('./')) ||
                              (await caches.match('/')) ||
                              (await caches.match('static/index.html'));
          if (cachedIndex) return cachedIndex;
        }
        return new Response('Offline - CoinVault Standalone PWA', {
          status: 503,
          statusText: 'Service Unavailable',
          headers: { 'Content-Type': 'text/html' }
        });
      });
    })
  );
});
