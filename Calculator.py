from tkinter import *
from mpmath import *
root=Tk()

root.title("Calculator")

calculation_entry=Entry(root)
calculation_entry.insert(0,"0")
calculation_entry.config(state="disabled")
calculation_entry.grid(row=0,column=0,columnspan=5)

click=False

class Custom_Button:
    def __init__(self,name,row,column):
        self.name=name
        self.row=row
        self.column=column
    def draw_button(self):
        num_button=Button(root,text=self.name,command=self.button_clicked)
        num_button.grid(row=self.row,column=self.column)
    def button_clicked(self):
        global click
        calculation_entry.config(state="normal")
        if click==False:
            calculation_entry.delete(0,END)
            click=True
        if self.name=="=":
            total=calculation_entry.get()
            if "^" in total:
                total=total.replace("^","**")
            if "√" in total:
                calculation_entry.insert(END,")")
            total=calculation_entry.get()
            total=total.replace("√","sqrt(")
            if "!" in total:
                calculation_entry.insert(0,"fac(")
            total=calculation_entry.get()
            total=total.replace("!",")")
            if "π" in total:
                total=total.replace("π","pi")
            if "|" in total:
                total=total.replace("|","fabs(",1)
                total=total.replace("|",")",2)
            output=eval(total)
            calculation_entry.delete(0,END)
            calculation_entry.insert(0,output)
            calculation_entry.config(state="disabled")
            click=False
        elif self.name=="⌫":
            calculation_entry.delete(len(calculation_entry.get())-1,END)
        if len(calculation_entry.get())==0:
            calculation_entry.insert(0,"0")
            click=False
            calculation_entry.config(state="disabled")
        elif self.name=="C":
            calculation_entry.delete(0,END)
            calculation_entry.insert(0,"0")
            calculation_entry.config(state="disabled")
            click=False
        else:
            calculation_entry.insert(END,self.name)
            calculation_entry.config(state="disabled")

buttons=[]
options=["⌫","C"]
symbols=["+","^","(",")","-","√","π","e","*","|","j","!",".","=","/"]
functions=["sin","cos","tan","csc","sec","cot","log","asin","acos","atan","acsc","asec","acot","ln","sinh","cosh","tanh","csch","sech","coth","asinh","acosh","atanh","acsch","asech","acoth"]

o=0
a=1
d=1
s=0
f=0

for c in range(5,7,1):
b=Custom_Button(options[o],0,c)
b.draw_button()
buttons.append(b)
o+=1

for r in range(1,9,1):
    for c in range(0,7,1):
        if d in [4,5,6,7,11,12,13,14,18,19,20,21,22,24,25]:
            b=Custom_Button(symbols[s],r,c)
            b.draw_button()
            buttons.append(b)
            s+=1
        elif d==23:
            b=Custom_Button("0",r,c)
            b.draw_button()
            buttons.append(b)
        elif d in [29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,50,51,52,53,54,55]:
            b=Custom_Button(functions[f],r,c)
            b.draw_button()
            buttons.append(b)
            f+=1
        elif d in [26,27,28,49,56]:
            print()
        else:
            b=Custom_Button(a,r,c)
            b.draw_button()
            buttons.append(b)
            a+=1
            d+=1

root.mainloop()
from tkinter import *
from mpmath import *
root=Tk()

root.title("Calculator")

calculation_entry=Entry(root)
calculation_entry.insert(0,"0")
calculation_entry.config(state="disabled")
calculation_entry.grid(row=0,column=0,columnspan=5)

click=False

class Custom_Button:
def __init__(self,name,row,column):
self.name=name
self.row=row
self.column=column
def draw_button(self):
num_button=Button(root,text=self.name,command=self.button_clicked)
num_button.grid(row=self.row,column=self.column)
def button_clicked(self):
global click
calculation_entry.config(state="normal")
if click==False:
calculation_entry.delete(0,END)
click=True
if self.name=="=":
total=calculation_entry.get()
if "^" in total:
total=total.replace("^","**")
if "√" in total:
calculation_entry.insert(END,")")
total=calculation_entry.get()
total=total.replace("√","sqrt(")
if "!" in total:
calculation_entry.insert(0,"fac(")
total=calculation_entry.get()
total=total.replace("!",")")
if "π" in total:
total=total.replace("π","pi")
if "|" in total:
total=total.replace("|","fabs(",1)
total=total.replace("|",")",2)
output=eval(total)
calculation_entry.delete(0,END)
calculation_entry.insert(0,output)
calculation_entry.config(state="disabled")
click=False
elif self.name=="⌫":
calculation_entry.delete(len(calculation_entry.get())-1,END)
if len(calculation_entry.get())==0:
calculation_entry.insert(0,"0")
click=False
calculation_entry.config(state="disabled")
elif self.name=="C":
calculation_entry.delete(0,END)
calculation_entry.insert(0,"0")
calculation_entry.config(state="disabled")
click=False
else:
calculation_entry.insert(END,self.name)
calculation_entry.config(state="disabled")

