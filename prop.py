#!/usr/bin/python
import re
from itertools import permutations
#Has the rules of propositional calculus.
class Prop:
    def __init__(self):
        self.flagset = set()

#Rules of inference.
    def mp(self, premise1, premise2, premise3):
        """
        Checks for the correct use of Modus Ponens.
        Both A->B,A,B and A,A->B,B are valid.
        """
        return (self.__mp_one_way(premise1, premise2, premise3) or
                self.__mp_one_way(premise2, premise1, premise3))
        
    
    
    def __mp_one_way(self, premise1, premise2, conclusion): #Modus Ponens
        """
        The first formula is split up and compared to the
        other two formulas.
        """
        
        #Convert the two premises and the conclusion to a wff.
        premise1 = Wff(premise1)
        premise2 = Wff(premise2)
        conclusion = Wff(conclusion)
        
        
        #Any exception that is thrown means something is not in the right
        #place and so we return false.
        try:
            return (premise1.main_op == 'imp' and
                    premise2.string == premise1.left and
                    conclusion.string == premise1.right)
        except:
            return False
        
    
    
    def mt(self, premise1, premise2, conclusion):
        return (self.__mt_one_way(premise1, premise2, conclusion) or
                self.__mt_one_way(premise2, premise1, conclusion))
    
    def __mt_one_way(self, premise1,premise2,conclusion): # Modus Tollens
        
        premise1 = Wff(premise1)
        premise2 = Wff(premise2)
        conclusion = Wff(conclusion)
        
        try:
            return (premise1.main_op == 'imp' and
                    premise2.main_op == 'neg' and
                    conclusion.main_op == 'neg' and
                    premise1.left == conclusion.left and
                    premise1.right == premise2.left)
        except:
            return False
        
    def hs(self, premise1, premise2, conclusion):
        return (self.__hs_one_way(premise1, premise2, conclusion) or
                self.__hs_one_way(premise2, premise1, conclusion))
        
    def __hs_one_way(self, premise1,premise2,conclusion): #Hypothetical Syllogism
        """
        All three formulas are split and compared to one another.
        """        
        
        premise1 = Wff(premise1)
        premise2 = Wff(premise2)
        conclusion = Wff(conclusion)
        
        try:
            return (premise1.main_op == 'imp' and
                    premise2.main_op == 'imp' and
                    conclusion.main_op == 'imp' and
                    premise1.left == conclusion.left and
                    premise1.right == premise2.left and
                    premise2.right == conclusion.right )
            
        except:
            return False
        
    
    
        
    def simp(self, premise,conclusion): #Simplification
        """
        The first formula is split and compared to the
        second.
        """
        
        premise = Wff(premise)
        conclusion = Wff(conclusion)
        
        try:
            return (premise.main_op == 'and' and
                    (premise.left == conclusion.string or
                     premise.right == conclusion.string)
                    )
            
        except:
            return False
    
    def conj(self, premise1, premise2, conclusion): #Conjunction
        """
        Conjunction uses the simplification method to
        validate that premise1 is tuple_of_form simplification of conclusion
        and premise2 is tuple_of_form simplification of conclusion.
        """
        return self.simp(conclusion, premise1) and self.simp(conclusion, premise2)
    
    
    def dil(self, premise1,premise2,premise3,conclusion):
        boolean = False
        for permutation in permutations((premise1,premise2,premise3),3):
            boolean = self.__dil_one_way(permutation[0],permutation[1],permutation[2], conclusion)
            if boolean:
                break
        return boolean
        
    def __dil_one_way(self, premise1, premise2, premise3, conclusion): #Dilemma
        
        premise1 = Wff(premise1)
        premise2 = Wff(premise2)
        premise3 = Wff(premise3)
        conclusion = Wff(conclusion)
        
        
        return (premise1.main_op == 'imp' and
                premise2.main_op == 'imp' and
                premise3.main_op == 'or' and
                conclusion.main_op == 'or' and
                {premise3.left, premise3.right} == {premise1.left, premise2.left} and
                {conclusion.left, conclusion.right} == {premise1.right, premise2.right})
    
    def ds(self, form1, form2, form3):
        return (self.__ds_one_way(form1, form2, form3) or
                self.__ds_one_way(form2, form1, form3))
    
    
    def __ds_one_way(self, a,b,c): #Disjunctive Syllogism 
        
        a = Wff(a)
        b = Wff(b)
        c = Wff(c)
        
        try:
            return (a.main_op == 'or' and
                    b.main_op == 'neg' and
                    (a.left == b.left and
                    a.right == c.string)
                    or
                    (a.right == b.left and
                     a.left == c.string)
                    )
            
        except:
            return False
        
    def add(self, a,b): #Addition
        
        a = Wff(a)
        b = Wff(b)
        
        try:
            return (b.main_op == 'or' and
                    (a.string in b.form))
            
        except:
            return False
        
 
