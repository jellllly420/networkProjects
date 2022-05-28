from sys import argv
from sympy import banded
from textrank4zh import TextRank4Sentence
import json
import numpy as np
import os

def find_lcs_len(s1, s2):  
    m = [ [ 0 for x in s2 ] for y in s1 ]  
    for p1 in range(len(s1)):  
        for p2 in range(len(s2)):  
            if s1[p1] == s2[p2]:  
                if p1 == 0 or p2 == 0:  
                    m[p1][p2] = 1 
                else:  
                    m[p1][p2] = m[p1-1][p2-1]+1 
            elif m[p1-1][p2] < m[p1][p2-1]:  
                m[p1][p2] = m[p1][p2-1]  
            else:               # m[p1][p2-1] < m[p1-1][p2]  
                m[p1][p2] = m[p1-1][p2]  
    return m[-1][-1] 

def crop(intervals, input, output):
    s = " ".join(["{}sec,{}sec".format(i[0], i[1]) for i in intervals]) 
    os.system("auto-editor {} --edit all --add-in {} -o {}".format(input, s, output))


def summarize(sentences, k=3):
    tr4s = TextRank4Sentence()
    tr4s.analyze(text="".join(sentences), lower=True, source = 'all_filters')
    idxs = []
    sets = []
    for item in tr4s.get_key_sentences(num=k):
        idxs.append(item.index)
        sets.append(item.sentence)
    idx = np.argsort(idxs)
    sets = np.array(sets)[idx]

    return sets

if __name__ == "__main__":
    bname = argv[1]
    with open('{}.json'.format(bname), encoding='utf-8') as f:
        j = json.load(f)

    j = [i for i in j if len(i["onebest"]) > 4]

    inters = [[ int(i['bg'])/1000, (int(i['ed'])) / 1000 ] for i in j]
    sentences = [i["onebest"] for i in j]

    sets = summarize(sentences)

    for i, s in enumerate(sets):
        targets = []
        for ss, inter in zip(sentences, inters):
            if find_lcs_len(ss, s) > 0.8 * len(ss):
                targets.append(inter)

        crop(targets, "{}.mp4".format(bname), "{}_{}.mp4".format(bname, i))