buttons=[]
options=["⌫","C"]
symbols=["+","^","(",")","-","√","π","e","*","|","j","!",".","=","/"]
functions=["sin","cos","tan","csc","sec","cot","log","asin","acos","atan","acsc","asec","acot","ln","sinh","cosh","tanh","csch","sech","coth","asinh","acosh","atanh","acsch","asech","acoth"]

o=0
a=1
d=1
s=0
f=0

for c in range(5,7,1):
b=Custom_Button(options[o],0,c)
b.draw_button()
buttons.append(b)
o+=1

for r in range(1,9,1):
for c in range(0,7,1):
if d in [4,5,6,7,11,12,13,14,18,19,20,21,22,24,25]:
b=Custom_Button(symbols[s],r,c)
b.draw_button()
buttons.append(b)
s+=1
elif d==23:
b=Custom_Button("0",r,c)
b.draw_button()
buttons.append(b)
elif d in [29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,50,51,52,53,54,55]:
b=Custom_Button(functions[f],r,c)
b.draw_button()
buttons.append(b)
f+=1
elif d in [26,27,28,49,56]:
print()
else:
b=Custom_Button(a,r,c)
b.draw_button()
buttons.append(b)
a+=1
d+=1

root.mainloop()
from tkinter import *
from mpmath import *
root=Tk()

root.title("Advanced Calculator")

calculation_entry=Entry(root)
calculation_entry.insert(0,"0")
calculation_entry.config(state="disabled")
calculation_entry.grid(row=0,column=0,columnspan=5)

click=False

class Custom_Button:
def __init__(self,name,row,column):
self.name=name
self.row=row
self.column=column
def draw_button(self):
num_button=Button(root,text=self.name,command=self.button_clicked)
num_button.grid(row=self.row,column=self.column)
def button_clicked(self):
global click
calculation_entry.config(state="normal")
if click==False:
calculation_entry.delete(0,END)
click=True
if self.name=="=":
total=calculation_entry.get()
if "^" in total:
total=total.replace("^","**")
if "√" in total:
calculation_entry.insert(END,")")
total=calculation_entry.get()
total=total.replace("√","sqrt(")
if "!" in total:
calculation_entry.insert(0,"fac(")
total=calculation_entry.get()
total=total.replace("!",")")
if "π" in total:
total=total.replace("π","pi")
if "|" in total:
total=total.replace("|","fabs(",1)
total=total.replace("|",")",2)
output=eval(total)
calculation_entry.delete(0,END)
calculation_entry.insert(0,output)
calculation_entry.config(state="disabled")
click=False
elif self.name=="⌫":
calculation_entry.delete(len(calculation_entry.get())-1,END)
if len(calculation_entry.get())==0:
calculation_entry.insert(0,"0")
click=False
calculation_entry.config(state="disabled")
elif self.name=="C":
calculation_entry.delete(0,END)
calculation_entry.insert(0,"0")
calculation_entry.config(state="disabled")
click=False
else:
calculation_entry.insert(END,self.name)
calculation_entry.config(state="disabled")

buttons=[]
options=["⌫","C"]
symbols=["+","^","(",")","-","√","π","e","*","|","j","!",".","=","/"]
functions=["sin","cos","tan","csc","sec","cot","log","asin","acos","atan","acsc","asec","acot","ln","sinh","cosh","tanh","csch","sech","coth","asinh","acosh","atanh","acsch","asech","acoth"]

o=0
a=1
d=1
s=0
f=0

for c in range(5,7,1):
b=Custom_Button(options[o],0,c)
b.draw_button()
buttons.append(b)
o+=1

