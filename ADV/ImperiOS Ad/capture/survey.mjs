// Recorrido de exploración de la cuenta demo a 1920×1080 (16:9), SOLO LECTURA: navega por el menú lateral,
// abre pestañas y enlaces a fichas de detalle, pero nunca pulsa botones de acción.
// Salida: out/survey/<nn>-<módulo>[-tab|-detalle]@2x.png + out/survey/survey.json (rutas, títulos, pestañas, botones visibles).
//
// Uso: node survey.mjs     (mismas variables de entorno que capture.mjs)
import { chromium } from 'playwright-core';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(process.env.CAPTURE_OUT || path.join(HERE, 'out'), 'survey');
const STATE = process.env.CAPTURE_STATE || path.join(os.tmpdir(), 'imperios-demo-state.json');
const { IMPERIOS_DEMO_URL: URL_LOGIN, IMPERIOS_DEMO_EMAIL: EMAIL, IMPERIOS_DEMO_PASSWORD: PASS } = process.env;
const redact = (s) => [EMAIL, PASS].filter(Boolean).reduce((t, v) => t.split(v).join('***'), String(s));
const log = (...a) => console.log(redact(a.join(' ')));
if (!URL_LOGIN || !EMAIL || !PASS) { console.error('Faltan IMPERIOS_DEMO_URL / _EMAIL / _PASSWORD'); process.exit(1); }

const VIEWPORT = { width: 1920, height: 1080 };
const exe = process.env.CHROMIUM_PATH ||
  (fs.existsSync('/opt/pw-browsers/chromium-1194/chrome-linux/chrome') ? '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' : undefined);
const opts = (extra = {}) => ({ viewport: VIEWPORT, deviceScaleFactor: 2, locale: 'es-ES', timezoneId: 'Europe/Madrid', colorScheme: 'light', ...extra });
// Acciones que nunca se pulsan en este recorrido (aunque parezcan navegación)
const DANGER = /(eliminar|borrar|delete|archivar|enviar|send|guardar|save|crear|nuevo|nueva|añadir|recalcular|actualizar|sincronizar|publicar|importar|desconectar|cerrar sesi|accept|aceptar|firmar|rechazar|\/edit|\/new)/i;

const slug = (s) => redact(s).normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 40);
async function settle(page) {
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
  await page.evaluate(() => document.fonts && document.fonts.ready).catch(() => {});
  await page.waitForTimeout(900);
}

