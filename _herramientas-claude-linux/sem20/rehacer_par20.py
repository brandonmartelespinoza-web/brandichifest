# rehacer_par20.py — reemplaza en la guía YA ENSAMBLADA (con imágenes incrustadas) la pestaña "Pared abdominal",
# el aviso inicial y el test final por los fragmentos de frag-sem20/, y renumera las figuras.
# Sirve cuando no está el chasis de SEM 17 que usa armar20.py (sesión nueva en la nube).
import re, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRAG = os.path.join(BASE, 'frag-sem20')
GUIA = os.path.join(os.path.dirname(BASE), 'SEM 20', 'GUIA-SEM20.html')

h = open(GUIA, encoding='utf8').read()
rd = lambda n: open(os.path.join(FRAG, n), encoding='utf8').read().strip()

# 1) pestaña par: todo lo que sigue al progress-tracker hasta el cierre de la pestaña
i = h.index('<div id="tab-par"')
k = h.index('<div class="pt-dots" id="pt-par-dots"></div>\n</div>\n', i) + len('<div class="pt-dots" id="pt-par-dots"></div>\n</div>\n')
j = h.index('\n</div>\n\n<div id="tab-per"', k)
h = h[:k] + rd('par.html') + h[j:]

# 2) aviso inicial
a = h.index('<div id="aviso-notas"')
b = h.index('</div>', a) + len('</div>')
h = h[:a] + rd('aviso.html') + h[b:]

# 3) test final
t = h.index('<div id="tab-test" class="tab-content">\n') + len('<div id="tab-test" class="tab-content">\n')
u = h.index('\n</div>\n\n<script>', t)
h = h[:t] + rd('test.html') + h[u:]

# 4) renumerar figuras e initDrag (igual que armar20.py)
n = 0
def ren(m):
    global n
    n += 1
    return f'<span class="fig-tag">Figura {n}</span>'
h = re.sub(r'<span class="fig-tag">Figura [^<]*</span>', ren, h)
dds = re.findall(r'<div class="dragdrop" id="(dd-[a-z0-9]+)"', h)
h = re.sub(r"\[('dd-[a-z0-9]+',?)*\]\.forEach\(initDrag\)",
           '[' + ','.join(f"'{d}'" for d in dds) + '].forEach(initDrag)', h)

open(GUIA, 'w', encoding='utf8').write(h)
print('OK', GUIA, len(h) // 1024, 'KB | figuras', n, '| dragdrops', len(dds))
