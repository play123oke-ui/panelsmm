self.addEventListener('install', event => {
  event.waitUntil(
    caches.open('panel-smm-cache').then(cache => {
      return cache.addAll([
        '/',
        '/static/style.css',
        '/static/script.js',
        '/static/icon-192x192.png',
        '/static/icon-512x512.png'
      ]);
    })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.filter(cacheName => cacheName !== 'panel-smm-cache').map(cacheName => caches.delete(cacheName))
      );
    })
  );
});
