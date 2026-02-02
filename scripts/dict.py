import codecs
import os

def createTypeDict(path):
    phonDict = {}
    files = []

    if os.path.isfile(path):
        files = [path]
    elif os.path.isdir(path):
        if not path[-1] == "/":
            path = path + "/"

        [path+file for file in os.listdir(os.fsdecode(corpusPath))]
    else:
        return 0

    for filePath in files:
        with codecs.open(filePath, mode='r', encoding='UTF-8') as inFile:
            for line in inFile:
                # remove puctuation
                line = line.replace(",", "")
                line = line.replace(".", "")
                line = line.replace("?", "")
                line = line.replace("!", "")
                line = line.replace(";", "")
                line = line.replace("\"", "")
                line = line.replace("‘", "")
                line = line.replace("’", "")

                # split sentence into words and add words to dictionary
                data = line.split()
                for word in data:
                    if word not in phonDict:
                        phonDict[word] = ""

    #print(type(phonDict))
    return phonDict

def graphToPhon(phonDict, phonRules):
    i = 1
    for word in phonDict.keys():
        temp = word
        for rule in phonRules:
            if rule.split()[0] in temp:
                if i <= 37:
                    temp = temp.replace(rule.split()[0], rule.split()[1].strip("\n").strip())
                else:
                    temp = temp.replace(rule.split()[0], rule.split()[1].strip("\n").strip())
            i += 1

        temp = ''.join([ch + ' ' for ch in temp])[:-1]

        phonDict[word] = temp

    return phonDict

def readPhonRules(path):
    rules = []
    with open(path) as ruleFile:
        for line in ruleFile:
            rules.append(line)
    return rules

def savePhonRules(dict):
    d = sorted(dict)
    with open("./phonDict.txt", 'w+') as outFile:
        for line in d:
            outFile.write(line + " " + dict[line].replace("  ", " ") + "\n")

def main(path):
    d = createTypeDict(path)
    print(type(d))
    rules = readPhonRules("../data/phonRules.txt")
    d = graphToPhon(d, rules)
    savePhonRules(d)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Script for creating a phonDict from a single file or folder.")
    parser.add_argument("inputPath", type=str, help="Pass in a path to either a single file or a folder.")
    args = parser.parse_args()

    main(args.inputPath)
