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
    else: 
        print("Syntax error.")
        exit()

#each grammar object will have its own method
#two main "parent types" -> <decl-list> <stmt-list>
def prog():
    global lookahead
    #decl_list only changes lookahead if int or real
    decl_list()
    #stmt_list
    stmt_list()

#decl-list#--------------------------------
def decl_list():
    global lookahead
    #do while loop
    decl()
    while((lookahead == "int") or (lookahead == "real")):
        decl()

def decl():
    global lookahead
    type()
    id_list()
    if lookahead == ";":
        print("FOUND ;")
        lookahead = lexan()
    else:
        print("Error at DECL")
        print(lookahead)

def type():
    global lookahead
    if lookahead == "int":
        print("FOUND int")
    elif lookahead == "real":
        print("FOUND real")
    lookahead = lexan()

def id_list():
    global lookahead
    #***check that id hasn't been declared yet in dictionary (type and id_list as key and value?)***
    #***if not add to dictionary else Syntax error exit********
    if id not in typeIdDict:
        typeIdDict.update({id:0})
    else:
        print("Syntax error")
        exit

    print(lookahead)
    lookahead = lexan()
    if lookahead == ",":
        print("FOUND ,")
        lookahead = lexan()
        id_list()


#stmt-list#------------------------------
def stmt_list():
    global lookahead
    #do while input equals (a declared id, printi, printr)
    stmt()
    while((lookahead == id) or (lookahead == "printi" or lookahead == "printr")):
        stmt()

def stmt():
    global lookahead

    if(id in typeIdDict): #if id in dict
        lookahead = lexan()
        if(lookahead == "="):
            lookahead = lexan()
            expr()
        else:
            print("Syntax Error AT =")
    elif("printi" in typeIdDict): #if printi in dict
        expr()
    elif("printr" in typeIdDict): #if printr in dict
        expr()
        
    else:
        print("Syntax Error AT STMT")

    if(lookahead == ";"):
        lookahead = lexan()
    else:
        print("Syntax Error AT STMT-;")

def expr(): #using variable v, from example in notes
    global lookahead
    v = term()
    while ((lookahead == "+") or (lookahead == "-")): 
    #need a third 'or' statement, for when lookahead == <term> 
    #but idk how to word that
        if lookahead == "+":
            print("FOUND +")
            match('+')
            v += term()
            #lookahead = lexan()
            #term()
        elif lookahead == "-":
            print("FOUND -")
            match('-')
            v -= term()
            #lookahead = lexan()
            #term()
        else: 
            print("Syntax Error at EXPR")
            return v

def term():
    global lookahead
    v = factor()
    while ((lookahead == "*") or (lookahead == "/")):
    #need a lookahead == <factor> in while loop
        if lookahead == "*":
            print("FOUND *")
            match("*")
            v *= factor()
            #lookahead = lexan()
            #factor()
        elif lookahead == "/":
            print("FOUND /")
            match("/")
            v /= factor()
            #lookahead = lexan()
            #factor()
        else:
            print("Syntax Error at TERM")
            return v

def factor():
    global lookahead
    v = base()
    if lookahead == "^":
        print("FOUND ^")
        lookahead = lexan()
        v = v ** factor() #<factor> ::= <base> ^ <factor>

def base():
    global lookahead
    if lookahead == "(":
        match('(')
        lookahead = lexan()
        expr()
        match(')')
        #not sure if I need to include ")" part of " ( <expr> )
    elif(id in typeIdDict): #if id in dict
        print(lookahead)
        lookahead = lexan() 
        #insert id into symbol table with the type t
    elif("intnum" in typeIdDict): #if intnum...???
        print(lookahead)
        lookahead = lexan()
    elif("realnum" in typeIdDict): #if realnum...???
        print(lookahead)
        lookahead = lexan()
        
    else:
        print("Syntax error at BASE")

def cond():
    global lookahead
    oprnd()
    if lookahead == "<": #<cond> ::= <oprnd> < <oprnd> |
        lookahead = lexan()
        oprnd()
    elif lookahead == "<=": #<oprnd> <= <oprnd> |
        lookahead = lexan()
        oprnd()
    elif lookahead == ">": #<oprnd> > <oprnd> |
        lookahead = lexan()
        oprnd()
    elif lookahead == ">=": #<oprnd> >= <oprnd> |
        lookahead = lexan()
        oprnd()
    elif lookahead == "==": #<oprnd> == <oprnd> |
        lookahead = lexan()
        oprnd()
    elif lookahead == "!=": #<oprnd> != <oprnd>
        lookahead = lexan()
        oprnd()
        
    else: 
        print("Syntax Error at COND")

def oprnd():
    global lookahead
    if id not in typeIdDict:
        typeIdDict.update({id:0})
    elif "intnum" in typeIdDict:
        print("Integer Number")
    elif "realnum" in typeIdDict:
        print("Real Number")
        exit

#main method
#file = open(sys.argv[1],"r")
file = open("test.txt","r")
wlist = file.read().split()
mitr = iter(wlist)
lookahead = lexan()

#not sure if two dictionaries are needed to implement symbol table
#dictionary for storing variables & for looking them up
#typeDict = {}
#id_listDict = {}

#OR one dictionary with type as key, idList as value?
listTest = []
typeIdDict = {} 
for w in wlist:
    listTest.append(w)

typeIdDict = { i: 0 for i in listTest }
    
prog()

if lookahead == "":
    print("Passed")
else:
    print("Syntax Error")
