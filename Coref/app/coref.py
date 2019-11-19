import spacy
import re
import sys
from app.fileParse import FileParser

regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
matchDic = {}

def main():
    list_file = sys.argv[1]
    response_directory = sys.argv[2]
    list_file_txt = open(list_file, 'r')
    lista = list_file_txt.readlines()
    processDict = {}

    for path in lista:
        start = path.strip().rfind('/')
        end = path.strip().find('.input')
        prefix = path.strip()[start+1:end]
        fp = FileParser()
        output = fp.parse_input_file(path.strip())
        actual_sent = output['sentences']
        actual_corefs = output['corefs']
        actual_np =output['noun_phrases']
        processDict[prefix] = [actual_sent, actual_corefs,actual_np]

    dict_of_coref_dic = exactMatching(processDict)
    printing(dict_of_coref_dic, response_directory)

def exactMatching(processDict):

    for i, value in processDict.items():

        sentences = value[0]

        coreferences = value[1]

        nounPhares = value[2]

        roots=[]

        for num, list in nounPhares.items():

            if list == []:
                continue
            else:
                for dic in list:
                    roots.append((dic['root'], num))

        matchedCoref = {}

        for id, first in coreferences.items():

            matchedCoref[id] = []

            for key, sent in sentences.items():

                if int(key) < int(first[1]):
                    continue

                if regex.search(first[0]) != None:
                    matchedCoref[id].append((key,first[0]))
                    break

                matches = re.findall(first[0], sent, re.I)

                for match in matches:
                    matchedCoref[id].append((key, match))

            for root in roots:
                
                if int(root[1]) <= int(first[1]):

                    continue

                else:

                    matchRoot = re.findall(root[0], first[0], re.I)

                    if matchRoot != []:

                        for match in matchRoot:

                            if id not in matchedCoref.keys():
                                    
                                matchedCoref[id] = [(root[1],root[0])]
                                
                            elif (root[1],root[0]) not in matchedCoref[id]:

                                matchedCoref[id].append((root[1],root[0]))


        matchDic[i] = matchedCoref

    return matchDic

def printing(matchDic,responseD):

    for i, coref_dict in matchDic.items():

        outF = open(responseD+i+'.response', "w")

        for i, j in coref_dict.items():
            print(j)
            outF.write('<COREF ID="{}">{}</COREF>'.format(i, j[0][1]))
            outF.write("\n")
            for i in range(1, len(j)):
                print(j[i][0])
                print(j[i][1])
                g = '{{{}}} {{{}}}'.format(j[i][0], j[i][1])
                print(g)
                outF.write(g)
                outF.write("\n")
            outF.write("\n")
        outF.close()
    
if __name__ == '__main__':
    main()