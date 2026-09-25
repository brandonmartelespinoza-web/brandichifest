# untab.py — borra las "pestañas" marrones de la plantilla de diapositiva (xref 11 del teórico,
# en x 0-60 y 741-801, y 205-245 pt) que quedaron dentro de los recortes renderizados de digestivo1.pdf
import sys, os
from PIL import Image, ImageDraw
IMG='/home/user/brandichifest/SEM 20/img/'
TABS=[(0,203,61,247),(740,203,802,247)]
OFF={'eso-micro1':(9,7),'eso-micro2':(6,10)}   # recortes manuales posteriores
spec={}
for f in ('spec1.txt','spec2.txt'):
    for l in open('/home/user/w20/'+f):
        l=l.strip()
        if not l or l.startswith('#'): continue
        p=[x.strip() for x in l.split('|')]; spec[p[0]]=p
for name,p in spec.items():
    if p[1]!='digestivo1.pdf' or p[2]!='c' or not os.path.exists(IMG+name+'.jpg'): continue
    a=p[3].split(); x0,y0,x1,y1=map(float,a[1:5]); sc=float(a[5])
    im=Image.open(IMG+name+'.jpg').convert('RGB'); W,H=im.size
    rawW=(x1-x0)*sc; f=min(1.0,1100/rawW)
    dx,dy=OFF.get(name,(0,0)); d=ImageDraw.Draw(im); P=im.load(); hit=False
    for tx0,ty0,tx1,ty1 in TABS:
        if tx1<=x0 or tx0>=x1 or ty1<=y0 or ty0>=y1: continue
        bx0=round((max(tx0,x0)-x0)*sc*f)-dx; bx1=round((min(tx1,x1)-x0)*sc*f)-dx
        by0=round((max(ty0,y0)-y0)*sc*f)-dy; by1=round((min(ty1,y1)-y0)*sc*f)-dy
        bx0=max(0,bx0); by0=max(0,by0); bx1=min(W-1,bx1); by1=min(H-1,by1)
        if bx1<=bx0 or by1<=by0: continue
        # color de relleno: columna vecina hacia el interior de la imagen, fila por fila
        sx = bx1+2 if tx0<5 else bx0-2
        sx=min(max(sx,0),W-1)
        for y in range(by0,by1+1):
            c=P[sx,y]
            for x in range(bx0,bx1+1): P[x,y]=c
        hit=True
    if hit:
        im.save(IMG+name+'.jpg',quality=92); print('limpio',name)
