#!/usr/bin/python
import unittest
from prop import Prop
class TestProp(unittest.TestCase):
    
    def setUp(self):
        self.prop = Prop()

#    def test_confirm_wff(self):
#        self.assertTrue(self.prop.confirm_wff("A\\/B"))
#        self.assertTrue(self.prop.confirm_wff("(A\\/B)"))
#        self.assertTrue(self.prop.confirm_wff("(A\\/B) -> C"))
#        self.assertFalse(self.prop.confirm_wff("A\\/B)"))

    def test_mp(self):
        self.assertTrue(self.prop.mp("A\\/B","~C","(A\\/B)->~C"))
        self.assertTrue(self.prop.mp("A\\/B","~C","(A\\/B)->~C"))
        self.assertFalse(self.prop.mp("A\\/B","~C","(A\\/B)->C"))
        
    def test_conj(self):
        self.assertTrue(self.prop.conj("A\\/B","~(C->D)","(A\\/B)*~(C->D)"))
    
    def test_hs(self):
        self.assertTrue(self.prop.hs("(A\\/B)->(C*D)","(C*D)->(~E*F)","(A\\/B)->(~E*F)"))
    
    def test_find_main_op(self):
        self.assertEqual(self.prop.find_main_op("(A\\/B)->~C"),(6,'imp'))
        self.assertEqual(self.prop.find_main_op("((A*B)\\/(A*B))->(B\\/C"),(14,'imp'))
        self.assertEqual(self.prop.find_main_op("(A\\/B)*~C"),(6,'and'))
        self.assertEqual(self.prop.find_main_op("(A\\/B)\\/~C"),(6,'or'))
        self.assertEqual(self.prop.find_main_op("(A\\/B)::~C"),(6,'equiv'))
        
    def test_strip_form(self):
        self.assertEqual(self.prop.strip_form("( A \\/ B ) -> ~C"),"(A\\/B)->~C")
        self.assertEqual(self.prop.strip_form(" ( ( A \\/ B ) -> ~C ) "),"(A\\/B)->~C")
        
    def test_simp(self):
        self.assertFalse(self.prop.simp("(A\\/B)->~C", "~C"))
        self.assertFalse(self.prop.simp("(A\\/B)*~C", "C"))
        self.assertTrue(self.prop.simp("(A\\/B)*~C", "~C"))
        
if __name__ == '__main__':
    unittest.main()

