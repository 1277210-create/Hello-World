import html
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hello World Motion Lab", page_icon="✨", layout="wide")

st.title("✨ Hello World Motion Lab")
st.caption("A tiny app for experimenting with names, typography, backgrounds, and motion.")

with st.sidebar:
    st.header("Controls")
    name = st.text_input("Your name", value="Hello World", max_chars=80)
    font_family = st.selectbox(
        "Font type",
        ["Arial", "Courier New", "Georgia", "Times New Roman", "Verdana",
         "Trebuchet MS", "Impact", "Comic Sans MS", "Palatino Linotype"],
    )
    font_size = st.slider("Font size (px)", min_value=20, max_value=120, value=48, step=2)
    background = st.selectbox(
        "Background",
        ["Light", "Dark", "Sky", "Sunset", "Forest", "Lavender", "Ocean", "Midnight"],
    )
    name_mode = st.selectbox("Name display mode", ["Centered", "Ticker Tape", "Repeated"])
    effect = st.selectbox(
        "Dynamic action",
        ["None", "Rain", "Snow", "Hail", "Wind Gust", "Confetti", "Tornado"],
    )
    speed = st.slider("Animation speed", min_value=0.5, max_value=2.5, value=1.0, step=0.1)
    st.caption("Tip: change one control at a time to see how it affects the display.")

backgrounds = {
    "Light": ("#f8fafc", "#111827"),
    "Dark": ("#111827", "#f9fafb"),
    "Sky": ("#dff4ff", "#10324a"),
    "Sunset": ("#ffcfb3", "#53284f"),
    "Forest": ("#173b2b", "#f0fff4"),
    "Lavender": ("#eee7ff", "#34245c"),
    "Ocean": ("#006d77", "#f0ffff"),
    "Midnight": ("#090b2b", "#e7e9ff"),
}
bg_color, text_color = backgrounds[background]
safe_name = html.escape(name) if name else "Your name appears here"
safe_font = html.escape(font_family, quote=True)

# Each effect is animated entirely in the embedded browser. This avoids rerunning
# the Streamlit script continuously and keeps the animation smooth.
page_html = r"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; }
  html, body { margin: 0; width: 100%; height: 100%; }
  body { font-family: __FONT__; }
  .stage {
    position: relative; width: 100%; height: 620px; overflow: hidden;
    border-radius: 18px; background: __BG__; color: __FG__;
    isolation: isolate;
  }
  #particles { position:absolute; inset:0; width:100%; height:100%; z-index:1; pointer-events:none; }
  .name-wrap {
    position:absolute; inset:0; z-index:3; display:flex; align-items:center;
    justify-content:center; padding:28px; overflow:hidden;
  }
  .name {
    font-size: __SIZE__px; font-weight:800; line-height:1.15;
    text-align:center; overflow-wrap:anywhere; max-width:100%;
    text-shadow: 0 2px 14px rgba(0,0,0,.12);
  }
  .ticker { white-space:nowrap; max-width:none; animation: marquee __TICKER_DURATION__s linear infinite; }
  .repeated { display:flex; flex-direction:column; gap:14px; align-items:center; }
  .repeated span { display:block; }
  .label {
    position:absolute; left:16px; bottom:12px; z-index:4; opacity:.65;
    font: 12px/1.4 system-ui, sans-serif; letter-spacing:.08em; text-transform:uppercase;
  }
  @keyframes marquee {
    from { transform:translateX(100%); }
    to { transform:translateX(-100%); }
  }
  @media (prefers-reduced-motion: reduce) {
    .ticker { animation-duration: __TICKER_DURATION_REDUCED__s; }
  }
</style>
</head>
<body>
<div class="stage" id="stage">
  <canvas id="particles"></canvas>
  <div class="name-wrap" id="nameWrap">__NAME_MARKUP__</div>
  <div class="label">Hello World Motion Lab</div>
