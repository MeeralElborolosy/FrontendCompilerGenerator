import re


class ReadingInputFile:
    def __init__(self, file_name):
        self.file_name = file_name
        self.RE = []
        self.RD = []
        self.keywords = []
        self.punctuations = []

    def read_file(self):
        f = open(self.file_name, "r")
        lines = f.readlines()
        for line in lines:
            data = line.split()
            if data[1] == '=':
                self.regular_definition(line)
                pass
            elif "{" in data[0]:
                self.keyword(line)
                pass
            elif "[" in data[0]:
                self.punctuation(line)
                pass
            else:  # if it's a colon
                self.regular_expression(line)  # going to next module
                pass

    def regular_definition(self, this_rd):
        # to next module
        name = this_rd.split("=")[0].strip()
        x = re.findall(r'\w\s*-\s*\w',this_rd)
        expressions = []
        if x:
            for i in range(0, len(x)):
                point = this_rd.find(x[i])
                start = point
                end = point + len(x[i]) - 1
                s = this_rd[start]
                e = this_rd[end]
                rng = ord(e)-ord(s)+1
                exp = ""
                exp = exp+'('
                if s.isalpha() and e.isalpha():
                    for j in range(0,rng):
                        exp = exp+chr(ord(s)+j)
                        if j != (rng-1):
                            exp = exp+'|'
                    exp = exp+')'
                    expressions.append(exp)
                elif s.isdigit() and e.isdigit():
                    for j in range(0,rng):
                        exp = exp+chr(ord(s)+j)
                        if j != (rng-1):
                            exp = exp+'|'
                    exp = exp+')'
                    expressions.append(exp)

            c = 0
            for i in range(0,len(this_rd)):
                if this_rd[i] == "|":
                    c = c+1
            expr = ""
            if c != 0:
                for i in range(0,c+1):
                    expr = expr+expressions[i]
                    if i != c:
                        expr = expr+'|'
            else:
                expr = expressions.pop()
            rd = [name, expr]
            self.RD.append(rd)
        else:
            part = this_rd.split("=", 1)
            i = 0
            check = ""
            rem = ''
            ch = part[1].strip()
            while i < len(ch) and ch[i].isalpha():
                check = check+ch[i]
                i = i+1
            if len(check) != len(ch):
                rem = ch.split(check)[1]
            res1 = any(check in sublist for sublist in self.RD)
            if res1:
                place = [(i, sublist.index(check)) for i, sublist in enumerate(self.RD) if check in sublist]
                expr = self.RD[place[0][0]][1] + rem
            else:
                expr = ch
            rd = [name, expr]
            self.RD.append(rd)
        pass

    def keyword(self, this_keyword):
        data = this_keyword.split()
        for i in range(0, len(data)):
            if "{" in data[i]:
                data[i] = data[i][1:]
            elif "}" in data[i]:
                data[i] = data[i].rstrip('}')
            if data[i]:
                self.keywords.append(data[i])

    def punctuation(self, this_punctuation):
        data = this_punctuation.split()
        for i in range(0, len(data)):
            if "[" in data[i]:
                data[i] = data[i][1:]
            if "]" in data[i]:
                data[i] = data[i].rstrip(']')
            if data[i]:
                j = 0
                while j < len(data[i]):
                    if data[i][j] == '\\':
                        self.punctuations.append(data[i][j] + data[i][j+1])
                        j = j + 1
                    else:
                        self.punctuations.append(data[i][j])
                    j = j + 1

        print(self.punctuations)

    def regular_expression(self, this_re):# to next  module
        print(this_re)
        rhs = this_re.split(':',1)[1]
        rhs = rhs.strip()
        name = this_re.split(':')[0].strip()
        expr = ""
        lamda = ""
        i=0
        print(rhs)
        print(name)
        while i < len(rhs):
            old_exp = expr
            ch = ""
            while i < len(rhs) and (rhs[i] == ' ' or rhs[i] == '\t'):
                i = i+1
            if i < len(rhs) and (rhs[i] == "(" or rhs[i] == ")" or rhs[i] == "*" or rhs[i] == "|" or rhs[i] == "+"):
                expr = expr+rhs[i]
                i = i+1
            elif i < len(rhs) and rhs[i] == '\\':
                lamda = lamda + rhs[i]
                i = i + 1
                if i < len(rhs) and rhs[i] == "L" :
                        lamda = lamda + rhs[i]
                        i = i + 1
                while i < len(rhs) and (rhs[i] == ' ' or rhs[i] == '\t'):
                        i = i + 1
                while i < len(rhs) and rhs[i].isalpha()==False :
                    if rhs[i] == ' ' or rhs[i] == '\t':
                        i = i+1
                    else:
                        lamda = lamda + rhs[i]
                        i = i+1
                expr = expr+lamda
            if i < len(rhs)and rhs[i] == '.':
                expr = expr + '\\'
                expr = expr + rhs[i]
                i = i+1
            while i < len(rhs) and rhs[i].isalpha():
                ch = ch+rhs[i]
                i = i+1
            if ch:
                res1 = any(ch in sublist for sublist in self.RD)
                if res1:
                    place = [(j, sublist.index(ch)) for j, sublist in enumerate(self.RD) if ch in sublist]
                    expr = expr+ '(' + self.RD[place[0][0]][1] + ')'
                else:
                    expr = expr+ch
            if expr == old_exp:
                expr = expr + rhs[i]
                i = i + 1

        print(expr)
        re = [name, expr]
        self.RE.append(re)


#read_file = ReadingInputFile('Case1/lexical.txt')
#read_file.read_file()
#print(read_file.RE)
#print(read_file.RD)
#print(read_file.keywords)
#print(read_file.punctuations)
