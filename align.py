import extractTiers, punctFix, combine, posTag
import subprocess, os, time
from os.path import exists

def main(corpusPath, targetTier):
    startTime = time.time()

    if not corpusPath[-1] == "/":
        corpusPath += "/"
    
    outputPath = "./processedData/"
    extractTiers.main(corpusPath, outputPath, targetTier)

    punctFix.main(outputPath)

    for file in os.listdir(corpusPath):
        fileName = os.fsdecode(file)
        if fileName.endswith(".flac"):
            target = outputPath+fileName.split('.')[0]+".wav"
            subprocess.run(["ffmpeg", "-i", corpusPath+fileName, target], stdout=subprocess.DEVNULL)
    
    subprocess.run(["praat", "--run", "./wavPreProcess"], stdout=subprocess.DEVNULL)

    subprocess.run(["mfa", "g2p", "./greek_test_model.zip", "./processedData/", "./phonDict.txt"])

    startAlignTime = time.time()

    subprocess.run(["mfa", "train", "--clean", "./processedData", "./phonDict.txt", "./alignedData/"])

    endAlignTime = time.time()

    combine.main("./alignedData/", corpusPath)

    posTag.main("../temp/")

    executionTime = (time.time() - startTime)

    with open("time.txt", "w") as timeOutput:
        timeOutput.write("Total execution time: " + str(executionTime) + "\n")
        timeOutput.write("Total alignment time: " + str(endAlignTime - startAlignTime))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Runs the aligment pipeline.')
    parser.add_argument('targetTier', type=str, help='the tier that the alignment is based on')
    args = parser.parse_args()
    main("../inputData/", args.targetTier) 
