import extractTiers, punctFix, combine, posTag
import subprocess, os, shutil, time
from os.path import exists

def main(corpusPath="../inputdata/", targetTier="word"):
    startTime = time.time()

    if not corpusPath[-1] == "/":
        corpusPath += "/"

    outputPath = "./processedData/"
    for generatedPath in (outputPath, "./alignedData/", "./temp/"):
        if os.path.exists(generatedPath):
            shutil.rmtree(generatedPath)
    extractTiers.main(corpusPath, outputPath, targetTier)

    punctFix.main(outputPath)

    for file in os.listdir(corpusPath):
        fileName = os.fsdecode(file)
        if fileName.endswith(".flac"):
            target = outputPath+fileName.split('.')[0]+".wav"
            subprocess.run(["ffmpeg", "-i", corpusPath+fileName, target], stdout=subprocess.DEVNULL)
        elif fileName.endswith(".wav"):
            subprocess.run(["cp", corpusPath+fileName, outputPath+fileName])

    subprocess.run(["praat", "--run", "./wavPreProcess"], stdout=subprocess.DEVNULL)

    # subprocess.run(["mfa", "g2p", "./greek_acoustic_model_25-09-2026.zip", "./processedData/", "./scripts/phonDict.txt"])

    startAlignTime = time.time()

    try:
        subprocess.run(
            ["mfa", "align", "--clean", "./processedData", "./phonDict.txt", "./greekModelNew_02-10-2026.zip", "./alignedData/"],
            check=True,
        )
    except subprocess.CalledProcessError as error:
        raise RuntimeError(
            "MFA alignment failed. Check the MFA error above, then rerun the pipeline."
        ) from error

    endAlignTime = time.time()

    combine.main("./alignedData/", corpusPath)

    posTag.main("./temp/")

    executionTime = (time.time() - startTime)

    with open("time.txt", "w") as timeOutput:
        timeOutput.write("Total execution time: " + str(executionTime) + "\n")
        timeOutput.write("Total alignment time: " + str(endAlignTime - startAlignTime))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Runs the aligment pipeline.')
    parser.add_argument('targetTier', type=str, help='the tier that the alignment is based on')
    parser.add_argument('folder', type=str, help='the folder containing the data')
    args = parser.parse_args()
    main(args.folder, args.targetTier) 
