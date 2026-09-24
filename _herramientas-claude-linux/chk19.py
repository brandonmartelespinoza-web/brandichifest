# chk19.py <frag.html> [...]  — controles de un fragmento (o de la guía ensamblada)
import re, sys, os
from html.parser import HTMLParser

IMG = '/home/user/brandichifest/SEM 19/img/'
VOID = {'br','img','input','hr','meta','link','source','wbr','area','col','path','circle','rect','line','ellipse','polygon','polyline','stop','use'}

class P(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True); s.stack=[]; s.err=[]; s.sec_depth=0; s.nested=0
    def handle_starttag(s,tag,a):
        if tag in VOID: return
        cls=dict(a).get('class','') or ''
        is_sec = tag=='div' and 'section' in cls.split()
        if is_sec:
            if any(x[1] for x in s.stack): s.nested+=1
        s.stack.append((tag,is_sec,s.getpos()))
    def handle_startendtag(s,tag,a): pass
    def handle_endtag(s,tag):
        if tag in VOID: return
        if not s.stack: s.err.append(f'cierre sobrante </{tag}> en {s.getpos()}'); return
        if s.stack[-1][0]==tag: s.stack.pop(); return
        # buscar hacia abajo
        for i in range(len(s.stack)-1,-1,-1):
            if s.stack[i][0]==tag:
                s.err.append(f'</{tag}> en {s.getpos()} cierra con abiertos {[x[0]+str(x[2]) for x in s.stack[i+1:]]}')
                del s.stack[i:]; return
        s.err.append(f'cierre huérfano </{tag}> en {s.getpos()}')

def check(path, allimgs):
    h=open(path,encoding='utf8').read()
    p=P(); p.feed(h); p.close()
    probs=list(p.err)
    if p.stack: probs.append('quedan abiertos: '+str([x[0]+str(x[2]) for x in p.stack][:6]))
    if p.nested: probs.append(f'{p.nested} .section anidadas')
    figs=re.findall(r'<figure class="fig"[\s\S]*?</figure>',h)
    for f in figs:
        if 'class="lee"' not in f: probs.append('figura sin .lee: '+re.sub(r'\s+',' ',f[:120]))
        if 'fig-tag' not in f: probs.append('figura sin fig-tag')
    imgs=re.findall(r'<img [^>]*src="img/([^"]+)"',h)
    for i in imgs:
        if not os.path.exists(IMG+i): probs.append('imagen faltante: '+i)
        allimgs.setdefault(i,[]).append(os.path.basename(path))
    for alt in re.findall(r'alt="([^"]*)"',h):
        if len(alt.split())>60: probs.append(f'alt largo ({len(alt.split())} palabras): {alt[:60]}')
        if len(alt.split())<5: probs.append('alt muy corto: '+alt)
    # tablas fuera de tbl-wrap
    for m in re.finditer(r'<table',h):
        before=h[max(0,m.start()-60):m.start()]
        if 'tbl-wrap' not in before: probs.append('tabla fuera de .tbl-wrap cerca de '+str(h[:m.start()].count('\n')+1))
    # preguntas
    for kind,fb in (('mt-q','mt-feedback'),('quiz-q','feedback')):
        for m in re.finditer(r'<div class="'+kind+r'" data-correct="([abcd])">([\s\S]*?)<div class="'+fb+r'">([\s\S]*?)</div>\s*</div>',h):
            ans,body,feed=m.groups()
            nl=body.count('<label>')
            if nl!=4: probs.append(f'{kind} con {nl} opciones: '+re.sub(r'<[^>]+>','',body)[:70])
            mm=re.search(r'Correcta:\s*([A-D])',feed)
            if not mm or mm.group(1).lower()!=ans: probs.append(f'{kind} data-correct={ans} vs feedback {mm.group(1) if mm else "?"}: '+re.sub(r'<[^>]+>','',body)[:70])
        # nombres de radio únicos por pregunta
    names=re.findall(r'<input type="radio" name="([^"]+)"',h)
    from collections import Counter
    for k,v in Counter(names).items():
        if v!=4: probs.append(f'radio name {k} aparece {v} veces')
    # dragdrops
    for m in re.finditer(r'<ul class="drag-list" id="(dd-\w+)-list">([\s\S]*?)</ul>',h):
        pos=sorted(int(x) for x in re.findall(r'data-pos="(\d+)"',m.group(2)))
        if pos!=list(range(1,len(pos)+1)): probs.append(f'{m.group(1)} data-pos {pos}')
        if f'checkDrag(\'{m.group(1)}\')' not in h: probs.append(f'{m.group(1)} sin botón checkDrag')
        if f'id="{m.group(1)}-result"' not in h: probs.append(f'{m.group(1)} sin -result')
    # svg: etiquetas html dentro de <text>
    for m in re.finditer(r'<text[^>]*>([\s\S]*?)</text>',h):
        if re.search(r'<(b|i|em|strong|br|span|sub|sup)[\s>/]',m.group(1)): probs.append('HTML dentro de <text> SVG: '+m.group(1)[:50])
    stats=dict(figs=len(figs),lee=h.count('class="lee"'),imgs=len(imgs),svgs=h.count('<svg'),
               mt=h.count('class="mini-test"'),mtq=h.count('class="mt-q"'),sema=h.count('class="semaforo'),
               fc=h.count('class="fc"'),dd=h.count('class="dragdrop"'),quiz=h.count('class="quiz-q"'),
               kb=len(h.encode())//1024, trap=h.count('class="trap"'),clin=h.count('class="clinical"'),
               honest=h.count('Nota de honestidad'))
    return probs,stats

allimgs={}
for f in sys.argv[1:]:
    probs,st=check(f,allimgs)
    print(f'== {os.path.basename(f)} {st}')
    for x in probs: print('   ✗',x)
dup={k:v for k,v in allimgs.items() if len(v)>1}
if dup: print('IMÁGENES DUPLICADAS:',dup)
if len(sys.argv)>2 or 'GUIA' in sys.argv[1]:
    unused=sorted(set(os.listdir(IMG))-set(allimgs))
    print('sin usar:',unused)
