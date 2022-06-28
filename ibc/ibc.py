import hashlib

from .ec import EC
from .fq import Fq
from .fq2 import Fq2
from .pairing import weil_pairing
from .misc import rand_between,sq_and_mul
from .prime import is_prime,rand_prime

def find_random_point(ec):
    """
    楕円曲線上のランダムな点を求める。
    
    @param ec:EC
    @return: 楕円曲線上のランダムな点。
    """
    
    # 楕円曲線は y^2 = x^3 + 1と仮定。
    assert isinstance(ec,EC)
    assert ec.ff.name() == "fq2"
    assert ec.a == 0
    assert ec.b == 1
    
    q = ec.modulo()
    assert q%3 == 2 # 3乗根を求めるための条件。
    
    y = rand_between(0,q - 1)
    x = sq_and_mul(y*y - 1,(2*q - 1)//3,q)
    
    x = ec.ff.int_to_fq2(x)
    y = ec.ff.int_to_fq2(y)
    p = ec.point(x,y)

    return p

def find_order_l(ec,l):
    """ 
    楕円曲線上で位数lを持つ点を求める。
    Ref: WASHINGTON p185
    
    @param ec:EC
    @param l: 戻り値として返る点の位数。
    @return: 位数lをもつ楕円曲線上の点。
    """
    assert isinstance(ec,EC)
    assert ec.ff.name() == "fq2"
    assert isinstance(l,int)
    
    p = None
    while True:        
        p = find_random_point(ec)
        p6 = ec.mul(6,p) # p6 = [6]p

        # p6の位数はl或いは1なので、p6 is not Noneの時点でp6の位数はl。
        if p6 is not None:
            break

    return p6
        
def prepare_params(low,high):
    """
    Pairingに使用するパラメータを生成。

    @param low: ランダムな素数の下限
    @param high: ランダムな素数の上限 
    @return: パラメータ(q,l)、ここでqは素数。
    """
    assert isinstance(low,int)
    assert isinstance(high,int)
    
    while True:
        l = rand_prime(low,high)
        q = 6*l - 1# q%3==2であることに注意、q%3==2はType B Curveであるために必要な条件。
        if is_prime(q):
            return q,l

def phi(ec,p):
    """
    Distortion Mapを計算。
    
    @param ec:EC
    @param p: 楕円曲線ec上の点(ec.point)
    @return: pにdistortion mapを適用した結果
    """
    assert isinstance(ec,EC)
    assert ec.ff.name() == "fq2"
    assert isinstance(p,ec.point)    
    phi.omega = ec.ff(1,0) # 非自明な1の三乗根。
    
    result = ec.point(p.x*phi.omega,p.y)
    return result

def modified_weil_pairing(ec,p1,p2,l):
    """
    位数lに関する、インプットをp1,p2とするModified Weil Pairingを計算。
    i.e. e_{l}(p1,p2)を計算、この値はFq2上でlのべき乗根である。
    
    @param ec:EC
    @param p1: 楕円曲線ec上の点
    @param p2: 楕円曲線ec上の点
    @param l: Weil Pairingに使う自然数
    @return: 位数lをもつFq2の値
    """
    assert isinstance(ec,EC)
    assert ec.ff.name() == "fq2"
    assert isinstance(p1,ec.point)
    assert isinstance(p2,ec.point)
    assert isinstance(l,int)
    
    s = find_random_point(ec)# 確率的に"悪い"ランダムな点を選ぶ可能性あり。
    return weil_pairing(ec,p1,phi(ec,p2),s,l)
    
def H1(ec,l,string):
    """
    文字列(或いはbytes)stringを位数lをもつ楕円曲線上の点に変換。
    
    @param ec:EC
    @param l:int
    @param string: 例えば、"alice@gmail.com"、b"bob@yahoo.co.jp"
    @return: 位数lをもつ楕円曲線ec上の点
    """
    assert isinstance(ec,EC)
    assert isinstance(l,int)
    assert ec.ff.name() == "fq2"
    assert isinstance(string,(str,bytes))
    
    if isinstance(string,str):
        s = string.encode()
    else:
        s = string
        
    q = ec.modulo()    
    y = int(hashlib.sha1(s).hexdigest(),16) % q    
    x = sq_and_mul(y*y - 1,(2*q - 1)//3,q)
    
    x = ec.ff.int_to_fq2(x)
    y = ec.ff.int_to_fq2(y)
    p = ec.point(x,y)
    assert ec.on_curve(p)

    p6 = ec.mul(6,p) #p6の位数はl或いは1。
    
    if p6 is None:
        print("[!] Error: please change the string!")
        return None
    else:
        return p6

def H2(p,n):
    """
    位数lをもつFq2の点pを長さがnである2進数の文字列に変換。
    H2(Fq2(x,y)) := Tr(Fq2(x,y)) + q*y、
    として定義する。
    ここでTrはFq2上のTrace Map。
    
    この定義を使用する理由は、H2は単射であるため、つまりCollision Free。
    Tr(Fq2(x,y))がFqの元つまり、{0,1,...,q-1}の内どれかであることに
    注意すれば、単射であることの証明は自明。

    @param p:Fq2
    @param n:int
    @return:str
    """
    assert p.name() == "fq2"
    assert isinstance(n,int)
    assert n > 0
    
    x = p.trace().val() + p.modulo()*p.y().val() # この値は整数であることに注意。(Fqの元ではない)
    format_str = "{:0" + str(n) + "b}"
    s = format_str.format(x)
    
    return s[0:n]

def xor(s1,s2):
    """
    2進数を表す文字列s1とs2のxorを計算。戻り値も2進数文字列。
    e.g. xor("101","111") => "010"

    @param s1: 2進数を表す文字列
    @param s2: 2進数を表す文字列
    @return: 2進数を表す文字列
    """
    assert len(s1) == len(s2)
    s = ""
    for b1,b2 in zip(s1,s2):
        s += str(int(b1)^int(b2))
    return s

def prepare(low,high):
    """
    公開鍵を生成。
    @param low:ランダムな素数の下限
    @param high:ランダムな素数の上限
    @return: ec(楕円曲線クラス),p(位数lをもつ楕円曲線上の点),l(int)
    """
    assert isinstance(low,int)
    assert isinstance(high,int)
    
    q,l = prepare_params(low,high)
    
    fq = Fq(q)
    fq2 = Fq2(fq)
    a = fq2.int_to_fq2(0)
    b = fq2.int_to_fq2(1)
    ec = EC(a,b,fq2) # Fq2上の楕円曲線: y^2 = x^3 + 1を定義。        
    p = find_order_l(ec,l)    

    return ec,p,l

def pub_keys(ec,p,l):
    """    
    公開鍵を用意する。
    変数pubが公開鍵となる。
    
    @param ec:EC
    @param p:Point
    @param l:int
    @return: s(int),pub(Point)
    """
    assert isinstance(ec,EC)
    assert isinstance(p,ec.point)
    assert isinstance(l,int)
    
    s = rand_between(1,l-1)
    pub = ec.mul(s,p)
    return s,pub

def priv_keys(ec,s,l,id_name):
    """
    秘密鍵を用意する。
    変数privが秘密鍵となる。
    @param ec:EC
    @param s:int
    @param l:int
    @param id_name:str
    @return: h1(Point),priv(Point)
    """
    assert isinstance(ec,EC)
    assert isinstance(s,int)
    assert isinstance(l,int)
    assert isinstance(id_name,str)
    
    h1 = H1(ec,l,id_name)
    priv = ec.mul(s,h1)
    return h1,priv

def enc(ec,m,pub,h1,p,l,n):
    """
    文字列mを暗号化する。
    c1,c2が暗号文。
    
    @param ec:EC
    @param m:str
    @param pub:Point
    @param h1:Point
    @param p:Point
    @param l:int
    @param n:int 2進数を表す文字列の長さを指定する引数。
    @return: c1(Point),c2(str)
    """
    assert isinstance(ec,EC)
    assert isinstance(m,str)
    assert isinstance(pub,ec.point)
    assert isinstance(h1,ec.point)
    assert isinstance(p,ec.point)
    assert isinstance(l,int)
    assert isinstance(n,int)
    
    r = rand_between(1,l-1)
    g_id = modified_weil_pairing(ec,h1,pub,l)
    
    c1 = ec.mul(r,p)
    c2 = xor(m,H2(g_id**r,n))
    return c1,c2

def dec(ec,c1,c2,priv,l,n):
    """
    暗号文(c1,c2)を復号化する。
    
    @param ec:EC
    @param c1:Point
    @param c2:str
    @param priv:Point
    @param l:int
    @param n:int 2進数を表す文字列の長さを指定する引数。
    @return: m(str)
    """
    assert isinstance(ec,EC)
    assert isinstance(c1,ec.point)
    assert isinstance(c2,str)
    assert isinstance(priv,ec.point)
    assert isinstance(l,int)    
    assert isinstance(n,int)
    
    w = modified_weil_pairing(ec,priv,c1,l)
    m = xor(c2,H2(w,n))
    return m
