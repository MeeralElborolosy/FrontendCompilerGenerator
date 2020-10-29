from itertools import takewhile
def groupby(ls):
    d = {}
    ls = [ y[0] for y in rules ]
    initial = list(set(ls))
    for y in initial:
        print(y)
        for i in rules:
            if i.startswith(y):
                if y not in d:
                    d[y] = []
                d[y].append(i)
    return d

def prefix(x):
    return len(set(x)) == 1


starting=""
rules=[]
common=[]


s= "EXPRESSION = SIMPLE_EXPRESSION A | SIMPLE_EXPRESSION 'relop' SIMPLE_EXPRESSION"
print("\n**************")
print("INPUT :")
print("**************")
print(s)

print("\n**************")
print("OUTPUT :")
print("**************")

while(True):
    rules=[]
    common=[]
    split=s.split("=")
    starting=split[0]
    for i in split[1].split("|"):
        rules.append(i)

#logic for taking commons out
    for k, l in groupby(rules).items():
        r = [l[0] for l in takewhile(prefix, zip(*l))]
        common.append(''.join(r))
#end of taking commons
    for i in common:
        new=starting+"_2"
        print(starting+"="+i+new)
        index=[]
        for k in rules:
            if(k.startswith(i)):
                index.append(k)

        print(new+" = ",end="")
        for j in index[:-1]:
            stringtoprint=j.replace(i,"", 1)+"|"
            if stringtoprint=="|":
                print("\L","|",end="")
            else:
                print(j.replace(i,"", 1)+"|",end="")
        stringtoprint=index[-1].replace(i,"", 1)+"|"
        if stringtoprint=="|":
            print("\L","",end="")
        else:
            print(index[-1].replace(i,"", 1)+"",end="")
        print("")
    break