#Replacement Rules
    def dn(self, form1,form2): #Double Negation
        
        form1a = Wff(form1)
        form2a = Wff(form2)
        form1b = Wff(form1a.left)
        form2b = Wff(form2a.left)
        
        #The second wff is the double negation.
        if (form1a.string == form2b.left and form2a.main_op == 'neg'
            and form2b.main_op == 'neg'):
            return True
            
        #The first wff is the double negation.
        else:
            return (form2a.string == form1b.left and form1a.main_op == 'neg'
            and form1b.main_op == 'neg')
            
            
    def dup(self, form1, form2):
                
        form1 = Wff(form1)
        form2 = Wff(form2)
        
        if (form1.main_op == 'or' and form1.left == form2.string):
            return form1.left == form1.right
        
        if (form1.main_op == 'and' and form1.left == form2.string):
            return form1.left == form1.right
        
        if (form2.main_op == 'or' and form2.left == form1.string):
            return form2.left == form2.right
        
        if (form2.main_op == 'and' and form2.left == form1.string):
            return form2.left == form2.right
        
        return False
            
    def comm(self, form1, form2): #Commutation
        
        form1 = Wff(form1)
        form2 = Wff(form2)
        
        if ((form1.main_op == 'or' and form2.main_op == 'or') or
            (form1.main_op == 'and' and form2.main_op == 'and')):
            return (form1.left == form2.right and
                    form1.right == form2.left)
            
        return False
        
