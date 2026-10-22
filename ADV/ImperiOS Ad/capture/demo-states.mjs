// Estados de cada interacción del vídeo demo (guion v4), a 1920×1080 @2x, con la posición de los elementos clave.
// Por cada estado: out/states/<id>.png (página completa @2x) + <id>.json (scroll, alto de página y cajas en px CSS,
// en coordenadas de documento). La composición de HyperFrames anima cursor, zoom y focos sobre estas cajas.
//
// Todo es navegación (URL, filas, pestañas, filtros, periodo) salvo UNA acción real autorizada por el usuario:
// en «Leads de campaña» se arrastra una tarjeta de «Contactado» a «Interesado».
//
// Uso: node demo-states.mjs [--drag] [id ...]   (mismas variables de entorno que capture.mjs)
// Sin --drag se omite el estado que mueve la tarjeta (así repetir capturas no cambia más datos).
import { chromium } from 'playwright-core';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(process.env.CAPTURE_OUT || path.join(HERE, 'out'), 'states');
const STATE = process.env.CAPTURE_STATE || path.join(os.tmpdir(), 'imperios-demo-state.json');
const { IMPERIOS_DEMO_URL: URL_LOGIN, IMPERIOS_DEMO_EMAIL: EMAIL, IMPERIOS_DEMO_PASSWORD: PASS } = process.env;
const redact = (s) => [EMAIL, PASS].filter(Boolean).reduce((t, v) => t.split(v).join('***'), String(s));
const log = (...a) => console.log(redact(a.join(' ')));
if (!URL_LOGIN || !EMAIL || !PASS) { console.error('Faltan IMPERIOS_DEMO_URL / _EMAIL / _PASSWORD'); process.exit(1); }
const exe = process.env.CHROMIUM_PATH ||
  (fs.existsSync('/opt/pw-browsers/chromium-1194/chrome-linux/chrome') ? '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' : undefined);
const opts = (extra = {}) => ({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2, locale: 'es-ES', timezoneId: 'Europe/Madrid', colorScheme: 'light', ...extra });

