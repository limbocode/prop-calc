#!/usr/bin/python
import re
from pyparsing import Literal,Word,ZeroOrMore,Forward,nums,oneOf,Group,srange

class Prop():
    def __init__(self):
        pass

    def mp(self, form1, form2, form3): #Modus Ponens

        a = self.split_form(form1)
        
        
        try:
            return (a[2] == 'imp' and
                    self.strip_form(form2) == a[0] and
                    self.strip_form(form3) == a[1])
        except:
            return False

    
    def mt(self, form1, form2, form3 ): # Modus Tollens
        
        a = self.split_form(form1)
        
        strip2 = self.strip_form(form2)
        strip3 = self.strip_form(form3)
        
        try:
            return (a[2] == 'imp' and
                    strip2[0] == '~' and
                    strip3[0] == '~' and
                    a[0] == self.strip_form(strip3[1:]) and
                    a[1] == self.strip_form(strip2[1:])
                    )
        except:
            return False
        
        
        
    def hs(self, form1, form2, form3): #Hypothetical Syllogism
        
        a = self.split_form(form1)
        b = self.split_form(form2)
        c = self.split_form(form3)
        
        try:
            return (a[2] == 'imp' and
                    b[2] == 'imp' and
                    c[2] == 'imp' and
                    a[0] == c[0] and
                    a[1] == b[0] and
                    b[1] == c[1])
            
        except:
            return False
        
    def simp(self, form1, form2): #Simplification
        
        a = self.split_form(form1)
        strip2 = self.strip_form(form2)
        
        try:
            return (a[2] == 'and' and
                    (a[0] == strip2 or
                     a[1] == strip2)
                    )
            
        except:
            return False
    
    def conj(self, form1, form2, form3): #Conjunction
        return self.simp(form3,form1) and self.simp(form3,form2)
    
    def ds(self, form1, form2, form3): #Disjunctive Syllogism
        
        a = self.split_form(form1)
        strip2 = self.strip_form(form2)
        strip3 = self.strip_form(form3)
        
        try:
            return (a[2] == 'or' and
                    strip2[0] == '~' and
                    ((strip3 == a[0] and
                    a[1] == self.strip_form(strip2[1:]))
                    or
                    (strip3 == a[1] and
                    a[0] == self.strip_form(strip2[1:])))
                    )
            
        except:
            return False
        
        
    def add(self, form1, form2): #Addition
        
        a = self.split_form(form2)
        strip1 = self.strip_form(form1)

        try:
            return (a[2] == 'or' and
                    (a[0] == strip1 or a[1] == strip1))
            
        except:
            return False
        
        
    def split_form(self, form):
        """
        Splits a formula up into a tuple where the first element is the
        first part of the formula before the main operator, the second
        element is the second part of the formula after the main operator,
        and the third is the name of the main operator.
        """
        
        form = self.strip_form(form)
        a = self.find_main_op(form)
        
        #checks for None
        if not a:
            return None
        
        if a[1] == 'neg':
            return (self.strip_form(form[1:]), 'neg')
        
        
        if a[1] in ['or','imp','equiv']:
            tuple1 = (self.strip_form(form[:a[0]]), self.strip_form(form[a[0]+2:]),
                       a[1])
            
        else:
            tuple1 = (self.strip_form(form[:a[0]]), self.strip_form(form[a[0]+1:]), 
                       a[1])
            
        return tuple1
    
    def dil(self, form1, form2, form3, form4): #Dilemma
        tup1 = self.split_form(form1)
        tup2 = self.split_form(form2)
        tup3 = self.split_form(form3)
        tup4 = self.split_form(form4)

        return ((tup1[2], tup2[2], tup3[2], tup4[2]) == ('imp','imp','or','or')
                and {tup3[0],tup3[1]} == {tup1[0],tup2[0]}
                and {tup4[0],tup4[1]} == {tup1[1],tup2[1]})



    def dn(self, form1, form2): #Double Negation
        return ((form1[:2] == '~~' and 
                self.strip_form(form1[2:]) == self.strip_form(form2))
                or
                (form2[:2] == '~~' and 
                self.strip_form(form2[2:]) == self.strip_form(form1))
                )
            
            
    def comm(self, form1, form2): #Commutation
        
        a = (self.find_main_op(form1)[0], self.find_main_op(form1)[1],
             self.find_main_op(form2)[1])
        
        return ((a[1],a[2]) in [('or','or'),('and','and')] and 
                 form1[a[0]+1:] + form1[a[0]] + form1[:a[0]] == form2)
        
        
    def assoc(self,form1, form2): #Association
        """
        First we will decide which way the association rule is applied.
        Then we will apply it and finally we will decide if
        it is valid.
        """
                
        a = self.split_form(form1)
        
        try:        
            if a[2] == 'or':
                return self.assocor(form1,form2)
            else:
                return self.assocand(form1,form2)
        except:
            return False
            
    def assocor(self, form1, form2):
                
                
        try:
            a = self.split_form(form1)
            b = self.split_form(form2)
            c = self.split_form(a[0])
            d = self.split_form(b[1])
            
            if (a[1] == d[1] and
                b[0] == c[0] and
                c[1] == d[0] and
                (a[2],b[2],c[2],d[2]) ==
                ('or','or','or','or')):
                
                return True
            
        except:
            pass
        
        try:
            a = self.split_form(form1)
            b = self.split_form(form2)
            c = self.split_form(a[1])
            d = self.split_form(b[0])
            
            
            if (a[0] == d[0] and
                b[1] == c[1] and
                c[0] == d[1] and
                (a[2],b[2],c[2],d[2]) ==
                ('or','or','or','or')):
                
                return True
            
        except:
            pass
        
        return False
    
    def assocand(self, form1, form2):
        
        try:
            a = self.split_form(form1)
            b = self.split_form(form2)
            c = self.split_form(a[0])
            d = self.split_form(b[1])
            
            if (a[1] == d[1] and
                b[0] == c[0] and
                c[1] == d[0] and
                (a[2],b[2],c[2],d[2]) ==
                ('and','and','and','and')):
                
                return True
            
        except:
            pass
        
        try:
            a = self.split_form(form1)
            b = self.split_form(form2)
            c = self.split_form(a[1])
            d = self.split_form(b[0])
            
            
            if (a[0] == d[0] and
                b[1] == c[1] and
                c[0] == d[1] and
                (a[2],b[2],c[2],d[2]) ==
                ('and','and','and','and')):
                
                return True
            
        except:
            pass
        
        return False


    def dup(self, form1, form2):
        return (self.__dup1(form1, form2) or
                self.__dup1(form2, form1))

    def __dup1(self, form1, form2): #Duplication
        a = self.split_form(form2)
        
        return (self.conj(form1, form1, form2) or(
                self.add(form1, form2) and
                a[0] == a[1]))
        
        
        
    def contra(self, form1, form2):
        return (self.__contra1(form1, form2) or
                self.__contra1(form2, form1))
            
    def __contra1(self, form1, form2): #Contraposition
        
        a = self.split_form(form1)
        b = self.split_form(form2)
        
        try:
            return (self.strip_form(b[0][1:]) == a[1] and
                    self.strip_form(b[1][1:]) == a[0] and
                    a[2] == 'imp' and
                    b[2] == 'imp')

        except:
            return False
            
            
            
    def dem(self, form1, form2):
        
        return (self.__dem1(form1, form2) or
                self.__dem1(form2, form1))
            
    def __dem1(self, form1, form2): #DeMorgan's
        try:
            split_form1 = self.split_form(form1)
            split_form2 = self.split_form(form2)
            if split_form1[1] != 'neg':
                return False 
            split_form1 = self.split_form(split_form1[0])
            if split_form1[2] == 'and':
                return self.__demand(split_form1, split_form2)
            else:
                return self.__demor(split_form1, split_form2)
            
        except:
            return False
        
    def __demor(self, split_form1, split_form2):
        a = split_form1
        b = split_form2
        
        try:
            return ('~' + a[0] == b[0] and
                     '~' + a[1] ==  b[1] and b[2] == 'and')
      
        except:
            return False
        
    def __demand(self, split_form1, split_form2):
        
        a = split_form1
        b = split_form2
        
        try:
            return ('~' + a[0] == b[0] and
                     '~' + a[1] ==  b[1] and b[2] == 'or')
      
        except:
            return False
        
        
        
    def be(self, form1, form2):
        try:
            return (self.__be1(form1, form2) or
                self.__be1(form2, form1))
        except:
            return False
        
    def __be1(self, form1, form2):
        a = self.split_form(form1)
        b = self.split_form(form2)
        c = self.split_form(b[0])
        d = self.split_form(b[1])
        
        return (a[2] == 'equiv' and
                b[2] == 'and' and
                c[2] == 'imp' and
                d[2] == 'imp' and
                a[0] == c[0] and
                a[0] == d[1] and
                a[1] == c[1] and
                a[1] == d[0]
                )


    def ce(self, form1, form2):
        
        try:
            return (self.__ce1(form1, form2) or
                self.__ce1(form2, form1))
        except:
            return False

    def __ce1(self, form1, form2):
        a = self.split_form(form1)
        b = self.split_form(form2)
        
        return (a[2] == 'imp' and
                b[2] == 'or' and
                '~' + a[0] == b[0] and
                a[1] == b[1])
    
    
    
    def exp(self, form1, form2):
        try:
            return (self.__exp1(form1, form2) or
                    self.__exp1(form2, form1))
            
        except:
            return False
    
    def __exp1(self, form1, form2):
        try:
            a = self.split_form(form1)
            b = self.split_form(form2)
            c = self.split_form(a[0])
            d = self.split_form(b[1])

            return (a[2] == 'imp' and
                    b[2] == 'imp' and
                    c[2] == 'and' and
                    d[2] == 'imp' and
                    a[1] == d[1] and
                    b[0] == c[0] and
                    c[1] == d[0])
            
        except:
            return False
        
        
    def dist(self, form1, form2):
        try:
            return (self.__dist1(form1, form2) or
                    self.__dist1(form2, form1))
        except:
            return False
        
    def __dist1(self, form1, form2):
        
        try:
            
            a = self.split_form(form1)
            b = self.split_form(form2)
            c = self.split_form(a[1])
            d = self.split_form(b[0])
            e = self.split_form(b[1])
            
            if a[2] == 'and':
                return self.__distand(a,b,c,d,e)
            else:
                return self.__distor(a, b, c, d, e)
            
        except:
            return False
        
    def __distand(self,a,b,c,d,e):
        try:     
            
            return (a[2] == 'and' and
                    b[2] == 'or' and
                    c[2] == 'or' and
                    d[2] == 'and' and
                    e[2] == 'and' and
                    a[0] == d[0] and
                    c[0] == d[1] and
                    c[1] == e[1] and
                    d[0] == e[0]
                    )
            
        except:
            return False
        
        
    def __distor(self,a,b,c,d,e):
        try:     
            
            return (a[2] == 'or' and
                    b[2] == 'and' and
                    c[2] == 'and' and
                    d[2] == 'or' and
                    e[2] == 'or' and
                    a[0] == d[0] and
                    c[0] == d[1] and
                    c[1] == e[1] and
                    d[0] == e[0]
                    )
            
        except:
            return False
        
        
    
    
    def find_main_op(self, form):
        """
        Takes a stripped formula as an argument. Not used
        directly. Used as a helper function to split_form.
        """
        subdepth = 0
        
        try:
            if form[0] == '~' and (len(form[1:]) == 1 or 
                                   self.strip_form(form[1:]) == form[2:-1]):
                return (0, 'neg')
            
        except:
            pass
                
