import os, codecs, errno

def addSpace(inPath, outPath):
    """ Reads a TextGrid file line by line and fixes punctuation if needed.

    This function reads from the input file and saves the modified contents to 
    the output file.
    
    Parameters
    ----------
    inPath : str
        relative, to this script, or absolute path to the input TextGrid file
    outPath : str
        relative, to this script, or absolute path to the output TextGrid file
    """

    with codecs.open(inPath, mode='r', encoding='utf-16be') as inFile:
        with codecs.open(outPath, mode='w', encoding='utf-16be') as outFile:
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
                    line = line.replace("xxx", "")
                outFile.write(line)

def rename(src, dst):
    """ Replaces the destination file with the source file and deletes the source file.

    Parameters
    ----------
    src : str
        relative, to this script, or absolute path to the source file
    dst : str
        relative, to this script, or absolute path to the destination file
    """

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
