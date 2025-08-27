#!/usr/bin/env python3
"""
PDF to Markdown Extractor

A simple tool to extract text from PDF files and convert them to Markdown format.
"""

import os
import sys
import argparse
import pymupdf4llm
from pathlib import Path


def find_pdf_files(search_dir=None):
    """Find PDF files in the system starting from a directory."""
    if search_dir is None:
        search_dir = Path.home()
    else:
        search_dir = Path(search_dir)
    
    pdf_files = []
    try:
        # Search for PDF files recursively, but limit depth to avoid too many results
        for pdf_file in search_dir.rglob("*.pdf"):
            if pdf_file.is_file():
                pdf_files.append(pdf_file)
                if len(pdf_files) >= 20:  # Limit to first 20 files found
                    break
    except PermissionError:
        pass
    
    return pdf_files


def select_from_list(pdf_files):
    """Let user select from a list of found PDF files."""
    if not pdf_files:
        return None
    
    print("\nFound PDF files:")
    for i, pdf_file in enumerate(pdf_files, 1):
        # Show relative path from home directory for cleaner display
        try:
            rel_path = pdf_file.relative_to(Path.home())
            display_path = f"~/{rel_path}"
        except ValueError:
            display_path = str(pdf_file)
        
        print(f"{i:2d}. {display_path}")
    
    if len(pdf_files) >= 20:
        print("    ... (showing first 20 results)")
    
    while True:
        try:
            choice = input(f"\nSelect a file (1-{len(pdf_files)}) or 'q' to quit: ").strip()
            if choice.lower() == 'q':
                return None
            
            index = int(choice) - 1
            if 0 <= index < len(pdf_files):
                return pdf_files[index]
            else:
                print(f"Please enter a number between 1 and {len(pdf_files)}")
        except ValueError:
            print("Please enter a valid number or 'q' to quit")


def get_pdf_path():
    """Get PDF file path from user input with multiple options."""
    print("\nChoose how to select your PDF file:")
    print("1. Enter file path manually")
    print("2. Search for PDF files from home directory")
    print("3. Search for PDF files from a specific directory")
    
    while True:
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == "1":
            return get_manual_path()
        elif choice == "2":
            pdf_files = find_pdf_files()
            if not pdf_files:
                print("No PDF files found in home directory.")
                continue
            return select_from_list(pdf_files)
        elif choice == "3":
            search_dir = input("Enter directory to search in: ").strip()
            if search_dir.startswith('"') and search_dir.endswith('"'):
                search_dir = search_dir[1:-1]
            elif search_dir.startswith("'") and search_dir.endswith("'"):
                search_dir = search_dir[1:-1]
            
            if not Path(search_dir).exists():
                print(f"Directory '{search_dir}' does not exist.")
                continue
            
            pdf_files = find_pdf_files(search_dir)
            if not pdf_files:
                print(f"No PDF files found in '{search_dir}'.")
                continue
            return select_from_list(pdf_files)
        else:
            print("Please enter 1, 2, or 3")


def get_manual_path():
    """Get PDF file path manually with improved handling."""
    while True:
        print("\nTip: You can drag and drop a file here, or copy/paste the full path")
        pdf_path = input("Enter the path to your PDF file: ").strip()
        
        # Handle different quote styles and clean up the path
        if pdf_path.startswith('"') and pdf_path.endswith('"'):
            pdf_path = pdf_path[1:-1]
        elif pdf_path.startswith("'") and pdf_path.endswith("'"):
            pdf_path = pdf_path[1:-1]
        
        # Handle file:// URLs (from drag and drop)
        if pdf_path.startswith('file://'):
            pdf_path = pdf_path[7:]
        
        # Expand user path (~)
        pdf_path = os.path.expanduser(pdf_path)
        
        # Convert to Path object for easier handling
        pdf_file = Path(pdf_path)
        
        # Check if file exists
        if not pdf_file.exists():
            print(f"Error: File does not exist.")
            print(f"Looked for: {pdf_file.absolute()}")
            retry = input("Try again? (y/n): ").strip().lower()
            if retry != 'y':
                return None
            continue
        
        # Check if it's a PDF file
        if pdf_file.suffix.lower() != '.pdf':
            print(f"Error: '{pdf_path}' is not a PDF file. Please provide a PDF file.")
            continue
        
        return pdf_file


def extract_pdf_to_markdown(pdf_path):
    """Extract text from PDF and convert to markdown."""
    try:
        print(f"Extracting text from: {pdf_path}")
        md_text = pymupdf4llm.to_markdown(str(pdf_path))
        return md_text
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return None


def save_markdown(md_text, pdf_path):
    """Save markdown text to file in the same directory as the PDF."""
    # Create output filename by replacing .pdf with .md
    output_path = pdf_path.with_suffix('.md')
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_text)
        print(f"Markdown saved to: {output_path}")
        return output_path
    except Exception as e:
        print(f"Error saving markdown file: {e}")
        return None


def main():
    """Main function to run the PDF extraction process."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Extract text from PDF files and convert to Markdown")
    parser.add_argument("pdf_file", nargs="?", help="Path to the PDF file to extract")
    args = parser.parse_args()
    
    print("PDF to Markdown Extractor")
    print("-" * 30)
    
    # Get PDF file path - either from command line or interactive selection
    if args.pdf_file:
        pdf_path = Path(args.pdf_file)
        if not pdf_path.exists():
            print(f"Error: File '{args.pdf_file}' does not exist.")
            sys.exit(1)
        if pdf_path.suffix.lower() != '.pdf':
            print(f"Error: '{args.pdf_file}' is not a PDF file.")
            sys.exit(1)
    else:
        pdf_path = get_pdf_path()
        if pdf_path is None:
            print("No file selected. Exiting.")
            sys.exit(0)
    
    # Extract PDF content to markdown
    md_text = extract_pdf_to_markdown(pdf_path)
    if md_text is None:
        sys.exit(1)
    
    # Save markdown to file
    output_path = save_markdown(md_text, pdf_path)
    if output_path is None:
        sys.exit(1)
    
    print(f"\nExtraction completed successfully!")
    print(f"Input PDF: {pdf_path}")
    print(f"Output Markdown: {output_path}")


if __name__ == "__main__":
    main()
