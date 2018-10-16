#!/usr/bin/python3
#CIS424 Project 2
#Yiyuan Zhao
#Dakotah Pettry

#imported to allow for terminal input through sys.argv[1]

import sys

#lexan uses mitr to iterate the parsed input file until there is nothing left
def lexan():
    global mitr
    try:
        return(next(mitr))
    except StopIteration:
        return('')

def match(ch):
    global lookahead
    if ch == lookahead:
        lookahead = lexan() #matches, gives next lexeme/token
        return True
    else:
        return False

#Checks if ID via lookahead is in dict already or if it's a forbidden NAME
#if not places the ID In dict with value of NONE
def newID():
    global lookahead
    global dict
    badNames = ["printi","printr","int","real"]
    if lookahead in dict.keys():
        #ID already in dict
        print("Syntax Error: ID ALREADY IN DICT")
        exit(1)
        return False
    elif lookahead in badNames:
        #Forbidden Name
        print("Syntax Error: FORBIDDEN ID NAME")
        exit(1)
        return False
    else:
        #Success
        dict[lookahead] = None
        #print(dict)
        return True

#checks if string is real number
def is_real(tempString):
    try:
        float(tempString)
        return True
    except ValueError:
        return False

#checks if string is int number
def is_int(tempString):
    try:
        int(tempString)
        return True
    except ValueError:
        return False
#each grammar object will have its own method
#two main "parent types" -> <decl-list> <stmt-list>
def prog():
    global lookahead
    #decl_list only changes lookahead if int or real
    while (lookahead != ""):
        # print(lookahead)
        decl_list()
        #stmt_list
        stmt_list()

#decl-list#-----------------------------
def decl_list():
    global lookahead
    #do while loop
    while((lookahead == "int") or (lookahead == "real")):
        decl()

def decl():
    global lookahead
    type()
    id_list()
    if not match(";"):
        print("Error at DECL")
        #print(lookahead)

def type():
    global lookahead
    typeList = ["int","real"]
    if lookahead in typeList:
        #print("FOUND int/real")
        lookahead = lexan()


def id_list():
    global lookahead
    #***check that id hasn't been declared yet in dictionary (type and id_list as key and value?)***
    #***if not add to dictionary else Syntax error exit********
    # print(lookahead)
    if newID():
       #worked
       lookahead = lexan()
    else:
       print("Syntax Errors 1")
       exit(1)
    if match(","):
        #print("FOUND ,")
        id_list()


#stmt-list#---------------------------
def stmt_list():
    global lookahead
    global dict
    #do while input equals (a declared id, printi, printr)
    while((lookahead in dict.keys()) or (lookahead == "printi") or (lookahead == "printr")):
        #print(dict)
        stmt()

def stmt():
    global lookahead
    global dict
    global finalPrint
    if(lookahead in dict.keys()): #if id in dict
        id = lookahead
        idVal = 0.0
        lookahead = lexan()
        if(match("=")):
            idVal = expr()
            if(match(";")):
                dict[id] = idVal
            elif(match("if")):
                if(cond()):
                    dict[id] = idVal
                elif(match("else")):
                    dict[id] = expr()
                    if(not(match(";"))):
                        print("Syntax Error: missing ;")
                        exit(1)
                else:
                    print("Syntax Error: missing else statements")
                    exit(1)
        else:
            print("Syntax Error AT = ")
            exit(1)
    elif(match("printi")): #if printi in dict
        temp1 = expr()
        if(not(match(";"))):
            print("Syntax Error: missing ;")
            exit(1)
        else:
            finalPrint.append(int(temp1));
    elif(match("printr")): #if printr in dict
        temp2 = expr()
        if(not(match(";"))):
            print("Syntax Error: missing ;")
            exit(1)
        else:
            finalPrint.append(float(temp2))
    else:
        # print(lookahead)
        print("Syntax Errors 2")
        exit(1)

def expr(): #using variable v, from example in notes
    global lookahead
    v = term()
    tempList = ["+","-"]
    while (lookahead in tempList):
        if match("+"):
            #print("FOUND +")
            v += term()
        elif match("-"):
            #print("FOUND -")
            v -= term()
        else:
            print("Syntax Errors 3")
            exit(1)
    return v

def term():
    global lookahead
    v = factor()
    mdlist = ["*","/"]
    while (lookahead in mdlist):
        if match("*"):
            #print("FOUND *")
            v *= factor()
        elif match("/"):
            #print("FOUND /")
            v /= factor()
        else:
            print("Syntax Error at TERM")
            exit(1)
    return v

def factor():
    global lookahead
    v = base()
    if match("^"):
        #print("FOUND ^ ")
        v = v ** factor() #<factor> ::= <base> ^ <factor>
    return v

def base():
    global lookahead
    global dict
    if match("("): #::= ( <expr> )
        v = expr()
        if(not(match(')'))):
            print("Syntax Error: missing ) bracket")
            exit(1)
        return v
    elif(lookahead in dict.keys()): #if id in dict
        #print(lookahead)
        v = dict[lookahead]
        lookahead = lexan()
        return v
    elif(is_real(lookahead)): #if realnum
        # print(lookahead)
        v = float(lookahead)
        lookahead = lexan()
        return v
    elif(is_int(lookahead)): #if intnum
        #print(lookahead)
        v = int(lookahead)
        lookahead = lexan()
        return v
    else:
        print("Syntax error at BASE")
        exit(1)
        #print(lookahead)

def cond():
    global lookahead
    prt1 = oprnd()
    if match("<"): #<cond> ::= <oprnd> < <oprnd> |
        prt2 = oprnd()
        return prt1 < prt2
    elif match("<="): #<oprnd> <= <oprnd> |
        prt2 = oprnd()
        return prt1 <= prt2
    elif match(">"): #<oprnd> > <oprnd> |
        prt2 = oprnd()
        return prt1 > prt2
    elif match(">="): #<oprnd> >= <oprnd> |
        prt2 = oprnd()
        return prt1 >= prt2
    elif match("=="): #<oprnd> == <oprnd> |
        prt2 = oprnd()
        return prt1 == prt2
    elif match("!="): #<oprnd> != <oprnd>
        prt2 = oprnd()
        return prt1 != prt2
    else:
        print("Syntax Error at COND")
        exit(1)

def oprnd():
    global lookahead
    global dict
    #TO DO -------------------------------------------------
    if(lookahead in dict.keys()):
        temp = dict[lookahead]
        lookahead = lexan()
        return temp
    elif(is_real(lookahead)):
        temp = float(lookahead)
        lookahead = lexan()
        return temp
    else:
        print("Syntax Error: OPRND")
        exit(1)


#main Method
file = open(sys.argv[1],"r")
wlist = file.read().split()
mitr = iter(wlist)
lookahead = lexan()
#master dictionary containing variables
dict = {}
finalPrint = []
prog()
if lookahead == "":
    for line in finalPrint:
        print(line)
else:
    print("Syntax Error")
