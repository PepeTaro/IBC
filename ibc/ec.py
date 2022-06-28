from .fq import Fq
from .fq2 import Fq2

def Point(ff):
    class _Point:
        """
        楕円曲線上の点を表すクラス
        """
        def __init__(self,x,y):
            assert isinstance(x,self._ff) and isinstance(y,self._ff) 
            self.x = x
            self.y = y
            
        def __str__(self):
            return "(%s,%s)"%(str(self.x),str(self.y))

        def __eq__(self,other):
            assert isinstance(other,_Point)            
            return self.x == other.x and self.y == other.y
        
        def __ne__(self,other):
            return not self == other
        
    point = _Point
    point._ff = ff
    return point
    
class EC:
    """
    楕円曲線: y^2 = x^3 + ax + b (ここでa,bは有限体の元)
    を表すクラス。

    *** Noneは楕円曲線群の単位元を表すことに注意。***
    
    """
    def __init__(self,a,b,ff):
        self.a = a
        self.b = b
        self.ff = ff # 有限体(Finite Field)
        self.point = Point(self.ff)

        assert isinstance(self.a,self.ff)
        assert isinstance(self.b,self.ff)

        # Discriminantを計算。
        disc = 4*(self.a**3) + 27*(self.b**2)

        # Singular elliptic curveを避ける。
        assert disc != 0

    def __str__(self):
        return "E(y^2 = x^3 + %s*x + %s)/F_%s"%(str(self.a),str(self.b),self.ff.prime())
    
    def on_curve(self,p):
        """
        点pが楕円曲線上にある場合True、そうでない場合Falseを返す。
        @param p:Point
        @return: bool
        """
        
        assert isinstance(p,self.point)
        
        if(p is None):
            return True
        else:
            test = p.y**2 - (p.x**3) - self.a*p.x - self.b
            return test == 0
            
    def double_and_add(self,n,p):
        """
        double-and-addアルゴリズムを使用して[n]Pを計算。
        
        @param n:int
        @param p:Point
        @return:Point
        """
        assert isinstance(n,int)
        assert isinstance(p,(self.point,None))

        if p is None: return None
        
        if n == 0: # [0]p => None
            return None
        elif n < 0: # e.g. [-5]p => [5](-p)
            return self.double_and_add(-n,self.neg(p))
        
        q = p
        r = None
        while(n > 0):
            if(n & 1): # nが奇数の場合。
                r = self.add(r,q)
            q = self.add(q,q)
            n >>= 1

        return r

    def neg(self,p):
        """
        -p を計算。
        
        @param p:Point
        @return:Point
        """
        assert isinstance(p,(self.point,type(None)))

        if p is None: return None        
        p = self.point(p.x,-p.y)
        return p
    
    def add(self,p1,p2):
        """
        p1 + p2を計算。
        [注意]
        Noneは単位元を表すことに注意。

        @param p1:Point
        @param p2:Point
        @return:Point
        """
        assert isinstance(p1,(self.point,type(None)))
        assert isinstance(p2,(self.point,type(None)))
        
        if(p1 is None):
            return p2
        elif(p2 is None):
            return p1
        elif(p1.x == p2.x and p1.y == -p2.y):
            return None
        elif(p1.x == p2.x and p1.y == p2.y):
            numer = 3*(p1.x**2) + self.a
            denom = 2*p1.y
        else:
            numer = p2.y - p1.y
            denom = p2.x - p1.x
            
        l = numer/denom
        x3 = l**2 - p1.x - p2.x
        y3 = l*(p1.x - x3) - p1.y
        
        return self.point(x3,y3)

    def sub(self,p1,p2):
        """
        p1 - p2を計算。
        @param p1:Point
        @param p2:Point
        @return:Point
        """
        assert isinstance(p1,(self.point,type(None)))
        assert isinstance(p2,(self.point,type(None)))

        return self.add(p1,self.neg(p2)) # p1 + (-p2)

    def mul(self,n,p):
        """
        [n]p を計算。
        @param n:int
        @param p:Point
        @return:Point
        """
        assert isinstance(n,int)
        assert isinstance(p,(self.point,type(None)))
        
        return self.double_and_add(n,p)
    
    def modulo(self):        
        return self.ff.modulo()
