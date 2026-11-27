import json,math,re,sys
from split import gaps
def syl(t):
    t=t.lower();w=re.findall(r"[a-z]+",t)
    n=sum(max(1,len(re.findall(r'[aeiouy]+',x))-(1 if x.endswith('e') and len(x)>3 else 0)) for x in w)
    if re.fullmatch(r"[a-z]\.?",t.strip()):n=1
    return n+0.6
def align(f,texts,noise=-38,expl=None):
    g,dur=gaps(f,noise,0.05)
    lead=g[0][1] if g and g[0][0]<0.05 else 0.0
    trail=g[-1][0] if g and g[-1][1]>dur-0.05 else dur
    cand=[(a,b) for a,b in g if a>lead+0.01 and b<trail-0.01]
    N=len(texts);G=len(cand)
    e=[syl(t) for t in texts];tot=sum(e)
    speech=(trail-lead)-sum(b-a for a,b in cand)*0.5
    k=speech/tot
    if expl: e=list(expl);k=speech/sum(e)  # expected lengths from a correctly-cut reference voice
    # points: index -1 = start(lead), cand i -> cut at gap i, end
    pts=[(lead,lead)]+cand+[(trail,trail)]
    INF=1e18
    # dp[j][i]: best cost placing first j items ending at point i (point i = gap after item j)
    dp=[[INF]*(G+2) for _ in range(N+1)];bk=[[-1]*(G+2) for _ in range(N+1)]
    dp[0][0]=0
    for j in range(1,N+1):
        for i in range(1,G+2):
            if j<N and i==G+1:continue
            if j==N and i!=G+1:continue
            for p in range(0,i):
                if dp[j-1][p]>=INF:continue
                s=pts[p][1];en=pts[i][0];L=en-s
                exp=k*e[j-1]
                c=((L-exp)/(0.35+0.25*exp))**2
                if i<=G: c-=3*min(pts[i][1]-pts[i][0],0.8)  # reward cutting at long gaps
                if dp[j-1][p]+c<dp[j][i]:dp[j][i]=dp[j-1][p]+c;bk[j][i]=p
    segs=[];i=G+1
    for j in range(N,0,-1):
        p=bk[j][i];segs.append((pts[p][1],pts[i][0]));i=p
    return segs[::-1],k
if __name__=='__main__':
    one=json.load(open('one.json'))
    f,part=sys.argv[1],sys.argv[2]
    txt=one[part].replace('[excited] ','').split(' ... ')
    segs,k=align(f,txt)
    for t,(a,b) in zip(txt,segs):print(f'{b-a:5.2f} {syl(t)*k:5.2f}  {t}')
