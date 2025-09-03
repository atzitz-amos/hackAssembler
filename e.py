GROUP = "group"
GROUP_OR = "group_or"
RANGE = "range"
CHAR = "char"
MOD_STAR = "mod_star"
MOD_PLUS = "mod_plus"
MOD_QUESTION_MARK = "mod_question_mark"
DOT = "dot"


class State:
    def __init__(self, isEnd):
        self.transitions = []
        self.epsilon = []
        self.isEnd = isEnd

    def add_transition(self, symbol, state, type_=0):
        self.transitions.append(NodeKey(symbol, state, type_))

    def add_epsilon(self, state):
        self.epsilon.append(state)


class Link:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __repr__(self):
        return repr(self.start)


class NodeKey:
    def __init__(self, key, value, type_=0):
        self.key = key
        self.value = value
        self.type_ = type_


class Parser:
    class Node:
        def __init__(self, name, value):
            self.name = name
            self.value = value

        def __str__(self):
            if type(self.value) == list:
                return f"{self.name}({', '.join(str(x) for x in self.value)})"
            return f"{self.name}({self.value})"

        __repr__ = __str__

    def __init__(self):
        self.i = 0
        self.group_n = 0
        self.stack = []

    def reg_exp(self, pattern):
        """
            Supports:
            - []
            - ()
            - a-z
            - |
            - * / + / ?
            - .
        """
        # O(n)

        def recursive_reg_exp(value):
            result = []

            while self.i < len(value):
                c = value[self.i]
                if c == "]" or c == ")" or c == "|":
                    return result
                if c == "[":
                    self.i += 1
                    result.append(self.Node(GROUP_OR, recursive_reg_exp(value)))
                    if value[self.i] != "]":
                        raise ValueError("No closing bracket found")
                elif c == "(":
                    self.i += 1
                    result.append(self.Node(GROUP, self.reg_exp(value)))
                    if value[self.i] != ")":
                        raise ValueError("No closing parenthesis found")
                elif c == "\\":
                    self.i += 1
                    result.append(self.Node(CHAR, ord(value[self.i])))
                elif c == "-":
                    last = result.pop()
                    if last.name != CHAR:
                        raise ValueError("Invalid range")
                    self.i += 1
                    result.append(self.Node(RANGE, (last.value, ord(value[self.i]))))
                elif c == "*":
                    last = result.pop()
                    result.append(self.Node(MOD_STAR, last))
                elif c == "+":
                    last = result.pop()
                    result.append(self.Node(MOD_PLUS, last))
                elif c == "?":
                    last = result.pop()
                    result.append(self.Node(MOD_QUESTION_MARK, last))
                elif c == ".":
                    result.append(self.Node(DOT, ""))
                else:
                    result.append(self.Node(CHAR, ord(c)))
                self.i += 1
            return result

        result = [recursive_reg_exp(pattern)]
        while self.i < len(pattern):
            if pattern[self.i] == "|":
                self.i += 1
                result.append(recursive_reg_exp(pattern))
            else:
                if len(result) == 1:
                    return result[0]
                return self.Node(GROUP_OR, result)

        if len(result) == 1:
            return result[0]
        return self.Node(GROUP_OR, result)

    def build_tree(self, nodes):
        #

        if type(nodes) == list:
            tree = self.build_tree(nodes[0])
            for i in range(1, len(nodes)):
                tree = self.concat(tree, self.build_tree(nodes[i]))
            return tree
        if nodes.name == GROUP:
            return self.build_tree(nodes.value)
        if nodes.name == GROUP_OR:
            tree = self.build_tree(nodes.value[0])
            for i in range(1, len(nodes.value)):
                tree = self.union(tree, self.build_tree(nodes.value[i]))
            return tree
        if nodes.name == RANGE:
            return self.from_range(nodes.value[0], nodes.value[1])
        if nodes.name == CHAR:
            return self.from_symbol(nodes.value)
        if nodes.name == MOD_STAR:
            return self.closure(self.build_tree(nodes.value))
        if nodes.name == MOD_PLUS:
            tree = self.build_tree(nodes.value)
            return self.concat(tree, self.closure(tree))
        if nodes.name == MOD_QUESTION_MARK:
            return self.union(self.from_epsilon(), self.build_tree(nodes.value))
        if nodes.name == DOT:
            return self.from_symbol(None)

    def from_symbol(self, symbol):
        start = State(False)
        end = State(True)
        start.add_transition(symbol, end)
        return Link(start, end)

    def from_range(self, a, b):
        start = State(False)
        end = State(True)
        start.add_transition([a, b], end, 1)
        return Link(start, end)

    def from_epsilon(self):
        start = State(False)
        end = State(True)
        start.add_epsilon(end)
        return Link(start, end)

    def concat(self, a, b):
        a.end.add_epsilon(b.start)
        a.end.isEnd = False
        return Link(a.start, b.end)

    def union(self, a, b):
        start = State(False)
        start.add_epsilon(a.start)
        start.add_epsilon(b.start)
        end = State(True)
        a.end.add_epsilon(end)
        b.end.add_epsilon(end)
        a.end.isEnd = False
        b.end.isEnd = False
        return Link(start, end)

    def closure(self, link):
        start = State(False)
        end = State(True)
        start.add_epsilon(end)
        start.add_epsilon(link.start)

        link.end.add_epsilon(end)
        link.end.add_epsilon(link.start)
        link.end.isEnd = False
        return Link(start, end)


class Matcher:
    def __init__(self, link):
        self.link = link

    def match(self, string):
        """ Backtrack the NFA """

        def backtrack(state, index):
            if state.isEnd:
                return index == len(string)
            for s in state.transitions:
                if index >= len(string):
                    return False
                if s.type_ == 0:
                    if s.key is not None and ord(string[index]) != s.key:
                        return False
                else:
                    if s.key[0] > ord(string[index]) or s.key[1] < ord(string[index]):
                        return False
                if backtrack(s.value, index + 1):
                    return True
            for s in state.epsilon:
                if backtrack(s, index):
                    return True
            return False

        return backtrack(self.link.start, 0)


import time

t0 = 0
t1 = 0
t2 = 0

n = 100000

for i in range(n):
    start = time.time()
    p = Parser()
    value = p.reg_exp(r"([a-z]+|[A-Z]+|[0-9]+|[a-zA-Z0-9]+)")
    t0 += time.time() - start

    start = time.time()
    x = (p.build_tree(value))
    t1 += time.time() - start

    start = time.time()
    m = Matcher(x).match("daasssssssssssssssasssssssssssssssssssython")
    t2 += time.time() - start

print("Parsing reg_exp:", str(t0) + "s / " + str(n), "=", str(t0 / n) + "s")
print("Building tree:", str(t1) + "s / " + str(n), "=", str(t1 / n) + "s")
print("Matching:", str(t2) + "s / " + str(n), "=", str(t2 / n) + "s")
print("Result:", m)
