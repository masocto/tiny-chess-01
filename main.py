# 4KB chess engine for tiny-chess-01 (MIT)
import json,os,sys,urllib.request,urllib.error
U=os.environ.get("MAKEFUN_ENV_URL")or sys.exit()
V={"p":100,"n":320,"b":330,"r":500,"q":900,"k":20000}
T={}
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
def A(f,d,a,b):
 if d==0:return E(f)
 v=-20000
 for x in M(f):
  v=max(v,-A(x,d-1,-b,-a))
  if v>=b:return v
 return v
def M(f):
 l=[];b=B(f);s=f.split()[1]=="w"
 for q,p in b.items():
  v=p.lower();o=q[0];r=int(q[1]);d=-1 if s else 1
  if v=="p":
   if 0<r+d<=8 and not b.get(o+str(r+d)):l.append(q+o+str(r+d))
   if(r==7 and not s)or(r==2 and s):
    if not b.get(o+str(r+d))and not b.get(o+str(r+2*d)):l.append(q+o+str(r+2*d))
   for x in[-1,1]:
    t=chr(ord(o)+x)
    if"a"<=t<="h":
     u=b.get(t+str(r+d),".")
     if u!="."and u.islower()!=p.isupper():l.append(q+t+str(r+d))
   if(r==4 and not s)or(r==5 and s):
    for x in[-1,1]:
     t=chr(ord(o)+x)
     if"a"<=t<="h"and b.get(t+str(r))==("p"if s else"P"):l.append(q+t+str(r+d))
  elif v=="n":
   for dx,dy in[(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]:
    t=chr(ord(o)+dx);u=r+dy
    if"a"<=t<="h"and 1<=u<=8:
     n=t+str(u)
     if not b.get(n)or b[n].islower()!=p.isupper():l.append(q+n)
  elif v in"brq":
   for dx,dy in(([(1,1),(1,-1),(-1,1),(-1,-1)]if v in"bq"else[])+([(1,0),(-1,0),(0,1),(0,-1)]if v in"rq"else[])):
    t=ord(o)+dx;u=r+dy
    while"a"<=chr(t)<="h"and 1<=u<=8:
     n=chr(t)+str(u)
     if b.get(n):
      if b[n].islower()!=p.isupper():l.append(q+n)
      break
     l.append(q+n);t+=dx;u+=dy
  elif v=="k":
   for dx in[-1,0,1]:
    for dy in[-1,0,1]:
     if dx or dy:
      t=chr(ord(o)+dx);u=r+dy
      if"a"<=t<="h"and 1<=u<=8:
       n=t+str(u)
       if not b.get(n)or b[n].islower()!=p.isupper():l.append(q+n)
 o=[]
 for x in l:
  if len(x)==4 and x[1]in"18"and B(f).get(x[:2],"").lower()=="p":
   o.append(x+"q");o.append(x+"r");o.append(x+"b");o.append(x+"n")
  else:o.append(x)
 return o
def C(f):
 b=-20000;m=None
 for x in M(f):
  v=-A(x,2,-20000,-b)
  if v>b:b=v;m=x
 return m or M(f)[0]
def R(p,b):
 req=urllib.request.Request(U+p,json.dumps(b).encode(),{"content-type":"application/json"})
 try:return json.load(urllib.request.urlopen(req))
 except urllib.error.HTTPError as e:sys.exit(f"{p}: HTTP {e.code}")
while 1:
 g=R("/game",{})
 if g["status"]=="done":break
 while g["status"]=="your_move":g=R("/move",{"game":g["game"],"move":C(g["fen"])})
 print(f"game {g['game']}: {g['outcome']} by {g['reason']}",file=sys.stderr)
print(f"done: {g.get('wins')} won, {g.get('draws')} drawn, {g.get('losses')} lost",file=sys.stderr)