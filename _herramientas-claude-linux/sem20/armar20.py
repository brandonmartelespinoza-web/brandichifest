# armar20.py — ensambla GUIA-SEM20.html a partir del chasis de SEM17 + fragmentos por pestaña
import re, os, sys, json

W = '/home/user/w20/'
SRC17 = '/home/user/work/src/GUIA-SEM17.html'
OUT = '/home/user/brandichifest/SEM 20/GUIA-SEM20.html'

TABS = [
  # id, etiqueta nav, color, light, prefijo semáforo, título progreso
  ('cap', '🧱 Plan general del tubo', '#0891b2', '#ecfeff', 'ca', 'Estructura general, motilidad e inervación del tubo digestivo'),
  ('boc', '👄 Boca y dientes', '#db2777', '#fdf2f8', 'bo', 'Cavidad bucal y dientes'),
  ('len', '👅 Lengua y gusto', '#e11d48', '#fff1f2', 'le', 'Lengua y corpúsculos gustativos'),
  ('sal', '💧 Glándulas salivales', '#0284c7', '#f0f9ff', 'sa', 'Glándulas salivales y secreción salival'),
  ('eso', '🍽️ Faringe y esófago', '#7c3aed', '#f5f3ff', 'es', 'Orofaringe y esófago'),
  ('par', '🧍 Pared abdominal', '#ea580c', '#fff7ed', 'pa', 'Pared abdominal y conducto inguinal'),
  ('per', '🫙 Peritoneo', '#059669', '#ecfdf5', 'pe', 'Peritoneo'),
  ('est', '🫃 Estómago', '#dc2626', '#fef2f2', 'et', 'Estómago: anatomía e histología'),
  ('int', '🌀 Intestino delgado y grueso', '#ca8a04', '#fefce8', 'in', 'Intestino delgado, grueso y apéndice'),
]
TEST = ('test', '🔴 Test final', '#1e3a8a', '#eff6ff')

h = open(SRC17, encoding='utf8').read()

# ---------- HEAD + STYLE ----------
style = h[h.find('<style'):h.find('</style>') + len('</style>')]
# bloque de colores por pestaña
style = re.sub(r'\n  #tab-\w+\{--tab-color:[^}]*\}', '', style)
colors = ''.join(f'\n  #tab-{t}{{--tab-color:{c};--tab-light:{l}}}' for t, _, c, l, _, _ in TABS)
colors += f'\n  #tab-{TEST[0]}{{--tab-color:{TEST[2]};--tab-light:{TEST[3]}}}'
extra_css = '''
  /* ====== AGREGADOS SEM 19 ====== */
  .pt-bar{background:#e5e7eb;border-radius:999px;height:10px;overflow:hidden}
  .pt-fill{height:100%;width:0;border-radius:999px;background:linear-gradient(90deg,var(--tab-color),#34d399);transition:width .5s ease}
  figure.fig img{width:100%;height:auto;display:block;margin:0 auto;border-radius:8px;border:1px solid #e5e7eb}
  .grid2>*,.grid3>*,.cmp>*{min-width:0}
  .honesty{border-left:4px solid #ca8a04;background:#fefce8}
  .fig-svg text{font-family:'Inter','Segoe UI',system-ui,-apple-system,'Helvetica Neue',Arial,sans-serif}
  nav button{flex:1 1 0;min-width:0;white-space:normal;line-height:1.25;padding:12px 8px}
  header p{color:#e2e8f0;opacity:.9}
  @media(max-width:700px){nav button{flex:0 0 auto;white-space:nowrap;padding:12px 12px}}
  @media(max-width:600px){.tab-content{padding:16px}.section{padding:18px}header{padding:20px 16px}header h1{font-size:1.25rem}.hdr-icon{display:none}}'''
style = style.replace('</style>', colors + '\n' + extra_css + '\n</style>')
style = style.replace("font-family:'Inter',sans-serif",
                      "font-family:'Inter','Segoe UI',system-ui,-apple-system,'Helvetica Neue',Arial,sans-serif")

head = '''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Semana 20 – Morfofisiología del Aparato Digestivo I – UNT</title>
<link rel="preload" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" as="style">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
<noscript><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"></noscript>
''' + style + '\n</head>\n'

