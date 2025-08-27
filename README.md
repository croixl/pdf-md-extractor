# PDF to Markdown Extractor

A simple Python tool to extract text from PDF files and convert them to Markdown format.

## Features

- **Multiple input methods**: Command line arguments, interactive file browser, or manual path entry
- **Auto-discovery**: Automatically finds PDF files in directories
- **Smart path handling**: Supports drag & drop, quoted paths, and special characters
- **Automatic output naming**: Replaces `.pdf` with `.md`
- **Same-directory output**: Saves markdown files alongside original PDFs
- **Comprehensive validation**: File existence, format, and permission checks
- **User-friendly interface**: Numbered file selection and clear error messages

## Installation

1. Clone or download this repository
2. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Method 1: Command Line (Direct)
```bash
python extract_pdf.py "path/to/your/document.pdf"
```

### Method 2: Interactive Mode
```bash
python extract_pdf.py
```

When you run in interactive mode, you'll get three options:

1. **Manual Path Entry**: Enter the file path directly (supports drag & drop)
2. **Auto-Search Home**: Automatically finds all PDF files in your home directory
3. **Search Specific Directory**: Search for PDFs in a specific folder

#### Interactive Example:
```
Choose how to select your PDF file:
1. Enter file path manually
2. Search for PDF files from home directory  
3. Search for PDF files from a specific directory

Select option (1-3): 2

Found PDF files:
 1. ~/Documents/report.pdf
 2. ~/Downloads/invoice.pdf
 3. ~/Wisdom_database/research.pdf

Select a file (1-3) or 'q' to quit: 1
```

The script will:
- Validate the file exists and is a PDF
- Extract the text content
- Save it as a Markdown file in the same directory
- Display the paths of both input and output files

## Example

```bash
$ python extract_pdf.py
PDF to Markdown Extractor
------------------------------
Enter the path to your PDF file: ~/Documents/report.pdf
Extracting text from: /home/user/Documents/report.pdf
Markdown saved to: /home/user/Documents/report.md

Extraction completed successfully!
Input PDF: /home/user/Documents/report.pdf
Output Markdown: /home/user/Documents/report.md
```

## Requirements

- Python 3.6+
- pymupdf4llm library (see requirements.txt)

## Error Handling

The script handles common errors:
- File not found
- Invalid file format (non-PDF files)
- Permission issues
- PDF extraction errors

## License

This project is open source and available under the MIT License.
