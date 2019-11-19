#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 19:14:19 2019

@author: ritesh
"""

#from shared import (a10_input_sent_w_coref,
#                          a10_input_sent_wo_coref,
#                          a10_corefs)
from app.coref import model as CR
from app.fileParse import FileParser

import spacy
import re
import sys


if __name__ == '__main__':

    list_file = sys.argv[1]
    response_directory = sys.argv[2]
    list_file_txt = open(list_file, 'r')
    lista = list_file_txt.readlines()
    read_dict = {}
    cr = CR()

    for path in lista:
        start = path.strip().rfind('/')
        end = path.strip().find('.input')
        prefix = path.strip()[start+1:end]
        fp = FileParser()
        output = fp.parse_input_file(path.strip())
        actual_sent = output['sentences']
        actual_corefs = output['corefs']
        actual_np =output['noun_phrases']
        read_dict[prefix] = [actual_sent, actual_corefs,actual_np]

    dict_of_coref_dic = cr.exactMatching(read_dict)
    cr.printing(dict_of_coref_dic, response_directory)