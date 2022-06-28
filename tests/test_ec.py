from ibc.ec import *

import unittest

class TestEC(unittest.TestCase):    
    def test_ec(self):
        fq = Fq(13)
        ec = EC(fq(3),fq(8),fq)
        p = ec.point(fq(9),fq(7))
        q = ec.point(fq(1),fq(8))
        pq = ec.add(p,q)
        p2 = ec.add(p,p)
        self.assertEqual(pq.x,2)
        self.assertEqual(pq.y,10)
        self.assertEqual(p2.x,9)
        self.assertEqual(p2.y,6)
                         
        fq = Fq(73)
        ec = EC(fq(8),fq(7),fq)
        p = ec.point(fq(32),fq(53))
        q = ec.point(fq(39),fq(17))
        r = ec.double_and_add(11,p)        
        self.assertEqual(r,q)
    
if __name__ == '__main__':
    unittest.main()        
