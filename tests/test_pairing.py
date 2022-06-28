from ibc.pairing import *

import unittest

class TestPairing(unittest.TestCase):    
    def test_miller(self):
        p = 631
        m = 5
        fq = Fq(p)
        ec = EC(fq(30),fq(34),fq)
        p = ec.point(fq(36),fq(60))
        q = ec.point(fq(121),fq(387))
        s = ec.point(fq(0),fq(36))
        qs = ec.add(q,s)
        
        f_p_qs = miller(ec,p,m,qs)
        f_p_s = miller(ec,p,m,s)
        self.assertEqual(f_p_qs,fq(103))
        self.assertEqual(f_p_s,fq(219))
        self.assertEqual(f_p_qs/f_p_s,fq(473))
        
        p_s = ec.sub(p,s)
        n_s = ec.neg(s)
        f_q_ps = miller(ec,q,m,p_s)
        f_q_s = miller(ec,q,m,n_s)
        self.assertEqual(f_q_ps,fq(284))
        self.assertEqual(f_q_s,fq(204))
        self.assertEqual(f_q_ps/f_q_s,fq(88))
        
        self.assertEqual((f_p_qs/f_p_s)/(f_q_ps/f_q_s),fq(242))

if __name__ == '__main__':
    unittest.main()        
    
