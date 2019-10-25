#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 11:53:03 2019
Assignment 1 Natural language Processing.
@author: ritesh
"""
import itertools
import math
from collections import Counter
import sys

training_file = None
test_file = None


if sys.argv[2] == '-test':
    training_file = sys.argv[1]
    test_file = sys.argv[3]
else:
    print("please provide required txt files.")

def main():

    #####reading data please specify file path if not working.
    with open(training_file, 'r') as inputFile:
        training_data = inputFile.readlines()
        
                
#####Unigram Processing#######
    unigramsList = []
    biagramData = []
    biagramList = []

    count = len(training_data)

    for val in training_data:
        lowerCase = val.lower()
        strip = lowerCase.strip()
        removeEndLine = strip.replace("\n","")
        splitData = removeEndLine.split(" ")
        dataArray = removetSpaces(splitData)
        unigramsList.append(dataArray)
    

    vocabularyR = []

    vocabularyR = list(itertools.chain(*unigramsList))

    unigramVocabulary = Counter(vocabularyR)
    unigramsTotalFrequency = sum(unigramVocabulary.values())
    BUV = Counter(vocabularyR)
    BUV['#'] = count

                            
######biagram processing#######

    for val in training_data:
        lowerCase = val.lower()
        strip = lowerCase.strip()
        removeEndLine = strip.replace("\n","")
        biagramData.append(removeEndLine)
    
    for val in biagramData:
        first = val.split(" ")
        first = removetSpaces(first)
        first.insert(0, "#")
        for i in range(0, len(first) - 1):
            biagrams = (first[i], first[i+1])
            biagramList.append(biagrams)
 
    BV = Counter(biagramList)


    with open(test_file, 'r') as inputFile2:
        test_data = inputFile2.readlines()   

    testData=[]
    
########This section is used to print values.############
    for data in test_data:
        data1=data.lower();
        data2=data1.replace("\n","")
        testData.append(data2)
        
    for i in range(0, len(testData)):
    #unigramProbabilty(cleaned_data[i])
        print('S = ', test_data[i])
        print("Unsmoothed Unigrams, logprob(S) =",unigramProbabilty(testData[i], unigramVocabulary, unigramsTotalFrequency))
        print("Unsmoothed Bigrams, logprob(S) =",biagramProb(testData[i], BV, BUV))
        print("Smoothed Bigrams, logprob(S) =",smoothedBiagramProb(testData[i], unigramVocabulary, BV, BUV))
                           

#This function removes spaces from the data.                           
def removetSpaces(arr):
    newArr = []
    for i in arr:
       if i != '':
           newArr.append(i)
    
    return newArr
                            
###Unigram Probability Function
    #This Funtion calculates the unigram probabilityt function.
def unigramProbabilty(sentence, unigramVocabulary, unigramsTotalFrequency):
    prob = 0
    arr = sentence.split(" ")
    arr = removetSpaces(arr)
    for i in range(0, len(arr)):
        a = unigramVocabulary[arr[i]]
        b = unigramsTotalFrequency
    
        if a == 0:
            return 'undefined'
            break;
        else:
            
            prob += math.log(a/float(b), 2)
    
    return round(prob, 4)





###biagram probability
    #This function calcualates biagram probability function.
    #BV is biagram vocabulary and BUV is bigram unigram vocabulary.
def biagramProb(sentence, BV, BUV):
    
    prob = 0
    
    arr = sentence.split(" ")
    arr = removetSpaces(arr)
    
    arr.insert(0, '#')
               
    for i in range(0,len(arr) - 1):
        a = BV[(arr[i], arr[i+1])]
        b = BUV[arr[i]]
        
        if a == 0:
            return 'undefined'
            break
        else:
            
            prob += math.log(a/float(b), 2)
     
    return round(prob, 4)
               

###smoothed biagram probability
#this function calculates smoothedBiagramProbability/
def smoothedBiagramProb(sentence, unigramVocabulary, BV, BUV):
    prob = 0
    arr = sentence.split(" ")
    arr = removetSpaces(arr)
    
    arr.insert(0, '#')
               
    for i in range(0, len(arr) - 1):
        size = len(unigramVocabulary.keys())
        a = BV[(arr[i], arr[i + 1])] + 1
        b = BUV[arr[i]] + size
        
      
        prob += math.log(a/float(b), 2)
            
    return round(prob, 4)

if __name__ == "__main__":
    main()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
