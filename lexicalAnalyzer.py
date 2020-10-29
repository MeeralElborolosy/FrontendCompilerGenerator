from generateDFAmin import *

class LexicalAnalyzer():
    def __init__(self, filename, output_filename):
        print('generating dfa')
        self.dfa = generateDFAmin(filename)
        self.output_filename = output_filename
        f = open(output_filename, 'w')
        f.close()
    def save(self):
        self.dfa.save(self.output_filename)

    def compile(self, filename):
        program_file = open(filename, 'r')
        stream = program_file.read()
        tokens = []
        components = stream.split()
        for component in components:
            dfa_state = self.dfa.start_state
            last_accepted_idx = -1
            last_accepted_label = None
            j = 0
            start = 0
            while j < len(component):
                c = component[j]
                dfa_state = self.dfa.go_to(dfa_state, c)
                if dfa_state in self.dfa.final_states:
                    last_accepted_idx = j
                    last_accepted_label = self.dfa.accepting_states[dfa_state]
                if dfa_state is None or (j == len(component) - 1 and last_accepted_idx != j and last_accepted_idx != -1):
                    tokens.append((last_accepted_label, component[start:last_accepted_idx+1]))
                    dfa_state = self.dfa.start_state
                    start = last_accepted_idx + 1
                    last_accepted_idx = -1
                    last_accepted_label = None
                    j = start - 1
                j = j + 1
            if last_accepted_idx == len(component) - 1:
                tokens.append((last_accepted_label, component[start:last_accepted_idx+1]))
            else:
                print(f'token {component[start:]} unidentified')
                return None
        return tokens


test0 = 'pdf_example.txt'
test0_code = 'code.txt'
test0_dfa = 'dfa_min0.txt'
test0_tokens = 'output0.txt'
test1 = 'Case1/lexical.txt'
test1_code = 'Case1/program.txt'
test1_dfa = 'dfa_min1.txt'
test1_tokens = 'output1.txt'
test2 = 'Case2/lexical.txt'
test2_code = 'Case2/program.txt'
test2_dfa = 'dfa_min2.txt'
test2_tokens = 'output2.txt'
test3 = 'Case3/lexical.txt'
test3_code = 'Case3/program.txt'
test3_dfa = 'dfa_min3.txt'
test3_tokens = 'output3.txt'
test4 = '' #insert lexical rules of new test case here
test4_code = '' #insert code of new test case here
test4_dfa = 'dfa_min4.txt'
test4_tokens = 'output4.txt'

test_cases = {
    'test0': (test0, test0_code, test0_dfa, test0_tokens),
    'test1': (test1, test1_code, test1_dfa, test1_tokens),
    'test2': (test2, test2_code, test2_dfa, test2_tokens),
    'test3': (test3, test3_code, test3_dfa, test3_tokens),
    'test4': (test4, test4_code, test4_dfa, test4_tokens)
}

test = test_cases['test0'] #edit this line to the test case required from the dictionary


