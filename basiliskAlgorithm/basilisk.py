#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 14:24:58 2019

@author: ritesh
"""
import re
import sys
import math
from operator import itemgetter

lexicon_file = None
context_file = None

if sys.argv[0] == 'basilisk.py':
    lexicon_file = sys.argv[1]
    context_file = sys.argv[2]
else:
    print("please provide required txt files.")

def main():
    lexicon, p = readLexicon(lexicon_file)
    context = readContext(context_file)
    
    pairs = addToMap(context)
    lexiconList = list(lexicon)
    
    
    print("Seed Words:", end = " ")
    for i in p:
        print(i, end = " ")
    lexiconList.sort()
    print("\n")
    print("Unique Words: ", len(pairs))
    for z in range(5):
        print("\nInteration: ", (z+1))
        scores = calculateRLogFScores(pairs, lexicon)
        scores.sort(reverse = True)
        listOfScores = topTenScores(scores)
        sortedListOfScores1 = sorted(listOfScores, key=itemgetter(1))
        sortedListOfScores2 = sorted(sortedListOfScores1, key = itemgetter(0), reverse = True)
        print("\nPATTERN POOL")
        for i, item in enumerate(sortedListOfScores2):
            print("%d. %s (%.3f)" % ((i + 1), item[1], item[0]))
        newHeadNouns = uniqueHeadNouns(sortedListOfScores2, pairs, lexicon)
        newWords = []
        for word in newHeadNouns:
            freq = getWordFreq(word, pairs, lexicon)
            avgLog = 0
            for item in freq:
                avgLog = avgLog + math.log(item, 2)
            avgLog = float(avgLog) / len(freq)
            newWords.append([avgLog, word])
        temp = sorted(newWords, key=itemgetter(1))
        getNewWords = sorted(temp, key=itemgetter(0), reverse=True)
       
        new_words = getTopFiveNewWords(getNewWords)
        print("\nNEW WORDS")
        for i in range(len(new_words)):
            print("%s (%0.3f)" % (new_words[i][1], new_words[i][0]))
        for i in range(len(new_words)):
            lexicon.add(getNewWords[i][1])


######Function that reads lexicon######
def readLexicon(fname):
    lexicon = set()
    p = []
    with open(fname) as f:
        for line in f:
            p.append(line.strip())
            line = line.lower().strip()
            lexicon.add(line)
            
    return lexicon, p

######Function that reads context#######
def readContext(fname):
    context = []
   
    with open(fname) as f:
        for line in f:
            first = re.match(r'(.*)\*(.*?)\:(.*)',
                                   line).group(1).lower().strip().split()
            second = re.match(r'(.*)\*(.*)', line).group(2).strip()
            context.append([first[-1], second])
    return context

#######Function that adds context ot the map######
def addToMap(context):
    pairs = {}
    for i in context:
        if i[1] in pairs:
            if i[0] in pairs[i[1]]:
                continue
            else:
                pairs[i[1]].append(i[0])
        else:
            pairs[i[1]] = [i[0]]
    return pairs

########Funtion that adds RLogF scores##########
def calculateRLogFScores(pairs, lexicon):
    scoreList = []
    for key in pairs:
        count = 0
        for value in pairs[key]:
            if value in lexicon:
                count += 1
        semfreq = count
        head_nouns = len(pairs[key])
        if head_nouns > 1 and semfreq > 1:
            RLogF = (float(semfreq) / head_nouns) *  math.log(semfreq, 2)
        else:
            RLogF = 0
        scoreList.append([RLogF, key])
        
    return scoreList

###########Function that adds top ten scores########
def topTenScores(scoreList):
    count = 0
    first = 0
    second = scoreList[9][0]
    for i in scoreList[10:]:
        first = i[0]
        if first == second:
            count += 1
        else:
            return [i for i in scoreList[:10 + count] if i[0] > 0]
    
##########Function that returns unique head nouns########
def uniqueHeadNouns(value, pairs, lexicon):
    heads = []
    for i in value:
        if pairs[i[1]] in heads:
            continue
        else:
            heads.extend(pairs[i[1]])
    result = list(set(heads) - lexicon)
    return result


#########Function that gets words frequency###########
def getWordFreq(word, pairs, lexicon):
    result = []
    for i in pairs:
        count = 0
        heads = pairs[i]
        if word in heads:
            for val in heads:
                if val in lexicon:
                    count += 1
            result.append(count + 1)
    return result

#########Function that gets top five new words.########3
def getTopFiveNewWords(wordList):   
    count = 0
    first = 0
    second = wordList[4][0]
    for i in wordList[5:]:
        first = i[0]
        if first == second:
            count += 1
        else:
            return [i for i in wordList[:5 + count]]
    
    
if __name__ == "__main__":
    main()