for r in range(1,9,1):
for c in range(0,7,1):
if d in [4,5,6,7,11,12,13,14,18,19,20,21,22,24,25]:
b=Custom_Button(symbols[s],r,c)
b.draw_button()
buttons.append(b)
s+=1
elif d==23:
b=Custom_Button("0",r,c)
b.draw_button()
buttons.append(b)
elif d in [29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,50,51,52,53,54,55]:
b=Custom_Button(functions[f],r,c)
b.draw_button()
buttons.append(b)
f+=1
elif d in [26,27,28,49,56]:
print()
else:
b=Custom_Button(a,r,c)
b.draw_button()
buttons.append(b)
a+=1
d+=1

root.mainloop()
from tkinter import *
from mpmath import *
root=Tk()

root.title("Advanced Calculator")

calculation_entry=Entry(root)
calculation_entry.insert(0,"0")
calculation_entry.config(state="disabled")
calculation_entry.grid(row=0,column=0,columnspan=5)

click=False

class Custom_Button:
def __init__(self,name,row,column):
self.name=name
self.row=row
self.column=column
def draw_button(self):
num_button=Button(root,text=self.name,command=self.button_clicked)
num_button.grid(row=self.row,column=self.column)
def button_clicked(self):
global click
calculation_entry.config(state="normal")
if click==False:
calculation_entry.delete(0,END)
click=True
if self.name=="=":
total=calculation_entry.get()
if "^" in total:
total=total.replace("^","**")
if "√" in total:
calculation_entry.insert(END,")")
total=calculation_entry.get()
total=total.replace("√","sqrt(")
if "!" in total:
calculation_entry.insert(0,"fac(")
total=calculation_entry.get()
total=total.replace("!",")")
if "π" in total:
total=total.replace("π","pi")
if "|" in total:
total=total.replace("|","fabs(",1)
total=total.replace("|",")",2)
output=eval(total)
calculation_entry.delete(0,END)
calculation_entry.insert(0,output)
calculation_entry.config(state="disabled")
click=False
elif self.name=="⌫":
calculation_entry.delete(len(calculation_entry.get())-1,END)
if len(calculation_entry.get())==0:
calculation_entry.insert(0,"0")
click=False
calculation_entry.config(state="disabled")
elif self.name=="C":
calculation_entry.delete(0,END)
calculation_entry.insert(0,"0")
calculation_entry.config(state="disabled")
click=False
else:
calculation_entry.insert(END,self.name)
calculation_entry.config(state="disabled")

buttons=[]
options=["⌫","C"]
symbols=["+","^","(",")","-","√","π","e","*","|","j","!",".","=","/"]
functions=["sin","cos","tan","csc","sec","cot","log","asin","acos","atan","acsc","asec","acot","ln","sinh","cosh","tanh","csch","sech","coth","asinh","acosh","atanh","acsch","asech","acoth"]

o=0
a=1
d=1
s=0
f=0

for c in range(5,7,1):
b=Custom_Button(options[o],0,c)
b.draw_button()
buttons.append(b)
o+=1

for r in range(1,9,1):
for c in range(0,7,1):
if d in [4,5,6,7,11,12,13,14,18,19,20,21,22,24,25]:
b=Custom_Button(symbols[s],r,c)
b.draw_button()
buttons.append(b)
s+=1
elif d==23:
b=Custom_Button("0",r,c)
b.draw_button()
buttons.append(b)
elif d in [29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,50,51,52,53,54,55]:
b=Custom_Button(functions[f],r,c)
b.draw_button()
buttons.append(b)
f+=1
elif d in [26,27,28,49,56]:
print()
else:
b=Custom_Button(a,r,c)
b.draw_button()
buttons.append(b)
a+=1
d+=1

root.mainloop()
from tkinter import *
from mpmath import *
root=Tk()

root.title("Advanced Calculator")

calculation_entry=Entry(root)
calculation_entry.insert(0,"0")
calculation_entry.config(state="disabled")
calculation_entry.grid(row=0,column=0,columnspan=5)

click=False

