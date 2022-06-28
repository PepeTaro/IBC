"""
Ref: https://crypto.stanford.edu/pbc/thesis.pdf p77.
"""

from .fq import Fq
from .misc import sq_and_mul_fq

def _int_to_fq2(fq2,n):
    """
    整数nをクラスfq2に変換。
    n => fq2(-n,-n)
    """
    assert fq2.name() == "fq2"
    assert isinstance(n,int)
    return fq2(-n,-n)

def _fq_to_fq2(fq2,p):
    """
    クラスfqをクラスfq2に変換。
    p = fq(n) => fq2(-n,-n)
    """
    assert fq2.name() == "fq2"
    assert p.name() == "fq"
    
    n = p.val()
    return fq2(-n,-n)

def _mul_tuple(p1,p2):
    """
    fq2クラスであるp1とp2の積を計算。    
    戻り値はfqクラスのタプルであることに注意。
    
    @param p1:Fq2
    @param p2:Fq2
    @return: (a,b) = (Fq,Fq)
    """    
    assert p1.name() == "fq2"
    assert p2.name() == "fq2"
    
    a = p1.y()*p2.y() - p1.x()*p2.y() - p1.y()*p2.x()
    b = p1.x()*p2.x() - p1.x()*p2.y() - p1.y()*p2.x()
    return a,b

def _mul_fq2(fq2,p1,p2):
    """
    fq2クラスであるp1とp2の積を計算。    
    
    @param fq2:
    @param p1:Fq2
    @param p2:Fq2
    @return: Fq2
    """
    assert fq2.name() == "fq2"
    assert p1.name() == "fq2"
    assert p2.name() == "fq2"
    
    (a,b) = _mul_tuple(p1,p2)
    return fq2(a,b)

def _inv_fq2(fq2,p):
    """
    1/pを計算。
    
    @param fq2:
    @param p:Fq2
    """
    assert fq2.name() == "fq2"
    assert p.name() == "fq2"
    assert p.x() != 0 or p.y() != 0
    
    if p.x() != 0:
        tmp = p.y()/p.x()
        denom = p.y()*tmp + p.x() - p.y()
        b = 1/denom
        a = tmp*b
    else: # p1.y != 0
        tmp = p.x()/p.y()
        denom = p.y() - (p.y() - p.x())*tmp
        a = 1/denom
        b = tmp*a

    return fq2(a,b)

def Fq2(fq):
    
    class _Fq2:
        """
        Fqの拡大体Fq2 = Fq[x]/(x^2 + x + 1)を表すクラス。
        
        [注意]
        q%3 == 2を満たさないと正しく動かないことに注意。
        """

        def __init__(self,x,y):
            assert isinstance(x,(self._fq,int))
            assert isinstance(y,(self._fq,int))
            
            if isinstance(x,self._fq): self._x = x
            else: self._x = self._fq(x % self._q)

            if isinstance(y,self._fq): self._y = y
            else: self._y = self._fq(y % self._q)

        def __str__(self):
            return "(%s,%s)"%(str(self._x),str(self._y))
    
        def __repr__(self):
            return str(self)
        
        def __add__(self,other):
            assert isinstance(other,_Fq2)
            return _Fq2(self._x + other._x,self._y + other._y)
            
        def __radd__(self,other):
            return self + other

        def __iadd__(self,other):
            assert isinstance(other,_Fq2)
            self._x = (self._x + other._x)
            self._y = (self._y + other._y)
            
            return self
        
        def __sub__(self,other):
            assert isinstance(other,_Fq2)
            return _Fq2(self._x - other._x,self._y - other._y)
        
        def __isub__(self,other):
            assert isinstance(other,_Fq2)
            self._x = (self._x - other._x)
            self._y = (self._y - other._y)
            
            return self
        
        def __mul__(self,other):
            assert isinstance(other,(_Fq2,self._fq,int))
            if isinstance(other,int):
                return self*_int_to_fq2(self.__class__,other)
            elif isinstance(other,self._fq):
                return self*_fq_to_fq2(self.__class__,other)
            else:
                return _mul_fq2(self.__class__,self,other)
            
        def __rmul__(self,other):
            return self*other
        
        def __imul__(self,other):
            assert isinstance(other,(_Fq2,self._fq,int))
            if isinstance(other,int):
                self._x,self._y = _mul_tuple(self,_int_to_fq2(other))
            elif isinstance(other,self._fq):
                self._x,self._y = _mul_tuple(self,_fq_to_fq2(other))
            else:
                self._x,self._y = _mul_tuple(self,other)
                
            return self
        
        def __truediv__(self,other):
            assert isinstance(other,(_Fq2,self._fq,int))
            assert other._x != 0 or other._y != 0
            
            if isinstance(other,int):
                return self*_inv_fq2(self.__class__,_int_to_fq2(other))
            elif isinstance(other,self._fq):
                return self*_inv_fq2(self.__class__,_fq_to_fq2(other))
            else:
                return self*_inv_fq2(self.__class__,other)
            
        def __rtruediv__(self,other):
            assert isinstance(other,int)            
            return _int_to_fq2(self.__class__,other)/self
        
        def __idiv__(self,other):
            assert isinstance(other,(_Fq,self._fq,int))
            if isinstance(other,int):
                d = _inv_fq2(self.__clas__,_int_to_fq2(other))
            elif isinstance(other,self._fq):
                d = _inv_fq2(self.__clas__,_fq_to_fq2(other))
            else:
                d = _inv_fq2(self.__clas__,other)

            self._x,self._y = _mul_tuple(self,d)
            return self
        
        def __pow__(self,e):
            r = sq_and_mul_fq(self,e)
            return r

        def __neg__(self):
            return _Fq2(-self._x,-self._y)
        
        def __eq__(self,other):
            assert isinstance(other,_Fq2) or isinstance(other,self._fq) or isinstance(other,int)
            if isinstance(other,int):
                n = (-other)%self._q # -other(マイナス)であることに注意。
                return self._x == n and self._y == n
            elif isinstance(other,self._fq):
                n = (-fq.val())%self._q
                return self._x == n and self._y == n
            else:
                return self._x == other._x and self._y == other._y
            
        def __ne__(self,other):
            return not self == other

        def x(self):
            return self._x

        def y(self):
            return self._y

        def trace(self):
            """
            Trace Mapを計算。
            Tr:Fq2 => Fq
            Tr((a,b)) := (a,b) + (a,b)**q.
            しかし(a,b)**q = (b,a)なので、
            Tr((a,b)) = (a,b) + (b,a) = (a+b,a+b) = -(a+b).
            [補足]
            (a+b,a+b) = (a+b)*x + (a+b)*x^2 = (a+b)(x + x^2) = -(a+b)
            最後の等式においてx^2 + x + 1 = 0を使用した。
            """
            z = self._x + self._y
            return self._fq(-z)
        
        @staticmethod
        def name():
            return fq2._name
        
        @staticmethod        
        def int_to_fq2(other):
            """
            整数otherをクラスfq2に変換。
            n => Fq2(-n,-n)
            """            
            assert isinstance(other,int)
            return _int_to_fq2(_Fq2,other)
        
        @staticmethod
        def modulo():
            return fq2._q

    assert fq.modulo()%3 == 2
    
    fq2 = _Fq2
    fq2._fq = fq
    fq2._q = fq.modulo()
    fq2._name = "fq2"
    return fq2

