// Capturas reales del CRM desde la cuenta demo (datos simulados), para la versión «producto real» en HyperFrames.
//
// Uso:
//   node capture.mjs check              # solo login; guarda la sesión
//   node capture.mjs explore            # login + mapa de la navegación (out/explore.json) + captura de la home
//   node capture.mjs shots [ids...]     # capturas a 2x de cada pantalla de screens.json
//   node capture.mjs record [ids...]    # grabación (webm → mp4) de las interacciones de cada pantalla
//
// Variables de entorno: IMPERIOS_DEMO_URL (login), IMPERIOS_DEMO_EMAIL, IMPERIOS_DEMO_PASSWORD,
// CHROMIUM_PATH (opcional), CAPTURE_OUT (opcional, por defecto ./out), CAPTURE_STATE (opcional).
// Las credenciales nunca se escriben en disco, en logs ni en la grabación: el login se hace en un
// contexto sin vídeo y solo se reutiliza su estado de sesión (cookies/localStorage), fuera del repo.
import { chromium } from 'playwright-core';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const CFG = JSON.parse(fs.readFileSync(path.join(HERE, 'screens.json'), 'utf8'));
const OUT = path.resolve(process.env.CAPTURE_OUT || path.join(HERE, 'out'));
const STATE = process.env.CAPTURE_STATE || path.join(os.tmpdir(), 'imperios-demo-state.json');
const { IMPERIOS_DEMO_URL: URL_LOGIN, IMPERIOS_DEMO_EMAIL: EMAIL, IMPERIOS_DEMO_PASSWORD: PASS } = process.env;
const SECRETS = [EMAIL, PASS].filter(Boolean);

const redact = (s) => SECRETS.reduce((t, v) => t.split(v).join('***'), String(s));
const log = (...a) => console.log(redact(a.join(' ')));
const die = (m) => { console.error(redact(m)); process.exit(1); };

for (const [k, v] of Object.entries({ IMPERIOS_DEMO_URL: URL_LOGIN, IMPERIOS_DEMO_EMAIL: EMAIL, IMPERIOS_DEMO_PASSWORD: PASS }))
  if (!v) die(`Falta la variable ${k}`);

const ORIGIN = new URL(URL_LOGIN).origin;
const exe = process.env.CHROMIUM_PATH ||
  (fs.existsSync('/opt/pw-browsers/chromium-1194/chrome-linux/chrome') ? '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' : undefined);

const ctxOpts = (extra = {}) => ({
  viewport: CFG.viewport,
  deviceScaleFactor: CFG.deviceScaleFactor,
  locale: CFG.locale,
  timezoneId: CFG.timezoneId,
  colorScheme: 'light',
  ...extra,
});

async function settle(page) {
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
  await page.evaluate(() => document.fonts && document.fonts.ready).catch(() => {});
  await page.waitForTimeout(600);
}

async function firstVisible(page, selectors) {
  for (const s of selectors) {
    const l = page.locator(s).first();
    if (await l.isVisible().catch(() => false)) return l;
  }
  return null;
}

