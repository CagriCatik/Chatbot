#!/usr/bin/env python3
# Usage: python convert_word_to_pdf.py document.docx output.pdf

import sys
from docx2pdf import convert

def main():
    if len(sys.argv) != 3:
        print("Usage: python convert_word_to_pdf.py input.docx output.pdf")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        # Convert the input file and save as the output file.
        convert(input_file, output_file)
        print(f"Successfully converted '{input_file}' to '{output_file}'.")
    except Exception as e:
        print("Error during conversion:", e)

if __name__ == "__main__":
    main()
