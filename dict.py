import os, codecs

def createDict(corpusPath):
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

                        # split sentence into words and add words to dictionary
                        data = line.split()
                        for word in data:
                            if word not in phonDict:
                                phonDict[word] = ""

    return phonDict

def main():
    d = createDict("./alignment_2/input/")
    print(d)

if __name__ == "__main__":
    main()