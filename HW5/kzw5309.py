############################################################
# CMPSC 442: Homework 5
############################################################

student_name = "Kun Wang"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import copy
import itertools

############################################################
# Section 1: Propositional Logic
############################################################

class Expr(object):
    def __hash__(self):
        return hash((type(self).__name__, self.hashable))

class Atom(Expr):
    def __init__(self, name):
        self.name = name
        self.hashable = name
    def __eq__(self, other):
        return type(self) == type(other) and self.name == other.name
    def __repr__(self):
        return "Atom(%s)" % self.name
    def atom_names(self):
        return {self.name}
    def evaluate(self, assignment):
        return assignment[self.name]
    def to_cnf(self):
        return self

class Not(Expr):
    def __init__(self, arg):
        self.arg = arg
        self.hashable = arg
    def __eq__(self, other):
        return type(self) == type(other) and self.arg == other.arg
    def __repr__(self):
        return "Not(%s)" % repr(self.arg)
    def atom_names(self):
        return self.arg.atom_names()
    def evaluate(self, assignment):
        return not self.arg.evaluate(assignment)
    def to_cnf(self):
        if isinstance(self.arg, Atom):
            return self
        elif isinstance(self.arg, And):
            return Or(*map(Not, self.arg.conjuncts)).to_cnf()
        elif isinstance(self.arg, Or):
            return And(*map(Not, self.arg.disjuncts)).to_cnf()
        elif isinstance(self.arg, Not):
            return self.arg.arg.to_cnf()
        elif isinstance(self.arg, Implies):
            return And(self.arg.left, Not(self.arg.right)).to_cnf()
        elif isinstance(self.arg, Iff):
            return Or(Not(Implies(self.arg.left, self.arg.right)), Not(Implies(self.arg.right, self.arg.left))).to_cnf()



class And(Expr):
    def __init__(self, *conjuncts):
        self.conjuncts = frozenset(conjuncts)
        self.hashable = self.conjuncts
    def __eq__(self, other):
        return type(self) == type(other) and self.conjuncts == other.conjuncts
    def __repr__(self):
        center = ["%s, " % (repr(d)) for d in self.conjuncts]
        center_str = "".join(center)[:-2]
        return "And(%s)" % center_str
    def atom_names(self):
        u = set()
        for d in self.conjuncts:
            u = u.union(d.atom_names())
        return u
    def evaluate(self, assignment):
        temp = True
        for d in self.conjuncts:
            temp = temp and d.evaluate(assignment)
        return temp
    def to_cnf(self):
        temp = list()
        for d in self.conjuncts:
            if isinstance(d, And):
                for x in d.conjuncts:
                    temp.append(x.to_cnf())
            else:
                temp.append(d.to_cnf())
        for i in temp:
            if isinstance(i, And):
                for y in i.conjuncts:
                    temp.append(y)
                temp.remove(i)
        return And(*temp)

class Or(Expr):
    def __init__(self, *disjuncts):
        self.disjuncts = frozenset(disjuncts)
        self.hashable = self.disjuncts
    def __eq__(self, other):
        return type(self) == type(other) and self.disjuncts == other.disjuncts
    def __repr__(self):
        center = ["%s, "%(repr(d)) for d in self.disjuncts]
        center_str = "".join(center)[:-2]
        return "Or(%s)"% center_str
    def atom_names(self):
        u = set()
        for d in self.disjuncts:
            u = u.union(d.atom_names())
        return u
    def evaluate(self, assignment):
        temp = False
        for d in self.disjuncts:
            temp = temp or d.evaluate(assignment)
        return temp
    def to_cnf(self):
        or_list = list()
        or_atom_list = list()
        or_and_list = list()
        for d in self.disjuncts:
            if isinstance(d, Or):
                for x in d.disjuncts:
                    or_list.append(x.to_cnf())
            else:
                or_list.append(d.to_cnf())
        for i in xrange(len(or_list)):
            if isinstance(or_list[i], Atom) or isinstance(or_list[i], Not):
                or_atom_list.append(or_list[i])
            elif isinstance(or_list[i], Or):
                or_atom_list = or_atom_list + list(or_list[i].disjuncts)
            else:
                or_and_list.append(or_list[i].conjuncts)
        if len(or_and_list) == 0:
            return Or(*or_atom_list)
        else:
            temp = list(itertools.product(*or_and_list))
            new_or_list = list()
            for i in xrange(len(temp)):
                list_i = list(temp[i])
                temp[i] = list_i + or_atom_list
                for j in temp[i]:
                    if isinstance(j, Or):
                        for x in j.disjuncts:
                            temp[i].append(x)
                        temp[i].remove(j)
                not_temp = {Not(x).to_cnf() for x in temp[i]}
                if len(not_temp.intersection(set(temp[i]))) == 0:
                    new_or_list.append(Or(*temp[i]))
            #print temp
            return And(*new_or_list)



