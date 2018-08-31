import kzw5309 as k
import os

print "1"
ham_dir = "homework6_data/train/ham/"
print k.load_tokens(ham_dir+"ham1")[200:204]
print k.load_tokens(ham_dir+"ham2")[110:114]

spam_dir = "homework6_data/train/spam/"
print k.load_tokens(spam_dir+"spam1")[1:5]
print k.load_tokens(spam_dir+"spam2")[:4]

print
print "2"
paths = ["homework6_data/train/ham/ham%d" % i for i in range(1, 11)]
p = k.log_probs(paths, 1e-5)
print p["the"]
#-3.6080194731874062
print p["line"]
#-4.272995709320345

paths = ["homework6_data/train/spam/spam%d" % i for i in range(1, 11)]
p = k.log_probs(paths, 1e-5)
print p["Credit"]
print p["<UNK>"]

print
print "3"
sf = k.SpamFilter("homework6_data/train/spam", "homework6_data/train/ham", 1e-5)
print sf.is_spam("homework6_data/train/spam/spam1")
print sf.is_spam("homework6_data/train/spam/spam2")
print sf.is_spam("homework6_data/train/ham/ham1")
print sf.is_spam("homework6_data/train/ham/ham2")

print
print "4"
print sf.most_indicative_spam(5)
print sf.most_indicative_ham(5)

print
print "5"
spam_dir = "homework6_data/dev/spam"
ham_dir = "homework6_data/dev/ham"
spam_paths = [os.path.join(spam_dir, f) for f in os.listdir(spam_dir) if os.path.isfile(os.path.join(spam_dir, f))]
ham_paths = [os.path.join(ham_dir, f) for f in os.listdir(ham_dir) if os.path.isfile(os.path.join(ham_dir, f))]
pt = 0
nf = 0
for spath in spam_paths:
    if sf.is_spam(spath):
        pt += 1
    else:
        nf += 1
print pt
print nf
ft = 0
pf = 0
for hpath in ham_paths:
    if sf.is_spam(hpath):
        ft += 1
    else:
        pf += 1
print ft
print pf