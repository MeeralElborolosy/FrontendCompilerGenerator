# #example for direct left recursion
# gram = {"A":["Aa","Ab","c","d"]
# }
import re
#example for indirect left recursion
gram = {
    "METHOD_BODY":["STATEMENT_LIST"],
    "STATEMENT_LIST":["STATEMENT","STATEMENT_LIST STATEMENT"],
    "STATEMENT":["DECLARATION","IF","WHILE","ASSIGNMENT"],
    "DECLARATION":["PRIMITIVE_TYPE 'id' ';'"],
    "PRIMITIVE_TYPE":["'INT'","'FLOAT'"],
    "IF":["'if' '(' EXPRESSION ')' '{' STATEMENT '}' 'else' '{' STATEMENT '}'"],
    "WHILE": ["'while' '(' EXPRESSION ')' '{' STATEMENT '}'"],
    "ASSIGNMENT":["'id' '=' EXPRESSION ';'"],
    "EXPRESSION":["SIMPLE_EXPRESSION","SIMPLE_EXPRESSION 'relop' SIMPLE_EXPRESSION"],
    "SIMPLE_EXPRESSION":["TERM","SIGN TERM","SIMPLE_EXPRESSION 'addop' TERM"],
    "TERM" : ["FACTOR" , "TERM 'mulop' FACTOR"],
    "FACTOR":["'id'","'num'","'(' EXPRESSION ')'"],
    "SIGN" : ["'+'","'-'"]

}

def removeDirectLR(gramA, A):
    """gramA is dictonary"""
    temp = gramA[A]
    tempCr = []
    tempInCr = []
    for i in temp:
        if i[0] == A:
            #tempInCr.append(i[1:])
            tempInCr.append(i[1:]+[A+"_2"])
        else:
			#tempCr.append(i)
            tempCr.append(i+[A+"_2"])
    tempInCr.append(["\L"])
    gramA[A] = tempCr
    gramA[A+"_2"] = tempInCr

    return gramA


def checkForIndirect(gramA, a, ai):
    if ai not in gramA:
        return False
    if a == ai:
        return True
    for i in gramA[ai]:
        if i[0] == ai:
            return False
        if i[0] in gramA:
            return checkForIndirect(gramA, a, i[0])
    return False

def rep(gramA, A):
    temp = gramA[A]
    newTemp = []
    for i in temp:
        if checkForIndirect(gramA, A, i[0]):
            t = []
            for k in gramA[i[0]]:
                t=[]
                t+=k
                t+=i[1:]
                newTemp.append(t)
        else:
            newTemp.append(i)
    gramA[A] = newTemp
    return gramA

def rem(gram):
    c = 1
    conv = {}
    gramA = {}
    revconv = {}
    for j in gram:
        conv[j] = "A"+str(c)
        gramA["A"+str(c)] = []
        c+=1



    for i in gram:

            check = ""
            check2=[]
            for k in gram[i]:
                temp = []
                if re.match('\+',k)==True:
                    check=k.split("+")
                    check2.append(check[0])
                    for a in range (1,len(check)-1):
                        check2.append("+")
                        check2.append(check[a+1])
                elif re.match('\*',k)==True:
                    check=k.split("*")
                    check2.append(check[0])
                    for a in range(1, len(check) - 1):
                        check2.append("*")
                        check2.append(check[a + 1])
                elif re.match('-',k)==True:
                    check=k.split("-")
                    check2.append(check[0])
                    for a in range(1, len(check) - 1):
                        check2.append("-")
                        check2.append(check[a + 1])
                check=k.split(" ")
                for b in range(0, len(check)):
                    if check[b] in conv:
                        temp.append(conv[check[b]])
                    else:
                        temp.append(check[b])

                gramA[conv[i]].append(temp)

    for i in range(c-1,0,-1):
        ai = "A"+str(i)
        for j in range(0,i):
            aj = gramA[ai][0][0]
            if ai!=aj :
                if aj in gramA and checkForIndirect(gramA,ai,aj):
                   gramA = rep(gramA, ai)

    for i in range(1,c):
        ai = "A"+str(i)
        for j in gramA[ai]:
            if ai==j[0]:
                gramA = removeDirectLR(gramA, ai)
                break

    op = {}
    for i in gramA:
        a = str(i)
        for j in conv:
            a = a.replace(conv[j], j)
        revconv[i] = a


    for i in gramA:
        l = []

        for j in gramA[i]:
            k = ""
            for m in j:
                if m in revconv:
                    k=k+m.replace(m,revconv[m])
                    k=k+" "
                else:
                    k=k+m
                    k=k+" "
            l.append(k)
        op[revconv[i]] = l

    return op

result = rem(gram)

for i in result:
    print(f'{i}->{result[i]}')