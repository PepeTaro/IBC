from .misc import sq_and_mul_fq,inv    
from .prime import is_prime

def Fq(q):
    class _Fq:
        """
        qを素数とする有限体{0,1,...,p-1}を表すクラス
        """
        
        def __init__(self,n):
            assert isinstance(n,(_Fq,int))
            
            if isinstance(n,_Fq):
                self._n = n._n
            else:
                self._n = n % self._q
        
        def __str__(self):
            return str(self._n)
    
        def __repr__(self):
            return str(self._n)
        
        def __add__(self,other):
            assert isinstance(other,(_Fq,int))
            if isinstance(other,int):
                return _Fq(self._n + other)
            else:
                return _Fq(self._n + other._n)
            
        def __radd__(self,other):
            return self + other

        def __iadd__(self,other):
            assert isinstance(other,(_Fq,int))
            if isinstance(other,int):
                self._n = (self._n + other) % self._q
            else:
                self._n = (self._n + other._n) % self._q

            return self
        
        def __sub__(self,other):
            assert isinstance(other,(_Fq,int))
            if isinstance(other,int):
                return _Fq(self._n - other)
            else:
                return _Fq(self._n - other._n)

        def __isub__(self,other):
            assert isinstance(other,(_Fq,int))
            if isinstance(other,int):
                self._n = (self._n - other) % self._q
            else:
                self._n = (self._n - other._n) % self._q

            return self
        
        def __mul__(self,other):
            assert isinstance(other,(_Fq,int))
            if isinstance(other,int):
                return _Fq(self._n*other)
            else:
                return _Fq(self._n*other._n)
            
        def __rmul__(self,other):
            return self*other

        def __imul__(self,other):
            assert isinstance(other,(_Fq,int))
            if isinstance(other,int):
                self._n = (self._n*other) % self._q
            else:
                self._n = (self._n*other._n) % self._q

            return self
        
        def __truediv__(self,other):
            assert isinstance(other,(_Fq,int))
            if isinstance(other,int):
                return _Fq(self._n*inv(other,self._q))
            else:
                return _Fq(self._n*inv(other._n,self._q))
            
        def __rtruediv__(self,other):
            assert isinstance(other,int)
            return _Fq(other)/self
        
        def __idiv__(self,other):
            assert isinstance(other,(_Fq,int))
            if isinstance(other,int):
                self._n = (self._n*inv(other,self._q)) % self._q
            else:
                self._n = (self._n*inv(other._n,self._q)) % self._q

            return self
        
        def __pow__(self,e):
            r = sq_and_mul_fq(self,e)
            return r

        def __neg__(self):
            return _Fq(-self._n)
        
        def __eq__(self,other):
            assert isinstance(other,(_Fq,int))
            if isinstance(other,int):
                return self._n == other
            else:
                return self._n == other._n
            
        def __ne__(self,other):
            return not self == other
        
        def val(self):
            return self._n

        def trace(self):
            # Trace Map
            return self._n
        
        @staticmethod
        def name():
            return fq._name

        @staticmethod
        def modulo():
            return fq._q
        
    assert is_prime(q)
    fq = _Fq
    fq._q = q
    fq._name = "fq"
    return fq
