from lexicalAnalyzer import *
from LL1_parser import *
import parsing_table
import ByteCodeGenerator

test = ['pdf_example.txt', 'code.txt', 'Output/dfa_min0.txt', 'Output/tokens_output0.txt', 'Output/parse_table0.txt', 'Output/stack_output0.txt', 'Output/parse_tree0.txt', 'Output/byte_code0.txt']
lexical_analyzer = LexicalAnalyzer(test[0], test[2])
lexical_analyzer.save()
tokens = lexical_analyzer.compile(test[1])
if tokens:  # no lexical errors
    f = open(test[3], 'w')
    for token in tokens:
        print(token)
        f.write(token[0])
        f.write('\n')
    parse_table, start = parsing_table.generate_parsing_table()
    print('Table:')
    print(parse_table)
    if parse_table:  # grammar is cfg
        f = open(test[4], 'w')
        print(parse_table, file=f)
        parse_tree = parse(tokens, parse_table, start, test[5])
        parse_tree.dfs(test[6])
        if parse_tree:  # no grammar errors
            byte_code_generator = ByteCodeGenerator.ByteCodeGenerator()
            byte_code_generator.annotate_parse_tree(parse_tree)
            rules = parse_tree.get_rules()
            if byte_code_generator.get_rules(parse_tree):  # no semantic errors
                bytecode = byte_code_generator.get_code(parse_tree)
                print(bytecode)
                f = open(test[7], 'w')
                print(bytecode, file=f)
