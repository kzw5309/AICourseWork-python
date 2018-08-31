import kzw5309 as k
#import dtest as k
print
print"1"
a, b, c = map(k.Atom, "abc")
d = k.Atom("d")
print a == a
print k.Atom("a") == k.Atom("b")
print k.And(k.Atom("a"), k.Not(k.Atom("b"))) == k.And(k.Not(k.Atom("b")), k.Atom("a"))
print k.Implies(a, k.Iff(b, c))
print k.And(a, k.Or(k.Not(b), c))
print k.And(a, k.Or(k.Not(a), c, k.Atom('d'), k.Atom('e')))

print
print "2"
print k.Atom("a").atom_names()
y = k.And(a, k.Or(k.Not(b), c))
print k.Not(y).atom_names()
print k.Not(k.Atom("a")).atom_names()

print
print "3"
e = k.Implies(k.Atom("a"), k.Atom("b"))
print e.evaluate({"a": False, "b": True})
print e.evaluate({"a": True, "b": False})
print e.evaluate({"a": False, "b": False})
print
e = k.Iff(k.Atom("a"), k.Atom("b"))
print e.evaluate({"a": False, "b": True})
print e.evaluate({"a": True, "b": False})
print e.evaluate({"a": False, "b": False})
print
e = k.And(k.Not(a), k.Or(b, c))
print e.evaluate({"a": False, "b": False,"c": True})

print
print "4"
e = k.Implies(k.Atom("a"), k.Atom("b"))
q = k.satisfying_assignments(e)
print next(q)
print next(q)
print next(q)
print
e = k.Iff(k.Iff(k.Atom("a"), k.Atom("b")), k.Atom("c"))
print list(k.satisfying_assignments(e))
print
e = k.Or(k.And(a, b), k.And(c, d))
print e
print list(k.satisfying_assignments(e))

print
print "5"
print k.Atom("a").to_cnf()
print k.And(a,b).to_cnf()
print k.Or(a,b).to_cnf()
print k.Iff(a, k.Or(b, c)).to_cnf()
print k.Or(k.And(a, b), k.And(c, d)).to_cnf()
print k.Or(k.And(a, b), k.Iff(c, d)).to_cnf()

print
print "6"
kb = k.KnowledgeBase()
kb.tell(a)
kb.tell(k.Implies(a, b))
print kb.get_facts()
print kb.ask(b)
print [kb.ask(x) for x in (a, b, c)]
print
kb = k.KnowledgeBase()
kb.tell(k.Iff(a, k.Or(b, c)))
kb.tell(k.Not(a))
#print kb.ask(a)
print [kb.ask(x) for x in (a, k.Not(a))]
print [kb.ask(x) for x in (b, k.Not(b))]
print [kb.ask(x) for x in (c, k.Not(c))]

print
print "p1"
print k.kb1.get_facts()
print k.kb1.ask(k.mythical_query)
print k.kb1.ask(k.magical_query)
print k.kb1.ask(k.horned_query)

print
print "p2"
print list(k.satisfying_assignments(k.party_constraints))

print
print "p3"
print k.kb3.get_facts()
print k.kb3.ask(k.s1_query)
print k.kb3.ask(k.s2_query)
print k.kb3.ask(k.p1_query)
print k.kb3.ask(k.p2_query)
print k.kb3.ask(k.e1_query)
print k.kb3.ask(k.e2_query)

print
print "p4"
print k.kb4.ask(k.query_Adams)
print k.kb4.ask(k.query_Brown)
print k.kb4.ask(k.query_Clark)

