# Greek MFA Project

# Description

This repository contains a various scripts used to pre-process data, and run a forced alignment pipeline using the [Montreal Forced Aligner](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner/).

# File Description and Overview
- align.py

This script contains the entire pipeline. And will initiate all of the other scripts found inside this repository. This script requires two inputs: the data folder containing the audio and TextGrid files, and the tier that the Montreal Forced Aligner will use.
  `python3 align.py /path/to/dataset/ nameOfTargetTier`

- combine.py

This script will combine the original TextGrid file with the MFA aligned TextGrid file.

- extractTiers.py

This script will create a TextGrid file containing one tier for use with the Montreal Forced Aligner.

- punctFix.py

This file contains various data-cleaning commands. This file can be edited to further clean TextGrid files.

- wavPreProcess

This is a Praat script written by E. Chodroff that will re-sample .wav files to 16kHz and extract a single channel as required for the Montreal Forced Aligner.

- greek_test_model.zip

This is the model that the Montreal Forced Aligner will use to align the transcripts to the audio files. This model was trained using the [Greek Internet Corpus](https://en.wiktionary.org/wiki/Appendix:Greek_word_lists) which contains ~72,000 tokens. 