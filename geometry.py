# 幾何ライブラリ

from functools import cmp_to_key
from typing import List
from math import*

Point=complex
def point(a,b)->Point:
  return a+b*1j

def print_Point(p:Point):
  x,y=p.real,p.imag
  print('{:.10f}'.format(x),'{:.10f}'.format(y))

def print_float(x:float):
  print('{:.10f}'.format(x))

def str_float(x:float)->str:
  return '{:.10f}'.format(x)

def norm(p:Point):
  return p.real**2+p.imag**2

def cmp(a:Point,b:Point)->bool:
  if not equal(a.real,b.real):
    if a.real<b.real:return -1
    else:return 1
  else:
    if a.imag<b.imag:return -1
    else:return 1

eps=1e-9

# 同じか判定
def equal(a:Point,b:Point)->float:
  return abs(a-b)<eps

# 単位ベクトルを求める
def unitVector(a:Point)->Point:
  return a/abs(a)

# 内積(dot product):a・b=|a||b|cosΘ
def dot(a:Point,b:Point)->float:
  return a.real*b.real+a.imag*b.imag

# 外積(cross product):a×b=|a||b|sinΘ
def cross(a:Point,b:Point)->float:
  return a.real*b.imag-a.imag*b.real

# 点pを反時計回りにtheta度回転
def rotate(p:Point,theta:float)->Point:
  return (cos(theta)*p.real-sin(theta)*p.imag)+(sin(theta)*p.real+cos(theta)*p.imag)*1j


class Line:
  def __init__(self,a,b,c=False):
    if c==False:
      # a,b は複素数
      self.a=a
      self.b=b
    else:
      # ax+by=c
      # a,b,c は実数
      if equal(a,0):
        self.a=(c/b)*1j
        self.b=1+(c/b)*1j
      elif equal(b,0):
        self.a=(c/a)+0j
        self.b=(c/a)+1j
      else:
        self.a=(c/b)*1j
        self.b=(c/a)+0j


class Segment:
  def __init__(self,a:Point,b:Point):
    self.a=a
    self.b=b


class Circle:
  def __init__(self,p:Point,r:float):
    self.p=p
    self.r=r

# 射影(projection)
# 直線Lに点pから引いた垂線の足を求める
def projection(L:Line,p:Point)->Point:
  t=dot(p-L.a,L.a-L.b)/norm(L.a-L.b)
  return L.a+(L.a-L.b)*t

# 反射(reflection)
# 直線Lを対称軸として点pと線対称の位置にある点を求める
def reflection(L:Line,p:Point)->Point:
  return p+(projection(L,p)-p)*2

# 点の回転方向
def CounterClockWise(a:Point,b:Point,c:Point)->int:
  p=b-a
  q=c-a
  
  # a,b,c が反時計回り -> 1
  # a,b,c が時計回り -> -1
  # c,a,b がこの順で同一直線状 -> 2
  # a,b,c がこの順で同一直線状 -> -2
  # b,c,a がこの順で同一直線状 -> 0
  
  if cross(p,q)>eps:
    return 1
  if cross(p,q)<-eps:
    return -1
  if dot(p,q)<0:
    return 2
  if norm(p)<norm(q):
    return -2
  return 0


# 2 直線の直交判定
def isOrthiogonal(a:Line,b:Line)->bool:
  return equal(dot(a.b-a.a,b.b-b.a),0)

# 2 直線の平行判定
def isParallel(a:Line,b:Line)->bool:
  return equal(cross(a.b-a.a,b.b-b.a),0)

# 2 線分の交差判定
def isIntersect(s:Segment,t:Segment)->bool:
  return CounterClockWise(s.a,s.b,t.a)*CounterClockWise(s.a,s.b,t.b)<=0 and CounterClockWise(t.a,t.b,s.a)*CounterClockWise(t.a,t.b,s.b)<=0