async function login(browser) {
  const ctx = await browser.newContext(opts());
  const page = await ctx.newPage();
  await page.goto(URL_LOGIN, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await settle(page);
  const user = page.locator('input[type="email"], input[autocomplete="username"]').first();
  const pass = page.locator('input[type="password"]').first();
  await user.click(); await user.pressSequentially(EMAIL, { delay: 30 });
  await pass.click(); await pass.pressSequentially(PASS, { delay: 30 });
  await page.locator('button[type="submit"]').first().click();
  await page.waitForFunction(() => !document.querySelector('input[type="password"]'), null, { timeout: 30000 });
  await settle(page);
  const home = page.url();
  await ctx.storageState({ path: STATE });
  fs.chmodSync(STATE, 0o600);
  await ctx.close();
  return home;
}

fs.mkdirSync(OUT, { recursive: true });
const browser = await chromium.launch({ executablePath: exe });
const report = { viewport: VIEWPORT, modules: [] };
let n = 0;
try {
  const home = await login(browser);
  log('login ok');
  const ctx = await browser.newContext(opts({ storageState: STATE }));
  // Oculta el email de la cuenta donde aparezca: texto transparente sobre su propio fondo (sin recuadro de color)
  await ctx.addInitScript((email) => {
    const paint = () => {
      const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      for (let t; (t = w.nextNode());) if (t.nodeValue.includes(email)) {
        const el = t.parentElement; el.style.setProperty('color', 'transparent', 'important'); el.style.setProperty('text-shadow', 'none', 'important');
      }
    };
    const start = () => { paint(); new MutationObserver(paint).observe(document.body, { subtree: true, childList: true, characterData: true }); };
    document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', start) : start();
  }, EMAIL);
  const page = await ctx.newPage();
  const shot = async (name) => {
    const file = `${String(++n).padStart(2, '0')}-${name}@2x.png`;
    await page.screenshot({ path: path.join(OUT, file) });
    return file;
  };
  const describe = () => page.evaluate(() => {
    const main = document.querySelector('main') || document.body;
    const vis = (el) => el.offsetParent !== null;
    const txt = (el) => (el.innerText || el.getAttribute('aria-label') || '').trim().replace(/\s+/g, ' ');
    return {
      h1: txt(main.querySelector('h1') || document.createElement('i')),
      tabs: [...main.querySelectorAll('[role="tab"]')].filter(vis).map(txt).filter(Boolean),
      buttons: [...new Set([...main.querySelectorAll('button')].filter(vis).map(txt).filter((t) => t && t.length < 40))],
      links: [...main.querySelectorAll('a[href]')].filter(vis).map((a) => ({ text: txt(a).slice(0, 60), href: a.getAttribute('href') })),
    };
  });

  await page.goto(home, { waitUntil: 'domcontentloaded' });
  await settle(page);
  // Rutas de los módulos del menú lateral (descubiertas en el primer recorrido); se entra directamente en cada una
  const ROUTES = [['Dashboard', '/'], ['Métricas', '/metrics'], ['Dirección', '/management'], ['Marketing', '/marketing'],
    ['Propiedades', '/properties'], ['Publicaciones', '/publications'], ['Contactos', '/contacts'], ['Clientes', '/clients'],
    ['Coincidencias', '/matches'], ['Documentos', '/documents'], ['Chat', '/leads'], ['Email', '/email'], ['Tareas', '/tasks'],
    ['Calendario', '/calendar'], ['Seguimientos', '/follow-ups'], ['Reporte diario', '/objectives'], ['Prospectos', '/prospects'],
    ['Ajustes', '/settings/profile']];

  // Con argumentos se recorren solo esas rutas (p. ej. node survey.mjs "/leads?leadId=…" /settings/team)
  const LIST = process.argv.length > 2 ? process.argv.slice(2).map((r) => [r, r]) : ROUTES;
  n = process.argv.length > 2 ? fs.readdirSync(OUT).filter((f) => f.endsWith('.png')).length : 0;
  for (const [label, path0] of LIST) {
    await page.goto(new URL(path0, home).href, { waitUntil: 'domcontentloaded' });
    await settle(page);
    await page.waitForTimeout(1200);
    const route = new URL(page.url()).pathname + new URL(page.url()).search;
    const info = await describe();
    const mod = { label, route, ...info, shots: [await shot(slug(label))] };

    // Pestañas del módulo (cambiar de pestaña no modifica datos)
    for (const tab of info.tabs.slice(0, 6)) {
      if (DANGER.test(tab)) continue;
      const t = page.getByRole('tab', { name: tab, exact: true }).first();
      if (!(await t.isVisible().catch(() => false))) continue;
      await t.click().catch(() => {});
      await settle(page);
      mod.shots.push(await shot(`${slug(label)}-tab-${slug(tab)}`));
    }

    // Primera ficha de detalle: primer enlace interno del contenido que lleve a otra ruta con identificador
    const detail = info.links.find((l) => l.href && l.href.startsWith('/') && !DANGER.test(l.text) && !DANGER.test(l.href) &&
      (/[?&][a-z]*id=/i.test(l.href) || /\/[0-9a-z-]{6,}$/i.test(l.href)) && !l.href.startsWith(route));
    if (detail) {
      await page.goto(new URL(detail.href, home).href, { waitUntil: 'domcontentloaded' });
      await settle(page);
      mod.detail = { from: detail.href, route: new URL(page.url()).pathname, ...(await describe()) };
      mod.shots.push(await shot(`${slug(label)}-detalle`));
    }
    report.modules.push(mod);
    log(`  ${label} → ${route} (${mod.shots.length} capturas)`);
  }
  const outJson = path.join(OUT, process.argv.length > 2 ? 'survey-extra.json' : 'survey.json');
  fs.writeFileSync(outJson, redact(JSON.stringify(report, null, 2)));
  await ctx.close();
} catch (e) {
  console.error(redact(`Error: ${e.message}`));
  process.exitCode = 1;
} finally {
  await browser.close();
}
