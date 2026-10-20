// Capturas de todas las pantallas del guion del vídeo demo (ADV/ImperiOS Demo/GUION-DEMO.md), a 1920×1080 @2x.
// SOLO LECTURA: entra por URL, abre filas/pestañas y cambia de periodo; nunca pulsa botones de acción.
// Salida: out/demo/<id>.png (vista) y <id>-full.png (página completa) + out/demo/index.json
//
// Uso: node demo-shots.mjs [id ...]      (mismas variables de entorno que capture.mjs)
import { chromium } from 'playwright-core';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(process.env.CAPTURE_OUT || path.join(HERE, 'out'), 'demo');
const STATE = process.env.CAPTURE_STATE || path.join(os.tmpdir(), 'imperios-demo-state.json');
const { IMPERIOS_DEMO_URL: URL_LOGIN, IMPERIOS_DEMO_EMAIL: EMAIL, IMPERIOS_DEMO_PASSWORD: PASS } = process.env;
const redact = (s) => [EMAIL, PASS].filter(Boolean).reduce((t, v) => t.split(v).join('***'), String(s));
const log = (...a) => console.log(redact(a.join(' ')));
if (!URL_LOGIN || !EMAIL || !PASS) { console.error('Faltan IMPERIOS_DEMO_URL / _EMAIL / _PASSWORD'); process.exit(1); }
const exe = process.env.CHROMIUM_PATH ||
  (fs.existsSync('/opt/pw-browsers/chromium-1194/chrome-linux/chrome') ? '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' : undefined);
const opts = (extra = {}) => ({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2, locale: 'es-ES', timezoneId: 'Europe/Madrid', colorScheme: 'light', ...extra });