const card = (text, extra = {}) => ({ text, card: true, ...extra });
// Coincidencia que se abre en el vídeo corto: 96/100 igual en la lista y en el detalle (en demo-match-20 la lista dice 100
// y el detalle 69). Abrir el detalle genera su «Análisis IA» si aún no lo tiene.
const MATCH = process.env.CAPTURE_MATCH || 'demo-match-63';
const matchLink = `main a[href="/matches/${MATCH}"]`;
// Escenas del guion → estados. Pasos: go, firstLink, click(css), clickText, type(css + text: solo filtra la vista), row(css de tabla|null),
// tab, period, scrollTo, drag.
const STATES = [
  { id: '01-dashboard', steps: [{ go: '/' }], boxes: { kpi1: card('Propiedades publicadas'), kpi4: card('Citas esta semana'), sinAtender: card('Contactos sin atender', { nth: 1 }), citas: card('Próximas citas') } },
  { id: '02a-contactos', steps: [{ go: '/contacts' }], boxes: { colFuente: { th: 'Fuente' }, colTemp: { th: 'Temperatura' }, colContacto: { th: 'Contacto' }, colTelefono: { th: 'Teléfono' }, filtro: { css: 'main [role="combobox"]', hasText: 'Fuente' }, tabla: { css: 'main table' } } },
  { id: '02b-contactos-filtro', steps: [{ go: '/contacts' }, { click: 'main [role="combobox"]', hasText: 'Fuente' }], boxes: { filtro: { css: 'main [role="combobox"]', hasText: 'Fuente' }, opcion: { css: '[role="option"]', hasText: 'Idealista' } } },
  { id: '02c-contactos-idealista', steps: [{ go: '/contacts' }, { click: 'main [role="combobox"]', hasText: 'Fuente' }, { click: '[role="option"]', hasText: 'Idealista' }], boxes: { colFuente: { th: 'Fuente' }, filtro: { css: 'main [role="combobox"]', hasText: 'Idealista' } } },
  { id: '03a-chat', steps: [{ go: '/leads' }], boxes: { lead: { css: 'main button[data-lead-id]' }, lista: { css: 'main button[data-lead-id]', union: 6 }, srcIdealista: { css: 'main button[data-lead-id] *', hasText: 'Idealista', exact: true }, srcFotocasa: { css: 'main button[data-lead-id] *', hasText: 'Fotocasa', exact: true }, srcWeb: { css: 'main button[data-lead-id] *', hasText: 'Web', exact: true }, srcWhatsApp: { css: 'main button[data-lead-id] *', hasText: 'WhatsApp', exact: true } } },
  { id: '03b-chat-conversacion', steps: [{ go: '/leads' }, { click: 'main button[data-lead-id]' }], boxes: { lead: { css: 'main button[data-lead-id]' }, propiedad: { text: 'Sobre ', nth: 0 }, plantilla: { text: 'Plantilla', exact: true } } },
  { id: '04-cliente', steps: [{ go: '/clients' }, { firstLink: '/clients/', notEdit: true }], boxes: { prefs: card('Preferencias de'), citas: card('Citas'), origen: card('Viene de') } },
  { id: '05a-propiedades', steps: [{ go: '/properties' }], boxes: { fila: { css: 'main table tbody tr' }, tabla: { css: 'main table' } } },
  { id: '05b-propiedad-ficha', steps: [{ go: '/properties' }, { firstLink: '/properties/', notEdit: true }], boxes: { foto: { css: 'main img', largest: true }, requisitos: card('Requisitos'), precio: card('Venta') } },
  { id: '05c-publicaciones', steps: [{ go: '/publications' }], boxes: { web: card('Web', { exact: true }), fotocasa: card('Fotocasa', { exact: true }), idealista: card('Idealista', { exact: true }), tabla: { css: 'main table' } } },
  { id: '06a-coincidencias', steps: [{ go: '/matches' }], boxes: { tarjeta: card('/ 100 pts'), tabs: card('Calientes'), porPropiedad: { text: 'Por propiedad' } } },
  { id: '06b-coincidencias-propiedad', steps: [{ go: '/matches' }, { clickText: 'Por propiedad' }], boxes: { porPropiedad: { text: 'Por propiedad' }, tarjeta: card('/ 100 pts') } },
  { id: '06c-match-lista', steps: [{ go: '/matches' }, { type: 'main input[placeholder^="Buscar"]', text: 'Marcos Gimeno' }], boxes: { tarjeta: { css: matchLink, card: true }, ver: { css: matchLink }, tabs: card('Calientes') } },
  { id: '06d-match-detalle', steps: [{ go: '/matches' }, { click: matchLink }],
    boxes: { puntuacion: card('Puntuación de coincidencia'), estado: card('Estado del match'), analisis: card('Análisis IA'), criterios: card('Por qué este score'), comprador: card('Comprador', { exact: true }), propiedad: card('Propiedad', { exact: true }) } },
  { id: '07a-calendario', steps: [{ go: '/calendar' }], boxes: { semana: { css: 'main button', hasText: 'Semana', exact: true }, mes: { css: 'main button', hasText: 'Mes', exact: true } } },
  { id: '07b-calendario-semana', steps: [{ go: '/calendar' }, { click: 'main button', hasText: 'Semana', exact: true }], boxes: { semana: { css: 'main button', hasText: 'Semana', exact: true } } },
  { id: '07c-tareas', steps: [{ go: '/tasks' }], boxes: { pendiente: { col: 'Pendiente' }, encurso: { col: 'En curso' }, hecho: { col: 'Hecho' } } },
  { id: '08a-marketing', steps: [{ go: '/marketing' }], boxes: { inversion: card('Inversión', { exact: true }), leads: card('Leads', { exact: true, nth: 1 }), cpl: card('Coste por lead', { exact: true }), campanas: card('Campañas', { exact: true }), campana1: { css: 'main table tbody tr' } } },
  { id: '08b-campana', steps: [{ go: '/marketing' }, { row: null }], boxes: { embudo: card('Del anuncio al lead'), conjuntos: card('Conjuntos de anuncios'), conjunto1: { css: 'main table tbody tr' } } },
  { id: '08c-conjunto', steps: [{ go: '/marketing' }, { row: null }, { firstLink: '/adsets/' }], boxes: { anuncios: card('Anuncios', { exact: true }), mejor: { bestRow: true } } },
  { id: '08d-leads-antes', steps: [{ go: '/marketing/leads' }], boxes: { contactado: { col: 'Contactado' }, interesado: { col: 'Interesado' }, tarjeta: { colCard: 'Contactado' } } },
  { id: '08e-leads-despues', steps: [{ go: '/marketing/leads' }, { drag: { from: 'Contactado', to: 'Interesado' } }], boxes: { contactado: { col: 'Contactado' }, interesado: { col: 'Interesado' }, movida: { moved: true } } },
  { id: '09-metricas-portales', steps: [{ go: '/metrics' }], boxes: { procedencia: card('Leads por procedencia'), embudo: card('Embudo de contactos'), agendamiento: card('Tasa agendamiento'), citados: { text: 'Citados', exact: true }, leyenda: { text: 'Idealista', exact: true } } },
  { id: '09a-rendimiento', steps: [{ go: '/metrics' }, { scrollTo: 'Rendimiento por propiedad' }], boxes: { seccion: card('Rendimiento por propiedad'), contactos: { th: 'Contactos' }, visitas: { th: 'Visitas' }, ofertas: { th: 'Ofertas' }, fila1: { css: 'main table', last: true, row: 0 } } },
  { id: '09b-metricas-propiedad', steps: [{ go: '/metrics' }, { scrollTo: 'Rendimiento por propiedad' }, { row: 'last' }, { period: 'Todo' }],
    boxes: { preguntado: card('Han preguntado'), visitas: card('Visitas realizadas'), ofertar: card('Quieren ofertar'), canceladas: card('Canceladas', { exact: true }), embudo: card('Embudo', { exact: true }), contactosPor: card('Contactos por'), visitasPor: card('Visitas por'), descartan: card('Por qué la descartan'), cancelaron: card('Por qué cancelaron') } },
  { id: '10a-direccion-reporte', steps: [{ go: '/management' }, { tab: 'Reporte comercial' }], boxes: { embudo: card('Embudo del equipo'), tabla: { css: 'main table' } } },
  { id: '10b-direccion-metas', steps: [{ go: '/management' }, { tab: 'Metas del mes' }], boxes: { comparativa: card('Comparativa del equipo'), tabla: { css: 'main table' } } },
  { id: '10c-direccion-facturado', steps: [{ go: '/management' }, { tab: 'Facturado' }], boxes: { cobrado: card('Cobrado'), pendiente: card('Pendiente total') } },
];

