from readfile import *
epsilon = '\L'


class NFA:
    def __init__(self, symbols, nodes, start_state, accepting_states):
        self.symbols = symbols
        self.init_states(nodes)
        print_nodes(self.states)
        self.start_state = start_state.id
        self.accepting_states = {state.id: state.label for state in accepting_states}
        self.transition_functions = []
        self.generate_transition_functions()
        self.init_eClosure()
        self.init_move()

    def init_states(self, nodes):
        ids = {}
        global new_id
        self.node_id = {}
        self.states = []
        for node in nodes:
            self.node_id[new_id] = node
            if node.id not in ids:
                ids[node.id] = new_id
                new_id = new_id + 1
            if node not in self.states:
                self.states.append(node)
        print(ids)
        print_nodes(self.states)
        for node in self.states:
            for i in range(0,len(node.adj_list)):
                node.adj_list[i][0] = ids[node.adj_list[i][0]]
                node.debug()
            node.id = ids[node.id]
        self.states.sort(key=lambda x: x.id)
        print('state ids:')
        for i in self.states:
            print(i.id)

    def generate_transition_functions(self):
        for i in self.states:
            for j in i.adj_list:
                self.transition_functions.append((i.id, j[0], j[1]))

    def get_num_states(self):
        return len(self.states)

    def get_node_by_id(self,id):
        return self.node_id[id]

    def init_eClosure(self):
        self.eClosures = []
        for node in self.states:
            output = [node.id]
            stack = [node.id]
            while len(stack) > 0:
                t = self.get_node_by_id(stack.pop())
                for u in t.adj_list:
                    if u[1] == epsilon:
                        if u[0] not in output:
                            output.append(u[0])
                            stack.append(u[0])
            self.eClosures.append(list(output))

    def init_move(self):
        self.moves = {}
        for node in self.states:
            for symbol in self.symbols:
                self.moves[(node.id,symbol)] = node.move(symbol)


    def eClosure(self, nodes):
        # output = []
        # for node in nodes:
        #     n = self.get_node_by_id(node)
        #     n_output = [n.id]
        #     stack = [n.id]
        #     while len(stack) > 0:
        #         t = self.get_node_by_id(stack.pop())
        #         for u in t.adj_list:
        #             if u[1] == epsilon:
        #                 if u not in n_output:
        #                     n_output.append(u[0])
        #                     stack.append(u[0])
        #     output = output + n_output
        output = set({})
        for n in nodes:
            output.update(self.eClosures[n])
        return list(output)

    def move(self, nodes, a):
        output = []
        # for node in nodes:
        #     n = self.get_node_by_id(node)
        #     output = output + n.move(a)
        for node in nodes:
            output = output + self.moves[(node, a)]
        return output

    def print_nfa(self):
        print('states:')
        print_nodes(self.states)
        print('symbols:')
        print(self.symbols)
        print('accepting states:')
        print(self.accepting_states)
        print('start state:')
        print(self.start_state)
        print('transition functions:')
        print(self.transition_functions)


class Node:
    def __init__(self, id, state, label=None):
        self.id = id
        self.state = state
        self.label = label
        self.adj_list = []

    def transition_to(self, node_id, char):
        if [node_id, char] not in self.adj_list:
            self.adj_list.append([node_id, char])

    def move(self, a):
        output = set({})
        for i in self.adj_list:
            if i[1] == a:
                output.add(i[0])
        return list(output)

    def display(self):
        print(f'id = {self.id} state = {self.state}')

    def debug(self):
        for i in self.adj_list:
            print(f'{self.id} {i[0]} {i[1]}')


class StateGroup:
    def __init__(self, start, end):
        self.start = start
        self.end = end


def generate_NFA(regex):
    global node_id
    global new_id
    new_id = 1
    node_id = 1
    print('generating nfa')
    output = []
    for r in regex:
        print('label:')
        print(r[0])
        postfix = infix_to_postfix(r[1])
        if (r[0][0] == '\\'):
            r[0] = r[0][1:]
        nfa = regex_to_NFA(r[0], postfix)
        output.append(nfa)
    print('merging nfas')
    final_nfa = merge_nfas(output)
    print('done')
    return final_nfa


def merge_nfas(nfas):
    global new_id
    accepting_states = []
    nodes = []
    symbols = set({})
    start_node = Node(0, False)
    for nfa in nfas:
        start_node.transition_to(nfa.start_state, epsilon)
        nodes.extend(nfa.states)
        symbols.update(nfa.symbols)
        key = list(nfa.accepting_states.keys())[0]
        end_node = nfa.get_node_by_id(key)
        accepting_states.append(end_node)
    nodes.append(start_node)
    symbols.remove(epsilon)
    new_id = 0
    return NFA(list(symbols), nodes, start_node, accepting_states)


def print_nodes(nodes):
    print('**************************')
    for node in nodes:
        node.debug()
    print('**************************')


def infix_to_postfix(input):
    priority = {
        '|':2,
        '^':3,
        '+':4,
        '*':4,
        '(':1
    }
    priority.setdefault(-1)
    stack = []
    output = ''
    con = False
    i = 0
    print(input)
    while i < len(input):
        c = input[i]
        if c == ' ':
            i = i + 1
            continue
        if c == ')':
            con = True
            top = stack.pop()
            while top != '(':
                output = output + top
                if len(stack) == 0:
                    break
                top = stack.pop()
        elif c == '(':
            if con:
                while len(stack) > 0 and priority['^'] <= priority[stack[len(stack) - 1]]:
                    output = output + stack.pop()
                stack.append('^')
                con = False
            stack.append(c)
        elif c in priority.keys():
            if c in ['*', '+']:
                con = True
            else:
                con = False
            while len(stack) > 0 and priority[c] <= priority[stack[len(stack)-1]]:
                output = output + stack.pop()
            stack.append(c)
        else:
            if con:
                while len(stack) > 0 and priority['^'] <= priority[stack[len(stack) - 1]]:
                    output = output + stack.pop()
                stack.append('^')
            else:
                con = True
            output = output + c
            if c == '\\':
                output = output + input[i+1]
                i = i + 1
        i = i + 1
        print(f'c = {c}')
        print(f'con = {con}')
        print(f'output = {output}')
        print(f'stack: {stack}')
    while len(stack) > 0:
        output = output + stack.pop()
    print(output)
    return output


