from math import sqrt 
from random import randint,getrandbits

def exp_mod(a,k,m):
    """
    繰り返し自乗法によりa**k(mod m)を計算。
    
    @param a:int
    @param k:int
    @param m:int
    @return: int
    """
    assert isinstance(a,int)
    assert isinstance(k,int)
    assert isinstance(m,int)
    assert k >= 0
    assert m >= 0
    
    if(m == 0): return a**k
    elif(k == 0): return 1
    
    b = 1
    while(k>=1):
        if(k%2 == 1):
            b = (a*b)%m
        a = (a*a)%m
        k = k//2
    return b

def miller_rabin_test(n,a):
    """
    Miller-Rabin判定法を使用してnが合成数か否かを判定。
    "合成数"であるか否かを判定することに注意。
    つまり、nが合成数ならTrue,そうでないならFalseを返す
    [注意]
    Falseの場合は素数 "かもしれない"(確率的である) ことを示唆している。

    @param n:int
    @param a:int
    @return:int    
    """
    assert isinstance(n,int)
    assert isinstance(a,int)
    assert n > 0
    assert a > 0
            
    if(n&1 == 0):# 偶数の場合
        return True

    k = 0
    q = n - 1
    while(q&1 == 0): # qが偶数の場合
        q //= 2
        k += 1
    val = exp_mod(a,q,n)
    
    if((val-1)%n !=0 and (val+1)%n !=0):
        for i in range(k):
            val *= val
            if((val+1)%n != 0):
                continue
            else:
                return False
        return True
    else:
        return False

def is_prime(n,tries=100):
    """
    Miller-Rabin判定法を使って、確率的にnが素数か否かを判定,素数ならTrue、そうでないならFalseを返す。
    triesが大きいほど判定信頼度は、増すが時間がかかる。

    @param n:int >= 2
    @param tries:int > 0
    @return: bool
    """
    assert isinstance(n,int)
    assert isinstance(tries,int)
    assert n >= 2
    assert tries > 0
        
    if(n == 2):# 自明な素数
        return True
    elif(n&1 == 0):# 2以外の偶数なら明らかにFalse
        return False

    for _ in range(tries):
        a = randint(1,n-1)  # 1からtest_number-1までの整数からランダムに一つ選択
        if(miller_rabin_test(n,a)):
            return False
    return True

def generate_n_bits_prime(n,tries=100):
    """
    nビットに近い素数を生成し返す。
    Miller-Rabin法を使用しているため確実に素数かどうかはわからない。

    @param n:int >= 2
    @param tries:int > 0
    @return: int    
    """
    assert isinstance(n,int)
    assert isinstance(tries,int)
    assert n >= 2
    assert tries > 0    
    
    prime_candidate = getrandbits(n) # 長さがbitsである乱数を生成
    prime_candidate |= 1 # 奇数に調整
    prime_candidate |= (1<<(n-1)) | (1<<(n-2))#prime_candidateが小さすぎる場合を防ぐ
    
    while(not is_prime(prime_candidate,tries)):# 素数となるまで繰り返す
        prime_candidate += 2

    return prime_candidate

def rand_prime(low,high):
    """
    low <= p < highを満たす素数pをランダムに選び、返す。
    [注意]
    low,highが近くすぎる場合は素数が存在しないため、ある程度離れている必要あり。
    
    @param low:int
    @param high:int
    @return: int
    """    
    assert isinstance(low,int)
    assert isinstance(high,int)
    assert low >= 2
    assert high >= 2
    assert high - low > 50 # HACK:
    
    while True:
        prime = randint(low,high)        
        if is_prime(prime):
            return prime    

    return prime
