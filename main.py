# 4KB chess engine for tiny-chess-01 (MIT)
import json,os,sys,urllib.request,urllib.error
U=os.environ.get("MAKEFUN_ENV_URL")or sys.exit()
V={"p":100,"n":320,"b":330,"r":500,"q":900,"k":20000}
def B(f):
 r={}
 for i,o in enumerate(f.split()[0].split("/")):
  c=0
  for x in o:
   if x.isdigit():c+=int(x)
   else:r["abcdefgh"[c]+str(8-i)]=x;c+=1
 return r
def E(f):
 b=B(f);s=0
 for p in b.values():s+=V[p.lower()]*(1 if p.isupper()else-1)
 return s
def S(f,m):
 b=B(f);t=m[2:4];v=0
 if t in b and b[t].islower()!=b[m[:2]].isupper():
  v=V[b[t].lower()]*(-1 if b[m[:2]].isupper()else 1)
 return E(f)+v
def A(f,d,a,b,l):
 if d==0:return E(f)
 v=-20000
 for x in l:
  v=max(v,-A(x,d-1,-b,-a,[]))
  if v>=b:return v
 return v
def C(g):
 l=g["legal_moves"];m=l[0];b=-20000
 for x in l:
  v=-A(x,2,-20000,-b,[])
  if v>b:b=v;m=x
 return m
def R(p,b):
 req=urllib.request.Request(U+p,json.dumps(b).encode(),{"content-type":"application/json"})
 try:return json.load(urllib.request.urlopen(req))
 except urllib.error.HTTPError as e:sys.exit(f"{p}: HTTP {e.code}")
while 1:
 g=R("/game",{})
 if g["status"]=="done":break
 while g["status"]=="your_move":g=R("/move",{"game":g["game"],"move":C(g)})
 print(f"game {g['game']}: {g['outcome']} by {g['reason']}",file=sys.stderr)
print(f"done: {g.get('wins')} won, {g.get('draws')} drawn, {g.get('losses')} lost",file=sys.stderr)