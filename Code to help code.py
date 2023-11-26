# opening the file
code_file = open(r'Space Invaders Retrieval File.txt','r')

## creating a list with all the contents
code_list = []
for line in code_file:
    code_list.append(line)

## iteration through the code list
code_iteration_counter = 0

while True:
    if code_iteration_counter == len(code_list):
        break
    if '#' in code_list[code_iteration_counter][0]:
        message = code_list[code_iteration_counter]
        b = code_list[code_iteration_counter + 1]

        letter_list = ['a','b','c','d','e','f','g','h','i','j',
                       'k','l','m','n','o','o','q','r','s','t','u','v','w','x','y','z']
        number_list = ['1','2','3','4','5','6','7','8','9','0']
        for i in letter_list:
            if i not in b:
                for i in number_list:
                    if i not in b:
                        c = True
        if c == True:
            if  '\n' in b:
                b = b[0::-2]
                b = b + '     ' + message
                code_list[code_iteration_counter + 1] = b
                code_list.pop(code_iteration_counter)
                c = False
            else:
                c = False
                code_iteration_counter = code_iteration_counter+ 1
        else:
           code_iteration_counter = code_iteration_counter+ 1
    else:
       code_iteration_counter = code_iteration_counter+ 1

code_file.close()

## changing the file to editing mode
a = open(r'Space Invaders End file.txt','w')
for line in code_list:
    a.write(line)
print(code_list)

        