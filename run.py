import intra as i
f = open('./texts/wp.txt')

string = ''
for line in f:
    string += line

t = i.Text(string)