class Custom_Button:
def __init__(self,name,row,column):
self.name=name
self.row=row
self.column=column
def draw_button(self):
num_button=Button(root,text=self.name,command=self.button_clicked)
num_button.grid(row=self.row,column=self.column)
def button_clicked(self):
global click
calculation_entry.config(state="normal")
if click==False:
calculation_entry.delete(0,END)
click=True
if self.name=="=":
total=calculation_entry.get()
if "^" in total:
total=total.replace("^","**")
if "√" in total:
calculation_entry.insert(END,")")
total=calculation_entry.get()
total=total.replace("√","sqrt(")
if "!" in total:
calculation_entry.insert(0,"fac(")
total=calculation_entry.get()
total=total.replace("!",")")
if "π" in total:
total=total.replace("π","pi")
if "|" in total:
total=total.replace("|","fabs(",1)
total=total.replace("|",")",2)
output=eval(total)
calculation_entry.delete(0,END)
calculation_entry.insert(0,output)
calculation_entry.config(state="disabled")
click=False
elif self.name=="⌫":
calculation_entry.delete(len(calculation_entry.get())-1,END)
if len(calculation_entry.get())==0:
calculation_entry.insert(0,"0")
click=False
calculation_entry.config(state="disabled")
elif self.name=="C":
calculation_entry.delete(0,END)
calculation_entry.insert(0,"0")
calculation_entry.config(state="disabled")
click=False
else:
calculation_entry.insert(END,self.name)
calculation_entry.config(state="disabled")

buttons=[]
options=["⌫","C"]
symbols=["+","^","(",")","-","√","π","e","*","|","j","!",".","=","/"]
functions=["sin","cos","tan","csc","sec","cot","log","asin","acos","atan","acsc","asec","acot","ln","sinh","cosh","tanh","csch","sech","coth","asinh","acosh","atanh","acsch","asech","acoth"]

o=0
a=1
d=1
s=0
f=0

for c in range(5,7,1):
b=Custom_Button(options[o],0,c)
b.draw_button()
buttons.append(b)
o+=1

for r in range(1,9,1):
for c in range(0,7,1):
if d in [4,5,6,7,11,12,13,14,18,19,20,21,22,24,25]:
b=Custom_Button(symbols[s],r,c)
b.draw_button()
buttons.append(b)
s+=1
elif d==23:
b=Custom_Button("0",r,c)
b.draw_button()
buttons.append(b)
elif d in [29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,50,51,52,53,54,55]:
b=Custom_Button(functions[f],r,c)
b.draw_button()
buttons.append(b)
f+=1
elif d in [26,27,28,49,56]:
print()
else:
b=Custom_Button(a,r,c)
b.draw_button()
buttons.append(b)
a+=1
d+=1

root.mainloop()
from tkinter import *
from mpmath import *
root=Tk()

root.title("Advanced Calculator")

calculation_entry=Entry(root)
calculation_entry.insert(0,"0")
calculation_entry.config(state="disabled")
calculation_entry.grid(row=0,column=0,columnspan=5)

click=False

class Custom_Button:
def __init__(self,name,row,column):
self.name=name
self.row=row
self.column=column
def draw_button(self):
num_button=Button(root,text=self.name,command=self.button_clicked)
num_button.grid(row=self.row,column=self.column)
def button_clicked(self):
global click
calculation_entry.config(state="normal")
if click==False:
calculation_entry.delete(0,END)
click=True
if self.name=="=":
total=calculation_entry.get()
if "^" in total:
total=total.replace("^","**")
if "√" in total:
calculation_entry.insert(END,")")
total=calculation_entry.get()
total=total.replace("√","sqrt(")
if "!" in total:
calculation_entry.insert(0,"fac(")
total=calculation_entry.get()
total=total.replace("!",")")
if "π" in total:
total=total.replace("π","pi")
if "|" in total:
total=total.replace("|","fabs(",1)
total=total.replace("|",")",2)
output=eval(total)
calculation_entry.delete(0,END)
calculation_entry.insert(0,output)
calculation_entry.config(state="disabled")
click=False
elif self.name=="⌫":
calculation_entry.delete(len(calculation_entry.get())-1,END)
if len(calculation_entry.get())==0:
calculation_entry.insert(0,"0")
click=False
calculation_entry.config(state="disabled")
elif self.name=="C":
calculation_entry.delete(0,END)
calculation_entry.insert(0,"0")
calculation_entry.config(state="disabled")
click=False
else:
calculation_entry.insert(END,self.name)
calculation_entry.config(state="disabled")

