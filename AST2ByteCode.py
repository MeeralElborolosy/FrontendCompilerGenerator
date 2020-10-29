class ASTNode:
    def __init__(self, type, val):
        self.type = type
        self.val = val
        self.code = None

class ByteCodeGenerator:
    def __init__(self):
        self.sym_table = {}
        self.vars = 0

    def get_offset(self, operand):
        if type(operand) is int:
            return operand
        else:
            return self.sym_table[operand][0]

    def num_type(self, num):
        if '.' in str(num):
            return 'f'
        return 'i'

    def add_byte_code(self, op_type):
        code = str(op_type) + 'add\n'
        return code, op_type

    def mul_byte_code(self, op_type):
        code = str(op_type) + 'mul\n'
        return code, op_type

    def cmp_byte_code(self, op1, op2, relop, op_type):
        off1 = self.get_offset(op1)
        off2 = self.get_offset(op2)
        code = ''
        val = 0
        return code, val

    def assign_byte_code(self, op1, op_type):
        off1 = self.get_offset(op1)
        code = str(op_type) + 'store_' + str(off1) + '\n'
        return code, op_type

    def num_byte_code(self, num):
        op_type = self.num_type(num.val.lex_val)
        code = 'b' + op_type + 'push ' + str(num.val.lex_val) + '\n'
        return code, op_type

    def id_byte_code(self, id, op_type):
        if id.val.lex_val in self.sym_table:
            code = 'b' + op_type + 'load_' + self.sym_table[id.id.val.lex_val][0] + '\n'
            return code, id.val.lex_val
        self.vars = self.vars + 1
        self.sym_table[id.val.lex_val] = (self.vars, op_type)
        return '', id.val.lex_val

    def while_byte_code(self, cond, statement):
        code = ''
        val = 0
        return code, val

    def if_byte_code(self, cond, st1, st2):
        branch = 0
        code = 'if_' + cond + ' ' + str(branch) + '\n'
        val = 0
        return code, val

    def ast2bytecode(self, node):
        if node.type == 'if':
            left_val, left_code = self.ast2bytecode(node.left)
            mid_val, mid_code = self.ast2bytecode(node.mid)
            right_val, right_code = self.ast2bytecode(node.right)
            code, val = self.if_byte_code(left_val, mid_val, right_val)
            return code, val
        elif node.type == 'num' or node.type == 'id':
            if node.type == 'num':
                code, val = self.num_byte_code(node)
            else:
                code, val = self.id_byte_code(node)
            return code, val
        elif node.type == 'assign':
            id = node.left.val.lex_val
            right_val, right_code = self.ast2bytecode(node.right)
            code, val = self.assign_byte_code(id, right_val)
            return right_code + code, val
        else:
            left_val, left_code = self.ast2bytecode(node.left)
            right_val, right_code = self.ast2bytecode(node.right)
            if node.type == 'addop':
                code, val = self.add_byte_code(left_val, right_val)
            elif node.type == 'mulop':
                code, val = self.mul_byte_code(left_val, right_val)
            elif node.type == 'relop':
                code, val = self.cmp_byte_code(left_val, right_val, node)
            return left_code + right_code + code, val
