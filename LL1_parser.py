import first_follow
production = 0
semantic = 1

class sematic_rule:
    def __init__(self, rule):
        self.rule = rule


class ParseTreeNode:
    def __init__(self, label, type=production):
        self.label = label
        self.parents = []
        self.children = []
        self.attributes = {}
        self.type = type

    def addChild(self, node):
        self.children.append(node)
        node.parents.append(self)

    def add_attribute(self, name, val):
        self.attributes[name] = val

    def get_attribute(self, name):
        return self.attributes[name]

    def dfs(self, filename=None):
        stack = [self]
        visited = []
        if filename:
            f = open(filename, 'w')
        while len(stack) > 0:
            t = stack.pop()
            if t in visited:
                continue
            print(t.label)
            if filename:
                print(t.label, file=f)
            for child in t.children:
                stack.append(child)
            visited.append(t)

    def get_rules(self):
        rules = ''
        for child in self.children:
            rules = rules + child.get_rules()
        if self.type is semantic:
            return rules + self.label
        return rules


def parse(tokens, table, start, fname):
    error = False
    f = open(fname, 'w')
    tokens.append('$')
    stack = ['$', start]
    parse_tree_head = ParseTreeNode(start)
    fin = ParseTreeNode('$')
    node_stack = [fin, parse_tree_head]
    i = 0
    token = tokens[i]
    while len(stack) > 0:
        print(stack, file=f)
        print(stack)
        top = stack.pop()
        tree_node = node_stack.pop()
        if type(top) is sematic_rule:
            continue
        if first_follow.terminal(top):
            if top != token[0]:
                print(tokens[i:], file=f)
                print(f'Error: missing {top}: discard {top}', file=f)
                print(tokens[i:])
                print(f'Error: missing {top}: discard {top}')
                error = True
                continue
            if token[0] == '$':
                print('Success', file=f)
                print('Success')
                if error:
                    return None
                return parse_tree_head
                #return True
            tree_node.label = (tree_node.label, token[1])
            i = i + 1
            if i == len(tokens):
                print('EOF', file=f)
                print('EOF')
                return None
            token = tokens[i]
        elif (top, token[0]) not in table:
            print(tokens[i:], file=f)
            print(f'Error: illegal {top}: discard {token}', file=f)
            print(tokens[i:])
            print(f'Error: illegal {top}: discard {token}')
            error = True
            stack.append(top)
            node_stack.append(tree_node)
            i = i + 1
            if i == len(tokens):
                print('EOF')
                return None
            token = tokens[i]
        else:
            next = table[(top, token[0])][:]
            if next == ['sync']:
                print(tokens[i:], file=f)
                print(f'Error: illegal {top}: sync is encountered, discard {top}', file=f)
                print(tokens[i:])
                print(f'Error: illegal {top}: sync is encountered, discard {top}')
                error = True
            else:
                if '\L' in next:
                    next.remove('\L')
                next.reverse()
                for label in next:
                    n = ParseTreeNode(label)
                    tree_node.addChild(n)
                    node_stack.append(n)
                stack.extend(next)
    print('Not accepted')
    return None