# ---------- SCRIPT ----------
script = h[h.rfind('<script>'):h.rfind('</script>') + len('</script>')]
script = script.replace('mf-s17-', 'mf-s20-')
mt_map = ',\n'.join(f"  'mt-{p}1':'{p}1','mt-{p}2':'{p}2'" for _, _, _, _, p, _ in TABS)
script = re.sub(r'const MT_SEMA_MAP = \{[\s\S]*?\};', 'const MT_SEMA_MAP = {\n' + mt_map + '\n};', script)
groups = ',\n'.join(f"  {t}:['{p}1','{p}2']" for t, _, _, _, p, _ in TABS)
script = re.sub(r'const SEMA_GROUPS=\{[\s\S]*?\};', 'const SEMA_GROUPS={\n' + groups + '\n};', script)

# ---------- BODY ----------
frag = {}
for t, *_ in TABS:
    frag[t] = open(W + f'frag/{t}.html', encoding='utf8').read()
frag['test'] = open(W + 'frag/test.html', encoding='utf8').read()
aviso = open(W + 'frag/aviso.html', encoding='utf8').read()

nav = '<nav id="navbar">\n'
for i, (t, lab, c, *_rest) in enumerate(TABS):
    nav += f'''  <button{' class="active"' if i == 0 else ''} onclick="show('{t}')" style="--tab-color:{c}">{lab}</button>\n'''
nav += f'''  <button onclick="show('test')" style="--tab-color:{TEST[2]}">{TEST[1]}</button>\n</nav>\n'''

body = '''<body>

<header>
  <div class="hdr-icon">🍽️</div>
  <div>
    <h1>Semana 20 — Morfofisiología del Aparato Digestivo I</h1>
    <p>Estructura histológica general del tubo digestivo · Motilidad · Cavidad bucal, labios, encías, paladar · Dientes · Lengua, papilas y corpúsculos gustativos · Glándulas salivales y secreción salival · Orofaringe · Esófago · Pared abdominal y conducto inguinal · Peritoneo · Estómago · Intestino delgado y grueso · Apéndice · Irrigación, linfáticos e inervación · Células enteroendocrinas · UNT 21/09 al 27/09</p>
  </div>
</header>

''' + nav + '\n' + aviso + '\n'

for i, (t, lab, c, l, p, titulo) in enumerate(TABS):
    body += f'''
<div id="tab-{t}" class="tab-content{' active' if i == 0 else ''}">
<div class="progress-tracker" id="pt-{t}">
  <div class="pt-header"><span class="pt-title">Progreso — {titulo}</span><span class="pt-pct" id="pt-{t}-pct">0%</span></div>
  <div class="pt-bar"><div class="pt-fill" id="pt-{t}-bar"></div></div>
  <div class="pt-dots" id="pt-{t}-dots"></div>
</div>
{frag[t].strip()}
</div>
'''
body += f'''
<div id="tab-test" class="tab-content">
{frag['test'].strip()}
</div>

'''

html = head + body + script + '\n</body>\n</html>\n'

# ---------- renumerar figuras ----------
n = 0
def ren(m):
    global n
    n += 1
    return f'<span class="fig-tag">Figura {n}</span>'
html = re.sub(r'<span class="fig-tag">Figura [^<]*</span>', ren, html)

# ---------- initDrag con los dd reales ----------
dds = re.findall(r'<div class="dragdrop" id="(dd-[a-z0-9]+)"', html)
html = re.sub(r"\[('dd-[a-z0-9]+',?)*\]\.forEach\(initDrag\)",
              '[' + ','.join(f"'{d}'" for d in dds) + '].forEach(initDrag)', html)

# ---------- incrustar imágenes (archivo único, funciona aunque se separe de img/) ----------
import base64
IMGDIR = os.path.join(os.path.dirname(OUT), 'img')
def emb(m):
    f = m.group(1)
    data = open(os.path.join(IMGDIR, f), 'rb').read()
    mime = 'image/png' if f.endswith('.png') else 'image/jpeg'
    return 'src="data:%s;base64,%s" data-file="%s"' % (mime, base64.b64encode(data).decode(), f)
if '--embed' in sys.argv:
    html = re.sub(r'src="img/([^"]+)"', emb, html)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'w', encoding='utf8').write(html)
print('OK', OUT, len(html) // 1024, 'KB', '| figuras', n, '| dragdrops', dds)
