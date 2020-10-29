import read_cfg
LHSs = []
LHS_objects = []
first_dict = {}
follow_dict = {}


def terminal(s):
    if s in LHSs:
        return False
    else:
        return True

def get_first1(line):
    for i in range(0, len(line.RHS)):
        if terminal(line.RHS[i][0]):
            line.LHS.first.append(line.RHS[i][0])
    if '\L' in line.RHS:
        line.LHS.first.append("\L")


def get_first2(string):
    for i in range(0, len(string.RHS)):
        count = 0
        if not terminal(string.RHS[i][0]):
            to_be_appended = []
            to_be_appended1 = first_dict.get(string.RHS[i][0])
            if '\L' in to_be_appended1:
                for j in range(0, len(to_be_appended1)):
                    if to_be_appended1[j] != '\L':
                        to_be_appended.append(to_be_appended1[j])
            else:
                to_be_appended = to_be_appended1
            if to_be_appended not in string.LHS.first:
                string.LHS.first.extend(to_be_appended)
            #print(string.LHS.first)

            for j in range(0, len(string.RHS[i])):
                flag = 0
                if '\L' in first_dict.get(string.RHS[i][j]):
                    count = count + 1
                    flag = 1  # it has an epsilon in first list
                    if count == len(string.RHS[i]):
                        string.LHS.first.append('\L')
                        break
                    to_be_appended = []
                    to_be_appended1 = first_dict.get(string.RHS[i][j+1])
                    if '\L' in to_be_appended1:
                        for j in range(0, len(to_be_appended1)):
                            if to_be_appended1[j] != '\L':
                                to_be_appended.append(to_be_appended1[j])
                    string.LHS.first.extend(to_be_appended)
                if flag == 0:
                    break

def follow1(strings):

    for string in strings:
        if string.start == True:
            if '$' not in follow_dict[string.LHS.name]:
                follow_dict[string.LHS.name].append('$')
    for lhs in LHS_objects:
        for string in strings:
            for rhs in string.RHS:
                flag = 0
                if lhs.name in rhs:

                    i = rhs.index(lhs.name)
                    i = i+1
                    while True:
                        if i < len(rhs):
                            if terminal(rhs[i]):
                                if rhs[i] not in follow_dict[lhs.name]:
                                    follow_dict[lhs.name].append(rhs[i])
                                    flag = 0
                            else:
                                to_be_appended = []
                                to_be_appended1 = first_dict[rhs[i]]
                                if '\L' in to_be_appended1:
                                    flag = 1
                                    for j in range(0, len(to_be_appended1)):
                                        if to_be_appended1[j] != '\L':
                                            to_be_appended.append(to_be_appended1[j])
                                else:
                                    flag = 0
                                for j in range(0, len(to_be_appended)):
                                    if to_be_appended[j] not in follow_dict[lhs.name]:
                                        follow_dict[lhs.name].extend(to_be_appended) #khaletha extend badal append
                        if flag == 0:
                            break
                        else:
                            if i + 1 < len(rhs):
                                i = i+1
                            else:
                                break


def follow2(strings):
    for lhs in LHS_objects:
        for string in strings:
            for rhs in string.RHS:
                if lhs.name in rhs:
                    i = rhs.index(lhs.name)
                    while True:
                        flag = 0
                        if i < len(rhs)-1:
                            if not terminal(rhs[i+1]):
                                non_terminal = rhs[i+1]
                                if '\L' in first_dict[non_terminal]:
                                    flag = 1
                            elif terminal(rhs[i+1]):
                                if rhs[i+1] not in follow_dict[lhs.name]:
                                    follow_dict[lhs.name].append(rhs[i+1])
                        if i == len(rhs)-1:
                            to_be_appended = follow_dict[string.LHS.name]
                            for j in range(0, len(to_be_appended)):
                                if to_be_appended[j] not in follow_dict[lhs.name]:
                                    follow_dict[lhs.name].extend(to_be_appended)
                            break
                        if flag == 1:
                            i = i+1
                        else:
                            break



def controller():
    Lines = read_cfg.save_to_list()
    strings = read_cfg.get_productions(Lines)
    #for i in range(0, len(strings)):
        # print(strings[i].RHS)

    for i in range(0, len(strings)):
        LHS_objects.append(strings[i].LHS)
        LHSs.append(strings[i].LHS.name)
    # GETTING FIRST
    for i in range(0, len(strings)):
        get_first1(strings[i])
        first_dict[strings[i].LHS.name] = strings[i].LHS.first
        first_dict[strings[i].LHS.name] = list(dict.fromkeys(first_dict[strings[i].LHS.name]))

    for i in range(len(strings) - 1, -1, -1):
        get_first2(strings[i])
        first_dict[strings[i].LHS.name] = strings[i].LHS.first
        first_dict[strings[i].LHS.name] = list(dict.fromkeys(first_dict[strings[i].LHS.name]))

    print('First')
    print(first_dict)
    # GETTING FOLLOW
    for string in strings:
        follow_dict[string.LHS.name] = []
    temp_dict = {}
    while True:
        follow1(strings)
        follow2(strings)
        if temp_dict == follow_dict:
            break
        else:
            temp_dict = follow_dict

    print('Follow')
    print(follow_dict)
    return strings, first_dict, follow_dict
