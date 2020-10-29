def read_semantic():
    file = open("java_modified_cfg_semantics.txt", "r")
    semantic_rules = {}
    for rule in file:
        string = ""
        production = []
        part = rule.split()
        key = part[0]
        if "{" not in part:
            for i in range(2, len(part)):
                production.append(part[i].strip("'"))

        elif "{" in part:
            i = part.index("{") + 1
            j = part.index("}")
            for k in range(i, j):
                string += part[k]
                string += " "
            for index in range(2, i-1):
                production.append(part[index].strip("'"))
            for index in range(j+1, len(part)):
                production.append(part[index].strip("'"))
        string = string.replace('\\n', '\n')
        string = string.replace('\\t', '\t')
        semantic_rules[(key, tuple(production))] = string
    return semantic_rules


"""
semantic_rules = read_semantic()
for key in semantic_rules.keys():
    print(f'{key}: \n{semantic_rules[key]}')
test1 = semantic_rules[('PRIMITIVE_TYPE', ("'float'",))]
exec(test1)
test2 = semantic_rules[('DECLARATION', ('PRIMITIVE_TYPE', "'id'", "';'",))]
exec(test2)
num_lexval = 15
test7 = semantic_rules[('FACTOR', ("'num'",))]
print(test7)
exec(test7)
test6 = semantic_rules[('TERM', ('FACTOR',))]
print(test6)
exec(test6)
test5 = semantic_rules[('SIMPLE_EXPRESSION', ('TERM',))]
print(test5)
exec(test5)
test4 = semantic_rules[('EXPRESSION', ('SIMPLE_EXPRESSION',))]
print(test4)
exec(test4)
id_lex_val = 'x'
test3 = semantic_rules[('ASSIGNMENT', ("'id'", "'assign'", 'EXPRESSION', "';'"))]
exec(test3)
"""