async function login(browser) {
  const ctx = await browser.newContext(ctxOpts());
  const page = await ctx.newPage();
  await page.goto(URL_LOGIN, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await settle(page);
  const user = await firstVisible(page, [
    'input[type="email"]', 'input[autocomplete="username"]', 'input[name*="mail" i]', 'input[id*="mail" i]',
    'input[name*="user" i]', 'input[id*="user" i]', 'input[type="text"]',
  ]);
  const pass = await firstVisible(page, ['input[type="password"]']);
  if (!user || !pass) {
    await page.screenshot({ path: path.join(OUT, '_login-no-form.png') });
    die('No encuentro el formulario de login (ver out/_login-no-form.png)');
  }
  await user.fill(EMAIL);
  await pass.fill(PASS);
  const submit = await firstVisible(page, [
    'button[type="submit"]', 'input[type="submit"]',
    'button:has-text("Entrar")', 'button:has-text("Iniciar")', 'button:has-text("Acceder")',
    'button:has-text("Login")', 'button:has-text("Sign in")', 'button:has-text("Log in")',
  ]);
  if (submit) await submit.click(); else await pass.press('Enter');
  try {
    await page.waitForFunction(() => !document.querySelector('input[type="password"]'), null, { timeout: 30000 });
  } catch {
    await page.screenshot({ path: path.join(OUT, '_login-failed.png') });
    die('El login no ha terminado (ver out/_login-failed.png; la captura no muestra la contraseña)');
  }
  await settle(page);
  const home = page.url();
  await ctx.storageState({ path: STATE });
  fs.chmodSync(STATE, 0o600);
  await ctx.close();
  log(`login ok → ${new URL(home).pathname}`);
  return home;
}

// Oculta en las capturas cualquier elemento que muestre el email de la cuenta demo, más los selectores de screens.json.
function masks(page) {
  return [page.getByText(EMAIL, { exact: false }), ...(CFG.mask || []).map((s) => page.locator(s))];
}

async function navLinks(page) {
  return page.evaluate(() => {
    const seen = new Set();
    return [...document.querySelectorAll('nav a, aside a, header a, [role="navigation"] a, a[href], [role="menuitem"], [role="tab"]')]
      .filter((el) => el.offsetParent !== null)
      .map((el) => ({ text: (el.innerText || el.getAttribute('aria-label') || '').trim().replace(/\s+/g, ' '), href: el.getAttribute('href') || null }))
      .filter((l) => l.text && l.text.length < 60 && !seen.has(l.text + l.href) && seen.add(l.text + l.href));
  });
}

async function goToScreen(page, home, s) {
  if (s.path) {
    await page.goto(new URL(s.path, ORIGIN).href, { waitUntil: 'domcontentloaded' });
  } else {
    await page.goto(home, { waitUntil: 'domcontentloaded' });
    await settle(page);
    let clicked = false;
    for (const label of s.nav || []) {
      const l = page.getByRole('link', { name: label, exact: false }).or(page.getByRole('button', { name: label, exact: false })).first();
      if (await l.isVisible().catch(() => false)) { await l.click(); clicked = label; break; }
    }
    if (!clicked) return false;
    log(`  ${s.id}: menú «${clicked}»`);
  }
  await settle(page);
  if (s.waitFor) await page.locator(s.waitFor).first().waitFor({ timeout: 15000 }).catch(() => {});
  return true;
}

async function runSteps(page, steps = []) {
  for (const st of steps) {
    if (st.do === 'wait') await page.waitForTimeout(st.ms || 500);
    else if (st.do === 'scroll') await page.mouse.wheel(0, st.y || 0), await page.waitForTimeout(400);
    else if (st.do === 'hover') await page.locator(st.sel).first().hover();
    else if (st.do === 'click') await page.locator(st.sel).first().click(), await settle(page);
    else if (st.do === 'type') await page.locator(st.sel).first().pressSequentially(st.text, { delay: st.delay || 70 });
  }
}

const mode = process.argv[2] || 'check';
const only = process.argv.slice(3);
const screens = CFG.screens.filter((s) => !only.length || only.includes(s.id));
fs.mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch({ executablePath: exe });
try {
  const home = await login(browser);
  if (mode === 'check') process.exit(0);

  if (mode === 'explore' || mode === 'shots') {
    const ctx = await browser.newContext(ctxOpts({ storageState: STATE }));
    const page = await ctx.newPage();
    if (mode === 'explore') {
      await page.goto(home, { waitUntil: 'domcontentloaded' });
      await settle(page);
      const links = await navLinks(page);
      fs.writeFileSync(path.join(OUT, 'explore.json'), redact(JSON.stringify({ home: new URL(home).pathname, links }, null, 2)));
      await page.screenshot({ path: path.join(OUT, '00-home@2x.png'), mask: masks(page) });
      log(`${links.length} enlaces → out/explore.json; home → out/00-home@2x.png`);
    } else {
      for (const s of screens) {
        if (!(await goToScreen(page, home, s))) { log(`  ${s.id}: sin entrada de menú (${(s.nav || []).join(' / ')}); pon "path" en screens.json`); continue; }
        await page.screenshot({ path: path.join(OUT, `${s.id}@2x.png`), mask: masks(page) });
        await page.screenshot({ path: path.join(OUT, `${s.id}-full@2x.png`), fullPage: true, mask: masks(page) });
        fs.writeFileSync(path.join(OUT, `${s.id}.json`), JSON.stringify({ id: s.id, beat: s.beat, path: new URL(page.url()).pathname }, null, 2));
        log(`  ${s.id}: ok`);
      }
    }
    await ctx.close();
  }

  if (mode === 'record') {
    const size = { width: CFG.viewport.width * CFG.deviceScaleFactor, height: CFG.viewport.height * CFG.deviceScaleFactor };
    for (const s of screens) {
      const dir = path.join(OUT, '_video', s.id);
      fs.rmSync(dir, { recursive: true, force: true });
      const ctx = await browser.newContext(ctxOpts({ storageState: STATE, recordVideo: { dir, size } }));
      const page = await ctx.newPage();
      const ok = await goToScreen(page, home, s);
      if (ok) await runSteps(page, s.record);
      const video = page.video();
      await ctx.close();
      if (!ok) { log(`  ${s.id}: sin entrada de menú; no se graba`); continue; }
      const webm = await video.path();
      const mp4 = path.join(OUT, `${s.id}.mp4`);
      execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', webm, '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', '-r', '60', mp4]);
      log(`  ${s.id}: ${mp4.startsWith(HERE) ? path.relative(HERE, mp4) : mp4}`);
    }
  }
} catch (e) {
  die(`Error: ${e.message}`);
} finally {
  await browser.close();
}
