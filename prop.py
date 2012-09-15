#!/usr/bin/python
import re

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
    a.hs("(A\\/B)->(C*D)","(C*D)->(~E*F)","(A\\/B)->(~E*F)")
    
        
    
        
        