#        if form[0] == '~' and self.strip_form(form[1:]) == form[2:-1]:
#            return (0, 'neg')
        
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
        form = re.sub(' ','',form)
        depth = 0
        for i,char in enumerate(form):
            if char == '(':
                depth += 1
            if char == ')':
                depth -= 1
            if depth == 0 and i == len(form) -1 and len(form) > 1:
                return self.strip_form(form[1:-1])
            elif depth == 0:
                break         
        return form 
    
    def syntax(self):
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
        expr = self.syntax()
        form1 = self.strip_form(form1)
        try:
            result = ''.join(list(expr.parseString(form1)))
        except:
            result = None
        return result == form1
        
        
    def confirm_validity(self, file1):        
        lst1 = self.proof_to_list(file1)
        lst2 = []
        for element in lst1:
            lst2.append(self.test(element))
        return all(lst2)
                    

    def confirm_validity_string(self, file1):
        str1 = ("There is a problem with the " +
                "following lines: ")
        lst1 = self.proof_to_list(file1)
        lst2 = []
        for element in lst1:
            lst2.append(self.test(element))
        if all(lst2):
            return "Proof is valid."
        else:
            for i,elem in enumerate(lst2):
                if elem == False:
                    str1 += str(i+1) + ", "
            return str1[:-2]

    def test(self, lst1):        
        lst1[1]
        lst2 = []
        
        if lst1[0] == 'return False':
            return False
        
        if lst1[1] != 'pr':
            str1 = "self." + lst1[1] + "(*lst2)"
            for x in lst1[2:]:
                lst2.append(x)
            lst2.append(lst1[0])
            try:
                return eval(str1)
            except:
                return False
        
        return True
        
        
        
    def proof_to_list(self, file1):
        lst1 = []
        lst3 = []
        for line in file1:
            line = line.rstrip()
            line = re.sub(r"\t+","\t",line)
            line = re.sub(r"\.\t+","\t",line)
            lst2 = line.split("\t")
            if len(lst2) == 3:
                lst2 = lst2[1:]
                lst2 = self.convert1(lst2)
                lst1.append(lst2)
            elif re.sub(r"\s+","",lst2[0]):
                print lst2
                print re.sub(r"\s+","",lst2[0])
                lst1.append(['return False','return False'])
        
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
            
        
    def prompt_for_file(self):
        filename = raw_input("Please enter the name of the file to be checked: ")
        return open(filename, 'r')
    
if __name__ == '__main__':
    a = Prop()
#    a.dil("((A\\/B)->C)->(D\\/F)","(F::G)->(A->F)",
#                                      "((A\\/B)->C)\\/(F::G)","(D\\/F)\\/(A->F)")
    file1 = open("proofs/proof6.txt",'r')
#    file1 = a.prompt_for_file()
    print a.confirm_validity_string(file1)
#    a.mt("Za->(Ha*Wa)","~(Ha*Wa)","~Za")
#
#    file1 = a.prompt_for_file()
#    print a.confirm_validity(file1)

#    print a.split_form("(F::G) -> (A -> F )")

    
        
        