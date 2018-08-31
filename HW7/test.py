import kzw5309 as k

print
print "1"
print k.tokenize(" This is an example. ")
print k.tokenize("'Medium-rare,' she said.")

print
print "2"
print k.ngrams(1, ["a", "b", "c"])
print k.ngrams(2, ["a", "b", "c"])
print k.ngrams(3, ["a", "b", "c"])

print
print "3"
m = k.NgramModel(1)
m.update("a b c d")
m.update("a b a b")
print m.prob((), "a")
print m.prob((), "c")
print m.prob((), "<END>")
print
m = k.NgramModel(2)
m.update("a b c d")
m.update("a b a b")
print m.prob(("<START>",), "a")
print m.prob(("b",), "c")
print m.prob(("a",), "x")

print
print "4"
m = k.NgramModel(1)
m.update("a b c d")
m.update("a b a b")
k.random.seed(1)
print [m.random_token(()) for i in range(25)]
print
m = k.NgramModel(2)
m.update("a b c d")
m.update("a b a b")
k.random.seed(2)
print [m.random_token(("<START>",)) for i in range(6)]
print [m.random_token(("b",)) for i in range(6)]

print
print "5"
m = k.NgramModel(1)
m.update("a b c d")
m.update("a b a b")
k.random.seed(1)
print m.random_text(13)

m = k.NgramModel(2)
m.update("a b c d")
m.update("a b a b")
k.random.seed(2)
print m.random_text(15)

print
print "6"
k.random.seed()
m = k.create_ngram_model(1, "frankenstein.txt")
print m.random_text(15)
m = k.create_ngram_model(2, "frankenstein.txt")
print m.random_text(15)
m = k.create_ngram_model(3, "frankenstein.txt")
print m.random_text(15)
m = k.create_ngram_model(4, "frankenstein.txt")
print m.random_text(15)
m = k.create_ngram_model(1, "brown-corpus.txt")
print m.random_text(15)

print
print "7"
m = k.NgramModel(1)
m.update("a b c d")
m.update("a b a b")
print m.perplexity("a b")
m = k.NgramModel(2)
m.update("a b c d")
m.update("a b a b")
print m.perplexity("a b")