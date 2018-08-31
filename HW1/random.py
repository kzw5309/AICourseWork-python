def simplify(a):
    d = {}
    for x, y in a:
        d[y] = d.get(y, 0) + x
    print d.items()
    result = zip(d.values(),d.keys())
    result = sorted(result, key=lambda item: item[1], reverse=True)
    result = tuple((x, y) for x, y in result if x != 0)
    if len(result) == 0:
        result = ((0, 0),)
    print result


def show(self):
    temp = self
    container = []
    for i in xrange(len(temp)):
        if temp[i][0] < 0:
            container.append('-')
            if i > 0:
                container.append(' ')
        elif i > 0:
            container.append('+')
            container.append(' ')
        if temp[i][0] != 1 or temp[i][1] == 0:
            container.append(str(temp[i][0]))
        if temp[i][1] > 0:
            container.append('x')
        if temp[i][1] > 1:
            container.append('^')
            container.append(str(temp[i][1]))
        if i < len(temp)-1:
            container.append(" ")
    return "".join(container)

p1 = kzw5309.Polynomial([(2,1), (1,0)])
q = kzw5309.Polynomial([(4,3), (3,2)])
p81 = kzw5309.Polynomial([(1,1), (1,0)])
p82 = kzw5309.Polynomial([(0,1),(2,3)])
p83 = kzw5309.Polynomial([(1,1),(2,3)])