# fix19.py — correcciones de encuadre/resolución detectadas en la auditoría visual (salida a fix/out para revisar)
import pymupdf, sys
from PIL import Image
S='/home/user/work/src/'; O='/home/user/work/fix/out/'
def xref(pdf, x):
    d=pymupdf.open(S+pdf); pix=pymupdf.Pixmap(d,x)
    if pix.colorspace is None or pix.colorspace.n!=3 or pix.n-pix.alpha>=4: pix=pymupdf.Pixmap(pymupdf.csRGB,pix)
    if pix.alpha: pix=pymupdf.Pixmap(pix,0)
    return Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
def clip(pdf, pg, r, sc):
    d=pymupdf.open(S+pdf); pix=d[pg-1].get_pixmap(matrix=pymupdf.Matrix(sc,sc),clip=pymupdf.Rect(*r))
    return Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
def frac(im, x0=0, y0=0, x1=1, y1=1):
    w,h=im.size; return im.crop((round(x0*w),round(y0*h),round(x1*w),round(y1*h)))
import os
def cur(name, im):
    # la imagen actual es un recorte superior (quizá reducido) del original: reproducirlo en resolución nativa
    f=[f for f in (name+'.jpg',name+'.png') if os.path.exists('/home/user/work/img/'+f)][0]
    cw,ch=Image.open('/home/user/work/img/'+f).size
    return im.crop((0,0,im.width,min(im.height,round(ch*im.width/cw))))
from PIL import ImageDraw
def px(im, x0=0, y0=0, x1=None, y1=None):
    return im.crop((x0,y0,x1 or im.width,y1 or im.height))
def white(im, *boxes):
    # rellena con el color de fondo (mediana de la fila justo encima de cada caja), no con blanco puro
    d=ImageDraw.Draw(im); P=im.load()
    for b in boxes:
        row=sorted(P[x,max(0,b[1]-3)] for x in range(b[0],min(b[2],im.width)))
        d.rectangle(b, fill=row[len(row)//2])
    return im
def trim_black(im, thr=20):
    g=im.convert('L').point(lambda v:255 if v>thr else 0); return im.crop(g.getbbox())
def stack(parts, gap=24, pad=16):
    W=max(p.width for p in parts)+2*pad; H=sum(p.height for p in parts)+gap*(len(parts)-1)+2*pad
    S_=Image.new('RGB',(W,H),'white'); y=pad
    for p in parts: S_.paste(p,((W-p.width)//2,y)); y+=p.height+gap
    return S_
def save(name, im, maxw=1100):
    if im.width>maxw: im=im.resize((maxw,round(im.height*maxw/im.width)),Image.LANCZOS)
    if os.path.exists('/home/user/work/img/'+name+'.png'): im.save(O+name+'.png',optimize=True)   # dibujo lineal: sin JPEG
    else: im.save(O+name+'.jpg',quality=90,optimize=True)
    print(f'{name:28s} {im.size}')

F={}
F['tor-elevadores-transverso']=lambda: px(white(xref('caja_toracica.pdf',45),(0,575,600,632)),y1=668)
F['mec-presiones-vol']=lambda: px(xref('fisio_resp_p1.pdf',77),y1=511)
F['mec-presiones']=lambda: px(white(xref('fisio_resp_p1.pdf',73),(0,366,412,520)),y1=512)
F['mec-surfactante']=lambda: px(white(xref('fisio_resp_p2.pdf',33),(695,462,1013,520)),y1=518)
F['gas-membrana']=lambda: xref('fisio_resp_p2.pdf',59)
F['gas-factores']=lambda: px(xref('fisio_resp_p2.pdf',72),y1=505)
F['gas-2-3dpg']=lambda: px(xref('fisio_resp_p2.pdf',91),y1=395)
F['vqr-vq-local']=lambda: px(xref('fisio_resp_p2.pdf',48),y1=516)
F['vqr-actividad']=lambda: px(xref('fisio_resp_p2.pdf',113),y1=500)
F['vqr-reflejo']=lambda: frac(cur('vqr-reflejo',xref('fisio_resp_p2.pdf',109)),x0=0.035,y1=0.975)
F['vqr-centros']=lambda: stack([clip('fisio_resp_p2.pdf',25,(145,95,352,354.5),2.6), clip('fisio_resp_p2.pdf',25,(358,336,457,381),2.6)],gap=10,pad=6)
F['esp-espirometro']=lambda: frac(cur('esp-espirometro',xref('espirometria.pdf',44)),x1=0.9)
F['esp-patrones']=lambda: clip('espirometria.pdf',8,(70,470,520,695),3)
F['esp-ventilacion-terminos']=lambda: px(xref('fisio_resp_p2.pdf',129),y1=474)
F['org-bazo-pulpas']=lambda: trim_black(xref('organos_linfoides.pdf',252))
F['org-bazo-pulpa-blanca']=lambda: xref('organos_linfoides.pdf',259)
F['org-malt']=lambda: trim_black(xref('organos_linfoides.pdf',285))
F['org-comparacion']=lambda: xref('organos_linfoides.pdf',293)
F['org-tld-mucosa']=lambda: xref('organos_linfoides.pdf',53)
def abierta():
    sc=2.4
    return stack([clip('organos_linfoides.pdf',33,(148,40,551,308),sc), clip('organos_linfoides.pdf',33,(575,63,952,126),sc),
                  clip('organos_linfoides.pdf',33,(472,318,915,540),sc), clip('organos_linfoides.pdf',33,(35,338,435,415),sc)])
F['org-bazo-abierta-cerrada']=abierta
A=dict(a.split('=') for a in sys.argv[1:] if '=' in a)
names=[a for a in sys.argv[1:] if '=' not in a] or list(F)
for n in names: save(n,F[n]())
