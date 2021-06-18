import os, codecs, re

def stripTiers(inPath, outPath, target):
    """ Removes all tiers from textgrid file except for the target tier.

    Parameters
    ----------
    inPath : str
        relative, to this script, or absolute path to the source directory
    outPath : str
        relative, to this script, or absolute path to the destination directory
    target : str
        label of the target tier
    """
    tiers = {}
    with codecs.open(inPath, mode='r', encoding='utf-16be') as inFile:
        for line in inFile:
            m = re.match(' *item \[([0-9]+)\]:', line) 
            if m:
                tiers[m.group(1)] = ""
                tier = m.group(1)
            n = re.match(' *name = "([a-zA-Z]+)"', line)
            if n:
                tiers[tier] = n.group(1).lower()
    
    with codecs.open(inPath, mode='r', encoding='utf-16be') as inFile:
        with codecs.open(outPath, mode='w', encoding='utf-16be') as outFile:
                delete = False
                for line in inFile:
                    if line.split(' ')[0] == "size":
                        outFile.write("size = 1\n")
                        continue
                    m = re.match(' *item \[([0-9]+)\]:', line)
                    if m:
                        if tiers[m.group(1)] != target.lower():
                            delete = True
                        if tiers[m.group(1)] == target.lower():
                            delete = False
                    if delete == False:
                        outFile.write(line)

def main(corpusPath, outPath, targetTier):
    directory = os.fsencode(corpusPath)
    outputPath = outPath

    if not os.path.exists(outputPath):
        os.makedirs(outputPath)

    for file in os.listdir(directory):
        fileName = os.fsdecode(file)
        if fileName.endswith(".TextGrid"):
            stripTiers(corpusPath+fileName, outputPath+fileName, targetTier)
    

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='add space after punctuation.')
    parser.add_argument('corpusPath', type=str, help='the path to the corpus folder')
    parser.add_argument('outPath', type=str, help='the path to the output folder')
    parser.add_argument('targetTier', type=str, help='the tier that the alignment is based on')
    args = parser.parse_args()
    main(args.corpusPath, args.outPath, args.targetTier) 