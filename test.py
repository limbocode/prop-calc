#!/usr/bin/python
import unittest
from prop import Prop
class TestProp(unittest.TestCase):
    
    def setUp(self):
        self.prop = Prop()
        self.expr = self.prop.syntax()    
        
        
#Tests for the Rules of Inference
    
    def test_mp(self):
        self.assertTrue(self.prop.mp("(A\\/B)->~C","A\\/B","~C"))
        self.assertTrue(self.prop.mp("A\\/B","(A\\/B)->~C","~C"))
        self.assertTrue(self.prop.mp("(A\\/B)->~C","A\\/B","~C"))
        self.assertFalse(self.prop.mp("(A\\/B)->C","A\\/B","~C"))
        self.assertFalse(self.prop.mp("A","A\\/B","~C"))
        
    def test_mt(self):
        self.assertTrue(self.prop.mt("Za->(Ha*Wa)","~(Ha*Wa)","~Za"))
        self.assertFalse(self.prop.mt("Za->(Ha*Wa)","Ha*Wa","~Za"))
        self.assertFalse(self.prop.mt("Za","Ha*Wa","~Za"))
        
    def test_hs(self):
        self.assertTrue(self.prop.hs("(A\\/B)->(C*D)","(C*D)->(~E*F)","(A\\/B)->(~E*F)"))
        self.assertTrue(self.prop.hs("(A\\/B)->(D)","(D)->(~E*F)","(A\\/B)->(~E*F)"))
        self.assertTrue(self.prop.hs("(A\\/B)->D","(D)->(~E*F)","(A\\/B)->(~E*F)"))
        self.assertFalse(self.prop.hs("(A\\/B)*(D)","(D)->(~E*F)","(A\\/B)->(~E*F)"))
        self.assertFalse(self.prop.hs("(A)","(D)->(~E*F)","(A\\/B)->(~E*F)"))
        
    def test_simp(self):
        self.assertFalse(self.prop.simp("(A\\/B)->~C", "~C"))
        self.assertFalse(self.prop.simp("(A\\/B)*~C", "C"))
        self.assertTrue(self.prop.simp("(A\\/B)*~C", "~C"))
        
    def test_conj(self):
        self.assertTrue(self.prop.conj("A\\/B","~(C->D)","(A\\/B)*~(C->D)"))
        
    def test_dil(self):
        self.assertTrue(self.prop.dil("((A\\/B)->C)->(D\\/F)","(F::G)->(A->F)",
                                      "((A\\/B)->C)\\/(F::G)","(D\\/F)\\/(A->F)"))
        self.assertTrue(self.prop.dil("(F::G)->(A->F)","((A\\/B)->C)->(D\\/F)",
                                      "((A\\/B)->C)\\/(F::G)","(D\\/F)\\/(A->F)"))
        
    def test_ds(self):
        self.assertTrue(self.prop.ds("(~A\\/(B->C))\\/~D","~(~A\\/(B->C))","~D"))
        self.assertTrue(self.prop.ds("(~A\\/(B->C))\\/~D","~(~D)","(~A\\/(B->C))"))
        self.assertFalse(self.prop.ds("(~A\\/(B->C))\\/~D","(~D)","(~A\\/(B->C))"))
        self.assertFalse(self.prop.ds("A","(~D)","(~A\\/(B->C))"))
        self.assertTrue(self.prop.ds("~(B\\/C)\\/~(A*D)", "~~(A*D)", "~(B\\/C)"))
        self.assertTrue(self.prop.ds("~(B\\/C)\\/~(A\\/D)", "~~(A\\/D)", "~(B\\/C)"))
         
    def test_add(self):
        self.assertTrue(self.prop.add("(A->B)","(A->B)\\/C"))
        self.assertTrue(self.prop.add("((((A\\/B)\\/C)\\/D)\\/E)\\/F","(((((A\\/B)\\/C)\\/D)\\/E)\\/F)\\/G"))
        self.assertFalse(self.prop.add("(B)","(A)"))
        
        
