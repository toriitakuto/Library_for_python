from collections import deque
 
class Edge:
  def __init__(self,frm,to,cap,flow):
    self.frm=frm
    self.to=to
    self.cap=cap
    self.flow=flow
 
class MaxFlow:
  def __init__(self,n):
    self.n=n
    self.g=[[] for i in range(n)]
    self.pos=[]
    self.Iter=[0]*n
    self.level=[0]*n
  
  def add_edge(self,frm,to,cap):
    assert 0<=frm<self.n
    assert 0<=to<self.n
    assert 0<=cap
    m=len(self.pos)
    frm_id=len(self.g[frm])
    self.pos.append([frm,frm_id])
    to_id=len(self.g[to])
    if frm==to:
      to_id+=1
    self.g[frm].append([to,to_id,cap])
    self.g[to].append([frm,frm_id,0])
    return m
  
  def get_edges(self):
    res=[]
    for i in range(len(self.pos)):
      e=self.g[self.pos[i][0]][self.pos[i][1]]
      re=self.g[e[0]][e[1]]
      E=Edge(re[0],e[0],e[2]+re[2],re[2])
      res.append(E)
    return res
  
  def bfs(self,s,t):
    self.level=[-1]*self.n
    self.level[s]=0
    dq=deque([s])
    while dq:
      v=dq.popleft()
      lv=self.level[v]
      for u,rev,cap in self.g[v]:
        if cap==0 or self.level[u]!=-1:
          continue
        self.level[u]=lv+1
        if u==t:
          return True
        dq.append(u)
    return False
  
  def dfs(self,s,t,limit):
    res=[t]
    while res:
      v=res[-1]
      if v==s:
        v=res.pop()
        flow=limit
        for w in res:
          e=self.g[w][self.Iter[w]]
          flow=min(flow,self.g[e[0]][e[1]][2])
        for w in res:
          e=self.g[w][self.Iter[w]]
          self.g[w][self.Iter[w]][2]+=flow
          self.g[e[0]][e[1]][2]-=flow
        return flow
      
      while self.Iter[v]<len(self.g[v]):
        e=self.g[v][self.Iter[v]]
        w=e[0]
        cap=self.g[w][e[1]][2]
        if cap>0 and self.level[v]>self.level[w]:
          res.append(w)
          break
        self.Iter[v]+=1
      else:
        res.pop()
        self.level[v]=self.n
        
    return 0
  
  def flow(self,s,t,flow_limit=1<<62):
    flow=0
    while flow<flow_limit and self.bfs(s,t):
      self.Iter=[0]*self.n
      while flow<flow_limit:
        f=self.dfs(s,t,flow_limit-flow)
        if f==0:
          break
        flow+=f
    return flow
 