</div>
<script>
(() => {
  const canvas = document.getElementById('particles');
  const ctx = canvas.getContext('2d');
  const stage = document.getElementById('stage');
  const effect = __EFFECT__;
  const speed = __SPEED__;
  let w = 0, h = 0, particles = [], raf = 0, last = 0;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function resize() {
    const rect = stage.getBoundingClientRect();
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    w = rect.width; h = rect.height;
    canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr);
    canvas.style.width = w + 'px'; canvas.style.height = h + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    makeParticles();
  }
  function rand(min, max) { return Math.random() * (max - min) + min; }
  function makeParticles() {
    const count = effect === 'None' ? 0 :
      effect === 'Confetti' ? 100 : effect === 'Tornado' ? 90 : 115;
    particles = Array.from({length: count}, () => ({
      x: rand(0, Math.max(w, 1)), y: rand(0, Math.max(h, 1)),
      vx: rand(-1, 1), vy: rand(1, 4), size: rand(2, 7),
      hue: rand(0, 360), angle: rand(0, Math.PI * 2), spin: rand(-.08, .08)
    }));
  }
  function drawRain(p, dt) {
    ctx.strokeStyle = 'rgba(65,160,255,.75)'; ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(p.x - 4, p.y + p.size * 3); ctx.stroke();
    p.x -= 1.5 * dt * speed; p.y += (7 + p.size) * dt * speed;
    if (p.y > h + 10) { p.y = -10; p.x = rand(0, w); }
    if (p.x < -10) p.x = w + 10;
  }
  function drawSnow(p, dt) {
    ctx.fillStyle = 'rgba(255,255,255,.95)';
    ctx.beginPath(); ctx.arc(p.x, p.y, p.size * .65, 0, Math.PI * 2); ctx.fill();
    p.x += Math.sin(p.y * .018 + p.angle) * 1.2 * dt * speed;
    p.y += (1.1 + p.size * .35) * dt * speed;
    if (p.y > h + 8) { p.y = -8; p.x = rand(0, w); }
    if (p.x < 0) p.x = w; if (p.x > w) p.x = 0;
  }
  function drawHail(p, dt) {
    ctx.fillStyle = 'rgba(180,225,255,.95)';
    ctx.beginPath(); ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = 'rgba(65,125,180,.75)'; ctx.stroke();
    p.x += 1.2 * dt * speed; p.y += (5 + p.size) * dt * speed;
    if (p.y > h + 10) { p.y = -10; p.x = rand(0, w); }
    if (p.x > w + 10) p.x = -10;
  }
  function drawWind(p, dt) {
    ctx.strokeStyle = 'rgba(125,190,220,.8)'; ctx.lineWidth = p.size * .35;
    ctx.lineCap = 'round'; ctx.beginPath();
    ctx.moveTo(p.x, p.y); ctx.bezierCurveTo(p.x + 14, p.y - 8, p.x + 25, p.y + 8, p.x + 42, p.y);
    ctx.stroke();
    p.x += (5 + p.size) * dt * speed; p.y += Math.sin(p.x * .025) * dt * speed;
    if (p.x > w + 50) { p.x = -50; p.y = rand(0, h); }
  }
  function drawConfetti(p, dt) {
    ctx.fillStyle = `hsl(${p.hue},90%,60%)`;
    ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.angle);
    ctx.fillRect(-p.size, -p.size * .45, p.size * 2, p.size); ctx.restore();
    p.x += (Math.sin(p.angle) * 2 + .7) * dt * speed;
    p.y += (2 + p.size * .5) * dt * speed; p.angle += p.spin * dt * speed;
    if (p.y > h + 10) { p.y = -10; p.x = rand(0, w); }
    if (p.x > w + 10) p.x = -10;
  }
  function drawTornado(p, dt) {
    const cx = w * .5, cy = h * .52;
    p.angle += .035 * dt * speed;
    p.y += .6 * dt * speed;
    if (p.y > h + 10) p.y = -10;
    const band = (p.y / Math.max(h, 1));
    const radius = 10 + band * Math.min(w * .42, 240);
    p.x = cx + Math.cos(p.angle) * radius;
    ctx.fillStyle = `rgba(170,185,195,${.25 + band * .35})`;
    ctx.beginPath(); ctx.ellipse(p.x, p.y, p.size * 1.8, p.size * .65, p.angle, 0, Math.PI * 2); ctx.fill();
  }
  function frame(now) {
    if (reduced) { ctx.clearRect(0, 0, w, h); return; }
    const dt = Math.min((now - (last || now)) / 16.67, 2.5);
    last = now; ctx.clearRect(0, 0, w, h);
    for (const p of particles) {
      if (effect === 'Rain') drawRain(p, dt);
      else if (effect === 'Snow') drawSnow(p, dt);
      else if (effect === 'Hail') drawHail(p, dt);
      else if (effect === 'Wind Gust') drawWind(p, dt);
      else if (effect === 'Confetti') drawConfetti(p, dt);
      else if (effect === 'Tornado') drawTornado(p, dt);
    }
    raf = requestAnimationFrame(frame);
  }
  resize();
  if (effect !== 'None' && !reduced) raf = requestAnimationFrame(frame);
  window.addEventListener('resize', resize);
})();
</script>
</body>
</html>
"""

if name_mode == "Centered":
    name_markup = f'<div class="name">{safe_name}</div>'
elif name_mode == "Ticker Tape":
    name_markup = f'<div class="name ticker">{safe_name}</div>'
else:
    repeated = "".join(f"<span>{safe_name}</span>" for _ in range(5))
    name_markup = f'<div class="name repeated">{repeated}</div>'

replacements = {
    "__FONT__": safe_font,
    "__BG__": bg_color,
    "__FG__": text_color,
    "__SIZE__": str(font_size),
    "__NAME_MARKUP__": name_markup,
    "__EFFECT__": repr(effect),
    "__SPEED__": str(speed),
    "__TICKER_DURATION__": str(max(8 / speed, 3)),
    "__TICKER_DURATION_REDUCED__": str(max(8 / speed, 3)),
}
for token, value in replacements.items():
    page_html = page_html.replace(token, value)

components.html(page_html, height=640, scrolling=False)

st.markdown(
    "Built with **Streamlit** and browser-side HTML/CSS/JavaScript. "
    "The motion runs in the embedded browser, so the Python app does not need a continuous rerun loop."
)
