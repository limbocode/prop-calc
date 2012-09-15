#!/usr/bin/python
import unittest
from prop import Prop
class TestProp(unittest.TestCase):
    
    def setUp(self):
        self.prop = Prop()
        
    def test_mp(self):
        pass
    
    def test_hs(self):
        pass
    
    def test_find_main_op(self):
        self.assertEqual(self.prop.find_main_op("(A\\/B)->~C"),(6,'imp'))
        self.assertEqual(self.prop.find_main_op("((A*B)\\/(A*B))->(B\\/C"),(14,'imp'))
        
    def test_strip_form(self):
        self.assertEqual(self.prop.strip_form("( A \\/ B ) -> ~C"),"(A\\/B)->~C")
        self.assertEqual(self.prop.strip_form(" ( ( A \\/ B ) -> ~C ) "),"(A\\/B)->~C")
        
if __name__ == '__main__':
    unittest.main()