# 2 直線の交点
def crossPoint(s:Line,t:Line)->Point:
  d1=cross(s.b-s.a,t.b-t.a)
  d2=cross(s.b-s.a,s.b-t.a)
  if equal(abs(d1),0) and equal(abs(d2),0):
    return t.a
  return t.a+(t.b-t.a)*(d2/d1)

def distanceBetweenLineAndPoint(l:Segment,p:Point)->float:
  return abs(cross(l.b-l.a,p-l.a))/abs(l.b-l.a)

# 線分lと点pの距離
def distanceBetweenSegmentAndPoint(l:Segment,p:Point)->float:
  if dot(l.b-l.a,p-l.a)<eps:
    return abs(p-l.a)
  if dot(l.a-l.b,p-l.b)<eps:
    return abs(p-l.b)
  return abs(cross(l.b-l.a,p-l.a))/abs(l.b-l.a)

# 線分s,tの距離
def distanceBetweenSegments(s:Segment,t:Segment)->float:
  if(isIntersect(s,t)):
    return 0
  ans=distanceBetweenSegmentAndPoint(s,t.a)
  ans=min(ans,distanceBetweenSegmentAndPoint(s,t.b))
  ans=min(ans,distanceBetweenSegmentAndPoint(t,s.a))
  ans=min(ans,distanceBetweenSegmentAndPoint(t,s.b))
  return ans

# 多角形の面積
def PolygonArea(p:List[Point])->float:
  res=0
  n=len(p)
  for i in range(n):
    res+=cross(p[i],p[(i+1)%n])
  return res/2

# 凸判定
def isConvex(p:List[Point])->float:
  # p は反時計回り
  n=len(p)
  for i in range(n):
    if CounterClockWise(p[(i-1)%n],p[i],p[(i+1)%n])==-1:
      return False
  return True

# 多角形 g に点 p が含まれるか
def isContained(g:List[Point],p:Point)->int:
  # 含む:2,辺上:1,含まない:0
  IN=False
  n=len(g)
  for i in range(n):
    a=g[i]-p
    b=g[(i+1)%n]-p
    if a.imag>b.imag:
      a,b=b,a
    if a.imag<=0 and 0<b.imag and cross(a,b)<0:
      IN^=1
    if cross(a,b)==0 and dot(a,b)<=0:
      return 1
  if IN:
    return 2
  return 0

# 凸包
def ConvexHull(g:List[Point])->List[Point]:        
  g.sort(key=cmp_to_key(cmp))
  CH=[]
  n=len(g)
  for p in g:
    # 同一直線上の3点を含める -> (<-eps)
    # 含めない -> (<eps)
    while len(CH)>1 and cross(CH[-1]-CH[-2],p-CH[-1])<-eps:
      CH.pop()
    CH.append(p)
  t=len(CH)
  for i in range(n-2,-1,-1):
    p=g[i]
    while len(CH)>t and cross(CH[-1]-CH[-2],p-CH[-1])<-eps:
      CH.pop()
    CH.append(p)
  return CH[:-1]

# 凸多角形の直径
def ConvexDiameter(p:List[Point])->float:
  n=len(p)
  i0,j0=0,0
  for i in range(1,n):
    if p[i].imag>p[i0].imag:
      i0=i
    if p[i].imag<p[j0].imag:
      j0=i
  
  mx=abs(p[i0]-p[j0])
  i=i0
  j=j0
  while i!=j0 or j!=i0:
    if(cross(p[(i+1)%n]-p[i],p[(j+1)%n]-p[j])>=0):
      j=(j+1)%n
    else:
      i=(i+1)%n
    if abs(p[i]-p[j])>mx:
      mx=abs(p[i]-p[j])
  return mx


# 凸多角形の切断
# 直線 L.a-L.b で切断して，その左側の凸多角形を返す
def ConvexCut(P:List[Point],L:Line)->List[Point]:
  ret=[]
  n=len(P)
  for i in range(n):
    now,nxt=P[i],P[(i+1)%n]
    if CounterClockWise(L.a,L.b,now)!=-1:
      ret.append(now)
    if CounterClockWise(L.a,L.b,now)*CounterClockWise(L.a,L.b,nxt)<0:
      ret.append(crossPoint(Line(now,nxt),L))
  return ret


