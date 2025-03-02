#!/usr/bin/env python3
# usage: python convert_multiple_word_to_pdf.py word_files_folder

import sys
from docx2pdf import convert

def main():
    if len(sys.argv) != 2:
        print("Usage: python convert_folder.py <folder_path>")
        sys.exit(1)

    folder = sys.argv[1]
    try:
        convert(folder)
        print(f"Successfully converted all Word documents in '{folder}'.")
    except Exception as e:
        print("Error during conversion:", e)

if __name__ == "__main__":
    main()
