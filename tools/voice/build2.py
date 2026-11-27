import json,subprocess,os,sys
from align import align
one=json.load(open('one.json'));wc=json.load(open('wchunks.json'))
def build(voice,pitch=1.0,wparts=(0,1,2)):
    os.makedirs('out',exist_ok=True)
    jobs=[]
    for part in ['A','B']:
        jobs.append((f'raw/{voice}-{part}.mp3',one[part].replace('[excited] ','').split(' ... '),one['keys'+part]))
    for i in wparts:
        f=f'raw/{voice}-W{i}.mp3'
        if os.path.exists(f): jobs.append((f,wc['W%d'%i],wc['W%d'%i]))
    clips={};t=0.0;listf=[];n=0
    for src,txt,keys in jobs:
        segs,_=align(src,txt)
        for key,(a,b) in zip(keys,segs):
            if key in clips: continue
            a=max(0,a-0.03);b=b+0.05;fn=f'out/{voice}_{n:04d}.wav';n+=1
            af=f'atrim={a:.3f}:{b:.3f},asetpts=N/SR/TB'
            if pitch!=1.0: af+=f',rubberband=pitch={pitch}:formant=shifted'
            af+=',afade=t=in:d=0.01,areverse,afade=t=in:d=0.02,areverse,apad=pad_dur=0.04'
            subprocess.run(['ffmpeg','-y','-loglevel','error','-i',src,'-af',af,'-ac','1','-ar','24000',fn],check=True)
            d=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',fn],capture_output=True,text=True).stdout)
            clips[key]=[round(t,3),round(t+d-0.04,3)];t+=d;listf.append(fn)
    open('out/list.txt','w').write(''.join(f"file '{os.path.abspath(f)}'\n" for f in listf))
    subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i','out/list.txt','-ac','1','-ar','24000','-b:a','40k',f'out/voice-{voice}.mp3'],check=True)
    json.dump({'file':f'voice-{voice}.mp3','clips':clips},open(f'out/voice-{voice}.json','w'))
    for f in listf: os.remove(f)
    print(voice,len(clips),'clips',round(t,1),'s',os.path.getsize(f'out/voice-{voice}.mp3')//1024,'KB')
if __name__=='__main__':
    for v in sys.argv[1:]:
        build(v,1.12 if v=='jett' else 1.0)