def merge_nodes(n1, n2):
    new_node = Node(n1.id, n1.state)
    for i in n1.adj_list:
        new_node.transition_to(i[0], i[1])
    for i in n2.adj_list:
        new_node.transition_to(i[0],i[1])
    return new_node


def make_state(id, transition_char=None, gp=None, gp2=None, regex=None, nodes=None): #character
    if regex is None:
        start_node = Node(id, False)
        end_node = Node(id+1, False)
        start_node.transition_to(end_node.id, transition_char)
        new_gp = StateGroup(start_node, end_node)
        return new_gp
    if regex == '*' or regex == '+':
        gp.end.transition_to(gp.start.id, epsilon)
        start_node = Node(id, False)
        end_node = Node(id + 1, False)
        start_node.transition_to(gp.start.id, epsilon)
        gp.end.transition_to(end_node.id, epsilon)
        if regex == '*':
            start_node.transition_to(end_node.id, epsilon)
        new_gp = StateGroup(start_node, end_node)
        return new_gp
    if regex == '|':
        start_node = Node(id, False)
        end_node = Node(id + 1, False)
        start_node.transition_to(gp.start.id, epsilon)
        start_node.transition_to(gp2.start.id, epsilon)
        gp.end.transition_to(end_node.id, epsilon)
        gp2.end.transition_to(end_node.id, epsilon)
        new_gp = StateGroup(start_node, end_node)
        return new_gp
    if regex == '^':
        for i in gp2.start.adj_list:
            gp.end.transition_to(i[0], i[1])
        for i in range(0,len(nodes)):
            if nodes[i].id == gp2.start.id:
                nodes.remove(nodes[i])
                break
        new_gp = StateGroup(gp.start, gp2.end)
        return new_gp


def regex_to_NFA(label, input):
    i = 0
    stack = []
    nodes = []
    symbols = []
    global node_id
    while i < len(input):
        #print(input[i])
        if input[i] == '\\':
            if i < len(input) - 1 and input[i+1] == 'L':
                string = input[i] + input[i+1]
            else:
                string = input[i+1]
            i = i + 1
            gp = make_state(id=node_id, transition_char=string)
            if string not in symbols:
                symbols.append(string)
            stack.append(gp)
            nodes.append(gp.start)
            nodes.append(gp.end)
            node_id = node_id + 2
        elif input[i].isalnum():
            string = input[i]
            gp = make_state(id=node_id, transition_char=string)
            if string not in symbols:
                symbols.append(string)
            stack.append(gp)
            nodes.append(gp.start)
            nodes.append(gp.end)
            node_id = node_id + 2
        elif input[i] == '*' or input[i] == '+':
            ex = stack.pop()
            gp = make_state(id=node_id, gp=ex, regex=input[i])
            stack.append(gp)
            nodes.append(gp.start)
            nodes.append(gp.end)
            node_id = node_id + 2
        elif input[i] == '|' or input[i] == '^':
            ex2 = stack.pop()
            ex1 = stack.pop()
            gp = make_state(id=node_id, gp=ex1, gp2=ex2, regex=input[i], nodes=nodes)
            stack.append(gp)
            if input[i] == '|':
                nodes.append(gp.start)
            nodes.append(gp.end)
            node_id = node_id + 2
        else:
            string = input[i]
            gp = make_state(id=node_id, transition_char=string)
            if string not in symbols:
                symbols.append(string)
            stack.append(gp)
            nodes.append(gp.start)
            nodes.append(gp.end)
            node_id = node_id + 2
        i = i + 1
    #print_nodes(nodes)
    #print(symbols)
    stack[len(stack)-1].end.state = True
    stack[len(stack)-1].end.label = label
    #return StateGroup(stack[0].start, stack[len(stack)-1].end), nodes
    return NFA(symbols, nodes, stack[0].start, [stack[len(stack)-1].end])


#print(r_exp)
#r_exp = [['id','(a)|(b)(A|B|C)+']]
#r_exp = [['id','(a)|(b)*']]
#generate_NFA([('label','a^(a|b)*')])[1].print_nfa()

debug1 = False
if debug1:
    read_file = ReadingInputFile('pdf_example.txt')
    read_file.read_file()
    r_exp = read_file.RE
    output = generate_NFA(r_exp)
    print('output')
    for label, nfa in output:
        print(label)
        nfa.print_nfa()
        eclosure = nfa.eClosure([nfa.start_state])
        print('eclosure')
        print(eclosure)
debug2 = False
if debug2:
    print(infix_to_postfix('\=\= | !\= | > | >\= | < | <\='))
    [[label, nfa]] = generate_NFA([['relop','\=\= | !\= | > | >\= | < | <\=']])
    nfa.print_nfa()
debug3 = False
if debug3:
    read_file = ReadingInputFile('pdf_example.txt')
    read_file.read_file()
    r_exp = read_file.RE
    nfa = generate_NFA(r_exp)
    nfa.print_nfa()
