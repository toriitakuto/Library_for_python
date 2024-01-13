class segtree():
  def __init__(self,init,func,ide):
    self.n=len(init)
    self.func=func
    self.ide=ide
    self.size=1<<(self.n-1).bit_length()
    self.tree=[self.ide for i in range(2*self.size)]
    for i in range(self.n):
      self.tree[self.size+i]=init[i]
    for i in range(self.size-1,0,-1):
      self.tree[i]=self.func(self.tree[2*i], self.tree[2*i|1])
  
  def update(self,k,x):
    k+=self.size
    self.tree[k]=x
    k>>=1
    while k:
      self.tree[k]=self.func(self.tree[2*k],self.tree[k*2|1])
      k>>=1
  
  def get(self,i):
    return self.tree[i+self.size]
  
  def query(self,l,r):
    l+=self.size
    r+=self.size
    l_res=self.ide
    r_res=self.ide
    while l<r:
      if l&1:
        l_res=self.func(l_res,self.tree[l])
        l+=1
      if r&1:
        r-=1
        r_res=self.func(self.tree[r],r_res)
      l>>=1
      r>>=1
    return self.func(l_res,r_res)

  def max_right(self,l,f):
    assert 0<=l<=self.n 
    assert f(self.ide)
    if l==self.n:
      return self.n
    l+=self.size
    res=self.ide
    while True:
      while l&1==0:
        l>>=1
      if not f(self.func(res,self.tree[l])):
        while l<self.size:
          l*=2
          if f(self.func(res,self.tree[l])):
            res=self.func(res,self.tree[l])
            l+=1
        return l-self.size
      res=self.func(res,self.tree[l])
      l+=1
      if l&(-l)==l:
        break
    return self.n
  
  def min_left(self,r,f):
    assert 0<=r<=self.n
    assert f(self.ide)
    if r==0:
      return 0
    r+=self.size
    res=self.ide
    while True:
      r-=1
      while r>1 and r&1:
        r>>=1
      if not f(self.func(self.tree[r],res)):
        while r<self.size:
          r=2*r+1     
          if f(self.func(self.tree[r],res)):
            res=self.func(self.tree[r],res)
            r-=1
        return r+1-self.size
      res=self.func(self.tree[r],res)
      if r&(-r)==r:
        break
    return 0
    
  def __getitem__(self,i):
    return self.get(i)
  
  def __setitem__(self,key,val):
    self.update(key,val)

  def __iter__(self):
    for i in range(self.n):
      yield self.tree[i+self.size]
          
  def __str__(self):
    return str(list(self))

