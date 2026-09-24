# render.py <pdf> <prefix> <scale> [pages e.g. 1,3,5-9]  -> /home/user/work/r/<prefix>-pNN.png
import pymupdf,sys
pdf,prefix,scale=sys.argv[1],sys.argv[2],float(sys.argv[3])
d=pymupdf.open(pdf)
pages=range(1,d.page_count+1)
if len(sys.argv)>4:
    pages=[]
    for part in sys.argv[4].split(','):
        if '-' in part: a,b=map(int,part.split('-')); pages+=range(a,b+1)
        else: pages.append(int(part))
for n in pages:
    pix=d[n-1].get_pixmap(matrix=pymupdf.Matrix(scale,scale))
    out=f"/home/user/work/r/{prefix}-p{n:02d}.png"; pix.save(out); print(out,pix.width,pix.height)
