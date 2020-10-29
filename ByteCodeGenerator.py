import read_semantic_rules
from LL1_parser import *


class ByteCodeGenerator:
    def __init__(self):
        self.sym_table = {}
        self.offset = 0
        self.line_no = 0
        self.semantic_rules = read_semantic_rules.read_semantic()
        #for key in self.semantic_rules.keys():
        #    print(f'{key}: \n{self.semantic_rules[key]}')

    def annotate_parse_tree(self, head):
        head.children.reverse()
        for child in head.children:
            self.annotate_parse_tree(child)
        key = []
        for x in head.children:
            if type(x.label) is tuple:
                key.append(x.label[0])
            else:
                key.append(x.label)
        if len(key) == 0:
            key = ['\\L']
        key = (head.label, tuple(key))
        if key in self.semantic_rules:
            rule_node = ParseTreeNode(self.semantic_rules[key], semantic)
            head.children.append(rule_node)

    def add_var(self, id, type):
        if id in self.sym_table.keys():
            print(f'variable {id} already declared')
            return False
        self.offset = self.offset + 1
        self.sym_table[id] = (self.offset, type)
        return True

    def get_var(self, id):
        if id not in self.sym_table.keys():
            print(f'variable {id} does not exist')
            return None
        return self.sym_table[id]

    def get_num_type(self, num):
        if '.' in str(num):
            return 'f'
        return 'i'

    def get_line_no(self):
        self.line_no = self.line_no + 1
        return self.line_no

    def get_curr_line_no(self):
        return self.line_no

    def get_end_line_no(self, code):
        n_lines = len(code.split(';'))
        return '+' + str(n_lines)


    def get_bytecode_relop(self, type, relop):
        op = 'if_' + str(type) + 'cmp'
        if relop == '==':
            return op + 'eq '
        if relop == '>':
            return op + 'gt '
        if relop == '>=':
            return op + 'ge '
        if relop == '<':
            return op + 'lt '
        if relop == '<=':
            return op + 'le '
        if relop == '!=':
            return op + 'ne '


    def get_bytecode_mulop(self, type, mulop):
        op = str(type)
        if mulop == '*':
            return op + 'mul'
        if mulop == '/':
            return op + 'div'


    def get_bytecode_addop(self, type, addop):
        op = str(type)
        if addop == '+':
            return op + 'add'
        if addop == '-':
            return op + 'sub'


    def get_rules(self, node):
        for child in node.children:
            if not self.get_rules(child):
                return False
        for child in node.children:
            if child.type is semantic:
                self.success = True
                exec(child.label)
                if not self.success:
                    return False
        return True

    def get_result_type(self, type1, type2):
        if type2 is None:
            return type1
        if type1 == type2:
            return type1
        print('inconsistent types')
        return None

    def get_code(self, head):
        nvars = len(self.sym_table.keys()) + 1
        stack_size = 0
        temp = 0
        lines = head.get_attribute('code')
        lines = lines.split(';')
        for i in range(0, len(lines)):
            if 'ldc' in lines[i] or 'load' in lines[i]:
                temp = temp + 1
            else:
                stack_size = max(stack_size, temp)
                temp = 0
            if '-+' in lines[i]:
                idx = lines[i].index('-+')
                rel_label = int(lines[i][idx + 2:])
                lines[i] = lines[i][:idx] + str(i + 1 - rel_label)
            if '+' in lines[i]:
                idx = lines[i].index('+')
                rel_label = int(lines[i][idx+1:])
                lines[i] = lines[i][:idx] + str(i+1+rel_label)
            lines[i] = str(i+1) + ':\t' + lines[i]
        lines[len(lines)-1] = lines[len(lines) - 1] + 'return\n'
        return '\t.limit stack ' + str(stack_size) + '\n\t.limit locals ' + str(nvars) + '\n' + '\n'.join(lines)
