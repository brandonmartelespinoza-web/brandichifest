# sheet.py <out.png> <cols> <cellW> img1 img2 ...  -> contact sheet with filename labels
import sys,os
from PIL import Image,ImageDraw,ImageFont
out,cols,cw=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]); files=sys.argv[4:]
ims=[]
for f in files:
    im=Image.open(f).convert('RGB'); r=cw/im.width; ims.append((os.path.basename(f),im.resize((cw,max(1,int(im.height*r))))))
rows=[ims[i:i+cols] for i in range(0,len(ims),cols)]
H=sum(max(im.height for _,im in row)+22 for row in rows)
S=Image.new('RGB',(cols*(cw+8),H),'white'); dr=ImageDraw.Draw(S)
try: font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',15)
except: font=None
y=0
for row in rows:
    x=0;rh=max(im.height for _,im in row)
    for name,im in row:
        dr.text((x+2,y+2),name,fill='red',font=font); S.paste(im,(x,y+20)); dr.rectangle([x,y+20,x+im.width-1,y+20+im.height-1],outline='gray'); x+=cw+8
    y+=rh+22
S.save(out); print(out,S.size)
