# 4KB chess engine for tiny-chess-01 (MIT)
import json,os,sys,urllib.request,urllib.error
U=os.environ.get("MAKEFUN_ENV_URL")or sys.exit()
N=50000
P={"p":100,"n":320,"b":330,"r":500,"q":900,"k":20000}
D={}
def p(f):
 r={}
 for i,o in enumerate(f.split()[0].split("/")):
  c=0
  for x in o:
   if x.isdigit():c+=int(x)
   else:r["abcdefgh"[c]+str(8-i)]=x;c+=1
 return r
def m(f):
 b=p(f);l=[]
 for s,q in b.items():
  v=q.lower();o=s[0];r=int(s[1]);d=-1 if q.isupper()else 1
  if v=="p":
   if 0<r+d<=8 and not b.get(o+str(r+d)):l.append(s+o+str(r+d))
   if v=="p"and((q.isupper()and r==7)or(q.islower()and r==2))and not b.get(o+str(r+d))and not b.get(o+str(r+2*d)):l.append(s+o+str(r+2*d))
   for x in[-1,1]:
    t=chr(ord(o)+x)
    if"a"<=t<="h"and b.get(t+str(r+d),".").islower()!=q.isupper():l.append(s+t+str(r+d))
   if v=="p"and((q.isupper()and r==4)or(q.islower()and r==5)):
    for x in[-1,1]:
     t=chr(ord(o)+x)
     if"a"<=t<="h"and b.get(t+str(r))=="P"if q.islower()else b.get(t+str(r))=="p":l.append(s+t+str(r+d))
  elif v=="n":
   for dx,dy in[(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]:
    t=chr(ord(o)+dx);u=r+dy
    if"a"<=t<="h"and 1<=u<=8:
     n=t+str(u)
     if not b.get(n)or b[n].islower()!=q.isupper():l.append(s+n)
  elif v in"brq":
   for dx,dy in([(1,1),(1,-1),(-1,1),(-1,-1)]if v in"bq"else[])+([(1,0),(-1,0),(0,1),(0,-1)]if v in"rq"else[]):
    t=ord(o)+dx;u=r+dy
    while"a"<=chr(t)<="h"and 1<=u<=8:
     n=chr(t)+str(u)
     if b.get(n):
      if b[n].islower()!=q.isupper():l.append(s+n)
      break
     l.append(s+n);t+=dx;u+=dy
  elif v=="k":
   for dx in[-1,0,1]:
    for dy in[-1,0,1]:
     if dx or dy:
      t=chr(ord(o)+dx);u=r+dy
      if"a"<=t<="h"and 1<=u<=8:
       n=t+str(u)
       if not b.get(n)or b[n].islower()!=q.isupper():l.append(s+n)
 for x in l:
  if len(x)==4 and x[1]in"18"and p(f).get(x[:2],"").lower()=="p":yield x+"q";yield x+"r";yield x+"b";yield x+"n"
  else:yield x
def e(f):
 b=p(f);s=0
 for q in b.values():s+=P[q.lower()]*(1 if q.isupper()else-1)
 return s
def k(f):
 return f
def a(f,d,a,b):
 global N
 if d==0 or N<=0:return e(f)
 N-=1
 h=k(f)
 if h in D:return D[h]
 v=-20000
 for x in m(f):
  v=max(v,-a(k(x),d-1,-b,-a))
  if v>=b:break
 D[h]=v
 return v
def c(f):
 global N,D
 N=50000;D={}
 b=-20000;z=None
 for x in m(f):
  v=-a(x,4,-20000,-b)
  if v>b:b=v;z=x
 return z
def Pst(p,b):
 r=p
 for k,v in b.items():r=urllib.request.Request(U+k,json.dumps(v).encode(),{"content-type":"application/json"})
 try:return json.load(urllib.request.urlopen(r))
 except urllib.error.HTTPError as x:sys.exit(f"{k}: HTTP {x.code}")
while 1:
 g=Pst("/game",{})
 if g["status"]=="done":break
 while g["status"]=="your_move":g=Pst("/move",{"game":g["game"],"move":c(g["fen"])})
 print(f"game {g['game']}: {g['outcome']} by {g['reason']}",file=sys.stderr)
print(f"done: {g.get('wins')} won, {g.get('draws')} drawn, {g.get('losses')} lost",file=sys.stderr)