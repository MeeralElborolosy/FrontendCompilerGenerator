from first_follow import *


epsilon = '\L'


def generate_parsing_table():
    productions, first_dic, follow_dic = controller()
    table = {}
    for p in productions:
        var = p.LHS.name
        if p.start:
            start = var
        rules = p.RHS
        for rule in rules:
            #print(rule)
            t = []
            leftmost_symbol = rule[0]
            if leftmost_symbol == epsilon:
                t = follow_dic[var]
            elif terminal(leftmost_symbol):
                t.append(leftmost_symbol)
            else:
                t = first_dic[leftmost_symbol]
            for symbol in t:
                if (var, symbol) in table:
                    print((var, symbol))
                    print(rule)
                    print('Error')
                    return None
                table[(var, symbol)] = rule
        follow_t = follow_dic[var]
        for t in follow_t:
            if (var, t) not in table:
                table[(var, t)] = ['sync']
    return table, start


def display_table(filename, table):
    f = open(filename, 'w')
    tups = table.keys()
    vars = []
    t = []
    for key in tups:
        if key[0] not in vars:
            vars.append(key[0])
        if key[1] not in t:
            t.append(key[1])
    print('\t', end='')
    print('\t', end='', file=f)
    for symbol in t:
        print(f'{symbol}\t', end='')
        print(f'{symbol}\t', end='', file=f)
    print('')
    print('', file=f)
    for var in vars:
        print(var, end='')
        f.write(var)
        for symbol in t:
            if (var, symbol) in table:
                print(table[(var, symbol)], end='')
                print(table[(var, symbol)], end='', file=f)
            else:
                print('\t', end='')
                print('\t', end='', file=f)
        print('')
        print('', file=f)
