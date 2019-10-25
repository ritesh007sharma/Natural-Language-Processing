#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 11:32:07 2019

@author: ritesh
"""
import sys

fileTransition = None
fileGenops = None
fileOper = None

#defination for transition paring.
def transitionParsing():
    words = []
    operators = []
    stack = []
    relations = []
    fPrint =[]
    
    #reading the file and printing required stuffs.
    with open(fileTransition, 'r') as f:
        i = 1
        line = f.readline()
        val = line.split()
        print(line.strip())
        for word in val[1:]:
            iN = '(' + str(i) + ')'
            words.append(str(word + iN))
            i = i + 1
        next(f)
        print("OPERATORS")
        for op in f:
            op = op.rstrip()
            print(op, end = " ")
            fPrint.append(op)
            operAndRelation = op.split('_')
            operators.append(operAndRelation)
          
    stack.append('ROOT(0)')
    
    print('\n')
    
    print("PARSING NOW")
    
    #for loop that does trasition parsing and prints.
    i = 0
    for op in operators:
        #if shift then you push word to stack.
        if(op[0] == 'Shift'):
            stack.append(words[i])
            print('Shifting word '+ words[i] + ' onto stack')
            i = i+1
        #if right arc then you gnerate relation.
        elif(op[0] == 'RightArc' and (len(stack) >= 2)):
         
            first = stack[len(stack) - 1]
            second = stack[len(stack) - 2]
            relation = second + ' -- ' + op[1] + ' --> ' + first
            relations.append(relation)
            stack.pop()
            print('Applying RightArc_' + op[1] + ' to produce relation: ' + relation)
        #if left arc then generate left arc transition relation.
        elif(op[0] == 'LeftArc' and (len(stack) >= 2)):
            first = stack[len(stack) - 1]
            second = stack[len(stack) - 2]
            relation = first + ' -- ' + op[1] + ' --> ' + second
            relations.append(relation)
            stack.pop(len(stack) - 2)
            print('Applying LeftArc_' + op[1] + ' to produce relation: ' + relation)
    print('\n')
    print('FINAL DEPENDENCY PARSE')
    for fParse in relations:
        print(fParse)

#transitionParsing()  

#checks of the 
def containsKey(dictionary, value, generate):
     if len(generate) != 0:
         for key, val in generate.items():
             dictionary.pop(key, val)
     i = 0
     mp = {}
     for items in dictionary.values():
         mp.update({i : items[0]})
         i = i + 1
     if(value in mp.values()):
         return False
     else:
         return True
     
    
#
def leftArc(stack, dictionary):
    first = stack[len(stack) - 1]
    second= stack[len(stack) - 2]
    
    for key, value in dictionary.items():
        val = value[0]
        oper = value[1]
        if(key == second and val == first):
            result = True
            break
        else:
            result = False
    return result, oper
   

def rightArc(stack, dictionary):
    first = stack[len(stack) - 1]
    second= stack[len(stack) - 2]
    
    for key, value in dictionary.items():
        val = value[0]
        oper = value[1]
        if(key == first and val == second):
            result = True
            break
        else:
            result = False
    return result, oper

#function the genrate the  gneops.
def genops():
    
    opsList = []
    with open(fileOper, 'r') as f:
        for w in f:
            l = w.rstrip()
            opsList.append(l)
            
    i = 1
    words = {}
    operatorSequence = []
    listOFMap = []
    goldParse = {}
    stack = []
    iwords = []
    relations = []
    generate = {}
    val1 = []
    val4 = []
    words.update({'0': 'ROOT(0)'})
    with open(fileGenops, 'r') as f:
        print("SENTENCE:", end= " ")
        #reading and putting required files in their slots.
        for val in f:
            iN = '(' + str(i) + ')'
            val1 = val.split()[0]
            val2 = val.split()[1]
            print(val2, end = " ")
            words.update({val1 : str(val2 + iN)})
            iwords.append(str(val2 + iN))
            val3 = val.split()[2]
            val4 = val.split()[3]
            val4 = val4.rstrip()
            listOFMap.append(val3)
            relations.append(val4)
            i = i + 1
    j = 0
    print("\nGOLD DEPENDENCIES")
    for i in listOFMap:
        first = words.get(str(i))
        second = words.get(str(j + 1))
        print(first + ' -- '+ relations[j] + ' --> ' + second)
        goldParse.update({second : [first, relations[j]]})
        
        j = j + 1
    
    print('\n')
    print("GENERATING PARSING OPERATORS")
    stack.append('ROOT(0)')

    i = 0
    #loop through the word len.
    while i <= len(iwords):
        l, operL = (leftArc(stack, goldParse))
        r, operR = (rightArc(stack, goldParse))
        #left arc doesnot require checking for head node.
        if(len(stack) >= 2 and l):
            
            first = stack[len(stack) - 1]
            second = stack[len(stack) - 2]
            generate.update({second : first})
            print('Generating LeftArc_' + operL + ' to produce relation: ' + first +' -- '+ operL+' --> '+ second)
            operatorSequence.append('LeftArc_' + operL)
            stack.pop(len(stack) - 2)
        #rightarc requires checking for head node. 
        elif(len(stack) >= 2 and r and containsKey(goldParse, stack[len(stack)-1], generate)):
        
            first = stack[len(stack) - 1]
            second = stack[len(stack) - 2]
            generate.update({first : second})
            print('Generating RightArc_' + operR + ' to produce relation: ' + second +' -- '+ operR+' --> '+ first)
            operatorSequence.append('RightArc_' + operR)
            stack.pop()
        else:
            #print shift if its not right arc or left arc. 
            if(i == len(iwords)):
                break
            stack.append(iwords[i])
            print("Shift")
            operatorSequence.append('Shift')
            i = i + 1
            
    print('\n')
    print('FINAL OPERATOR SEQUENCE')
    for i in operatorSequence:
        print(i)
     
            
if sys.argv[1] == '-simulate':
    fileTransition = sys.argv[2]
    transitionParsing()

elif sys.argv[1] == '-genops':
    fileOper = sys.argv[2]
    fileGenops = sys.argv[3]
    genops()
    
    
else:
    print("please provide required txt files.")



