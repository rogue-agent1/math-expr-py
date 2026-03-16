import math,operator
OPS={'+':operator.add,'-':operator.sub,'*':operator.mul,'/':operator.truediv,'^':operator.pow}
PREC={'+':1,'-':1,'*':2,'/':2,'^':3}
FUNCS={'sin':math.sin,'cos':math.cos,'tan':math.tan,'sqrt':math.sqrt,'abs':abs,'log':math.log,'exp':math.exp}
def tokenize(expr):
    tokens=[]; i=0
    while i<len(expr):
        if expr[i].isspace(): i+=1
        elif expr[i] in '()+-*/^,': tokens.append(expr[i]); i+=1
        elif expr[i].isdigit() or expr[i]=='.':
            j=i
            while j<len(expr) and (expr[j].isdigit() or expr[j]=='.'): j+=1
            tokens.append(float(expr[i:j])); i=j
        elif expr[i].isalpha():
            j=i
            while j<len(expr) and expr[j].isalpha(): j+=1
            word=expr[i:j]
            tokens.append(('FUNC',word) if word in FUNCS else ('VAR',word))
            i=j
        else: i+=1
    return tokens
def evaluate(expr,variables=None):
    variables=variables or {}; tokens=tokenize(expr)
    pos=[0]
    def parse_expr(min_prec=0):
        left=parse_atom()
        while pos[0]<len(tokens) and isinstance(tokens[pos[0]],str) and tokens[pos[0]] in PREC and PREC[tokens[pos[0]]]>min_prec:
            op=tokens[pos[0]]; pos[0]+=1
            right=parse_expr(PREC[op])
            left=OPS[op](left,right)
        return left
    def parse_atom():
        t=tokens[pos[0]]
        if isinstance(t,(int,float)): pos[0]+=1; return t
        if isinstance(t,tuple):
            if t[0]=='FUNC':
                pos[0]+=1; assert tokens[pos[0]]=='('; pos[0]+=1
                arg=parse_expr(); assert tokens[pos[0]]==')'; pos[0]+=1
                return FUNCS[t[1]](arg)
            if t[0]=='VAR': pos[0]+=1; return variables.get(t[1],0)
        if t=='(': pos[0]+=1; val=parse_expr(); pos[0]+=1; return val
        if t=='-': pos[0]+=1; return -parse_atom()
        pos[0]+=1; return 0
    return parse_expr()
if __name__=="__main__":
    assert evaluate("2+3*4")==14
    assert evaluate("(2+3)*4")==20
    assert abs(evaluate("sin(3.14159/2)")-1)<0.001
    assert evaluate("sqrt(16)")==4
    assert evaluate("2^10")==1024
    assert evaluate("x*2+1",{'x':5})==11
    print(f"2+3*4 = {evaluate('2+3*4')}")
    print(f"sin(pi/2) = {evaluate('sin(3.14159/2)'):.4f}")
    print("All tests passed!")
