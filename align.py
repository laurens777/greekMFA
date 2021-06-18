import extractTiers, punctFix, combine
import subprocess, os

def main(corpusPath, targetTier):
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

    subprocess.run(["mfa", "train", "--clean", "./processedData", "./phonDict.txt", "./alignedData/"])

    combine.main("./alignedData/", "./data/")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Runs the aligment pipeline.')
    parser.add_argument('corpusPath', type=str, help='the path to the corpus folder')
    parser.add_argument('targetTier', type=str, help='the tier that the alignment is based on')
    args = parser.parse_args()
    main(args.corpusPath, args.targetTier) 