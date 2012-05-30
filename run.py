import intra as i
f = open('./texts/pl.txt')

string = ''
for line in f:
    string += line

t = i.Text(string)
