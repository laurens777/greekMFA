import codecs
import textgrids
import spacy
import copy
import os
from os.path import exists

from itertools import product
from collections import deque

def tag(folder, fileName):
    with codecs.open(folder+fileName, mode='r', encoding='utf-8') as inFile:
        with codecs.open("./temp.TextGrid", mode='w', encoding='utf-8') as outFile:
            for line in inFile:
                outFile.write(line)

    nlp = spacy.load("el_core_news_lg")

    rules = readPhonRules("./phonRules.txt")

    grid = textgrids.TextGrid("./temp.TextGrid")

    word_list = []
    print(grid.keys())
    for inter in grid["words"]:
        if str(inter.text) == "":
            continue
        word_list.append(inter)

    # print(grid["Sentence"])
    tagged_list = []
    
    for inter in grid["Sentence"]:
        inter = fixPunct(str(inter.text))
        doc = nlp(inter)
        for word in doc:
            if word.pos_ == "PUNCT" or word.pos_ == "SPACE":
                continue
            tagged_list.append([word.text, word.morph, word.pos_])

    word_seq = needleman_wunsch(word_list, tagged_list)
    # print(word_seq)
    # for i in word_seq:
    #     if i[1] == None:
    #         print(i[0], word_list[i[0]])
    #     elif i[0] == None:
    #         print(i[0], " - ", tagged_list[i[1]])
    #         continue
    #     else:
    #         print(i[0], word_list[i[0]], tagged_list[i[1]])

    new_textgrid = textgrids.TextGrid()
    new_textgrid.xmin = grid.xmin
    new_textgrid.xmax = grid.xmax

    for t in grid:
        new_textgrid[t] = grid[t]
        if t == "words":
            new_tier = copy.deepcopy(grid[t])
            for inter in new_tier:
                inter.text = ''
            for tup in word_seq:
                if tup[0] == None or tup[1] == None:
                    continue
                else:
                    for inter in new_tier:
                        if inter.xmin == word_list[tup[0]].xmin:
                            morph_tags = str(tagged_list[tup[1]][1]).split("|")
                            tags = ""
                            for tag in morph_tags:
                                if tag == "":
                                    continue
                                elif tag.split("=")[1] == "Yes":
                                    tags = tags  + "." + tag.split("=")[0]
                                else:
                                    tags = tags  + "." + tag.split("=")[1]
                            inter.text = graphToPhon(tagged_list[tup[1]][0], rules) + "." + tagged_list[tup[1]][2] + tags
            new_textgrid["Gloss"] = new_tier

    with codecs.open("../output/"+fileName, mode='w', encoding='utf-16') as outFile:
        outFile.write(str(new_textgrid))
        print("done writing")

    os.remove("./temp.TextGrid")
    

def needleman_wunsch(x, y):
    """Run the Needleman-Wunsch algorithm on two sequences.

    x, y -- sequences.

    Code based on pseudocode in Section 3 of:

    Naveed, Tahir; Siddiqui, Imitaz Saeed; Ahmed, Shaftab.
    "Parallel Needleman-Wunsch Algorithm for Grid." n.d.
    https://upload.wikimedia.org/wikipedia/en/c/c4/ParallelNeedlemanAlgorithm.pdf
    """
    N, M = len(x), len(y)
    s = lambda a, b: int(a == b)

    DIAG = -1, -1
    LEFT = -1, 0
    UP = 0, -1

    # Create tables F and Ptr
    F = {}
    Ptr = {}

    F[-1, -1] = 0
    for i in range(N):
        F[i, -1] = -i
    for j in range(M):
        F[-1, j] = -j

    option_Ptr = DIAG, LEFT, UP
    for i, j in product(range(N), range(M)):
        option_F = (
            F[i - 1, j - 1] + s(str(x[i].text), y[j][0]),
            F[i - 1, j] - 1,
            F[i, j - 1] - 1,
        )
        F[i, j], Ptr[i, j] = max(zip(option_F, option_Ptr))

    # Work backwards from (N - 1, M - 1) to (0, 0)
    # to find the best alignment.
    alignment = deque()
    i, j = N - 1, M - 1
    while i >= 0 and j >= 0:
        direction = Ptr[i, j]
        if direction == DIAG:
            element = i, j
        elif direction == LEFT:
            element = i, None
        elif direction == UP:
            element = None, j
        alignment.appendleft(element)
        di, dj = direction
        i, j = i + di, j + dj
    while i >= 0:
        alignment.appendleft((i, None))
        i -= 1
    while j >= 0:
        alignment.appendleft((None, j))
        j -= 1

    return list(alignment)

def graphToPhon(word, phonRules):
    i = 1
    temp = word
    for rule in phonRules:
        if rule.split()[0] in temp:
            if i <= 37:
                temp = temp.replace(rule.split()[0], rule.split()[1].strip("\n").strip())
            else:
                temp = temp.replace(rule.split()[0], rule.split()[1].strip("\n").strip())
        i += 1
    return temp

def fixPunct(sent):
    sent = sent.replace(",", ", ")
    sent = sent.replace(" ,", ",")
    sent = sent.replace(".", ". ")
    sent = sent.replace(" .", ".")
    sent = sent.replace("?", "? ")
    sent = sent.replace(" ?", "?")
    sent = sent.replace("!", "! ")
    sent = sent.replace(" !", "!")
    sent = sent.replace("  ", " ")
    return sent

def readPhonRules(path):
    rules = []
    with open(path, encoding="UTF-8") as ruleFile:
        for line in ruleFile:
            rules.append(line)
    return rules

def main(aligned):
    if not os.path.exists("../output/"):
        os.makedirs("../output/")

    for file in os.listdir(aligned):
        fileName = os.fsdecode(file)
        if fileName.endswith(".TextGrid"):
            if exists(aligned+fileName):
                tag(aligned, fileName)

if __name__ == "__main__":
    main("./temp/")
