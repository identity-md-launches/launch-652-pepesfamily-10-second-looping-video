"""Deterministic original flat artwork. Emits two silent H.264 MP4s."""
import sys, math, subprocess, zipfile, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
try:
 from PIL import Image, ImageDraw, ImageFont
except ImportError:
 dependency_dir=Path(tempfile.gettempdir())/'pepes-renderlib'
 with zipfile.ZipFile(next((ROOT/'vendor').glob('pillow-*.whl'))) as wheel:wheel.extractall(dependency_dir)
 sys.path.insert(0,str(dependency_dir))
 from PIL import Image, ImageDraw, ImageFont
G='#3DDC84'; DARK='#131813'; WHITE='#E6EAE6'
S=2
fonts={}
def font(sz):
 if sz not in fonts: fonts[sz]=ImageFont.truetype(str(ROOT/'assets/IBMPlexMono-Regular.ttf'),sz*S)
 return fonts[sz]
def render(i):
 t=i/30 if i<299 else 0
 im=Image.new('RGB',(1920*S,1080*S),'#181D19'); d=ImageDraw.Draw(im)
 def box(b,fill,outline=None,w=2,r=0):
  b=tuple(round(v*S) for v in b)
  if r:d.rounded_rectangle(b,r*S,fill,outline,w*S)
  else:d.rectangle(b,fill,outline,w*S)
 def ell(b,fill,outline=None,w=2):d.ellipse(tuple(round(v*S) for v in b),fill,outline,w*S)
 def line(p,fill,w=2):d.line([(round(x*S),round(y*S)) for x,y in p],fill,w*S)
 def txt(x,y,s,size=26,col=G,center=False,spacing=2):
  f=font(size); widths=[d.textlength(c,font=f)/S+spacing for c in s]; width=sum(widths)-spacing
  if center:x-=width/2
  for c,cw in zip(s,widths):d.text((round(x*S),round(y*S)),c,font=f,fill=col); x+=cw
 # Instrument wall: no labels, original panel designs.
 for row in range(6):
  for col in range(12):
   x=18+col*158; y=18+row*148; k=row*12+col
   box((x,y,x+146,y+135),'#0D0F0D','#646C65',1,9)
   for dx in (8,138):
    for dy in (8,127):ell((x+dx-2,y+dy-2,x+dx+2,y+dy+2),'#555D56')
   typ=k%3
   phase=2*math.pi*t/10
   if typ==0:
    box((x+14,y+17,x+132,y+78),'#050605','#444D45',1,4)
    for n in range(3):line([(x+18,y+30+n*16),(x+129,y+30+n*16)],'#1C3021',1)
    pts=[(x+18+a,y+48+16*math.sin(a*.09+phase*(1+k%3)+k)) for a in range(112)]
    line(pts,G,2)
   elif typ==1:
    box((x+16,y+16,x+130,y+78),'#D3D8D1',None,1,5)
    for a in range(7):
     ang=math.pi+a*math.pi/6
     line([(x+73+44*math.cos(ang),y+72+44*math.sin(ang)),(x+73+38*math.cos(ang),y+72+38*math.sin(ang))],'#526052',2)
    ang=-math.pi/2+.6*math.sin(phase*(1+k%2)+k)
    line([(x+73,y+71),(x+73+37*math.cos(ang),y+71+37*math.sin(ang))],'#18251C',3)
   else:
    for a in range(8):
     h=16+36*(.5+.5*math.sin(phase*(1+k%2)+a*.7+k))
     box((x+17+a*14,y+78-h,x+25+a*14,y+78),G if a<6 else '#78A08A')
   for a in range(3):
    ell((x+18+a*35,y+94,x+38+a*35,y+114),'#303831','#87948A',2)
    line([(x+28+a*35,y+104),(x+28+a*35+6*math.sin(phase+k+a),y+97)],'#C0C9C0',2)
   on=math.sin(phase*(1+k%3)+k*2.13)>.15
   ell((x+122,y+99,x+131,y+108),G if on else '#22432D')
 if 3.8<=t<4:
  strength=.12*math.sin(math.pi*(t-3.8)/.2)
  im=Image.blend(im,Image.new('RGB',im.size,'#3D6349'),strength);d=ImageDraw.Draw(im)
 # Floor.
 box((0,918,1920,1080),'#101511'); line([(0,918),(1920,918)],G,3)
 # Central terminal frame.
 box((501,137,1419,751),'#080B09','#050605',5,22)
 box((513,145,1407,739),'#ADB6AD','#DCE2DC',3,15)
 box((531,163,1389,720),'#050605','#3F4B40',3,8)
 for x in (523,1397):
  for y in (154,731):ell((x-3,y-3,x+3,y+3),'#505C52')
 # Screen timeline, exact supplied case for literal terminal text and URL.
 if t<2 or t>=9.5:
  alpha=1 if t<2 else min(1,(t-9.5)/.25)
  if t>=9.5:
   fade=max(0,1-(t-9.5)/.25)
   white=tuple(int(v*fade) for v in (230,234,230))
   box((601,328,719,446),'#050605',white,4)
   txt(660,342,'P',65,white,True)
   box((719,328,1319,446),white)
   txt(1019,366,'PEPESFAMILY',43,'#050605',True,3)
   txt(960,480,'pepesfamily.fun',25,tuple(int(v*fade) for v in (146,156,147)),True,3)
  if t>=9.5 or int(t*2)%2==0:txt(583,219,'> █',32,col=tuple(int(v*alpha) for v in (61,220,132)))
 elif t<4:
  s='> launch $PEPES ......... OK'; n=min(len(s),int((t-2)/1.65*len(s))+1)
  txt(583,219,s[:n],29)
  if t>=3.8:
   box((1252,303,1347,359),G,None,2,10);txt(1300,314,'OK',28,'#050605',True)
 elif t<6.5:
  txt(583,219,'> launch $PEPES ......... OK',29)
  for j,word in enumerate(('buy   $PEPES','buy   $PEPES','sell  $PEPES')):
   a=t-(4+j*.7)
   if a>=0:
    y=350+j*83-48*min(2,max(0,(t-4)/.7))
    txt(583,y,'> '+word,30,G if j<2 else '#FF7B72')
 elif t<8.5:
  a=min(1,(t-6.5)/.3); color=tuple(int(v*a) for v in (61,220,132))
  txt(960,341,'3% OF EVERY TRADE',38,color,True,3)
  txt(960,411,'GOES TO HOLDERS',38,color,True,3)
 else:
  box((601,328,719,446),'#050605',WHITE,4)
  txt(660,342,'P',65,WHITE,True)
  box((719,328,1319,446),WHITE)
  txt(1019,366,'PEPESFAMILY',43,'#050605',True,3)
  txt(960,480,'pepesfamily.fun',25,'#929C93',True,3)
 # Seven original rear-view frogs, with varied heights and rhythms.
 frogs=[(653,973,.79),(848,978,.86),(1052,974,.81),(1249,980,.84),(741,1060,1.0),(968,1070,1.08),(1193,1062,.98)]
 for k,(cx,base,scale) in enumerate(frogs):
  phase=2*math.pi*t/10
  sway=4*math.sin(phase*(1+k%3)+k*.9); bob=3*math.sin(phase*(2+k%2)+k)
  bounce=0
  for wave in range(3):
   age=t-(4.68+wave*.7+(k//3)*.07)
   if 0<age<.42:bounce=18*math.sin(math.pi*age/.42)
  x=cx+sway;y=base+bob-bounce
  ell((cx-67*scale,base-12,cx+67*scale,base+9),'#070B08')
  def fb(a,b,c,e,color,outline='#162F19',w=4,r=0):box((x+a*scale,y+b*scale,x+c*scale,y+e*scale),color,outline,w,r)
  def fe(a,b,c,e,color,outline='#21451A',w=4):ell((x+a*scale,y+b*scale,x+c*scale,y+e*scale),color,outline,w)
  fe(-53,-21,-8,1,'#64A84D');fe(10,-21,55,1,'#64A84D')
  fb(-49,-64,49,-17,'#B08D5C','#463E2B',4,8);line([(x,y-52*scale),(x,y-20*scale)],'#635037',3)
  raised=k>=4 and 6.8<t<8.0
  lift=math.sin(math.pi*min(1,(t-6.8)/.15)/2) if raised else 0
  if raised and t>7.8:lift=max(0,(8-t)/.2)
  line([(x-42*scale,y-111*scale),(x-(73+15*lift)*scale,y+(-86-154*lift)*scale)],'#21451A',22)
  line([(x-42*scale,y-111*scale),(x-(73+15*lift)*scale,y+(-86-154*lift)*scale)],'#64A84D',14)
  line([(x+42*scale,y-112*scale),(x+67*scale,y-78*scale)],'#21451A',22)
  line([(x+42*scale,y-112*scale),(x+67*scale,y-78*scale)],'#64A84D',14)
  fb(-55,-142,55,-57,'#2C60CC','#152C58',4,18)
  # Eye bumps merge into the head; no eyes or facial features.
  fe(-62,-209,-3,-150,'#64A84D');fe(5,-212,65,-152,'#64A84D')
  fe(-80,-193,81,-119,'#64A84D')
  # Flat rear head contour and collar detail.
  line([(x-31*scale,y-126*scale),(x,y-122*scale),(x+32*scale,y-127*scale)],'#21451A',3)
 # Coins appear in three waves and land individually on the frogs.
 for j in range(3):
  for k,(cx,base,scale) in enumerate(frogs):
   start=4+j*.7+(k//3)*.07; a=(t-start)/.68
   if 0<=a<=1:
    sx=790+k*54; ex=cx
    x=sx+(ex-sx)*a+18*math.sin(a*math.pi)
    y=687+(base-200*scale-687)*a-170*math.sin(math.pi*a)
    ell((x-22,y-22,x+22,y+22),G,'#21451A',3)
    txt(x,y-13,'3%',17,'#153C23',True,0)
 return im.resize((1920,1080),Image.Resampling.LANCZOS)

def encoder(path,square=False):
 args=['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1080' if square else '1920x1080','-r','30','-i','pipe:0','-f','lavfi','-i','anullsrc=r=48000:cl=stereo','-t','10','-c:v','libx264','-preset','medium','-qp','18','-profile:v','high','-x264-params','ipratio=1:pbratio=1','-force_key_frames','0,9.96','-pix_fmt','yuv420p','-c:a','aac','-b:a','64k','-movflags','+faststart',path]
 return subprocess.Popen(args,stdin=subprocess.PIPE)
if __name__=='__main__':
 Path('artifacts').mkdir(exist_ok=True)
 p=encoder('artifacts/video.mp4');q=encoder('artifacts/video-square.mp4',True)
 for i in range(300):
  im=render(i);p.stdin.write(im.tobytes());q.stdin.write(im.crop((420,0,1500,1080)).tobytes())
  if i%30==0:print(f'{i}/300',flush=True)
 p.stdin.close();q.stdin.close()
 assert p.wait()==q.wait()==0
