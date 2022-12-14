import bisect


class BIT_SortedMultiset:
    def __init__(self, A, compress=True, sort_flag=False):
        self.compress = compress
        self.N = len(A)
        self.log = 0
        while self.N >= 1 << (self.log + 1):
            self.log += 1
        if compress:
            if sort_flag:
                self.A = A
            else:
                self.A = sorted(A)
            self.index_dic = {}
            for i in range(len(A)):
                self.index_dic[self.A[i]] = i
        else:
            self.A = A
        self.BIT = [0] * (self.N + 5)
        self.size = 0
        self.cnt = [0] * self.N

    def BIT_add(self, i, x):
        idx = i + 1
        while idx < self.N + 1:
            self.BIT[idx] += x
            idx += idx & (-idx)

    def BIT_query(self, i):
        res = 0
        idx = i + 1
        while idx:
            res += self.BIT[idx]
            idx -= idx & (-idx)
        return res

    def BIT_lower_left(self, w):
        if w <= 0 or w > self.size:
            return None
        x = 0
        k = 1 << self.log
        while k > 0:
            if x + k < self.N and self.BIT[x + k] < w:
                w -= self.BIT[x + k]
                x += k
            k //= 2
        return x

    def __contains__(self, x):
        if self.compress:
            x = self.index_dic[x]
        return self.cnt[x] >= 1

    def __len__(self):
        return self.size

    def add(self, x):
        if self.compress:
            x = self.index_dic[x]
        self.BIT_add(x, 1)
        self.size += 1
        self.cnt[x] += 1

    def discard(self, x):
        if self.compress:
            x = self.index_dic[x]
        if self.cnt[x] > 0:
            self.BIT_add(x, -1)
            self.size -= 1
            self.cnt[x] -= 1
            return True
        return False

    def find_kth_val(self, k):
        res = self.BIT_lower_left(k + 1)
        if res == None:
            return None
        if self.compress:
            res = self.A[res]
        return res

    def __getitem__(self, x):
        if x < 0:
            x += self.size
        if x < 0 or x >= self.size:
            raise IndexError
        return self.find_kth_val(x)

    def index_right(self, x):
        if x < self.A[0]:
            return 0
        if self.compress:
            y = bisect.bisect_right(self.A, x) - 1
        else:
            y = min(x, self.N - 1)
        return self.BIT_query(y)

    def index(self, x):
        if x <= self.A[0]:
            return 0
        if self.compress:
            y = bisect.bisect_right(self.A, x) - 1
        else:
            y = x
        if y >= self.N:
            y = self.N - 1
        elif self.A[y] == x:
            y -= 1
        return self.BIT_query(y)

    def gt(self, x):
        return self.find_kth_val(self.index_right(x))

    def ge(self, x):
        return self.find_kth_val(self.index(x))

    def lt(self, x):
        return self.find_kth_val(self.index(x) - 1)

    def le(self, x):
        return self.find_kth_val(self.index_right(x) - 1)

    def __str__(self):
        return (
            "{"
            + ", ".join(map(str, [self.find_kth_val(i) for i in range(self.size)]))
            + "}"
        )