#Tests for the Replacement Rules
    def test_dn(self):
        self.assertTrue(self.prop.dn("A","~~A"))
        self.assertTrue(self.prop.dn("~~A","A"))
        self.assertTrue(self.prop.dn("~~(A->(B*C))","A->(B*C)"))
        
    def test_dup(self):
        self.assertTrue(self.prop.dup("A","A*A"))
        self.assertTrue(self.prop.dup("A","A\\/A"))
        self.assertTrue(self.prop.dup("A*A","A"))
        self.assertTrue(self.prop.dup("A\\/A","A"))
        
    def test_comm(self):
        self.assertTrue(self.prop.comm("E*F","F*E"))
        self.assertTrue(self.prop.comm("E*(F->G)","(F->G)*E"))
        
    def test_assoc(self):
        self.assertTrue(self.prop.assoc("(A*B)*C","A*(B*C)"))
        self.assertTrue(self.prop.assoc("A*(B*C)","(A*B)*C"))
        self.assertTrue(self.prop.assoc("(A*B)*(C->D)","A*(B*(C->D))"))
        self.assertTrue(self.prop.assoc("(A*B)*(C*D)","A*(B*(C*D))"))
        self.assertTrue(self.prop.assoc("(A\\/B)\\/C","A\\/(B\\/C)"))
        self.assertFalse(self.prop.assoc("",""))

    def test_assocand(self):
        self.assertTrue(self.prop.assocand("(A*B)*C","A*(B*C)"))
        self.assertTrue(self.prop.assocand("A*(B*C)","(A*B)*C"))
        self.assertTrue(self.prop.assocand("(A*B)*(C->D)","A*(B*(C->D))"))

    def test_assocor(self):
        self.assertTrue(self.prop.assoc("(A\\/B)\\/C","A\\/(B\\/C)"))
        self.assertFalse(self.prop.assoc("(A\\/B)*C","A\\/(B\\/C)"))      
        
    def test_contra(self):
        self.assertTrue(self.prop.contra("A->B","~B->~A"))
        self.assertTrue(self.prop.contra("~B->~A","A->B"))
        self.assertFalse(self.prop.contra("",""))
 
    def test_dem(self):
        self.assertTrue(self.prop.dem("~(A*B)","~A\\/~B"))
        self.assertTrue(self.prop.dem("~(A\\/B)","~A*~B"))
        self.assertTrue(self.prop.dem("~A\\/~B","~(A*B)"))
        self.assertTrue(self.prop.dem("~A*~B","~(A\\/B)"))
        self.assertFalse(self.prop.dem("",""))
        
    def test_be(self):
        self.assertTrue(self.prop.be("A::B","((A->B)*(B->A))"))
        self.assertTrue(self.prop.be("((A->B)*(B->A))","A::B"))
        self.assertFalse(self.prop.be("",""))

    def test_ce(self):
        self.assertTrue(self.prop.ce("A->B","~A\\/B"))
        self.assertTrue(self.prop.ce("~A\\/B","A->B"))
        self.assertFalse(self.prop.ce("",""))
        
    def test_dist(self):
        self.assertTrue(self.prop.dist("A*(B\\/C)","(A*B)\\/(A*C)"))
        self.assertTrue(self.prop.dist("Ax*(By\\/Cz)","(Ax*By)\\/(Ax*Cz)"))
        self.assertTrue(self.prop.dist("(A*B)\\/(A*C)","A*(B\\/C)"))
        self.assertTrue(self.prop.dist("A\\/(B*C)","(A\\/B)*(A\\/C)"))
        self.assertFalse(self.prop.dist("",""))
        
    def test_exp(self):
        self.assertTrue(self.prop.exp("(A*B)->C","A->(B->C)"))
        self.assertTrue(self.prop.exp("A->(B->C)","(A*B)->C"))
        self.assertFalse(self.prop.exp("",""))
        
        
        
#Predicate Logic Methods

    def test_ui(self):
        self.assertTrue(self.prop.ui("(x)(Cx->Mx)","Ca->Ma"))
        self.assertTrue(self.prop.ui("(x)(Mx->Vx)","Ma->Va"))
        self.assertTrue(self.prop.ui("( x )( Mx -> Vx )","Ma->Va"))
        self.assertFalse(self.prop.ui("",""))
        
    def test_eg(self):
        self.assertTrue(self.prop.eg("Oa*Ea*Na","(\exists x)(Ox*Ex*Nx)"))
        
    def test_ei(self):
        self.assertTrue(self.prop.ei("(\exists x)(Ox*Ex*Nx)","Oa*Ea*Na"))
        
    def test_ug(self):
        self.assertTrue(self.prop.ug("Ca->Ma","(x)(Cx->Mx)"))
        
#Tests for conditional and indirect proofs.
    def test_cp(self):
        self.assertTrue(self.prop.cp("A","F->~E","A->(F->~E)"))
        self.assertTrue(self.prop.cp("Ax","Fy->~Ez","Ax->(Fy->~Ez)"))
    
    def test_ip(self):
        self.assertTrue(self.prop.ip("E","I*~I","~E"))
        self.assertTrue(self.prop.ip("E","~I*~~I","~E"))
        self.assertTrue(self.prop.ip("E","(I)*~I","~E"))
        self.assertTrue(self.prop.ip("E","(A->B)*~(A->B)","~E"))
        self.assertTrue(self.prop.ip("E","~(A->B)*~~(A->B)","~E"))
        self.assertTrue(self.prop.ip("Ex","~(Ax->By)*~~(Ax->By)","~Ex"))
        self.assertFalse(self.prop.ip("E","~~(A->B)*~~(A->B)","~E"))
        
        