#        tuple_of_form = (self.find_main_op(form1)[0], self.find_main_op(form1)[1],
#             self.find_main_op(form2)[1])
#        
#        return ((tuple_of_form[1],tuple_of_form[2]) in [('or','or'),('and','and')] and 
#                 form1[tuple_of_form[0]+1:] + form1[tuple_of_form[0]] + form1[:tuple_of_form[0]] == form2)
#        
        
    def assoc(self,form1, form2): #Association
        """
        First we will decide which way the association rule is applied.
        Then we will apply it and finally we will decide if
        it is valid.
        """
        
        form1 = Wff(form1)
        form2 = Wff(form2)
        
        form1L = Wff(form1.left)
        form2R = Wff(form2.right)
        
        if (form1L.left == form2.left and form1L.right == form2R.left and
            form1.right == form2R.right):
            return ((from1L.main_op == 'or' and form1.main_op == 'or' and form2.main_op == 'or'
                    and form2R.main_op == 'or') or (from1L.main_op == 'and' 
                    and form1.main_op == 'and' and form2.main_op == 'and'
                    and form2R.main_op == 'and')
                    )
                
        tuple_of_form = self.split_form(form1)
        
        try:        
            if tuple_of_form[2] == 'or':
                return self.assocor(form1,form2)
            else:
                return self.assocand(form1,form2)
        except:
            return False
            
    def assocor(self, form1, form2):
                
                
        try:
            tuple_of_form = self.split_form(form1)
            b = self.split_form(form2)
            c = self.split_form(tuple_of_form[0])
            d = self.split_form(b[1])
            
            if (tuple_of_form[1] == d[1] and
                b[0] == c[0] and
                c[1] == d[0] and
                (tuple_of_form[2],b[2],c[2],d[2]) ==
                ('or','or','or','or')):
                
                return True
            
        except:
            pass
        
        try:
            tuple_of_form = self.split_form(form1)
            b = self.split_form(form2)
            c = self.split_form(tuple_of_form[1])
            d = self.split_form(b[0])
            
            
            if (tuple_of_form[0] == d[0] and
                b[1] == c[1] and
                c[0] == d[1] and
                (tuple_of_form[2],b[2],c[2],d[2]) ==
                ('or','or','or','or')):
                
                return True
            
        except:
            pass
        
        return False
    
    def assocand(self, form1, form2):
        
        try:
            tuple_of_form = self.split_form(form1)
            b = self.split_form(form2)
            c = self.split_form(tuple_of_form[0])
            d = self.split_form(b[1])
            
            if (tuple_of_form[1] == d[1] and
                b[0] == c[0] and
                c[1] == d[0] and
                (tuple_of_form[2],b[2],c[2],d[2]) ==
                ('and','and','and','and')):
                
                return True
            
        except:
            pass
        
        try:
            tuple_of_form = self.split_form(form1)
            b = self.split_form(form2)
            c = self.split_form(tuple_of_form[1])
            d = self.split_form(b[0])
            
            
            if (tuple_of_form[0] == d[0] and
                b[1] == c[1] and
                c[0] == d[1] and
                (tuple_of_form[2],b[2],c[2],d[2]) ==
                ('and','and','and','and')):
                
                return True
            
        except:
            pass
        
        return False
  
        
    def contra(self, form1, form2):
        return (self.__contra1(form1, form2) or
                self.__contra1(form2, form1))
            
    def __contra1(self, form1, form2): #Contraposition
        
        tuple_of_form = self.split_form(form1)
        b = self.split_form(form2)
        
        try:
            return (self.strip_form(b[0][1:]) == tuple_of_form[1] and
                    self.strip_form(b[1][1:]) == tuple_of_form[0] and
                    tuple_of_form[2] == 'imp' and
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
        tuple_of_form = split_form1
        b = split_form2
        
        try:
            return ('~' + tuple_of_form[0] == b[0] and
                     '~' + tuple_of_form[1] ==  b[1] and b[2] == 'and')
      
        except:
            return False
        
    def __demand(self, split_form1, split_form2):
        
        tuple_of_form = split_form1
        b = split_form2
        
        try:
            return ('~' + tuple_of_form[0] == b[0] and
                     '~' + tuple_of_form[1] ==  b[1] and b[2] == 'or')
      
        except:
            return False
        
        
    def be(self, form1, form2):
        try:
            return (self.__be1(form1, form2) or
                self.__be1(form2, form1))
        except:
            return False
        
    def __be1(self, form1, form2):
        tuple_of_form = self.split_form(form1)
        b = self.split_form(form2)
        c = self.split_form(b[0])
        d = self.split_form(b[1])
        
        return (tuple_of_form[2] == 'equiv' and
                b[2] == 'and' and
                c[2] == 'imp' and
                d[2] == 'imp' and
                tuple_of_form[0] == c[0] and
                tuple_of_form[0] == d[1] and
                tuple_of_form[1] == c[1] and
                tuple_of_form[1] == d[0]
                )


    def ce(self, form1, form2):
        
        try:
            return (self.__ce1(form1, form2) or
                self.__ce1(form2, form1))
        except:
            return False

    def __ce1(self, form1, form2):
        tuple_of_form = self.split_form(form1)
        b = self.split_form(form2)
        
        return (tuple_of_form[2] == 'imp' and
                b[2] == 'or' and
                '~' + tuple_of_form[0] == b[0] and
                tuple_of_form[1] == b[1])
    
        
        
    def dist(self, form1, form2):
        try:
            return (self.__dist1(form1, form2) or
                    self.__dist1(form2, form1))
        except:
            return False
        
    def __dist1(self, form1, form2):
        
        try:
            
            tuple_of_form = self.split_form(form1)
            b = self.split_form(form2)
            c = self.split_form(tuple_of_form[1])
            d = self.split_form(b[0])
            e = self.split_form(b[1])
            
            if tuple_of_form[2] == 'and':
                return self.__distand(tuple_of_form,b,c,d,e)
            else:
                return self.__distor(tuple_of_form, b, c, d, e)
            
        except:
            return False
        
    def __distand(self,tuple_of_form,b,c,d,e):
        try:     
            
            return (tuple_of_form[2] == 'and' and
                    b[2] == 'or' and
                    c[2] == 'or' and
                    d[2] == 'and' and
                    e[2] == 'and' and
                    tuple_of_form[0] == d[0] and
                    c[0] == d[1] and
                    c[1] == e[1] and
                    d[0] == e[0]
                    )
            
        except:
            return False
        
        
    def __distor(self,tuple_of_form,b,c,d,e):
        try:     
            
            return (tuple_of_form[2] == 'or' and
                    b[2] == 'and' and
                    c[2] == 'and' and
                    d[2] == 'or' and
                    e[2] == 'or' and
                    tuple_of_form[0] == d[0] and
                    c[0] == d[1] and
                    c[1] == e[1] and
                    d[0] == e[0]
                    )
            
        except:
            return False
        
        
    def exp(self, form1, form2): #Exportation
        try:
            return (self.__exp1(form1, form2) or
                    self.__exp1(form2, form1))
            
        except:
            return False
    
    def __exp1(self, form1, form2):
        try:
            tuple_of_form = self.split_form(form1)
            b = self.split_form(form2)
            c = self.split_form(tuple_of_form[0])
            d = self.split_form(b[1])

            return (tuple_of_form[2] == 'imp' and
                    b[2] == 'imp' and
                    c[2] == 'and' and
                    d[2] == 'imp' and
                    tuple_of_form[1] == d[1] and
                    b[0] == c[0] and
                    c[1] == d[0])
            
        except:
            return False
        
#Conditional proof methods and structural checks.      
    def cp(self, form1, form2, form3):
        tuple_of_form = self.split_form(form3)
        form1 = self.strip_form(form1)
        form2 = self.strip_form(form2)

        return (form1 == tuple_of_form[0] and
                form2 == tuple_of_form[1] and
                tuple_of_form[2] == 'imp')
        
    def ip(self, form1, form2, form3):
        form1 = self.strip_form(form1)
        form3 = self.strip_form(form3)
        return (self.__is_contradiction(form2) and
                (form1 == '~' + form3 or
                     form3 == '~' + form1 or
                     form1 == '~(' + form3 + ')' or
                     form3 == '~(' + form1 + ')'))
        
        
    def __is_contradiction(self,form1):
        tuple_of_form = self.split_form(form1)
        try:
            return (tuple_of_form[2] == 'and' and
                    (tuple_of_form[0] == '~' + tuple_of_form[1] or
                     tuple_of_form[1] == '~' + tuple_of_form[0] or
                     tuple_of_form[0] == '~(' + tuple_of_form[1] + ')' or
                     tuple_of_form[1] == '~(' + tuple_of_form[0] + ')'))
            
        except:
            return False
        
    def confirm_structure(self, ip, refs):
        for tuple1 in refs:
            if not len(tuple1) == 1:
                lst1 = []
                
                for tuple2 in ip:
                    # if the line number is outside the scope of 
                    # an assumption we must be cautious
                    if tuple1[0] > tuple2[1]:
                        lst1.append(tuple2)
                for ref in tuple1[1:]:
                    if self.__is_between(ref,lst1):
                        return False
        return True
                        
                                                
    def __is_between(self,ref,lst1):
        if lst1:
            for range1 in lst1:
                if (ref <= range1[1] and
                    ref >= range1[0]):
                    return True
        return False
    
    def ip_do_not_cross(self,lst1):
        lst2 = []
        for element in lst1:
            if (element[1] == 'assp' or
                element[1] == 'fs'):
                lst2.append(element[0])
            if element[1] in ('ip','cp', 'ug'):
                x = lst2.pop()
                if not element[2] == x:
                    return False
        return not bool(lst2)
        
        
        
#Predicate Logic Methods

class Pred(Prop):
    def __init__(self):
        super(Pred, self).__init__()

    def ui(self, form1, form2):
       
        try:
            dict1 = {}
            form1 = self.strip_form(form1)
            form2 = self.strip_form(form2)
            var = form1[1]
            form1 = form1[4:-1]
            for i in range(len(form1)):
                if form1[i] == var:
                    if not dict1.has_key(var):
                        dict1[var] = form2[i]
                    else:
                        return re.sub(var,dict1[var],form1) == form2
  
        except:
            return False
        
        
    def eg(self, form1, form2):
        
        try:
            dict1 = {}
            form1 = self.strip_form(form1)
            form2 = self.strip_form(form2)
            var = form2[8]
            form2 = form2[11:-1]
            for i in range(len(form2)):
                if form2[i] == var:
                    if not dict1.has_key(var):
                        dict1[var] = form1[i]
                    else:
                        return re.sub(var,dict1[var],form2) == form1
                
        except:
            return False
        
    def ei(self, form1, form2):
        try:
            dict1 = {}
            form1 = self.strip_form(form1)
            form2 = self.strip_form(form2)
            var = form1[8]
            form1 = form1[11:-1]
            for i in range(len(form1)):
                if form1[i] == var:
                    if not dict1.has_key(var):
                        dict1[var] = form2[i]
                        break
            if dict1[var] not in self.flagset and re.sub(var,dict1[var],form1) == form2:
                self.flagset.add(dict1[var])
                return True
                
        except:
            return False
    
    def ug(self, flag, form1, form2): #Universal Generalization
        """
        This method compares the flagged variable, the first 
        formula in the Universal Generalization subproof and
        the conclusion to the subproof. The flagged variable 
        is discarded if the proof is valid.
        """
        try: #Anything that goes wrong here means that something is incorrect.
            form1 = self.strip_form(form1) #Get rid of access space
            form2 = self.strip_form(form2)
            var = form2[1]
            form2 = form2[4:-1]
            bool1 = bool(re.sub(var,flag,form2) == form1)
            if bool1:
                self.flagset.discard(flag) #Once the ug subproof is complete flagged variable can be used again.
                return True
            else:
                return False
  
        except:
            return False
        
    def fs(self, flag):
        
        try:
            
            bool1 = bool(flag not in self.flagset)
            if bool1:
                self.flagset.add(flag)
                return True
            else:
                return False
            
        except:
            return False
        
        
#QN Rules

    def qn1(self, form1, form2):
        return (self.__qn1oneway(form1, form2) or
                self.__qn1oneway(form2, form1))
        

    def __qn1oneway(self, form1, form2):
        
        try:
                
            form1 = self.strip_form(form1)
            form2 = self.strip_form(form2)
            var = form1[2]
            
            return (form1[0:4] == '~('+var+')' and
                    form2[0:10] == "(\\exists" + var + ")" and
                    self.split_form('~' + form1[4:]) == self.split_form(form2[10:]))
            
        except:
            return False
        
        
    def qn2(self, form1, form2):
        try:
            return (self.__qn2oneway(form1, form2) or
                    self.__qn2oneway(form2, form1))
        except:
            return False
       
        
    def __qn2oneway(self, form1, form2):
        
        try:
            form1 = self.strip_form(form1)
            form2 = self.strip_form(form2)
            var = form2[1]
            
            
            return (form1[0:11] == '~(\\exists'+var+')' and
                    self.split_form('~('+form1[11:]+')') == self.split_form(form2[3:])
                    and
                    form2[0:3] == '('+var+')')
        except:
            return False
        
        
    def qn3(self, form1, form2):
        return (self.__qn3oneway(form1, form2) or
                self.__qn3oneway(form2, form1))
        
        
    def __qn3oneway(self, form1, form2):
        
        try:
            form1 = self.strip_form(form1)
            form2 = self.strip_form(form2)
            var = form1[2]
            
            return (form1[0:4] == '~('+var+')' and
                    form2[0:10] == '(\\exists'+var+')' and
                    self.split_form(form1[4:]) == self.split_form('~('+form2[10:]+')'))
            
        except:
            return False
        
        
    def qn4(self, form1, form2):
        return (self.__qn4oneway(form1, form2) or
                self.__qn4oneway(form2, form1))
        
        
    def __qn4oneway(self, form1, form2):
        
        try:
            form1 = self.strip_form(form1)
            form2 = self.strip_form(form2)
            var = form2[1]
            
            return (form1[0:11] == '~(\\exists'+var+')' and
                    self.split_form(form1[11:]) == self.split_form('~('+form2[3:]+')')
                    and
                    form2[0:3] == '('+var+')')
        except:
            return False
        
        
#Class that represents a well-formed formula.
class Wff:
    """
    Takes the string representation of the tuple. ("A","B","imp")
    Has left for left of main op, right for right of main op, and main_op for main_op
    The tuple form also contains these.
    """

    def __init__(self, form):
        
        #Change the the string "A -> B" to "A->B".
        self.string = self.strip_form(form)
        self.form = self.string
        
        #Find the name and index of main operator.
        tuple_of_form = self.find_main_op(self.form)
        
        #If any of the following if statements are true, the method is
        #broken out of with a return.
        
        #There is no main operator.
        if not tuple_of_form:
            self.form = (self.form,'')
            self.left = self.form[0]
            self.right = ''
            self.main_op = ''
            return
        
        #Main operator is a 'negation'. Length is 1.
        if tuple_of_form[1] == 'neg':
            self.form = (self.form[1:], 'neg')
            self.left = self.form[0]
            self.right = ''
            self.main_op = 'neg'
            return
        
        #Main operator is 'or', 'imp', or 'quiv'. All are length 2.
        if tuple_of_form[1] in ['or','imp','equiv']:
            self.form = (self.form[:tuple_of_form[0]], self.form[tuple_of_form[0]+2:],
                       tuple_of_form[1])
            self.left = self.form[0]
            self.right = self.form[1]
            self.main_op = self.form[2]
            return
            
        #Main operator is an 'and'. Length is 1.
        else:
            self.form = (self.form[:tuple_of_form[0]], self.form[tuple_of_form[0]+1:], 
                       tuple_of_form[1])
            self.left = self.form[0]
            self.right = self.form[1]
            self.main_op = self.form[2]

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
    
    def find_main_op(self, form):
        """
        Takes tuple_of_form wff and converts it to tuple_of_form tuple. 
        ie ("name of operator", index_of_operator)
        """
        
        if form[0] == '~':
            return (0, 'neg') 

        #This could be better implemented as tuple_of_form stack.
        
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


#Confirms the validity of the proof.
class Confirm:
    def __init__(self):
        pass
    
    def confirm_validity(self, file1):
        lst1,ip,refs = self.proof_to_list(file1)
        lst2 = []
        
        for element in lst1:
            lst2.append(self.test(element))
            
        return (all(lst2) and 
                self.confirm_structure(ip, refs)
                and
                self.ip_do_not_cross(lst1))


    def confirm_validity_string(self, file1):
        str1 = ("There is tuple_of_form problem with the " +
                "following lines: ")
        lst1,ip,refs = self.proof_to_list(file1)
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
        
        if not (lst1[1] == 'pr' or lst1[1] == 'assp'
                or lst1[1] == 'fs'):
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
                lst1.append(['return False','return False'])
        
        ip   = self.__ip(lst1)
        refs = self.__refs(lst1)

        
        for element in lst1:
            lst2 = self.convert2(element, lst1)
            lst2[1] = lst2[1].lower()
            lst3.append(lst2)

        return (lst3,ip,refs)

    
    def __refs(self,lst1):
        lst2 = []
        for i,element in enumerate(lst1):
            if (not isinstance(element[-1],int)
                or
                element[-3].lower() in ('cp','ip','ug')):
                
                lst2.append((i+1,))
                
            elif not isinstance(element[-2],int):
                lst2.append((i+1,element[-1]))
            else:
                lst2.append((i+1,element[-2],element[-1]))
        return lst2  
    
    def __ip(self,lst1):
        lst2 = []
        for element in lst1:
            try:
                if element[1].lower() in ('cp','ip','ug'):
                    lst2.append((element[-2],element[-1]))
            except:
                pass
        return lst2
    

    def flatten(self, x):
        result = []
        for el in x:
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
        if not len(lst1) == 2: #Not tuple_of_form premise or assumption.
            for i, x in enumerate(lst1[2:]):
                lst1[i+2] = lst2[x - 1][0]
            
        return lst1
            
        
    def prompt_for_file(self):
        filename = raw_input("Please enter the name of the file to be checked: ")
        return open(filename, 'r')
    
if __name__ == '__main__':
    a = Wff("A->B")
    b = Wff("~A")
    c = Wff("A*B")
    print a.form
    print b.form
    print c.form
    a = "A->B"
    b = "A"
    c = "B"
    prop = Prop()
    print prop.mp(a,b,c)
    print prop.mp(b,a,c)
    print prop.mp(c,a,c)
    print prop.mp(b,a,"B->C")
    b = "~B"
    c = "~A"
    print prop.mt(a,b,c)
    b = "B->C"
    c = "A->C"
    print prop.hs(a,b,c)
    print prop.hs(b,a,c)
    print prop.hs(b,c,c)
    a = "A*B"
    b = "A"
    c = "B"
    print prop.simp(a, b)
    print prop.simp(a, c)
    a = "A->B"
    b = "C->D"
    c = "A\\/C"
    d = "B\\/D"
    print prop.dil(a, b, c, c)
    print prop.dil(a, b, c, d)
    print prop.dil(b,a, c, d)
    print prop.dil(a, b, c, c)
    d = "~C"
    e = "~A"
    print prop.ds(c,d,"A")
    print prop.ds(c,d,e)
    a = "A"
    b = "B"
    c = "A\\/B"
    print prop.add(a, c)
    print prop.add(b,c)
    print prop.dn("A","~~A")
    print prop.dn("~~A","~~~~A")
    print prop.dn("~~A","A")
    print prop.dn("~A","A")
    
    a = 'A'
    b = 'A\\/A'
    c = 'A*A'
    
    print prop.dup(a,b)
    print prop.dup(a,c)
    print prop.dup(b,a)
    print prop.dup(c,"B")
    
    a = 'A\\/B'
    b = 'B\\/A'
    c = 'A*B'
    d = 'B*A'
    print prop.comm(a,b)
    print prop.comm(c,d)
    print prop.comm("A","B")
#    tuple_of_form = Prop()
##    print tuple_of_form.confirm_validity_string(file1)
##    tuple_of_form.mt("Za->(Ha*Wa)","~(Ha*Wa)","~Za")
##
##    file1 = tuple_of_form.prompt_for_file()
##    print tuple_of_form.confirm_validity(file1)
#
##    print tuple_of_form.split_form("(F::G) -> (A -> F )")
#
#    file1 = open("proofs/proof14.txt",'r')
#    print tuple_of_form.confirm_validity(file1)

    
        
        