class Implies(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.hashable = (left, right)
    def __eq__(self, other):
        return type(self) == type(other) and self.left == other.left and self.right == other.right
    def __repr__(self):
        return "Implies(%s, %s)"%(repr(self.left), repr(self.right))
    def atom_names(self):
        return self.left.atom_names().union(self.right.atom_names())
    def evaluate(self, assignment):
        if not self.left.evaluate(assignment) or self.right.evaluate(assignment):
            return True
        else:
            return False
    def to_cnf(self):
        return Or(Not(self.left), self.right).to_cnf()

class Iff(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.hashable = (left, right)
    def __eq__(self, other):
        return type(self) == type(other) and (self.left == other.right and self.right == other.left) or (self.left == other.left and self.right == other.right)
    def __repr__(self):
        return "Iff(%s, %s)" % (repr(self.left), repr(self.right))
    def atom_names(self):
        return self.left.atom_names().union(self.right.atom_names())
    def evaluate(self, assignment):
        if self.right.evaluate(assignment) == self.left.evaluate(assignment):
            return True
        else:
            return False
    def to_cnf(self):
        return And(Or(Not(self.left), self.right), Or(Not(self.right), self.left)).to_cnf()

def satisfying_assignments(expr):
    atoms = list(expr.atom_names())
    assignments = {a: False for a in atoms}
    for i in xrange(2**len(atoms)):
        j = 0
        assignments = copy.deepcopy(assignments)
        for a in atoms:
            if i != 0 and i % 2**j == 0:
                assignments[a] = not assignments[a]
            j += 1
        if expr.evaluate(assignments):
            yield assignments





class KnowledgeBase(object):
    def __init__(self):
        self.facts = set()
    def get_facts(self):
        return self.facts
    def tell(self, expr):
        self.facts.add(expr)
        new_e = And(*self.facts).to_cnf()
        self.facts.clear()
        for x in new_e.conjuncts:
            self.facts.add(x)
    def ask(self, expr):
        clauses = copy.deepcopy(self.facts)
        clauses.add(Not(expr))
        new_e = And(*clauses).to_cnf()
        clauses.clear()
        for x in new_e.conjuncts:
            if isinstance(x, Or):
                clauses.add(x.disjuncts)
            else:
                clauses.add(frozenset([x]))
        new = set()
        pairs = set()
        while 1:
            clauses = clauses.union(new)
            clauses_list = list(clauses)
            #print len(clauses)
            for i in xrange(len(clauses_list)):
                for j in xrange(i+1, len(clauses_list)):
                    temp_tuple = (clauses_list[i], clauses_list[j])
                    if temp_tuple not in pairs:
                        resolvent = None
                        pairs.add(temp_tuple)
                        union_c = clauses_list[i].union(clauses_list[j])
                        union_n = frozenset([x.atom_names().pop() for x in union_c])
                        if (len(union_c) - len(union_n)) == 1:
                            not_i_d = {Not(x).to_cnf() for x in clauses_list[i]}
                            inter_d = clauses_list[j].intersection(not_i_d)
                            if len(inter_d) == 1:
                                different_j_d = clauses_list[j].difference(inter_d)
                                not_inter_d = {Not(x).to_cnf() for x in inter_d}
                                different_i_d = clauses_list[i].difference(not_inter_d)
                                resolvent = different_i_d.union(different_j_d)
                        if isinstance(resolvent, frozenset):
                            if len(resolvent) == 0:
                                return True
                            else:
                                new.add(resolvent)
            if new.issubset(clauses):
                return False




############################################################
# Section 2: Logic Puzzles
############################################################

# Puzzle 1

# Populate the knowledge base using statements of the form kb1.tell(...)
kb1 = KnowledgeBase()
my = Atom("mythical")
mo = Atom("mortal")
mam = Atom("mammal")
ho = Atom("horned")
mag = Atom("magical")
kb1.tell(Implies(my, Not(mo)))
kb1.tell(Implies(Not(my), And(mo, mam)))
kb1.tell(Implies(Or(Not(mo), mam), ho))
kb1.tell(Implies(ho, mag))
# Write an Expr for each query that should be asked of the knowledge base
mythical_query = my
magical_query = mag
horned_query = ho

# Record your answers as True or False; if you wish to use the above queries,
# they should not be run when this file is loaded
is_mythical = False
is_magical = True
is_horned = True

# Puzzle 2
a = Atom("a")
j = Atom("j")
m = Atom("m")
# Write an Expr of the form And(...) encoding the constraints
party_constraints = And(Implies(Or(m, a), j), Implies(Not(m), a), Implies(a, Not(j)))

# Compute a list of the valid attendance scenarios using a call to
# satisfying_assignments(expr)
valid_scenarios = [{'a': False, 'j': True, 'm': True}]

# Write your answer to the question in the assignment
puzzle_2_question = """
Ann does not come, but John and Mary come.
"""

# Puzzle 3

# Populate the knowledge base using statements of the form kb3.tell(...)
kb3 = KnowledgeBase()
p1 = Atom("p1")
p2 = Atom("p2")
e1 = Atom("e1")
e2 = Atom("e2")
s1 = Atom("s1")
s2 = Atom("s2")

kb3.tell(Iff(p1, Not(e1)))
kb3.tell(Iff(p2, Not(e2)))
kb3.tell(Iff(And(p1, e2), s1))
kb3.tell(Iff(Or(And(p1, e2), And(e1, p2)), s2))
kb3.tell(And(Or(s1, s2), Or(Not(s1), Not(s2))))

s1_query = s1
s2_query = s2
p1_query = p1
e1_query = e1
p2_query = p2
e2_query = e2
# Write your answer to the question in the assignment; the queries you make
# should not be run when this file is loaded
puzzle_3_question = """
s1_query = s1
s2_query = s2
p1_query = p1
e1_query = e1
p2_query = p2
e2_query = e2
I make these queries to check if each room contains prize or not and authenticity of both statements

Answer:
The sign on the first door is false, but the sign on the second door is true.
As a result, the first room is empty, and the second room contains a prize.
"""

# Puzzle 4

# Populate the knowledge base using statements of the form kb4.tell(...)
kb4 = KnowledgeBase()
ia = Atom("ia")
ib = Atom("ib")
ic = Atom("ic")
ka = Atom("ka")
kb = Atom("kb")
kc = Atom("kc")
asay = And(ia, kb, Not(kc))
bsay = And(ib, Not(kb))
csay = And(ic, Or(Not(ia), Not(ib)), And(ka, kb))
kb4.tell(Or(And(asay, bsay, Not(csay)), And(asay, Not(bsay), csay), And(Not(asay), bsay, csay)))

query_Adams = ia
query_Brown = ib
query_Clark = ic



# Uncomment the line corresponding to the guilty suspect
# guilty_suspect = "Adams"
guilty_suspect = "Brown"
# guilty_suspect = "Clark"

# Describe the queries you made to ascertain your findings
puzzle_4_question = """
Made three queries:
query_Adams = ia
query_Brown = ib
query_Clark = ic
I ask the knowledge base whether Adams, Brown and Clark is innocent. 
If it returns False, it means the person is guilty.
If it returns True, it means the person is innocent.

Answer:
With these three queries, I can deduce who is guilty and who is innocent.
The guilty man is Brown who also lies. Adams and Clark are innocent and say the truth.
"""

############################################################
# Section 3: Feedback
############################################################

feedback_question_1 = """
It takes me about 20 hours.
"""

feedback_question_2 = """
The most challenging part of this assignment is design an efficient ask function.
"""

feedback_question_3 = """
I like the part that setups the logical expression. There should be more instructions and details about what we should do.
"""
