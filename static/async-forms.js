// static/js/async-forms.js

// -------------------- IndexedDB minimal --------------------
const DB_NAME = 'async-form-db';
const STORE = 'queue';

function idbOpen() {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, 1);
    req.onupgradeneeded = () => req.result.createObjectStore(STORE, { keyPath: 'id', autoIncrement: true });
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}
function idbAdd(item) {
  return idbOpen().then(db => new Promise((resolve, reject) => {
    const tx = db.transaction(STORE, 'readwrite');
    tx.objectStore(STORE).add(item);
    tx.oncomplete = resolve;
    tx.onerror = () => reject(tx.error);
  }));
}
function idbGetAll() {
  return idbOpen().then(db => new Promise((resolve, reject) => {
    const tx = db.transaction(STORE, 'readonly');
    const req = tx.objectStore(STORE).getAll();
    req.onsuccess = () => resolve(req.result || []);
    req.onerror = () => reject(req.error);
  }));
}
function idbDelete(id) {
  return idbOpen().then(db => new Promise((resolve, reject) => {
    const tx = db.transaction(STORE, 'readwrite');
    tx.objectStore(STORE).delete(id);
    tx.oncomplete = resolve;
    tx.onerror = () => reject(tx.error);
  }));
}

// -------------------- Helpers --------------------
function isAsyncEnabled(form) {
  return form.hasAttribute('data-enable-async-send') ||
         form.querySelector('input[name="enable-async-send"]');
}

function serializeForm(form) {
  // Supporto generico: inviamo come application/x-www-form-urlencoded
  const fd = new FormData(form);
  // Rimuovo il marcatore dalla payload dati
  fd.delete('enable-async-send');
  const params = new URLSearchParams();
  for (const [k, v] of fd.entries()) {
    // NB: i file non vengono gestiti in questo profilo "semplice"
    if (v instanceof File) continue;
    params.append(k, v);
  }
  return params.toString();
}

async function sendNow(job) {
  const headers = new Headers({
    'Content-Type': 'application/x-www-form-urlencoded'
  });
  // Propaghiamo il nostro "header logico"
  if (job.headerEnabled) headers.set('enable-async-send', '1');

  const res = await fetch(job.action, {
    method: job.method,
    headers,
    body: job.body,
    credentials: 'same-origin'
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res;
}

async function flushQueueFromPage() {
  try {
    const items = await idbGetAll();
    for (const item of items) {
      await sendNow(item);
      await idbDelete(item.id);
    }
  } catch (e) {
    // Silenzioso: ritenteremo alla prossima connessione
  }
}

// -------------------- Intercetta submit di tutti i form --------------------
function attachInterceptor() {
  document.addEventListener('submit', async (e) => {
    const form = e.target;
    if (!(form instanceof HTMLFormElement)) return;
    if (!isAsyncEnabled(form)) return; // non marcato → lascia il flusso normale

    e.preventDefault(); // blocca submit nativo
    const action = form.getAttribute('action') || window.location.href;
    const method = (form.getAttribute('method') || 'GET').toUpperCase();

    const body = serializeForm(form);
    const job = {
      action,
      method: method === 'GET' ? 'POST' : method, // evitiamo GET con body
      body,
      headerEnabled: true,
      enqueued_at: Date.now()
    };

    // Se online, prova subito
    if (navigator.onLine) {
      try {
        await sendNow(job);
        form.reset();
        form.dispatchEvent(new CustomEvent('async-send:sent', { bubbles: true }));
        return;
      } catch (_) { /* cadrà in coda */ }
    }

    // Accoda
    try {
      await idbAdd(job);
      form.reset();
      form.dispatchEvent(new CustomEvent('async-send:queued', { bubbles: true }));
      // Chiedi al SW il Background Sync, se supportato
      if ('serviceWorker' in navigator && 'SyncManager' in window) {
        const reg = await navigator.serviceWorker.ready;
        await reg.sync.register('async-form-queue');
      }
    } catch (err) {
      console.error('Queue error', err);
      form.dispatchEvent(new CustomEvent('async-send:error', { bubbles: true, detail: err }));
    }
  });
}

attachInterceptor();

// Fallback iOS/vecchi browser: quando torna online, svuota dalla pagina
window.addEventListener('online', flushQueueFromPage);