async function settle(page) {
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
  await page.evaluate(() => document.fonts && document.fonts.ready).catch(() => {});
  await page.waitForTimeout(1500);
}

async function login(browser) {
  const ctx = await browser.newContext(opts());
  const page = await ctx.newPage();
  await page.goto(URL_LOGIN, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await settle(page);
  await page.locator('input[type="email"], input[autocomplete="username"]').first().pressSequentially(EMAIL, { delay: 25 });
  await page.locator('input[type="password"]').first().pressSequentially(PASS, { delay: 25 });
  await page.locator('button[type="submit"]').first().click();
  await page.waitForFunction(() => !document.querySelector('input[type="password"]'), null, { timeout: 30000 });
  await settle(page);
  const home = page.url();
  await ctx.storageState({ path: STATE });
  fs.chmodSync(STATE, 0o600);
  await ctx.close();
  return home;
}

const loc = (page, s) => {
  let l = page.locator(s.click || s.css);
  if (s.hasText) l = l.filter({ hasText: s.exact ? new RegExp(`^\\s*${s.hasText}\\s*$`) : s.hasText });
  return l.first();
};

// Columna de tablero (kanban) cuyo encabezado contiene el texto: el ancestro alto y estrecho del encabezado
const COLUMN_FN = `(name) => {
  const heads = [...document.querySelectorAll('main *')].filter((e) => e.offsetParent && e.children.length <= 2 && (e.textContent || '').trim().replace(/\\s*·?\\s*\\d+$/, '').trim() === name);
  for (const h of heads) { let n = h; for (let i = 0; i < 8 && n; i++, n = n.parentElement) { const r = n.getBoundingClientRect(); if (r.height > 400 && r.width < 420 && r.width > 150) return n; } }
  return null;
}`;

let moved = null;
async function run(page, home, step) {
  if (step.go) { await page.goto(new URL(step.go, home).href, { waitUntil: 'domcontentloaded' }); return settle(page); }
  if ('firstLink' in step) {
    const hrefs = await page.$$eval('main a[href]', (as) => as.map((a) => a.getAttribute('href')));
    const h = hrefs.find((x) => x && x.includes(step.firstLink) && !(step.notEdit && /\/(edit|new)$/.test(x)));
    if (!h) throw new Error(`sin enlace que contenga ${step.firstLink}`);
    await page.goto(new URL(h, home).href, { waitUntil: 'domcontentloaded' }); return settle(page);
  }
  if (step.click) { await loc(page, step).click(); return settle(page); }
  if (step.type) { await page.locator(step.type).first().fill(step.text); await page.waitForTimeout(600); return settle(page); }
  if (step.clickText) { await page.getByText(step.clickText, { exact: false }).first().click(); return settle(page); }
  if ('row' in step) {
    const tables = page.locator('main table');
    const t = step.row === 'last' ? tables.last() : tables.first();
    await t.locator('tbody tr').first().click(); return settle(page);
  }
  if (step.tab) { await page.getByRole('tab', { name: step.tab, exact: true }).first().click(); return settle(page); }
  if (step.period) {
    const b = page.getByRole('button', { name: step.period, exact: true }).first();
    if (await b.isVisible().catch(() => false)) { await b.click(); await settle(page); }
    return;
  }
  if (step.scrollTo) {
    await page.getByText(step.scrollTo, { exact: true }).first().scrollIntoViewIfNeeded();
    await page.mouse.wheel(0, -120); return page.waitForTimeout(700);
  }
  if (step.drag) {
    // ÚNICA acción que modifica datos (autorizada): mover la primera tarjeta de una columna a otra
    const info = await page.evaluate(({ from, to, fn }) => {
      const col = eval(fn);
      const a = col(from), b = col(to);
      if (!a || !b) return null;
      const cardEl = [...a.querySelectorAll('*')].find((e) => /\+34\d{6,}/.test(e.textContent || '') && e.getBoundingClientRect().height > 60 && e.getBoundingClientRect().height < 200);
      if (!cardEl) return null;
      cardEl.scrollIntoView({ block: 'center' });
      const r = cardEl.getBoundingClientRect(), rb = b.getBoundingClientRect();
      const name = (cardEl.innerText || '').split('\n')[0].trim();
      return { name, x: r.x + r.width / 2, y: r.y + 24, tx: rb.x + rb.width / 2, ty: rb.y + 120 };
    }, { ...step.drag, fn: COLUMN_FN });
    if (!info) throw new Error('no encuentro las columnas o la tarjeta');
    await page.mouse.move(info.x, info.y);
    await page.mouse.down();
    await page.mouse.move(info.x + 12, info.y + 6, { steps: 4 });
    await page.mouse.move(info.tx, info.ty, { steps: 30 });
    await page.waitForTimeout(300);
    await page.mouse.up();
    await page.evaluate(() => window.getSelection()?.removeAllRanges());
    await settle(page);
    const ok = await page.evaluate(({ to, name, fn }) => { const c = eval(fn)(to); return !!c && (c.innerText || '').includes(name); }, { to: step.drag.to, name: info.name, fn: COLUMN_FN });
    moved = { name: info.name, from: step.drag.from, to: step.drag.to, ok };
    log(`    tarjeta «${info.name}»: ${step.drag.from} → ${step.drag.to} ${ok ? 'OK' : '(no se ve en la columna destino)'}`);
  }
}

// Calcula las cajas en coordenadas de documento (px CSS)
async function measure(page, boxes) {
  return page.evaluate(({ boxes, colFn, movedName }) => {
    const col = eval(colFn);
    const vis = (e) => e && e.offsetParent !== null;
    const doc = (r) => r && ({ x: Math.round(r.x + scrollX), y: Math.round(r.y + scrollY), w: Math.round(r.width), h: Math.round(r.height) });
    const isCard = (e) => { const cs = getComputedStyle(e); return parseFloat(cs.borderTopLeftRadius) >= 8 && (parseFloat(cs.borderTopWidth) > 0 || cs.boxShadow !== 'none'); };
    const byText = (s) => {
      const all = [...document.querySelectorAll('main *, [role="listbox"] *, [role="dialog"] *')].filter((e) => vis(e) && e.children.length <= 3);
      const t = (e) => (e.textContent || '').trim().replace(/\s+/g, ' ');
      const m = all.filter((e) => (s.exact ? t(e) === s.text : t(e).startsWith(s.text)) && ![...e.children].some((c) => (s.exact ? t(c) === s.text : t(c).startsWith(s.text))));
      let el = m[s.nth || 0];
      if (el && s.card) { let n = el; while (n && n.tagName !== 'MAIN' && !isCard(n)) n = n.parentElement; if (n && n.tagName !== 'MAIN') el = n; }
      return el;
    };
    const out = {};
    for (const [k, s] of Object.entries(boxes)) {
      try {
        let el = null, r = null;
        if (s.text) el = byText(s);
        else if (s.th) {
          const th = [...document.querySelectorAll('main th')].find((e) => vis(e) && (e.textContent || '').trim().replace(/\s*[↓↑]$/, '') === s.th);
          if (th) { const tb = th.closest('table').getBoundingClientRect(), rt = th.getBoundingClientRect(); r = { x: rt.x, y: rt.y, width: rt.width, height: tb.bottom - rt.y }; }
        } else if (s.col) el = col(s.col);
        else if (s.colCard) { const c = col(s.colCard); el = c && [...c.querySelectorAll('*')].find((e) => /\+34\d{6,}/.test(e.textContent || '') && e.getBoundingClientRect().height > 60 && e.getBoundingClientRect().height < 200); }
        else if (s.moved) { const c = movedName && col(movedName.to); el = c && [...c.querySelectorAll('*')].find((e) => (e.innerText || '').startsWith(movedName.name) && e.getBoundingClientRect().height > 60 && e.getBoundingClientRect().height < 200); }
        else if (s.bestRow) {
          const rows = [...document.querySelectorAll('main table tbody tr')].filter(vis);
          const cpl = (tr) => parseFloat((tr.lastElementChild?.textContent || '').replace(/[^\d,]/g, '').replace(',', '.')) || Infinity;
          el = rows.sort((a, b) => cpl(a) - cpl(b))[0];
        } else if (s.css) {
          let els = [...document.querySelectorAll(s.css)].filter(vis);
          if (s.hasText) els = els.filter((e) => s.exact ? (e.textContent || '').trim() === s.hasText : (e.textContent || '').includes(s.hasText));
          if (s.last) els = els.slice(-1);
          if (s.largest) els.sort((a, b) => b.getBoundingClientRect().width * b.getBoundingClientRect().height - a.getBoundingClientRect().width * a.getBoundingClientRect().height);
          el = els[0];
          if (el && 'row' in s) el = el.querySelectorAll('tbody tr')[s.row];
          if (el && s.card) { let n = el; while (n && n.tagName !== 'MAIN' && !isCard(n)) n = n.parentElement; if (n && n.tagName !== 'MAIN') el = n; }
          if (s.union && els.length) { const rs = els.slice(0, s.union).map((e) => e.getBoundingClientRect()); const x = Math.min(...rs.map((q) => q.x)), y = Math.min(...rs.map((q) => q.y)); r = { x, y, width: Math.max(...rs.map((q) => q.right)) - x, height: Math.max(...rs.map((q) => q.bottom)) - y }; }
        }
        out[k] = doc(r || (el && el.getBoundingClientRect())) || null;
      } catch (e) { out[k] = null; }
    }
    return out;
  }, { boxes, colFn: COLUMN_FN, movedName: moved });
}

// Oculta elementos flotantes fijos pegados al borde derecho (botón del engranaje)
const hideFloating = (page) => page.evaluate(() => {
  for (const e of document.querySelectorAll('body *')) {
    const cs = getComputedStyle(e);
    if (cs.position !== 'fixed') continue;
    const r = e.getBoundingClientRect();
    if (r.right >= innerWidth - 4 && r.width < 120 && r.height < 120) e.style.setProperty('visibility', 'hidden', 'important');
  }
});

fs.mkdirSync(OUT, { recursive: true });
const DRAG = process.argv.includes('--drag');
const only = process.argv.slice(2).filter((a) => a !== '--drag');
const browser = await chromium.launch({ executablePath: exe });
try {
  const home = await login(browser);
  log('login ok');
  const ctx = await browser.newContext(opts({ storageState: STATE }));
  // Oculta el email de la cuenta (texto y campos): texto transparente sobre su propio fondo, sin recuadro
  await ctx.addInitScript((email) => {
    const paint = () => {
      const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      for (let t; (t = w.nextNode());) if (t.nodeValue.includes(email)) {
        const el = t.parentElement; el.style.setProperty('color', 'transparent', 'important'); el.style.setProperty('text-shadow', 'none', 'important');
      }
      document.querySelectorAll('input').forEach((i) => { if (i.value && i.value.includes(email)) i.style.setProperty('color', 'transparent', 'important'); });
    };
    const start = () => { paint(); new MutationObserver(paint).observe(document.body, { subtree: true, childList: true, characterData: true }); };
    document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', start) : start();
  }, EMAIL);
  // El engranaje flotante (ajustes, icono girando) se vuelve a montar al navegar: se oculta también con una regla CSS fija
  await ctx.addInitScript(() => {
    const add = () => { const st = document.createElement('style'); st.textContent = 'button:has(> span[class*="settings"][class*="animate-spin"]){visibility:hidden!important}'; document.head.appendChild(st); };
    document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', add) : add();
  });
  const page = await ctx.newPage();
  for (const s of STATES.filter((x) => (!only.length || only.includes(x.id)) && (DRAG || !x.steps.some((st) => st.drag)))) {
    try {
      for (const st of s.steps) await run(page, home, st);
      await hideFloating(page);
      await page.evaluate(() => window.getSelection()?.removeAllRanges());
      const meta = await page.evaluate(() => ({ scrollY: Math.round(scrollY), pageH: document.documentElement.scrollHeight, url: location.pathname + location.search }));
      const boxes = await measure(page, s.boxes || {});
      await page.screenshot({ path: path.join(OUT, `${s.id}.png`), fullPage: true });
      fs.writeFileSync(path.join(OUT, `${s.id}.json`), JSON.stringify({ id: s.id, viewport: { w: 1920, h: 1080 }, scale: 2, ...meta, boxes, ...(s.id.startsWith('08e') ? { moved } : {}) }, null, 2));
      const missing = Object.entries(boxes).filter(([, v]) => !v).map(([k]) => k);
      log(`  ${s.id} → ${meta.url} · ${Object.keys(boxes).length - missing.length}/${Object.keys(boxes).length} cajas${missing.length ? ' (faltan: ' + missing.join(', ') + ')' : ''}`);
    } catch (e) {
      log(`  ${s.id}: FALLO ${e.message.split('\n')[0]}`);
    }
  }
  await ctx.close();
} catch (e) {
  console.error(redact(`Error: ${e.message}`));
  process.exitCode = 1;
} finally {
  await browser.close();
}
