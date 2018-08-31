import kzw5309


def f(a):
    return [a]


def p(b):
    return b != 'a'

test11 = ["a", 2, "c", ('b','c')]
test121 = [[1,2],[3,4]]
test122 = ["abc", (0,[0])]
test131 = [[1,2,3]]
test132 = [[1,2], [3,4], [5,6]]

test211 = (1,2,3)
test212 = [0,0,0]
test22 = ["abc", (1,2,3), "", []]
test23 = [[1,2,3,4,5], [1,2,3,4,5,6], "abcde", "abcdef"]

test31 = [[1,2,3],"abc"]
test32 = [[1,2,3], "abc"]

test41 = ["This is an example", "   Extra  SPACE   "]
test42 = ["This Is An Example", "We love Python"]
test43 = ["Zip Code: 19104", "Pi is 3.1415..."]
test44 = ["to_mixed_case", "_EXAMPLE__NAME__"]

print kzw5309.extract_and_apply(test11, p, f)
print kzw5309.concatenate(test121)
print kzw5309.concatenate(test122)
print kzw5309.transpose(test131)
print kzw5309.transpose(test132)

print kzw5309.copy(test211)
print kzw5309.copy(test212)
test212[0]=1
print test212
print [kzw5309.all_but_last(x) for x in test22]
print [kzw5309.every_other(x) for x in test23]

print [list(kzw5309.prefixes(x)) for x in test31]
print [list(kzw5309.suffixes(x)) for x in test31]
print [list(kzw5309.slices(x)) for x in test32]

print [kzw5309.normalize(x) for x in test41]
print [kzw5309.no_vowels(x) for x in test42]
print [kzw5309.digits_to_words(x) for x in test43]
print [kzw5309.to_mixed_case(x) for x in test44]

p = kzw5309.Polynomial([(2,1), (1,0)])
q = kzw5309.Polynomial([(4,3), (3,2)])
p81 = kzw5309.Polynomial([(1,1), (1,0)])
p82 = kzw5309.Polynomial([(0,1),(2,3)])
p83 = kzw5309.Polynomial([(1,1),(2,3)])

print p
print q
print p.get_polynomial()
t = -p; print t.get_polynomial()
t = -(-p); print t.get_polynomial()
t = p + p; print t.get_polynomial()
r = p + q; print r.get_polynomial()
t = p - p; print t.get_polynomial()
r = p - q; print r.get_polynomial()
t = p * p; print t.get_polynomial()
r = p * q; print r.get_polynomial()
print [p(x) for x in range(5)]
q = -(p * p) + p
print [q(x) for x in range(5)]
t = -p + (p * p); print t.get_polynomial()
t.simplify(); print t.get_polynomial()
r = p - p; print r.get_polynomial()
r.simplify(); print r.get_polynomial()
p = kzw5309.Polynomial([(1, 1), (1, 0)])
qs = (p, p + p, -p, -p - p, p * p)
for q in qs: q.simplify(); print str(q)
p = kzw5309.Polynomial([(0, 1), (2, 3)])
print str(p); print str(p * p); print str(-p * p)
q = kzw5309.Polynomial([(1, 1), (2, 3)])
print str(q); print str(q * q); print str(-q * q)
print "separate"

p, q = kzw5309.Polynomial([(2,1),(1,0)]), kzw5309.Polynomial([(2,1), (-1,0)])
print p; print q

r = (p * p) + (q * q) - (p * q); print r

r.simplify(); print r
print [(x, r(x)) for x in range(-4, 5)]

