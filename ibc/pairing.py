"""
Ref: An Introduction to Mathematical Cryptography,Chapter 6 --- (1)
"""
from .ec import EC
from .fq import Fq
from .fq2 import Fq2
from .misc import rand_between,sq_and_mul

def g_pq(ec,p,q,r):
    """
    (1) Theorem 6.41(a)
    この関数はMiller's algorithm内において使用される。
    div(g_pq) = [P] + [Q] - [P + Q] - [inf]を満たす
     関数g_pq(r)を計算、ここでinfは楕円曲線群の単位元。
    
    @param ec:EC
    @param p:Point
    @param q:Point
    @param r:Point
    @return:fq or fq2        
    """
    assert isinstance(ec,EC)
    assert p is not None and isinstance(p,ec.point)
    assert q is not None and isinstance(q,ec.point)
    assert r is not None and isinstance(r,ec.point)
        
    if(p.x == q.x and p.y == q.y): # Tangent Point
        if(p.y == 0):  # Vertical
            return r.x - p.x
        else:          # Non-Vertical Tangent
            l = (3*(p.x**2) + ec.a)/(2*p.y)
    elif(p.x == q.x): # Vertical
        return r.x - p.x
    else:             # Non-Vertical
        l = (q.y - p.y)/(q.x - p.x)
        
    numer = r.y - p.y - l*(r.x - p.x)
    denom = r.x + p.x + q.x - l*l
    return numer/denom
        
def miller(ec,p,m,r):
    """    
    (1) Theorem 6.41(b)
    div(f_p) = m[P] - [mP] - (m-1)[inf]を満たす関数f_p(r)を 
    Miller's algorithmを使用して計算。
    
    @param ec:EC
    @param p:Point
    @param m:int
    @param r:Point
    @return: fq or fq2
    """
    
    assert isinstance(ec,EC)
    assert isinstance(m,int)
    assert p is not None and isinstance(p,ec.point)
    assert r is not None and isinstance(r,ec.point)
    
    t = p
    f = 1
    bits = "{:b}".format(m)
    n = len(bits)
    
    for i in range(1,n):
        f = (f*f)*g_pq(ec,t,t,r)
        t = ec.add(t,t)
        if(bits[i] == '1'):
            f = f*g_pq(ec,t,p,r)
            t = ec.add(t,p)
    return f
    
def weil_pairing(ec,p,q,s,m):
    """
    Weil pairing e_m(P,Q) := (f_P(Q+S)/f_P(S)) / (f_Q(P-S)/f_Q(-S))
    　を計算。
    f_Pとf_QはMiller's algorithmによって返された関数。
    
    @param ec:EC
    @param p:Point
    @param q:Point
    @param s:Point
    @param m:int
    @return: fq or fq2
    """
    
    assert isinstance(ec,EC)
    assert isinstance(m,int)
    assert p is not None and isinstance(p,ec.point)
    assert q is not None and isinstance(q,ec.point)
    assert s is not None and isinstance(s,ec.point)
    
    qs = ec.add(q,s)
    ps = ec.sub(p,s)
    neg_s = ec.neg(s)

    f_p_qs = miller(ec,p,m,qs)
    f_p_s = miller(ec,p,m,s)

    f_q_ps = miller(ec,q,m,ps)
    f_q_neg_s = miller(ec,q,m,neg_s)

    numer = f_p_qs/f_p_s
    denom = f_q_ps/f_q_neg_s
    
    return numer/denom
