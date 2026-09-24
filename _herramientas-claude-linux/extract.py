# extract.py spec.txt  — lines: name | pdf | mode | args
#  mode x: args = xref            -> native embedded image
#  mode c: args = page x0 y0 x1 y1 scale  -> clip render (pdf points)
import pymupdf,sys,os
from PIL import Image
S='/home/user/work/src/'; O='/home/user/work/img/'
MAXW=1100
for line in open(sys.argv[1]):
    line=line.strip()
    if not line or line.startswith('#'): continue
    name,pdf,mode,args=[x.strip() for x in line.split('|')]
    d=pymupdf.open(S+pdf); a=args.split()
    out=O+name+'.png'
    if mode=='x':
        pix=pymupdf.Pixmap(d,int(a[0]))
        if pix.n-pix.alpha>=4 or pix.colorspace is None or pix.colorspace.n!=3:
            pix=pymupdf.Pixmap(pymupdf.csRGB,pix)
        if pix.alpha: pix=pymupdf.Pixmap(pix,0)
        pix.save(out)
    else:
        p=d[int(a[0])-1]; x0,y0,x1,y1=map(float,a[1:5]); sc=float(a[5])
        pix=p.get_pixmap(matrix=pymupdf.Matrix(sc,sc),clip=pymupdf.Rect(x0,y0,x1,y1)); pix.save(out)
    im=Image.open(out).convert('RGB')
    if im.width>MAXW: im=im.resize((MAXW,int(im.height*MAXW/im.width)),Image.LANCZOS)
    im.save(out,optimize=True)
    print(f"{name:28s} {im.size} {os.path.getsize(out)//1024}KB")
