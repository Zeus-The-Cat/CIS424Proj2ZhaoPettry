#!/usr/bin/python3
#imported to allow for terminal input through sys.argv[1]

import sys

#lexan uses mitr to iterate the parsed input file until there is nothing left
def lexan():
    global mitr
    try:
        return(next(mitr))
    except StopIteration:
        return('')

#each grammar object will have it's own method
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
    #***Need to make this a do while loop****
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
    #***check that id hasn't been declared yet in dictionary***
    #***if not add to dictionary else Syntax error exit********
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
    #***MAKES THIS A DO WHILE LOOP***-------TO-DO-------------
    stmt()

def stmt():
    global lookahead
        #if id in dictionary
        if(true):
            lookahead = lexan()
            if(lookahead == "="):
                lookahead = lexan()
                expr()
            else:
                print("Syntax Error AT =")
        #if printi
        else if(true):
            continue
        #if printr
        else if(true):
            continue
        else:
            print("Syntax Error AT STMT")

        if(lookahead == ";"):
            lookahead = lexan()
        else:
            print("Syntax Error AT STMT-;")

def expr():
    global lookahead
    #START HERE DAKOTAH <--------------------------------

def term():
    global lookahead

def factor():
    global lookahead

def base():
    global lookahead

def cond():
    global lookahead

def oprnd():
    global lookahead

#main Method
file = open(sys.argv[1],"r")
wlist = file.read().split()
mitr = iter(wlist)
lookahead = lexan()
prog()

if lookahead == "":
    print("Passed")
else:
    print("Syntax Error")
