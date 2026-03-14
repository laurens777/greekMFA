import os
import unicodedata

def main(file_path):
    # Get the directory and base name
    dir_name = os.path.dirname(file_path)
    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)

    # Create output file path in the same folder
    output_file = os.path.join(dir_name, name + "_clean" + ext)

    # Read the input file and extract words
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    words = []
    for line in lines:
        parts = line.strip().split('\t')
        if len(parts) >= 2:
            word = parts[1]
            if word.isalpha() and all(unicodedata.name(c, '').startswith('GREEK') for c in word):
                words.append(word)

    # Write the words to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        for word in words:
            f.write(word + '\n')

    return 0

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Extract Greek words from a tab-separated file.")
    parser.add_argument("file_path", help="Path to the input file")
    args = parser.parse_args()
    main(args.file_path)