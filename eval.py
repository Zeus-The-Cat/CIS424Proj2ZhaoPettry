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

#decl-list#-----------------------------
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
    else:
        print("FOUND real")
    lookahead = lexan()

def id_list():
    global lookahead
    #***check that id hasn't been declared yet in dictionary (type and id_list as key and value?)***
    #***if not add to dictionary else Syntax error exit********
    #if id not in dict:
    #    dict.update({type:id_list}) e.g., key could be 'x' or 'f', value could be 0 or 0.0
    #else:
    #    print("Syntax error")
    #    exit
    
    #DELETE WHEN FINISHED WITH ^^ ---------TO-DO--------
    print(lookahead)
    lookahead = lexan()
    if lookahead == ",":
        print("FOUND ,")
        lookahead = lexan()
        id_list()


#stmt-list#---------------------------
def stmt_list():
    global lookahead
    #do while input equals (a declared id, printi, printr)
    stmt()
    while((lookahead == id) or (lookahead == "printi" or lookahead == "printr")):
        stmt()

def stmt():
    global lookahead

    if(true): #if id in dict
        lookahead = lexan()
        if(lookahead == "="):
            lookahead = lexan()
            expr()
        else:
            print("Syntax Error AT =")
    elif(true): #if printi in dict
        expr()
    elif(true): #if printr in dict
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
    while (true):
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
    factor()
    if lookahead == "*":
        print("FOUND *")
        lookahead = lexan()
        factor()
    elif lookahead == "/":
        print("FOUND /")
        lookahead = lexan()
        factor()
    else:
        print("Syntax Error at TERM")

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
    elif(true): #if id in dict
        print(lookahead)
        lookahead = lexan() 
        #insert id into symbol table with the type t
    elif(true): #if intnum...???
        print(lookahead)
        lookahead = lexan()
    elif(true): #if realnum...???
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
    #TO DO -------------------------------------------------
    #if id not in dict:
    #    dict.update({key:value}) ***key could be 'x' or 'f', value could be 0 or 0.
    #elif intnum:
    #    print something?
    #elif realnum:
    #    print something?
    #else:
    #    print("Syntax error")
    #    exit


#main Method
file = open(sys.argv[1],"r")
wlist = file.read().split()
mitr = iter(wlist)
lookahead = lexan()

#not sure if two dictionaries are needed
#typeDict = {}
#id_listDict = {}

#OR if the one dictionary is: typeIdDict = {} with type as key, idList as value?
listTest = []
for w in wlist:
    listTest.append(w)
    
prog()

if lookahead == "":
    print("Passed")
else:
    print("Syntax Error")
