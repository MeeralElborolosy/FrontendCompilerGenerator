from minimize_DFA import *
def generateDFAmin(filename):
    read_file = ReadingInputFile(filename)
    read_file.read_file()
    r_exp = []
    puncs = read_file.punctuations
    for punc in puncs:
        r_exp.append([punc, punc])
    keywords = read_file.keywords
    for keyword in keywords:
        r_exp.append([keyword, keyword])
    r_exp = r_exp + read_file.RE
    print('r_exp')
    print(r_exp)
    nfa = generate_NFA(r_exp)
    nfa.print_nfa()
    print('converting nfa to dfa')
    dfa = DFA()
    dfa.convert_from_nfa(nfa)
    dfa.print_dfa()
    print('minimizing dfa')
    res_dct = {(dfa.transition_functions[i][0], dfa.transition_functions[i][1]): dfa.transition_functions[i][2] for i in
                range(0, len(dfa.transition_functions), 1)}
    dfamin = DFAmin(dfa.states, dfa.symbols, dfa.start_state, res_dct, dfa.accepting_states)
    dfamin.minimize()
    dfamin.print()
    return dfamin

def loadDFAmin(filename):
    pass

