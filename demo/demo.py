import os
import sys
sys.path.append("..")

from ibc.ibc import prepare,pub_keys,priv_keys,enc,dec

def randbits(n):
    """
    nビットである乱数を返す。
    
    @param n:int
    @return: str
    """
    assert isinstance(n,int)
    assert n > 0
    
    format_str = "{:0"+str(n)+"b}"

    if os.name == "posix":
        # Entropy poolを使用するためもしかしたら遅い。
        with open("/dev/random", 'rb') as f:
            s = f.read(n//2) #HACK:n//2            
    else: # os.name == "nt" or "java"
        s = os.urandom(n//2)
        
    integer = int.from_bytes(s,'big')
    b = format_str.format(integer)        
    
    return b[0:n]

def main():
    n = 20
    security_bit = 10
    
    print("[!] 共通鍵を生成中...")
    m = randbits(n)    
    print("[*] 共通鍵: {%s}"%(m))
    
    id_name = "Alice@gmail.com"
    print("[*] IDとして'%s'を使用。"%(id_name))

    low = 1 << (security_bit-1)
    high = (1 << security_bit) - 1
    ec,p,l = prepare(low,high)
    
    s,pub = pub_keys(ec,p,l)
    print("[*] 公開鍵: {%s}"%(pub))
    
    h1,priv = priv_keys(ec,s,l,id_name)
    print("[*] 秘密鍵: {%s}"%(priv))
    
    c1,c2 = enc(ec,m,pub,h1,p,l,n)
    print("[*] 暗号化された共通鍵: {%s,%s}"%(c1,c2))
    
    M = dec(ec,c1,c2,priv,l,n)
    print("[*] 復号化された共通鍵: {%s}"%(M))

    print("[?] 元の共通鍵 == 復号化された共通鍵?: ",m == M)
    
if __name__ == '__main__':
    main()
