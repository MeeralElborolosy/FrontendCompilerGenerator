from NFA_to_DFA import *


class DisjointSet(object):
    def __init__(self, items):
        self._disjoint_set = list()
        if items:
            for item in set(items):
                self._disjoint_set.append([item])

    def _get_index(self, item):
        for s in self._disjoint_set:
            for _item in s:
                if _item == item:
                    return self._disjoint_set.index(s)
        return None

    def find(self, item):
        for s in self._disjoint_set:
            if item in s:
                return s
        return None

    def find_set(self, item):
        s = self._get_index(item)
        return s + 1 if s is not None else None

    def union(self, item1, item2):
        i = self._get_index(item1)
        j = self._get_index(item2)
        if i != j:
            self._disjoint_set[i] += self._disjoint_set[j]
            del self._disjoint_set[j]

    def get(self):
        return self._disjoint_set


class DFAmin(object):
    def __init__(self, states=None,terminals=None, start_state=None, transitions=None, final_states=None):
        self.states = states
        self.terminals = terminals
        self.start_state = start_state
        self.transitions = transitions
        self.final_states = final_states.keys()
        self.accepting_states = final_states

    def generate_stuck_states(self):
        states = [True for i in range(0, len(self.states)+1)]
        for k, v in self.transitions.items():
            if k[0] != v:
                states[int(k[0])] = False
        self.is_stuck = states

    def go_to(self, state, transition):
        for k, v in self.transitions.items():
            if k == tuple((state, transition)):
                return v

    def _remove_unreachable_states(self):
        '''
        Removes states that are unreachable from the start state
        '''
        g = defaultdict(list)
        for k, v in self.transitions.items():
            g[k[0]].append(v)
        # do DFS
        stack = [self.start_state]
        reachable_states = set()
        while stack:
            state = stack.pop()
            if state not in reachable_states:
                stack += g[state]
            reachable_states.add(state)
        self.states = [state for state in self.states if state in reachable_states]
        self.final_states = [state for state in self.final_states if state in reachable_states]
        self.transitions = {k: v for k, v in self.transitions.items() if k[0] in reachable_states}

    def minimize(self):
        self._remove_unreachable_states()
        def order_tuple(a, b):
            return (a, b) if a < b else (b, a)
        table = {}
        sorted_states = sorted(self.states)
        # initialize the table
        for i, item in enumerate(sorted_states):
            for item_2 in sorted_states[i + 1:]:
                table[(item, item_2)] = not (((item in self.final_states) == (item_2 in self.final_states)) and ((item not in self.final_states) or (self.accepting_states[item] == self.accepting_states[item_2])))
        flag = True
        # table filling method
        while flag:
            flag = False
            for i, item in enumerate(sorted_states):
                for item_2 in sorted_states[i + 1:]:
                    if table[(item, item_2)]:
                        continue
                    # check if the states are distinguishable
                    for w in self.terminals:
                        t1 = self.transitions.get((item, w), None)
                        t2 = self.transitions.get((item_2, w), None)
                        if t1 is not None and t2 is not None and t1 != t2:
                            marked = table[order_tuple(t1, t2)]
                            flag = flag or marked
                            table[(item, item_2)] = marked
                            if marked:
                                break
        d = DisjointSet(self.states)
        # form new states
        for k, v in table.items():
            if not v:
                d.union(k[0], k[1])
        self.states = [str(x) for x in range(1, 1 + len(d.get()))]
        new_final_states = []
        new_accepting_states = {}
        self.start_state = str(d.find_set(self.start_state))
        for s in d.get():
            for item in s:
                if item in self.final_states:
                    new_final_states.append(str(d.find_set(item)))
                    new_accepting_states[str(d.find_set(item))] = self.accepting_states[item]
                    break
        self.transitions = {(str(d.find_set(k[0])), k[1]): str(d.find_set(v))
                            for k, v in self.transitions.items()}
        self.final_states = new_final_states
        self.accepting_states = new_accepting_states
        print(len(self.states))
        print('**************************')
        print('DFA AFTER MINIMIZATION :')
        print('**************************')
        self.print()
        self.generate_stuck_states()

    def print(self):
        print('**Transition table ( start state , input , end state ):')
        print(self.transitions)
        print('**Start state:')
        print(self.start_state)
        print('**Final states:')
        print(self.final_states)
        print('**Accepting states:')
        print(self.accepting_states)
        print('**Labels:')
        print(set([self.accepting_states[key] for key in self.accepting_states.keys()]))
        print(f'**Number of states = {len(self.states)}')

    def save(self, filename):
        f = open(filename,'a+')
        print('**Transition table ( start state , input , end state ):', file=f)
        print(self.transitions, file=f)
        print('**Start state :', file=f)
        print(self.start_state, file=f)
        print('**Final state :', file=f)
        print(self.final_states, file=f)
        print('**Accepting states:', file=f)
        print(self.accepting_states, file=f)
        print('**Labels:', file=f)
        print(set([self.accepting_states[key] for key in self.accepting_states.keys()]), file=f)
        print(f'**Number of states = {len(self.states)}', file=f)
