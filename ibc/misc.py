from copy import copy
from random import randint
from .prime import is_prime

def rand_between(low,high):
    """
    low <= x <= highを満たす乱数xを返す。
    @param low:int
    @param high:int
    @return: int
    """

    return randint(low,high)

def sq_and_mul(a,e,n):
    """
    a**e (mod n)を高速に計算。
    
    @param a:int
    @param e:int
    @param n:int
    @return:int
    """
    assert isinstance(a,int)
    assert isinstance(e,int)
    assert isinstance(n,int)
    assert e > 0
    assert n > 1
    
    b = "{:b}".format(e)
    t = len(b)
    r = a
    for i in range(1,t):
        r = r*r % n
        if(b[i] == '1'):
            r = r*a % n
    return r            

def sq_and_mul_fq(a,e):
    """
    sq_and_mulと同じ計算をするが、この関数では引数aがFq或いはFq2。
    
    @param a:fq or fq2
    @param e:int
    @return: fq or fq2 
    """
    assert a.name() == "fq" or a.name() == "fq2"
    assert isinstance(e,int)
    
    b = "{:b}".format(e)
    t = len(b)
    r = copy(a)
    
    for i in range(1,t):
        r *= r
        if(b[i] == '1'):
            r *= a
    return r            

def inv(a,p):
    """
    1/a (mod p)を計算。
    フェルマーの小定理を使って計算していることに注意、
    つまり 1/a = a**(p - 2) (mod p).
    
    @param a:int
    @param p:int
    @return:int 
    """
    assert isinstance(a,int)
    assert isinstance(p,int)
    #assert is_prime(p) HACK: assertを切らないと、ここで時間がかかりすぎる。
    assert a%p != 0
    
    if a < 0:# aが負の場合、正数にまず変換。
        return sq_and_mul(a%p,p-2,p)
    else:
        return sq_and_mul(a,p-2,p)
