#!/usr/bin/python
import re
from pyparsing import Literal,Word,ZeroOrMore,Forward,nums,oneOf,Group,srange

class Prop():
    def __init__(self):
        pass

    def mp(self, form1, form2, form3): #Modus Ponens
        """
        Takes three arguments, the implication (A), the conclusion (B), 
        and the formula (A -> B). This method identifies the main
        operator in the formula and compares the strings to the implication
        and conclusion. It does not check to see if the formula
        itself is valid. This is done by the is_valid_formula method.
        """
        a = self.find_main_op(form3)
        if a[1] != 'imp':
            return False
        
        str1 = self.strip_form(form3[:a[0]])
        str2 = self.strip_form(form3[a[0]+2:])
        
        return self.strip_form(form1) == str1 and self.strip_form(form2) == str2
        
        
    def hs(self, form1, form2, form3):
        """
        Takes the first two formulas and compares it to the third.
        """ 
        a = self.find_main_op(form1)
        b = self.find_main_op(form2)
        c = self.find_main_op(form3)
        
        if (a[1],b[1],c[1] ) != ('imp','imp','imp'):
            return False
        
        str1 = self.strip_form(form1[:a[0]])
        str2 = self.strip_form(form1[a[0]+2:])
        str3 = self.strip_form(form2[:b[0]])
        str4 = self.strip_form(form2[b[0]+2:])
        str5 = self.strip_form(form3[:c[0]])
        str6 = self.strip_form(form3[c[0]+2:])
        
        return str1 == str5 and str2 == str3 and str4 == str6
        
    def simp(self, form1, form2):
        """
        Confirms that form2 can be derived from form1 by simplification.
        """
        a = self.find_main_op(form1)
        if a[1] != 'and':
            return False
        
        str1 = self.strip_form(form1[:a[0]])
        str2 = self.strip_form(form1[a[0]+1:])
        
        return self.strip_form(form2) == str1 or self.strip_form(form2) == str2
    
    def conj(self, form1, form2, form3):
        """
        Conjunction is a very closely related to simplification. If form1 and
        form2 can both be derived from form3 through simplification, then
        it is a valid conjunction.
        """
        return self.simp(form3,form1) and self.simp(form3,form2)
    
    def ds(self, form1, form2, form3):
        """
        Disjunction.
        """
        a = self.find_main_op(form1)
        if a[1] != 'or':
            return False
        
        if form2[0] != '~':
            return False
        
        str1 = self.strip_form(form1[:a[0]])
        str2 = self.strip_form(form1[a[0]+2:])
        str3 = self.strip_form(form2[1:])
        str4 = self.strip_form(form3)
        
        if str3 != str1:
            if str3 != str2:
                return False
            else:
                return str1 == str4
        
        if str3 != str2:
            if str3 != str1:
                return False
            else:
                return str2 == str4
            
        return False
        
        
    def add(self, form1, form2):
        
        a = self.find_main_op(form2)
        
        if a[1] != 'or':
            return False
        
        lst1 = []
        
        lst1.append(self.strip_form(form2[:a[0]]))
        lst1.append(self.strip_form(form2[a[0]+2:]))
        
        return self.strip_form(form1) in lst1
        
        
    def split_form(self, form):
        """
        Takes as an argument a formula and splits this formula
        into a tuple based on the main operator with the first
        two elements of the tuple being the two parts of the
        formula and the last two elements being the main operator
        name and its index.
        """    
        a = self.find_main_op(self.strip_form(form))
        if a[1] in ['or','imp','equiv']:
            tuple1 = (self.strip_form(form[:a[0]]), self.strip_form(form[a[0]+2:]),
                       a[0], a[1])
            
        else:
            tuple1 = (self.strip_form(form[:a[0]]), self.strip_form(form[a[0]+1:]), 
                       a[0], a[1])
            
        return tuple1
    
    def dil(self, form1, form2, form3, form4):
        """
        After we have exhausted all of the ways this can be False all we have is True.
        """
        tup1 = self.split_form(form1)
        tup2 = self.split_form(form2)
        tup3 = self.split_form(form3)
        tup4 = self.split_form(form4)
        
        #Checks that the main operators of each formula are correct.
        if (tup1[3], tup2[3], tup3[3], tup4[3]) != ('imp','imp','or','or'):
            return False
        
        
        if {tup3[0],tup3[1]} != {tup1[0],tup2[0]}:
            return False
        
        if {tup4[0],tup4[1]} != {tup1[1],tup2[1]}:
            return False
        

        return True
    
    
    def find_main_op(self, form):
        """
        Finds the main operator of a formula (assuming no extra parentheses
         and returns its index and type.
        """
        subdepth = 0
        for i, char in enumerate(form):
            if char == '(':
                subdepth += 1
            if char == ')':
                subdepth -= 1
            if char == '*' and subdepth == 0:
                return (i, 'and')
            if char == '\\' and subdepth == 0:
                if form[i+1] == '/':
                    return (i, 'or')
            if char == ':' and subdepth == 0:
                if form[i+1]  == ':':
                    return (i, 'equiv')
            if char == '-' and subdepth == 0:
                if form[i+1] == '>':
                    return (i, 'imp')
            
                     

    def strip_form(self, form):        
        """
        Strips the formula of any whitespace and excessive parentheses.
        """
        form = re.sub(' ','',form)
        if form[0] == '(' and form[-1] == ')':
            form = form[1:-1]
        return form 
    
    def synatx(self):
        """
        Defines the syntax of a well formed formula. This method is used
        by confirm_wff.
        """
        op = oneOf( '\/ -> * ::')
        lpar  = Literal('(') .suppress()
        rpar  = Literal( ')' ).suppress()
        statement = Word(srange('[A-Z]'),srange('[a-z]'))
        expr = Forward()
        atom = statement | Group( lpar + expr + rpar )
        expr << atom + ZeroOrMore( op + expr )
        return expr
    
    def confirm_wff(self, form1):
        """
        Confims that the formula is indeed a well formed formula.
        """
        expr = self.synatx()
        try:
            expr.parseString(form1)
            return True
        except:
            return False
        
        
    def confirm_validity(self, file1):
        """
        Takes a file iterates through each line of the file calling the
        appropriate methods when necessary. The first step is to strip the 
        formulas.  The next is to check that each
        formula is in the correct form. If not return the incorrect 
        formula with the appropriate error message. The next step is to check
        each line of the proof and that each of the rules of propositional
        calculus has been applied correctly. If not return the mistake. If
        this method runs through each line of the file skipping and blank 
        lines, then it will return that the proof is valid.
        """
        
if __name__ == '__main__':
    a = Prop()
    a.dil("((A\\/B)->C)->(D\\/F)","(F::G)->(A->F)",
                                      "((A\\/B)->C)\\/(F::G)","(D\\/F)\\/(A->F)")
    
        
    
        
        