# 円の交差判定
def IsIntersectCircle(c1:Circle,c2:Circle)->int:
  d=abs(c1.p-c2.p)
  
  # 2 円が離れている
  if d>c1.r+c2.r+eps:
    return 4
  # 外接
  if equal(d,c1.r+c2.r):
    return 3
  # 内接
  if equal(d,abs(c1.r-c2.r)):
    return 1
  # 内包
  if d<abs(c1.r-c2.r)-eps:
    return 0
  # 2 交点を持つ
  return 2

# 三角形の内心
def InscribedCircle(a:Point,b:Point,c:Point)->Circle:
  A,B,C=abs(b-c),abs(c-a),abs(b-a)
  p=point(A*a.real+B*b.real+C*c.real,A*a.imag+B*b.imag+C*c.imag)
  p/=(A+B+C)
  r=distanceBetweenSegmentAndPoint(Line(a,b),p)
  return Circle(p,r)

# 三角形の外心
def CircumscribedCircle(a:Point,b:Point,c:Point)->Circle:
  p=(a-b)*norm(c)+(b-c)*norm(a)+(c-a)*norm(b)
  p/=(a-b)*c.conjugate()+(b-c)*a.conjugate()+(c-a)*b.conjugate()
  r=abs(p-a)
  return Circle(p,r)

# 円Cと直線Lの交点
def CrossPoint_Circle_Line(C:Circle,L:Line)->List[Point]:
  res=[]
  d=distanceBetweenLineAndPoint(L,C.p)
  if d>C.r+eps:
    return res
  h=projection(L,C.p)
  if equal(d,C.r):
    return [h]
  e=unitVector(L.b-L.a)
  ph=sqrt(C.r**2-d**2)
  res.append(h-e*ph)
  res.append(h+e*ph)
  return res

# 2 円の交点
def CrossPointCircles(C1:Circle,C2:Circle)->List[Point]:
  res=[]
  mode=IsIntersectCircle(C1,C2)
  d=abs(C1.p-C2.p)
  if mode==4 or mode==0:
    return res
  if mode==3:
    t=C1.r/(C1.r+C2.r)
    res.append(C1.p+(C2.p-C1.p)*t)
    return res
  if mode==1:
    if C2.r<C1.r-eps:
      res.append(C1.p+(C2.p-C1.p)*(C1.r/d))
    else:
      res.append(C2.p+(C1.p-C2.p)*(C2.r/d))
    return res
  rc1=(C1.r**2+d**2-C2.r**2)/(2*d)
  rs1=sqrt(C1.r**2-rc1**2)
  if C1.r-abs(rc1)<eps:
    rs1=0
  e12=(C2.p-C1.p)/abs(C2.p-C1.p)
  res.append(C1.p+rc1*e12+rs1*e12*point(0,1))
  res.append(C1.p+rc1*e12+rs1*e12*point(0,-1))
  return res

# 点pを通る円cの接線
def tangentToCircle(p:Point,c:Circle)->List[Point]:
  return CrossPointCircles(c,Circle(p,sqrt(norm(c.p-p)-c.r**2)))

# 2円の共通接線
def tangent(c1:Circle,c2:Circle)->List[Line]:
  res=[]
  d=abs(c1.p-c2.p)
  if equal(d,0):
    return []
  u=unitVector(c2.p-c1.p)
  v=rotate(u,pi/2)
  for s in [-1,1]:
    h=(c1.r+c2.r*s)/d
    if equal(h**2,1):
      res.append(Line(c1.p+h*u*c1.r,c1.p+h*u*c1.r+v))
    elif 1-h*h>0:
      U=u*h
      V=v*sqrt(1-h*h)
      res.append(Line(c1.p+(U+V)*c1.r,c2.p-(U+V)*c2.r*s))
      res.append(Line(c1.p+(U-V)*c1.r,c2.p-(U-V)*c2.r*s))
  return res
