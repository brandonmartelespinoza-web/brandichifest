# ex20.py spec.txt [nombres...] — extrae figuras a /home/user/w20/raw (revisar antes de copiar a img/)
#  name | pdf | x | xref                      -> imagen nativa
#  name | pdf | c | page x0 y0 x1 y1 scale   -> render de región (texto vectorial nítido)
import pymupdf, sys, os
from PIL import Image
S='/home/user/w20/src/'; O='/home/user/w20/raw/'; MAXW=1100
only=set(sys.argv[2:])
for line in open(sys.argv[1]):
    line=line.strip()
    if not line or line.startswith('#'): continue
    parts=[x.strip() for x in line.split('|')]
    name,pdf,mode,args=parts[:4]; post=parts[4] if len(parts)>4 else ''
    if only and name not in only: continue
    d=pymupdf.open(S+pdf); a=args.split()
    if mode=='x':
        pix=pymupdf.Pixmap(d,int(a[0]))
        if pix.colorspace is None or pix.colorspace.n!=3 or pix.n-pix.alpha>=4: pix=pymupdf.Pixmap(pymupdf.csRGB,pix)
        if pix.alpha: pix=pymupdf.Pixmap(pix,0)
    else:
        p=d[int(a[0])-1]; x0,y0,x1,y1=map(float,a[1:5]); sc=float(a[5])
        pix=p.get_pixmap(matrix=pymupdf.Matrix(sc,sc),clip=pymupdf.Rect(x0,y0,x1,y1))
    im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
    if im.width>MAXW: im=im.resize((MAXW,round(im.height*MAXW/im.width)),Image.LANCZOS)
    if post.startswith('w '):   # tapar fragmentos ajenos (px, tras reescalar) con el color de fondo vecino
        from PIL import ImageDraw
        v=list(map(int,post[2:].split())); dr=ImageDraw.Draw(im); P=im.load()
        for k in range(0,len(v),4):
            b=v[k:k+4]; row=sorted(P[x,max(0,b[1]-2)] for x in range(b[0],min(b[2],im.width))) or [(255,255,255)]
            dr.rectangle(b,fill=row[len(row)//2])
    im.save(O+name+'.jpg',quality=90,optimize=True)
    print(f'{name:26s} {im.size}')
