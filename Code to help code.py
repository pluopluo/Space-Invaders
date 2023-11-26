file = open(r'Space Invaders Retrieval File.txt','r')
code_list = []
for a in file:
    code_list.append(a)

print(code_list)
## iteration through the code list
e = 0
while True:
    if e == len(code_list):
        break
    if '#' in code_list[e][0]:
        message = code_list[e]
        b = code_list[e + 1]
        if '\n' in b:
            b = b[0::-2]
        b = b + '     ' + message
        code_list[e + 1] = b
        code_list.pop(e)
    else:
        e = e + 1

file.close()
## changing the file to editing mode
file = open(r'Space Invaders Retrieval File.txt','w')
for line in code_list:
    file.write(line)
print(code_list)

        