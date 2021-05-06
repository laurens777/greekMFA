import os, codecs, errno

def addSpace(inPath, outPath):
    with codecs.open(inPath, mode='r', encoding='UTF-16') as inFile:
        with codecs.open(outPath, mode='w', encoding='UTF-16') as outFile:
            for line in inFile:
                if "text" in line:
                    line = line.replace(",", ", ")
                    line = line.replace(",  ", ", ")
                    line = line.replace(" ,", ",")
                    line = line.replace(".", ". ")
                    line = line.replace(".  ", ". ")
                    line = line.replace(" .", ".")
                    line = line.replace("?", "? ")
                    line = line.replace("?  ", "? ")
                    line = line.replace(" ?", "?")
                    line = line.replace("!", "! ")
                    line = line.replace("!  ", "! ")
                    line = line.replace(" !", "!")
                outFile.write(line)

def rename(src, dst):
    try:
        os.replace(src, dst)
        os.remove(src)
    except OSError:
        pass

def main(corpusPath):
    directory = os.fsencode(corpusPath)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".TextGrid"):
            addSpace(corpusPath+filename, corpusPath+filename+".tmp")
            rename(corpusPath+filename+".tmp", corpusPath+filename)


if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description='add space after punctuation.')
	parser.add_argument('corpusPath', type=str, help='the path to the corpus folder')
	args = parser.parse_args()
	main(args.corpusPath) 