class SOE:
  def __init__(self,m):
    self.sieve=[-1]*(m+1)
    self.prime=[]
    for i in range(2,m+1):
      if self.sieve[i]==-1:
        self.prime.append(i)
        self.sieve[i]=i
        j=2*i
        while j<=m:
          self.sieve[j]=i
          j+=i
  
  def primes(self):
    # primes
    return self.prime
  
  def fact(self,n):
    # prime factorization
    d=[]
    while n!=1:
      p=self.sieve[n]
      c=0
      while n%p==0:
        c+=1
        n//=p
      d.append((p,c))
    return d
  
  def div(self,n):
    # divisors
    c=[1]
    while n!=1:
      p=self.sieve[n]
      cnt=1
      n//=p
      while self.sieve[n]==p:
        cnt+=1
        n//=p
      s=c.copy()
      for i in s:
        for j in range(1,cnt+1):
          c.append(i*(p**j))
    return c

