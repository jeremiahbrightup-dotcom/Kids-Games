import json,re,subprocess,sys
def gaps(f,noise=-38,d=0.06):
    out=subprocess.run(['ffmpeg','-hide_banner','-i',f,'-af',f'silencedetect=noise={noise}dB:d={d}','-f','null','-'],capture_output=True,text=True).stderr
    st=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',out)]
    en=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',out)]
    dur=float(re.search(r'Duration: (\d+):(\d+):([\d.]+)',out).group(3))+60*int(re.search(r'Duration: (\d+):(\d+)',out).group(2))
    return list(zip(st,en)),dur
def split(f,n,noise=-38):
    g,dur=gaps(f,noise)
    # drop leading/trailing silence
    lead=g[0][1] if g and g[0][0]<0.05 else 0
    trail=g[-1][0] if g and g[-1][1]>dur-0.05 else dur
    inner=[x for x in g if x[0]>lead+0.01 and x[1]<trail-0.01]
    if len(inner)<n-1: return None,len(inner)
    top=sorted(sorted(inner,key=lambda x:x[1]-x[0],reverse=True)[:n-1])
    segs=[];s=lead
    for a,b in top: segs.append((s,a)); s=b
    segs.append((s,trail))
    return segs,len(inner)
if __name__=='__main__':
    f,n=sys.argv[1],int(sys.argv[2])
    segs,ng=split(f,n)
    print(ng, None if not segs else [round(b-a,2) for a,b in segs])
