from collections import defaultdict
from regex_to_NFA import *

class DFA:
    def __init__(self):
        self.accepting_states = {}
        self.symbols = []
        self.start_state = 0
        self.transition_functions = []
        self.q = []
        self.states = []

    def convert_from_nfa(self, nfa):
        self.symbols = nfa.symbols
        start_state = nfa.start_state
        nfa_transition_dict = {}
        dfa_transition_dict = {}

        # Combine NFA transitions
        for transition in nfa.transition_functions:
            starting_state = transition[0]
            ending_state = transition[1]
            transition_symbol = transition[2]

            if (starting_state, transition_symbol) in nfa_transition_dict:
                nfa_transition_dict[(starting_state, transition_symbol)].append(ending_state)
            else:
                nfa_transition_dict[(starting_state, transition_symbol)] = [ending_state]
        self.q.append(tuple(nfa.eClosure([start_state])))

        visitied = []
        # Convert NFA transitions to DFA transitions
        for dfa_state in self.q:
            if dfa_state in visitied:
                continue
            visitied.append(dfa_state)
            for symbol in nfa.symbols:
                s = nfa.move(dfa_state, symbol)
                if s is None:
                    continue
                u = nfa.eClosure(s)
                if u is None:
                    continue
                if u not in self.q and u not in visitied:
                    self.q.append(tuple(u))
                dfa_transition_dict[(dfa_state, symbol)] = u
        # Convert NFA states to DFA states
        for key in dfa_transition_dict:
            self.transition_functions.append(
            (self.q.index(tuple(key[0])), key[1], self.q.index(tuple(dfa_transition_dict[key]))))
        for q_state in self.q:
            nfa_accepting_states = nfa.accepting_states
            for nfa_accepting_state in nfa_accepting_states.keys():
                if nfa_accepting_state in q_state:
                    self.accepting_states[self.q.index(q_state)] = nfa_accepting_states[nfa_accepting_state]
                    break
        for i in range(0,len(self.q)):
            self.states.append(i)

    def print_dfa(self):
        print('Terminals :')
        print("".join(self.symbols))
        print('Transition table ( start state, end state, input):')
        for transition in sorted(self.transition_functions):
            print(f'{transition[0]} {transition[2]} {transition[1]}')
            #print(" ".join(str(value) for value in transition))
        print('**************************')
        print('DFA BEFORE MINIMIZATION :')
        print('**************************')
        print('**Transition table ( start state , input , end state ):')
        print(self.transition_functions)
        print('**Start state :')
        print(self.start_state)
        print('**Final state :')
        print(self.accepting_states)
        print('**Labels:')
        print(set([self.accepting_states[key] for key in self.accepting_states.keys()]))
        print(f'**Number of states = {len(self.states)}')
