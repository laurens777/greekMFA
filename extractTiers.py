import os, codecs, re
from textgrids import TextGrid

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
    tg = TextGrid(inPath)

    try:
        tier = tg[target]
    except:
        tier = tg[target.lower()]

    new_tg = TextGrid()
    new_tg.xmin = tg.xmin
    new_tg.xmax = tg.xmax
    new_tg[target] = tier

    with open(outPath, 'w', encoding="utf-8") as f:
        f.write(new_tg.__str__())

def main(corpusPath, outPath, targetTier):
    directory = os.fsencode(corpusPath)
    outputPath = outPath

    if not os.path.exists(outputPath):
        os.makedirs(outputPath)

    for file in os.listdir(directory):
        print(file)
        fileName = os.fsdecode(file)
        if fileName.endswith(".TextGrid"):
            inPath = os.path.join(corpusPath, fileName)
            outPath = os.path.join(outputPath, fileName)

            print(f"Processing: {inPath}")

            try:
                stripTiers(inPath, outPath, targetTier)
            except Exception as e:
                print(f"ERROR in {fileName}: {type(e).__name__}: {e}")
                raise

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='This file contains the code for extracting a specific tier from a textgrid file by tier name.')
    parser.add_argument('corpusPath', type=str, help='the path to the corpus folder')
    parser.add_argument('outPath', type=str, help='the path to the output folder')
    parser.add_argument('targetTier', type=str, help='the tier that is targeted for extraction')
    args = parser.parse_args()
    main(args.corpusPath, args.outPath, args.targetTier) 
