import kzw5309 as k

print "1"
c = k.load_corpus('brown-corpus.txt')
print c[1402]
print c[1799]

print
print "2 & 3"
t = k.Tagger(c)
print t.most_probable_tags(["The", "man", "walks", "."])
print t.most_probable_tags(["The", "blue", "bird", "sings"])
print t.most_probable_tags(["Pandiculation", "blue", "bird", "sings"])

print
print "4"
s = "I am waiting to reply".split()
print s
print t.most_probable_tags(s)
print t.viterbi_tags(s)
print
s = "I saw the play".split()
print s
print t.most_probable_tags(s)
print t.viterbi_tags(s)
print
s = "I get a check from the boss .".split()
print s
print t.most_probable_tags(s)
print t.viterbi_tags(s)
print
s = "I test my result".split()
print s
print t.most_probable_tags(s)
print t.viterbi_tags(s)