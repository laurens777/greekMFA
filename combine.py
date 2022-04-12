import os, codecs, re
from os.path import exists

def combineTiers(mfaFile, original, outFile):
    # first loop through the mfa aligned file will write the phone tier
    with codecs.open(mfaFile, mode='r', encoding='utf-8') as inFile:
        with codecs.open(outFile, mode='w', encoding='utf-8') as output:
            skip = False
            for line in inFile:
                l = re.match('size = 2', line)
                if l:
                    line = "size = 5\n"
                m = re.match(' *item \[([0-9]+)\]:', line) 
                if m:
                    if m.group(1) == '1':
                        skip = True
                        continue
                    elif m.group(1) == '2':
                        skip = False
                        line = "    item [1]:\n"
                if skip == True:
                    continue
                n = re.match(' *name = \"[a-zA-z]* - phones\"', line)
                if n:
                    line = "        name = \"Phone\"\n"
                output.write(line)

    with codecs.open(mfaFile, mode='r', encoding='utf-8') as inFile:
        with codecs.open(outFile, mode='a', encoding='utf-8') as output:
            skip = True
            for line in inFile:
                m = re.match(' *item \[([0-9]+)\]:', line) 
                if m:
                    if m.group(1) == '1':
                        skip = False
                        line = "    item [2]:\n"
                    elif m.group(1) == '2':
                        skip = True
                        continue
                if skip == True:
                    continue
                n = re.match(' *name = \"[a-zA-Z]* - words\"', line)
                if n:
                    line = "        name = \"Word\"\n"
                output.write(line)

    with codecs.open(original, mode='r', encoding='utf-16be') as inFile:
        with codecs.open(outFile, mode='a', encoding='utf-8') as output:
            skip = True
            for line in inFile:
                m = re.match(' *item \[([0-9]+)\]:', line) 
                if m:
                    if m.group(1) == '2':
                        skip = False
                        line = "    item [3]:\n"
                    elif m.group(1) == '3':
                        line = "    item [4]:\n"
                    elif m.group(1) == '4':
                        line = "    item [5]:\n"
                if skip == True:
                    continue
                output.write(line)

def main(aligned, original):
    if not os.path.exists("../temp/"):
        os.makedirs("../temp/")

    for file in os.listdir(aligned):
        fileName = os.fsdecode(file)
        if fileName.endswith(".TextGrid"):
            if exists(original+fileName):
                combineTiers(aligned+fileName, original+fileName, "../temp/"+fileName)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Runs the aligment pipeline.')
    parser.add_argument('alignedPath', type=str, help='the path to the aligned corpus folder')
    parser.add_argument('originalPath', type=str, help='the path to the original corpus folder')
    args = parser.parse_args()
    main(args.alignedPath, args.originalPath)
