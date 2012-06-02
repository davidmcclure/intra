import text as t
f = open('./texts/cp.txt')

string = ''
for line in f:
    string += line

text = t.Text(string)
