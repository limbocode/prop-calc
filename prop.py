#!/usr/bin/python
import re
from pyparsing import Literal,Word,ZeroOrMore,Forward,nums,oneOf,Group,srange

class Prop():
    def __init__(self):
        pass

    def mp(self, form1, form2, form3): #Modus Ponens
        """
        Takes three arguments, the formula (A->B), the implication (A),
        and the conclusion (B), This method identifies the main
        operator in the formula and compares the strings to the implication
        and conclusion. It does not check to see if the formula
        itself is valid. This is done by the confirm_wff method.
        """
        a = self.find_main_op(form1)
        if a[1] != 'imp':
            return False
        
        str1 = self.strip_form(form1[:a[0]])
        str2 = self.strip_form(form1[a[0]+2:])
        
        return self.strip_form(form2) == str1 and self.strip_form(form3) == str2
        
        
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
        depth = 0
        for i,char in enumerate(form):
            if char == '(':
                depth += 1
            if char == ')':
                depth -= 1
            if depth == 0 and i == len(form) -1:
                return self.strip_form(form[1:-1])
            elif depth == 0:
                break         
        return form 
    
    def syntax(self):
        """
        Defines the syntax of a well formed formula. This method is used
        by confirm_wff.
        """
        op = oneOf( '\\/ -> * ::')
        lpar  = Literal('(')
        rpar  = Literal( ')' )
        statement = Word(srange('[A-Z]'),srange('[a-z]'))
        expr = Forward()
        atom = statement | lpar + expr + rpar
        expr << atom + ZeroOrMore( op + expr )
        expr.setResultsName("expr")
        return expr
    
    def confirm_wff(self, form1):
        """
        Confims that the formula is indeed a well formed formula.
        """
        expr = self.syntax()
        form1 = self.strip_form(form1)
        try:
            result = ''.join(list(expr.parseString(form1)))
        except:
            result = None
        return result == form1
        
        
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
        
        lst1 = self.proof_to_list(file1)
        lst2 = []
        for element in lst1:
            lst2.append(self.test(element))
        return all(lst2)


    def test(self, lst1):
        """
        The order of the list should be conclusion, reason, and referenced
        formulas.
        """
        
        lst1[1]
        lst2 = []
        
        if lst1[1] != 'pr':
            str1 = "self." + lst1[1] + "(*lst2)"
            for x in lst1[2:]:
                lst2.append(x)
            lst2.append(lst1[0])
            return eval(str1)
        
        return True
        
        
        
    def proof_to_list(self, file1):
        """
        Returns a list that is ready to be used with confirm_validity.
        The order of the list returned should be reason, referenced formulas,
        and conclusion. This will make it easy to use with the
        other methods.
        """
        lst1 = []
        lst3 = []
        for line in file1:
            line = line.rstrip()
            line = re.sub(r"\t+","\t",line)
            line = re.sub(r"\.\t+","\t",line)
            lst2 = line.split("\t")
            lst2 = lst2[1:]
            lst2 = self.convert1(lst2)
            lst1.append(lst2)
        
        for element in lst1:
            lst2 = self.convert2(element, lst1)
            lst2[1] = lst2[1].lower()
            lst3.append(lst2)

        return lst3
    
    
    def flatten(self, x):

        result = []
        for el in x:
            #if isinstance(el, (list, tuple)):
            if hasattr(el, "__iter__") and not isinstance(el, basestring):
                result.extend(self.flatten(el))
            else:
                result.append(el)
        return result
        
    
    def convert1(self, lst1):
        
        lst1[1] = lst1[1].split(' ')
        try:
            lst1[1][1] = lst1[1][1].split(',')
        except:
            pass
        
        lst1 = self.flatten(lst1)
        
        if len(lst1) > 2:
            for i, x in enumerate(lst1[2:]):
                lst1[i + 2] = int(x)
                
        return lst1
        
    def convert2(self, lst1, lst2):
        if not len(lst1) == 2:
            for i, x in enumerate(lst1[2:]):
                lst1[i+2] = lst2[x - 1][0]
            
        return lst1
#        print lst1
#        print lst2
            
    
    def reason_to_list(self, reason):
        
        reason = reason.lower()
        
        if reason == 'pr':
            return ['pr']
        
        if reason in ['simp']:
            lst1 = reason.split(' ')
            lst1[1] = int(lst1[1])
            return lst1
        
        if reason in ['mp','conj']:
            pass
            
            
    def ref_to_string(self):
        """
        Takes the references of in the reasoning and returns
        the actual strings.
        """
            
            
        
        
    def prompt_for_file(self):
        """
        Asks for a file to confirm the validity of and gives this
        file to confirm_validity.
        """
    
if __name__ == '__main__':
    a = Prop()
#    a.dil("((A\\/B)->C)->(D\\/F)","(F::G)->(A->F)",
#                                      "((A\\/B)->C)\\/(F::G)","(D\\/F)\\/(A->F)")
    file1 = open("proof.txt",'r')
    print a.confirm_validity(file1)
#    a.confirm_validity(file1)

    
        
        