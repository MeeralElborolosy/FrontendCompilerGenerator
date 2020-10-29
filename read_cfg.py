class LHS(object):
    def __init__(self, name):
        self.first = []
        self.follow = []
        self.name = name

    def display(self):
        print(f'First({self.name}) = {self.first}')
        print(f'Follow({self.name}) = {self.follow}')


class string(object):
    def __init__(self, name, start):
        self.RHS = []   # list of lists
        self.LHS = LHS(name)
        self.start = start  # True or false

    def display(self):
        print(f'{self.LHS.name} -> {self.RHS}')
        self.LHS.display()


def remove_LF(productions):
    for p in productions:
        if len(p.RHS) == 1:
            continue
        idx = 0
        similar = True
        found = False
        factor = []
        while similar and idx < len(p.RHS[0]):
            factor.append(p.RHS[0][idx])
            for rule in p.RHS[1:]:
                if idx >= len(rule):
                    similar = False
                    break
                if rule[idx] != factor[idx]:
                    similar = False
                    break
            if similar:
                found = True
            idx = idx + 1
        if found:
            new_s = string(p.LHS.name + '_2', False)
            for f in factor:
                for i in range(0, len(p.RHS)):
                    p.RHS[i].remove(f)
                    if len(p.RHS[i]) == 0:
                        p.RHS[i] = ['\L']
            new_s.RHS = p.RHS[:]
            factor.append(new_s.LHS.name)
            p.RHS = []
            p.RHS.append(factor)
            productions.append(new_s)
    return productions


def remove_LR(productions):
    for p in productions:
        var = p.LHS.name
        for rule in p.RHS:
            if rule[0] == var:
                p.RHS.remove(rule)
                name = var + '_2'
                new_s = string(name, False)
                new_s.RHS = [rule[1:]]
                new_s.RHS[0].append(name)
                new_s.RHS.append(['\L'])
                for r in p.RHS:
                    r.append(name)
                productions.append(new_s)
                break
    return productions


def save_to_list():
    f = open("java_cfg.txt", "r")
    Lines = []
    line_index = 0
    last_index = 0
    for line in f:
        if line[0] == '#':
            Lines.append([line[2:]])
            line_index = line_index + 1
            last_index += 1
        else:
            Lines[last_index-1].append(line)
            line_index = line_index + 1
    final_Lines = []
    for line in Lines:
        if len(line) > 1:
            this_str = ""
            for part in line:
                this_str += part.strip('\n')
                this_str += " "
            final_Lines.append([this_str])
        else:
            this_str = line[0]
            final_Lines.append([this_str.strip('\n')])
    f.close()
    return final_Lines


def get_productions(Lines):
    productions = []
    line_counter = 0
    for line in Lines:
        sides = line[0].split('=', 1)
        sides[0] = sides[0].strip()
        if line_counter == 0:
            string_instance = string(sides[0], True)
        else:
            string_instance = string(sides[0], False)
        rhs = sides[1]
        try:
            ored = rhs.split("|")
            string_instance.RHS = []
            for part in ored:
                production = part.split()
                for i in range(0, len(production)):
                    if "'" in production[i]:
                        production[i] = production[i].strip("'")
                string_instance.RHS.append(production)
        except:
            symbols = rhs.strip()
            string_instance.RHS = []
            string_instance.RHS.append(symbols)
        productions.append(string_instance)
        line_counter = line_counter + 1
    productions = remove_LF(productions)
    productions = remove_LR(productions)
    for i in range(0, len(productions)):
        print(f'{productions[i].LHS.name} -> {productions[i].RHS}')
    return productions

lines = save_to_list()
op = get_productions(lines)