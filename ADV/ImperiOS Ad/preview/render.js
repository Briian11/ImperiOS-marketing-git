// Uso:
//   node render.js stills <out_dir> t1 t2 ...       -> PNG de instantes concretos
//   node render.js video <out.mp4> [sub=3]          -> vídeo 60 fps con motion blur por submuestreo
const { chromium } = require(process.env.PW || 'playwright-core');
const { spawn } = require('child_process');
const fs = require('fs'), path = require('path');
const TL = JSON.parse(fs.readFileSync(path.join(__dirname, process.env.TL || 'timeline.json')));
const VARIANT = process.env.VARIANT || 'A';
(async () => {
  const [mode, out, ...rest] = process.argv.slice(2);
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--disable-gpu-vsync'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.join(__dirname, 'src/reel.html'));
  await p.evaluate(async ([beats, v]) => { await window.ready; window.setBeats(beats); window.setVariant(v); }, [TL.beats, VARIANT]);
  if (mode === 'stills') {
    fs.mkdirSync(out, { recursive: true });
    for (const t of rest.map(Number)) {
      await p.evaluate(t => window.render(t), t);
      await p.screenshot({ path: path.join(out, `t_${t.toFixed(2).padStart(5, '0')}.png`) });
    }
  } else {
    const sub = +(rest[0] || 3), fps = TL.fps * sub;
    const T0 = +(rest[1] || 0), T1 = +(rest[2] || TL.duration);
    const i0 = Math.round(T0 * fps), n = Math.round(T1 * fps);
    const ff = spawn('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
      '-vf', `tmix=frames=${sub}:weights='${Array(sub).fill(1).join(' ')}',fps=${TL.fps}`,
      '-c:v', 'libx264', '-preset', 'slow', '-crf', '14', '-pix_fmt', 'yuv420p', '-r', String(TL.fps), out], { stdio: ['pipe', 'inherit', 'inherit'] });
    const t0 = Date.now();
    for (let i = i0; i < n; i++) {
      await p.evaluate(t => window.render(t), i / fps);
      const buf = await p.screenshot({ type: 'jpeg', quality: 94 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (i % 300 === 0) console.log(`frame ${i}/${n} · ${((Date.now() - t0) / 1000).toFixed(0)} s`);
    }
    ff.stdin.end();
    await new Promise(r => ff.on('close', r));
  }
  await b.close();
})();
