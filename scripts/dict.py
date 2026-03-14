import os

def createTypeDict(path):
    """ Creates a dictionary of unique words from text files and adds a phonological
        representation of the word, reating a pronunciation dictionary.

    Parameters
    ----------
    inputPath : str
        relative, to this script, or absolute path to the source directory or file to be processed.
    """
    phonDict = {}
    files = []

    if os.path.isfile(path):
        files = [path]
    elif os.path.isdir(path):
        if not path[-1] == "/":
            path = path + "/"

        [path+file for file in os.listdir(os.fsdecode(path))]
    else:
        raise ValueError(f"Invalid path: {path}")

    for filePath in files:
        with open(filePath, mode='r', encoding='UTF-8') as inFile:
            for line in inFile:
                # split sentence into words and add words to dictionary
                data = line.split()
                for word in data:
                    if word.lower() not in phonDict:
                        phonDict[word.lower()] = ""

    #print(type(phonDict))
    return phonDict

def graphToPhon(phonDict, phonRules):
    for word in phonDict.keys():
        temp = word
        for rule in phonRules:
            if rule.split()[0] in temp:
                temp = temp.replace(rule.split()[0], rule.split()[1].strip("\n").strip())

        temp = ''.join([ch + ' ' for ch in temp])[:-1]
        temp = temp.replace("*", "i/j")

        phonDict[word] = temp

    return phonDict

def readPhonRules(path):
    rules = []
    with open(path) as ruleFile:
        for line in ruleFile:
            rules.append(line)
    return rules

def savePhonRules(phonDict):
    d = sorted(phonDict)
    with open("./phonDict.txt", 'w+') as outFile:
        for line in d:
            outFile.write(line + " " + phonDict[line].replace("  ", " ") + "\n")

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
