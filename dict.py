import os, codecs

def createTypeDict(corpusPath):
    phonDict = {}

    directory = os.fsencode(corpusPath)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".TextGrid"):
            with codecs.open(corpusPath+filename, mode='r', encoding='UTF-16') as inFile:
                for line in inFile:
                    if "text" in line:
                        # remove puctuation
                        line = line.replace(",", "")
                        line = line.replace(".", "")
                        line = line.replace("?", "")
                        line = line.replace("!", "")
                        line = line.replace(";", "")
                        line = line.replace("\"", "")

                        # split sentence into words and add words to dictionary
                        data = line.split()
                        for word in data:
                            if word not in phonDict:
                                phonDict[word] = ""
    print(type(phonDict))
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
                    temp = temp.replace(rule.split()[0], rule.split()[1].strip("\n").strip()+" ")
            i += 1
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

def main():
    d = createTypeDict("./alignment_2/input/")
    print(type(d))
    rules = readPhonRules("./pronuciationConverter.txt")
    d = graphToPhon(d, rules)
    savePhonRules(d)
    

if __name__ == "__main__":
    main()