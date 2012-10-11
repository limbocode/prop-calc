import re

def strip(form):
    form = re.sub(' ','',form)
    depth = 0
    for i,char in enumerate(form):
        if char == '(':
            depth += 1
        if char == ')':
            depth -= 1
        if depth == 0 and i == len(form) -1 and len(form) > 1:
            return strip(form[1:-1])
        elif depth == 0:
            break         
    return form


def find_main_op(form):
    subdepth = 0
    
    try:
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
        
        if form[0] == '~':
            return (0, 'neg')
        
    except:
        pass


def split(form):
    form = strip(form)
    a = find_main_op(form)
    if not a:
        return None
    
    if a[1] == 'neg':
        return (strip(form[1:]), 'neg')
    
    
    if a[1] in ['or','imp','equiv']:
        tuple1 = (strip(form[:a[0]]), strip(form[a[0]+2:]),
                   a[1])
        
    else:
        tuple1 = (strip_form(form[:a[0]]), strip(form[a[0]+1:]), 
                   a[1])
        
    return tuple1


def confirm(forms, rule):
    wtup = rule[0]
    maintup = rule[1]
    if len(forms) != len(wtup):
        return False

    dict1 = {}

    for index,form in enumerate(forms):
        if maintup[index]:
            splitform = split(form)
            if splitform[-1] != maintup[index]:
                return False

            else:
                for m,wff in enumerate(wtup[index]):
                    if dict1.has_key(wff):
                        if dict1[wff] != splitform[m]:
                            return False
                    else:
                        dict1[wff] = splitform[m]

        else:
            stripform = strip(form)
            if dict1.has_key(wtup[index][0]):
                x = dict1[wtup[index][0]]
                if x != stripform:
                    return False
                else:
                    dict1[wtup[index][0]] = stripform

    return True

if __name__ == "__main__":

    a = ('A -> Bx','A','Bx')

    mp = ((('p','q'),('p',),('q',)),('imp',None,None))
    
    c = ('p->q','~q','~p')
    
    mt = ((('p','q'),('q'),('p')),('imp','neg','neg')) 
 
    comm = ((('p','q'),('q','p')),('or','or'))
    
    d = ('p\\/q','q\\/p')
    
    print confirm(a,mp)
    
    print confirm(c,mt)
    
    print confirm(d,comm)
    
