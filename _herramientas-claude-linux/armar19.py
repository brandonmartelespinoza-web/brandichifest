# armar19.py — ensambla GUIA-SEM19.html a partir del chasis de SEM17 + fragmentos por pestaña
import re, os, sys, json

W = '/home/user/work/'
SRC17 = W + 'src/GUIA-SEM17.html'
OUT = '/home/user/brandichifest/SEM 19/GUIA-SEM19.html'

TABS = [
  # id, etiqueta nav, color, light, prefijo semáforo, título progreso
  ('par', '🦴 Pared torácica y diafragma', '#0891b2', '#ecfeff', 'pa', 'Pared torácica y diafragma'),
  ('pul', '🫁 Pulmones, bronquios y pleura', '#7c3aed', '#f5f3ff', 'pu', 'Pulmones, árbol bronquial y pleura'),
  ('med', '🧭 Mediastino y ganglios', '#db2777', '#fdf2f8', 'me', 'Mediastino y ganglios linfáticos'),
  ('mec', '🌬️ Mecánica respiratoria', '#ea580c', '#fff7ed', 'mc', 'Respiración y mecánica ventilatoria'),
  ('esp', '📈 Espirometría y ventilación', '#059669', '#ecfdf5', 'es', 'Espirometría y ventilación alveolar'),
  ('gas', '🩸 Transporte de gases', '#dc2626', '#fef2f2', 'ga', 'Transporte de gases y curva de la Hb'),
  ('vqr', '⚖️ V/Q y regulación', '#ca8a04', '#fefce8', 'vq', 'Relación V/Q y regulación'),
  ('tim', '🛡️ Tejido linfoide y timo', '#4f46e5', '#eef2ff', 'ti', 'Tejido linfoide y timo'),
  ('org', '🧫 Ganglio, bazo y MALT', '#0f766e', '#f0fdfa', 'or', 'Ganglio, bazo, amígdalas y MALT'),
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
<title>Semana 19 – Tórax, Aparato Respiratorio II y Sistema Linfático – UNT</title>
<link rel="preload" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" as="style">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
<noscript><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"></noscript>
''' + style + '\n</head>\n'

# ---------- SCRIPT ----------
script = h[h.rfind('<script>'):h.rfind('</script>') + len('</script>')]
script = script.replace('mf-s17-', 'mf-s19-')
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
  <div class="hdr-icon">🫁</div>
  <div>
    <h1>Semana 19 — Tórax, Aparato Respiratorio II y Sistema Linfático</h1>
    <p>Esqueleto, articulaciones y músculos del tórax · Diafragma y nervios frénicos · Pulmones, segmentación y árbol bronquial · Raíces pulmonares · Pleura · Mediastino (ITMIG) y ganglios (IASLC) · Respiración y anatomía funcional · Mecánica respiratoria, pleuras y surfactante · Espirometría, volúmenes y capacidades · Ventilación alveolar y espacio muerto · Transporte de gases y curva de la hemoglobina · Relación V/Q · Regulación de la respiración · Tejido linfoide, timo, ganglio, bazo, amígdalas, MALT y placas de Peyer · UNT 14/09 al 20/09</p>
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

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'w', encoding='utf8').write(html)
print('OK', OUT, len(html) // 1024, 'KB', '| figuras', n, '| dragdrops', dds)
