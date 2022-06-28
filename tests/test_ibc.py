from ibc.ibc import *
from ibc.fq import Fq

from random import randint

import unittest

alpha = '!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'

def _random_str(n):
    s = ""
    for i in range(n):
        s += alpha[randint(0,93)]
    return s

class TestIBC(unittest.TestCase):    
    def test_ibc(self):
        for i in range(5): # 何回か繰り返す
            
            id_len = randint(1,100)
            id_name = _random_str(id_len)
            
            n = randint(2,1000)
            format_str = "{:0"+str(n)+"b}"            
            
            #id_name = "Alice@gmail.com"
            #n = 256

            key = randint(2,1000) 
            m = (format_str.format(key))[0:n]
            self.assertEqual(len(m),n)
            
            ec,p,l = prepare(10**20,10**30)
            s,pub = pub_keys(ec,p,l)
            h1,priv = priv_keys(ec,s,l,id_name)
            c1,c2 = enc(ec,m,pub,h1,p,l,n)
            M = dec(ec,c1,c2,priv,l,n)
            
            self.assertEqual(m,M)

if __name__ == '__main__':
    unittest.main()        
    

