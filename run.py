import text as t
f = open('./texts/wp.txt')

string = ''
for line in f:
    string += line

text = t.Text(string)