#Tests for utilities
    def test_split_form(self):
        self.assertEqual(self.prop.split_form("(F::G)->(A->F)"), ("F::G","A->F","imp"))
        self.assertEqual(self.prop.split_form("(F::G)->(A ->F)"), ("F::G","A->F","imp"))
        self.assertEqual(self.prop.split_form("(F::G) -> (A -> F )"), ("F::G","A->F","imp"))
        self.assertEqual(self.prop.split_form("~(A*B) -> C"), ("~(A*B)","C","imp"))
        self.assertEqual(self.prop.split_form("~(A\\/B) \\/ C"), ("~(A\\/B)","C","or"))
        self.assertEqual(self.prop.split_form("~(B\\/C)\\/~(A*D)"), ("~(B\\/C)","~(A*D)","or"))
        self.assertEqual(self.prop.split_form("~(A*B)"), ("A*B",'neg'))
        self.assertTrue(self.prop.split_form("A") == None)
    
    def test_find_main_op(self):
        self.assertEqual(self.prop.find_main_op("~(A*B)->C"), (6,'imp'))
        self.assertEqual(self.prop.find_main_op("(A\\/B)->~C"),(6,'imp'))
        self.assertEqual(self.prop.find_main_op("((A*B)\\/(A*B))->(B\\/C"),(14,'imp'))
        self.assertEqual(self.prop.find_main_op("(A\\/B)*~C"),(6,'and'))
        self.assertEqual(self.prop.find_main_op("(A\\/B)\\/~C"),(6,'or'))
        self.assertEqual(self.prop.find_main_op("(A\\/B)::~C"),(6,'equiv'))
        self.assertEqual(self.prop.find_main_op("~(A\\/D)"),(0,'neg'))
        self.assertEqual(self.prop.find_main_op("~~(A\\/D)"),(0,'neg'))
        self.assertTrue(self.prop.find_main_op("A") == None)
        self.assertTrue(self.prop.find_main_op("") == None)
        
    def test_strip_form(self):
        self.assertEqual(self.prop.strip_form("( A \\/ B ) -> ~C"),"(A\\/B)->~C")
        self.assertEqual(self.prop.strip_form(" ( ( A \\/ B ) -> ~C ) "),"(A\\/B)->~C")
        self.assertEqual(self.prop.strip_form(" ( ( A \\/ B )) "),"A\\/B")
        self.assertEqual(self.prop.strip_form("(F::G) -> (A -> F )"),"(F::G)->(A->F)")
        self.assertEqual(self.prop.strip_form("( x )(Cx ->Mx)"),"(x)(Cx->Mx)")
        
    def test_confirm_structure(self):
        self.assertTrue(self.prop.confirm_structure([(7,16),(6,17),(5,18),(4,19)],
                                                    [(1,),(2,),(3,),(4,),(5,),(6,),(7,),(8,1,5),
                                                     (9,4),(10,8,9),(11,10),(12,2,11),
                                                     (13,7,12),(14,13),(15,3,6),(16,14,15),
                                                     (17,),(18,),(19,),(20,)]))
        
        
    
    def test_confirm_validity(self):
        self.assertTrue(self.prop.confirm_validity(open("./proofs/proof.txt",'r')))
        self.assertTrue(self.prop.confirm_validity(open("./proofs/proof2.txt",'r')))
        self.assertTrue(self.prop.confirm_validity(open("./proofs/proof3.txt",'r')))
        self.assertFalse(self.prop.confirm_validity(open("./proofs/proof4.txt",'r')))
        self.assertFalse(self.prop.confirm_validity(open("./proofs/proof5.txt",'r')))
        self.assertFalse(self.prop.confirm_validity(open("./proofs/proof6.txt",'r')))
        self.assertTrue(self.prop.confirm_validity(open("./proofs/proof7.txt",'r')))
        self.assertTrue(self.prop.confirm_validity(open("./proofs/proof8.txt",'r')))
        self.assertTrue(self.prop.confirm_validity(open("./proofs/proof9.txt",'r')))
        
    def test_confirm_validity_string(self):
        self.assertEqual(self.prop.confirm_validity_string(open("./proofs/proof6.txt",'r')),
                         "There is a problem with the following lines: 5, 6")
        print self.prop.confirm_validity(open("./proofs/proof7.txt",'r'))
        
        
        
    
    
    def test_confirm_wff(self):
        self.assertTrue(self.prop.confirm_wff("A\\/B"))
        self.assertTrue(self.prop.confirm_wff("(A\\/B)"))
        self.assertTrue(self.prop.confirm_wff("(A\\/B) -> C"))
        self.assertFalse(self.prop.confirm_wff("A\\/B)"))
    
if __name__ == '__main__':
    unittest.main()

