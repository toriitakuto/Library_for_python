from math import gcd


class Fraction:
    def __init__(self, num, den=1):
        if type(num) == float or type(num) == str:
            assert den == 1
            if type(num) == float:
                S = str("{:.10f}".format(num))
            else:
                S = num
            N = len(S)
            point = -1
            for i in range(N):
                if S[i] == ".":
                    point = i
            if point != -1:
                F = Fraction(int(S[:point] + S[point + 1 :]), 10 ** (N - 1 - point))
            else:
                F = Fraction(int(S), 1)
            self.num = F.num
            self.den = F.den
        elif type(num) == type(den) == int:
            assert den != 0
            """
            inf = 10**9
            if den == 0:
                if num > 0:
                    self.num = inf
                    self.den = 1
                elif num < 0:
                    self.num = -inf
                    self.den = 1
                else:
                    raise Exception
                return
            """
            den, num = max((den, num), (-den, -num))
            g = gcd(den, num)
            self.num = num // g
            self.den = den // g
        else:
            raise Exception

    def __str__(self):
        return str(self.num) + "/" + str(self.den)

    def __pos__(self):
        return self

    def __neg__(self):
        num, den = self.num, self.den
        return Fraction(-num, den)

    def __add__(self, other):
        if type(other) != Fraction:
            other = Fraction(other)
        num1, den1 = self.num, self.den
        num2, den2 = other.num, other.den
        return Fraction(num1 * den2 + num2 * den1, den1 * den2)

    def __sub__(self, other):
        if type(other) != Fraction:
            other = Fraction(other)
        num1, den1 = self.num, self.den
        num2, den2 = other.num, other.den
        return Fraction(num1 * den2 - num2 * den1, den1 * den2)

    def __mul__(self, other):
        if type(other) != Fraction:
            other = Fraction(other)
        num1, den1 = self.num, self.den
        num2, den2 = other.num, other.den
        return Fraction(num1 * num2, den1 * den2)

    def __truediv__(self, other):
        if type(other) != Fraction:
            other = Fraction(other)
        num1, den1 = self.num, self.den
        num2, den2 = other.num, other.den
        return Fraction(num1 * den2, num2 * den1)

    def __pow__(self, x):
        assert type(x) == int
        num, den = self.num, self.den
        if x >= 0:
            return Fraction(num**x, den**x)
        else:
            return Fraction(den ** (-x), num ** (-x))

    __radd__ = __add__

    def __rsub__(self, other):
        if type(other) != Fraction:
            other = Fraction(other)
        num1, den1 = other.num, other.den
        num2, den2 = self.num, self.den
        return Fraction(num1 * den2 - num2 * den1, den1 * den2)

    __rmul__ = __mul__

    def __rtruediv__(self, other):
        if type(other) != Fraction:
            other = Fraction(other)
        num1, den1 = other.num, other.den
        num2, den2 = self.num, self.den
        return Fraction(num1 * den2, num2 * den1)

    def __eq__(self, other):
        if type(other) != Fraction:
            other = Fraction(other)
        num1, den1 = self.num, self.den
        num2, den2 = other.num, other.den
        return num1 == num2 and den1 == den2

    def __lt__(self, other):
        if type(other) != Fraction:
            other = Fraction(other)
        num1, den1 = self.num, self.den
        num2, den2 = other.num, other.den
        return num1 * den2 < num2 * den1

    def __le__(self, other):
        if type(other) != Fraction:
            other = Fraction(other)
        num1, den1 = self.num, self.den
        num2, den2 = other.num, other.den
        return num1 * den2 <= num2 * den1

    def __gt__(self, other):
        if type(other) != Fraction:
            other = Fraction(other)
        num1, den1 = self.num, self.den
        num2, den2 = other.num, other.den
        return num1 * den2 > num2 * den1

    def __ge__(self, other):
        if type(other) != Fraction:
            other = Fraction(other)
        num1, den1 = self.num, self.den
        num2, den2 = other.num, other.den
        return num1 * den2 >= num2 * den1
    
    def floor(self):
      return self.num//self.den
