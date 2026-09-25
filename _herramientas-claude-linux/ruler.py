# ruler.py out.png frac img...  -> franja inferior de cada imagen con reglas cada 10 px (y absoluto)
import sys
from PIL import Image, ImageDraw, ImageFont
out,fr=sys.argv[1],float(sys.argv[2]); fs=sys.argv[3:]
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',12)
tiles=[]
for f in fs:
    im=Image.open(f).convert('RGB'); W,H=im.size; y0=int(H*(1-fr))
    t=Image.new('RGB',(W+50,H-y0+18),'white'); t.paste(im.crop((0,y0,W,H)),(50,18)); d=ImageDraw.Draw(t)
    d.text((2,2),f,fill='red',font=font)
    for y in range((y0//10+1)*10,H,10):
        c=(255,0,0) if y%50==0 else (0,160,255); d.line([(40,y-y0+18),(W+50,y-y0+18)] if y%50==0 else [(40,y-y0+18),(50,y-y0+18)],fill=c)
        if y%50==0 or y%10==0 and False: d.text((0,y-y0+12),str(y),fill='black',font=font)
    tiles.append(t)
Wt=max(t.width for t in tiles); Ht=sum(t.height for t in tiles)
S=Image.new('RGB',(Wt,Ht),'white'); y=0
for t in tiles: S.paste(t,(0,y)); y+=t.height
S.save(out); print(S.size)