// Pantallas por escena del guion. Pasos: {go}, {firstLink}, {click: selector (primer elemento)}, {row: texto|null (primera fila)},
// {rowAfter: título de sección}, {tab: texto}, {period: texto}, {scrollTo: texto}
const SHOTS = [
  { id: '01-dashboard', steps: [{ go: '/' }] },
  { id: '02-contactos', steps: [{ go: '/contacts' }] },
  { id: '03-chat', steps: [{ go: '/leads' }, { click: 'main button[data-lead-id]' }] },
  { id: '04-cliente', steps: [{ go: '/clients' }, { firstLink: '/clients/demo-cli', notEdit: true }] },
  { id: '05a-propiedades', steps: [{ go: '/properties' }] },
  { id: '05b-propiedad-ficha', steps: [{ go: '/properties' }, { firstLink: '/properties/', notEdit: true }] },
  { id: '05c-publicaciones', steps: [{ go: '/publications' }] },
  { id: '06-coincidencias', steps: [{ go: '/matches' }] },
  { id: '07a-calendario', steps: [{ go: '/calendar' }] },
  { id: '07b-tareas', steps: [{ go: '/tasks' }] },
  { id: '07c-seguimientos', steps: [{ go: '/follow-ups' }] },
  { id: '08-whatsapp', steps: [{ go: '/settings/whatsapp' }] },
  { id: '09a-documentos', steps: [{ go: '/documents' }] },
  { id: '09b-hoja-visita', steps: [{ go: '/documents/visit-sheet' }] },
  { id: '10a-marketing', steps: [{ go: '/marketing' }] },
  { id: '10b-campana', steps: [{ go: '/marketing' }, { row: null }] },
  { id: '10c-conjunto', steps: [{ go: '/marketing' }, { row: null }, { firstLink: '/adsets/' }] },
  { id: '10d-leads-campana', steps: [{ go: '/marketing/leads' }] },
  { id: '11a-rendimiento-propiedades', steps: [{ go: '/metrics' }, { scrollTo: 'Rendimiento por propiedad' }] },
  { id: '11b-metricas-propiedad', steps: [{ go: '/metrics' }, { scrollTo: 'Rendimiento por propiedad' }, { rowAfter: 'Rendimiento por propiedad' }, { period: 'Todo' }] },
  { id: '12a-direccion-reporte', steps: [{ go: '/management' }, { tab: 'Reporte comercial' }] },
  { id: '12b-direccion-metas', steps: [{ go: '/management' }, { tab: 'Metas del mes' }] },
  { id: '12c-direccion-facturado', steps: [{ go: '/management' }, { tab: 'Facturado' }] },
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

async function run(page, home, step) {
  if (step.go) { await page.goto(new URL(step.go, home).href, { waitUntil: 'domcontentloaded' }); return settle(page); }
  if ('firstLink' in step) {
    const hrefs = await page.$$eval('main a[href]', (as) => as.map((a) => a.getAttribute('href')));
    const h = hrefs.find((x) => x && x.includes(step.firstLink) && !(step.notEdit && /\/(edit|new)$/.test(x)));
    if (!h) throw new Error(`sin enlace que contenga ${step.firstLink}`);
    await page.goto(new URL(h, home).href, { waitUntil: 'domcontentloaded' }); return settle(page);
  }
  if ('row' in step) {
    const rows = page.locator('main table tbody tr');
    await (step.row ? rows.filter({ hasText: step.row }) : rows).first().click(); return settle(page);
  }
  if (step.rowAfter) {
    // primera fila de la tabla de la sección con ese título (la tabla es la última de la página)
    await page.getByText(step.rowAfter, { exact: true }).first().scrollIntoViewIfNeeded();
    await page.locator('main table').last().locator('tbody tr').first().click(); return settle(page);
  }
  if (step.click) { await page.locator(step.click).first().click(); return settle(page); }
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
}

fs.mkdirSync(OUT, { recursive: true });
const only = process.argv.slice(2);
const browser = await chromium.launch({ executablePath: exe });
const idxFile = path.join(OUT, 'index.json');
const index = only.length && fs.existsSync(idxFile) ? JSON.parse(fs.readFileSync(idxFile, 'utf8')).filter((x) => !only.includes(x.id)) : [];
try {
  const home = await login(browser);
  log('login ok');
  const ctx = await browser.newContext(opts({ storageState: STATE }));
  // Tapa el email de la cuenta (texto y campos de formulario)
  await ctx.addInitScript((email) => {
    const paint = () => {
      const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      for (let t; (t = w.nextNode());) if (t.nodeValue.includes(email)) {
        const el = t.parentElement; el.style.setProperty('background', '#FF00FF', 'important'); el.style.setProperty('color', 'transparent', 'important');
      }
      document.querySelectorAll('input').forEach((i) => { if (i.value && i.value.includes(email)) i.style.setProperty('color', 'transparent', 'important'); });
    };
    const start = () => { paint(); new MutationObserver(paint).observe(document.body, { subtree: true, childList: true, characterData: true }); };
    document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', start) : start();
  }, EMAIL);
  const page = await ctx.newPage();
  for (const s of SHOTS.filter((x) => !only.length || only.includes(x.id))) {
    try {
      for (const st of s.steps) await run(page, home, st);
      await page.screenshot({ path: path.join(OUT, `${s.id}.png`) });
      await page.screenshot({ path: path.join(OUT, `${s.id}-full.png`), fullPage: true });
      const u = new URL(page.url());
      index.push({ id: s.id, path: u.pathname + u.search });
      log(`  ${s.id} → ${u.pathname}`);
    } catch (e) {
      log(`  ${s.id}: FALLO ${e.message.split('\n')[0]}`);
      index.push({ id: s.id, error: redact(e.message.split('\n')[0]) });
    }
  }
  index.sort((a, b) => a.id.localeCompare(b.id));
  fs.writeFileSync(idxFile, JSON.stringify(index, null, 2));
  await ctx.close();
} catch (e) {
  console.error(redact(`Error: ${e.message}`));
  process.exitCode = 1;
} finally {
  await browser.close();
}
