import subprocess,json,hashlib,struct
from pathlib import Path
results=[]
for name,w,h in [('video.mp4',1920,1080),('video-square.mp4',1080,1080)]:
 p=Path('artifacts')/name
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
 v,a=probe['streams'];assert (v['codec_name'],v['profile'],v['pix_fmt'],v['width'],v['height'],v['r_frame_rate'],v['nb_frames'])==('h264','High','yuv420p',w,h,'30/1','300')
 assert a['codec_name']=='aac' and float(probe['format']['duration'])==10 and float(a['duration'])==10
 assert p.stat().st_size<15000000
 md5=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-an','-vf',r'select=eq(n\,0)+eq(n\,299)','-fps_mode','passthrough','-f','framemd5','-'],text=True)
 hashes=[x.rsplit(',',1)[-1].strip() for x in md5.splitlines() if not x.startswith('#')]
 assert len(hashes)==2 and hashes[0]==hashes[1]
 audio=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-f','s16le','-'])
 assert not any(audio)
 data=p.read_bytes();atoms=[];offset=0
 while offset<len(data):
  size,typ=struct.unpack('>I4s',data[offset:offset+8]);atoms.append(typ.decode());assert size>=8;offset+=size
 assert atoms.index('moov')<atoms.index('mdat')
 results.append(dict(path=str(p),duration_seconds=10,width=w,height=h,fps=30,frames=300,video_codec='H.264 High / yuv420p',audio='AAC-LC stereo 48 kHz, decoded samples all zero',bytes=len(data),first_last_decoded_frame_md5=hashes[0],faststart=True,sha256=hashlib.sha256(data).hexdigest()))
Path('validation.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
