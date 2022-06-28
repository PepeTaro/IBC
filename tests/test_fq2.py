from ibc.fq2 import *
from random import randint

import unittest

class TestFq2(unittest.TestCase):
    def test_trace(self):
        q = 111347
        fq = Fq(q)
        fq2 = Fq2(fq)        
        a = fq2(376,138)
        b = fq2(384,76)

        self.assertEqual(a**q,fq2(138,376))
        self.assertEqual(b**q,fq2(76,384))
        self.assertEqual(a.trace(),fq(-(376 + 138)))
        self.assertEqual(b.trace(),fq(-(384 + 76)))
            
    def test_mul(self):
        q = 889673
        fq = Fq(q)
        fq2 = Fq2(fq)
        
        n = 100
        for i in range(n):
            a = randint(0,q-1)
            b = randint(0,q-1)
            c = randint(0,q-1)
            d = randint(0,q-1)
            x = fq2(a,b)
            y = fq2(c,d)
            
            A = b*(b - 2*a)
            B = a*(a - 2*b)
            C = (b*d - a*d - b*c)
            D = (a*c - a*d - b*c)
            self.assertEqual(x**2,fq2(A,B))
            self.assertEqual(x*y,fq2(C,D))
            self.assertEqual(x**2,x*x)
            self.assertEqual(x**3,x*x*x)
            self.assertEqual(x**4,x*x*x*x)

if __name__ == '__main__':
    unittest.main()
        