buttons=[]
options=["⌫","C"]
symbols=["+","^","(",")","-","√","π","e","*","|","j","!",".","=","/"]
functions=["sin","cos","tan","csc","sec","cot","log","asin","acos","atan","acsc","asec","acot","ln","sinh","cosh","tanh","csch","sech","coth","asinh","acosh","atanh","acsch","asech","acoth"]

o=0
a=1
d=1
s=0
f=0

for c in range(5,7,1):
b=Custom_Button(options[o],0,c)
b.draw_button()
buttons.append(b)
o+=1

for r in range(1,9,1):
for c in range(0,7,1):
if d in [4,5,6,7,11,12,13,14,18,19,20,21,22,24,25]:
b=Custom_Button(symbols[s],r,c)
b.draw_button()
buttons.append(b)
s+=1
elif d==23:
b=Custom_Button("0",r,c)
b.draw_button()
buttons.append(b)
elif d in [29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,50,51,52,53,54,55]:
b=Custom_Button(functions[f],r,c)
b.draw_button()
buttons.append(b)
f+=1
elif d in [26,27,28,49,56]:
print()
else:
b=Custom_Button(a,r,c)
b.draw_button()
buttons.append(b)
a+=1
d+=1

root.mainloop()
from tkinter import *
from mpmath import *
root=Tk()

root.title("Advanced Calculator")

calculation_entry=Entry(root)
calculation_entry.insert(0,"0")
calculation_entry.config(state="disabled")
calculation_entry.grid(row=0,column=0,columnspan=5)

click=False

class Custom_Button:
def __init__(self,name,row,column):
self.name=name
self.row=row
self.column=column
def draw_button(self):
num_button=Button(root,text=self.name,command=self.button_clicked)
num_button.grid(row=self.row,column=self.column)
def button_clicked(self):
global click
calculation_entry.config(state="normal")
if click==False:
calculation_entry.delete(0,END)
click=True
if self.name=="=":
total=calculation_entry.get()
if "^" in total:
total=total.replace("^","**")
if "√" in total:
calculation_entry.insert(END,")")
total=calculation_entry.get()
total=total.replace("√","sqrt(")
if "!" in total:
calculation_entry.insert(0,"fac(")
total=calculation_entry.get()
total=total.replace("!",")")
if "π" in total:
total=total.replace("π","pi")
if "|" in total:
total=total.replace("|","fabs(",1)
total=total.replace("|",")",2)
output=eval(total)
calculation_entry.delete(0,END)
calculation_entry.insert(0,output)
calculation_entry.config(state="disabled")
click=False
elif self.name=="⌫":
calculation_entry.delete(len(calculation_entry.get())-1,END)
if len(calculation_entry.get())==0:
calculation_entry.insert(0,"0")
click=False
calculation_entry.config(state="disabled")
elif self.name=="C":
calculation_entry.delete(0,END)
calculation_entry.insert(0,"0")
calculation_entry.config(state="disabled")
click=False
else:
calculation_entry.insert(END,self.name)
calculation_entry.config(state="disabled")

buttons=[]
options=["⌫","C"]
symbols=["+","^","(",")","-","√","π","e","*","|","j","!",".","=","/"]
functions=["sin","cos","tan","csc","sec","cot","log","asin","acos","atan","acsc","asec","acot","ln","sinh","cosh","tanh","csch","sech","coth","asinh","acosh","atanh","acsch","asech","acoth"]

o=0
a=1
d=1
s=0
f=0

for c in range(5,7,1):
b=Custom_Button(options[o],0,c)
b.draw_button()
buttons.append(b)
o+=1

for r in range(1,9,1):
for c in range(0,7,1):
if d in [4,5,6,7,11,12,13,14,18,19,20,21,22,24,25]:
b=Custom_Button(symbols[s],r,c)
b.draw_button()
buttons.append(b)
s+=1
elif d==23:
b=Custom_Button("0",r,c)
b.draw_button()
buttons.append(b)
elif d in [29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,50,51,52,53,54,55]:
b=Custom_Button(functions[f],r,c)
b.draw_button()
buttons.append(b)
f+=1
elif d in [26,27,28,49,56]:
print()
else:
b=Custom_Button(a,r,c)
b.draw_button()
buttons.append(b)
a+=1
d+=1

root.mainloop()