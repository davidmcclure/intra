import intra as i
f = open('./texts/cp.txt')

string = ''
for line in f:
    string += line

t = i.Text(string)
