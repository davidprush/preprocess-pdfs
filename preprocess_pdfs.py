#!/usr/bin/env python3

import os
import subprocess
import time
import datetime
import glob
from pathlib import Path
import argparse
import sys
import shutil

# Function to get current timestamp
def timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Function to log and print messages
def log_print(message, log_file, quiet=False):
    with open(log_file, "a") as f:
        f.write(f"{message}\n")
    if not quiet or "Error:" in message:
        print(message)

# Function to delete PDF file
def delete_pdf(pdf_file, log_file, quiet, no_delete, keep_pdfs):
    if no_delete or keep_pdfs:
        log_print(f"{timestamp()}: Skipping deletion of {pdf_file} per user option.", log_file, quiet)
        return 0
    log_print(f"{timestamp()}: Deleting {pdf_file}...", log_file, quiet)
    try:
        os.remove(pdf_file)
    except Exception as e:
        log_print(f"{timestamp()}: Error: Failed to delete {pdf_file}: {e}", log_file, quiet)
        return 1
    return 0

# Function to delete PNG file
def delete_png(png_file, log_file, quiet, no_delete, keep_pngs):
    if no_delete or keep_pngs:
        log_print(f"{timestamp()}: Skipping deletion of {png_file} per user option.", log_file, quiet)
        return 0
    log_print(f"{timestamp()}: Deleting {png_file}...", log_file, quiet)
    try:
        os.remove(png_file)
    except Exception as e:
        log_print(f"{timestamp()}: Error: Failed to delete {png_file}: {e}", log_file, quiet)
        return 1
    return 0

# Function to handle errors based on user preference
def handle_error(error_msg, log_file, quiet, error_handling):
    log_print(error_msg, log_file, quiet)
    if error_handling == "exit":
        log_print(f"{timestamp()}: Exiting script due to error as per --error-handling 'exit' option.", log_file, quiet)
        sys.exit(1)

# Function to append text to a single file with a header
def append_to_single_file(pdf_file, text_file, single_file, log_file, quiet):
    if not os.path.isfile(text_file):
        return False
    try:
        with open(text_file, "r") as src, open(single_file, "a") as dest:
            dest.write(f"\n=== {pdf_file} ===\n")
            dest.write(src.read())
            dest.write("\n")
        log_print(f"{timestamp()}: Appended text from {text_file} to {single_file}", log_file, quiet)
        os.remove(text_file)  # Remove temp file after appending
        return True
    except Exception as e:
        log_print(f"{timestamp()}: Error: Failed to append {text_file} to {single_file}: {e}", log_file, quiet)
        return False

# Function to check dependencies
def check_dependencies():
    missing = []
    
    # Check Python 3 (should always pass if script is running, but included for completeness)
    if sys.version_info < (3, 0):
        missing.append("Python 3 is required. Install it from https://www.python.org/downloads/\n"
                       "  - macOS: brew install python\n"
                       "  - Linux: sudo apt-get install python3 (Ubuntu/Debian) or sudo dnf install python3 (Fedora)")

    # Check ImageMagick (convert)
    if not shutil.which("convert"):
        missing.append("ImageMagick is missing (required for 'convert'). Install it:\n"
                       "  - macOS: brew install imagemagick\n"
                       "  - Linux: sudo apt-get install imagemagick (Ubuntu/Debian) or sudo dnf install imagemagick (Fedora)\n"
                       "  - Windows: Download from https://imagemagick.org/script/download.php")

    # Check Tesseract
    if not shutil.which("tesseract"):
        missing.append("Tesseract OCR is missing. Install it:\n"
                       "  - macOS: brew install tesseract\n"
                       "  - Linux: sudo apt-get install tesseract-ocr (Ubuntu/Debian) or sudo dnf install tesseract (Fedora)\n"
                       "  - Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")

    if missing:
        print("Error: The following dependencies are missing:")
        for dep in missing:
            print(dep)
        print("Please install the missing dependencies and try again.")
        sys.exit(1)

# Set up argument parser with detailed help
parser = argparse.ArgumentParser(
    description="A script to preprocess multi-page PDF files by converting them to PNGs and extracting text using ImageMagick and Tesseract. "
                "Processes all pages of each PDF, logs progress and errors, and provides a summary of results.",
    epilog="Examples:\n"
           "  python3 preprocess_pdfs.py                    # Process PDFs with default settings\n"
           "  python3 preprocess_pdfs.py -i ./pdfs          # Process PDFs from './pdfs'\n"
           "  python3 preprocess_pdfs.py -o ./text          # Save text to './text'\n"
           "  python3 preprocess_pdfs.py -q -l errors.log   # Quiet mode, log to 'errors.log'\n"
           "  python3 preprocess_pdfs.py -k                 # Keep PDFs\n"
           "  python3 preprocess_pdfs.py -p                 # Keep PNGs\n"
           "  python3 preprocess_pdfs.py -n                 # Keep all files\n"
           "  python3 preprocess_pdfs.py -e exit            # Exit on first error\n"
           "  python3 preprocess_pdfs.py -s all_text.txt    # Append all text to 'all_text.txt'\n"
           "  python3 preprocess_pdfs.py -i pdfs -o text -q -l mylog.txt -n -e continue -s combined.txt  # Combined options",
    formatter_class=argparse.RawDescriptionHelpFormatter
)
parser.add_argument("-i", "--input-dir", default=".", 
                    help="Directory containing PDF files to process (default: current directory '.')")
parser.add_argument("-o", "--output-dir", default="extracted-text", 
                    help="Directory where extracted text files will be saved (default: 'extracted-text')")
parser.add_argument("-q", "--quiet", action="store_true", 
                    help="Limit terminal output and log file entries to errors only (default: verbose output)")
parser.add_argument("-l", "--log-file", 
                    help="Custom name for the log file (default: 'preprocess_log_YYYYMMDD_HHMMSS.txt')")
parser.add_argument("-k", "--keep-pdfs", action="store_true", 
                    help="Prevent deletion of original PDF files (default: delete PDFs)")
parser.add_argument("-p", "--keep-pngs", action="store_true", 
                    help="Prevent deletion of intermediate PNG files (default: delete PNGs)")
parser.add_argument("-n", "--no-delete", action="store_true", 
                    help="Prevent deletion of any files (PDFs and PNGs), overrides --keep-pdfs and --keep-pngs")
parser.add_argument("-e", "--error-handling", choices=["exit", "continue"], default="continue",
                    help="Action on error: 'exit' to stop script, 'continue' to proceed (default: 'continue')")
parser.add_argument("-s", "--single-file", 
                    help="Append all extracted text to a single file with headers (default: separate files per page)")
args = parser.parse_args()

# Check dependencies before proceeding
check_dependencies()

# Set variables from arguments
input_dir = args.input_dir
output_dir = args.output_dir
quiet = args.quiet
log_file = args.log_file if args.log_file else f"preprocess_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
keep_pdfs = args.keep_pdfs
keep_pngs = args.keep_pngs
no_delete = args.no_delete
error_handling = args.error_handling
single_file = args.single_file

# Start time tracking
start_time = time.time()

# Initialize counters and error tracking
success_count = 0
fail_count = 0
error_count = 0
files_with_errors = []

# Step 1 & 2: Verify and create output directory
log_print(f"{timestamp()}: Directory '{output_dir}' check...", log_file, quiet)
if not os.path.isdir(output_dir):
    log_print(f"{timestamp()}: Directory '{output_dir}' does not exist. Creating it now...", log_file, quiet)
    try:
        os.makedirs(output_dir, exist_ok=True)
    except Exception as e:
        handle_error(f"{timestamp()}: Error: Failed to create '{output_dir}' directory: {e}", log_file, quiet, error_handling)
        error_count += 1
else:
    log_print(f"{timestamp()}: Directory '{output_dir}' already exists.", log_file, quiet)

# Check if there are no PDF files in the input directory
log_print(f"{timestamp()}: Checking for PDF files in '{input_dir}'...", log_file, quiet)
pdf_files = glob.glob(os.path.join(input_dir, "*.pdf"))
if not pdf_files:
    log_print(f"{timestamp()}: No PDF files found in '{input_dir}'.", log_file, quiet)
    log_print(f"{timestamp()}: Preprocessing complete! No files to process.", log_file, quiet)
    log_print(f"{timestamp()}: Summary:", log_file, quiet)
    log_print(f"{timestamp()}:   Total files successfully processed: {success_count}", log_print, quiet)
    log_print(f"{timestamp()}:   Total files not processed: {fail_count}", log_file, quiet)
    log_print(f"{timestamp()}:   Total errors encountered: {error_count}", log_file, quiet)
    duration = int(time.time() - start_time)
    log_print(f"{timestamp()}:   Script duration: {duration} seconds", log_file, quiet)
    if files_with_errors:
        log_print(f"{timestamp()}: Files with errors:", log_file, quiet)
        for file in files_with_errors:
            log_print(f"{timestamp()}:   - {file}", log_file, quiet)
    exit(0)

# Step 3: Process each PDF file
for pdf_file in pdf_files:
    base_name = Path(pdf_file).stem
    file_had_error = False

    # Step 4: Convert PDF to PNGs (multi-page support)
    log_print(f"{timestamp()}: Converting {pdf_file} to PNGs...", log_file, quiet)
    try:
        subprocess.run(["convert", "-density", "300", pdf_file, "-quality", "100", f"{base_name}-%d.png"], check=False, stderr=subprocess.DEVNULL)
    except Exception as e:
        handle_error(f"{timestamp()}: Error: Failed to convert {pdf_file} to PNGs: {e}", log_file, quiet, error_handling)
        error_count += 1
        file_had_error = True

    # Check if any PNGs were created
    png_files = glob.glob(f"{base_name}-[0-9]*.png")
    if not png_files:
        log_print(f"{timestamp()}: No PNG files generated for {pdf_file}.", log_file, quiet)
        log_print(f"{timestamp()}: Skipping deletion of {pdf_file} due to conversion failure.", log_file, quiet)
        log_print(f"{timestamp()}: Processing of {pdf_file} incomplete due to errors.", log_file, quiet)
        fail_count += 1
        if not file_had_error:  # Only add if not already added from conversion error
            files_with_errors.append(pdf_file)
        continue

    # Step 5: Delete PDF file if conversion succeeded (unless prevented)
    error_count += delete_pdf(pdf_file, log_file, quiet, no_delete, keep_pdfs)
    if error_count > (len(png_files) + 1):  # Adjust based on prior errors
        file_had_error = True

    # Process each PNG file (multi-page handling)
    page_success = 0
    page_fail = 0
    for png_file in png_files:
        page_base_name = Path(png_file).stem
        temp_text_file = f"{output_dir}/{page_base_name}.txt"

        # Step 6: Convert PNG to text using Tesseract
        log_print(f"{timestamp()}: Converting {png_file} to {temp_text_file}...", log_file, quiet)
        try:
            subprocess.run(["tesseract", png_file, f"{output_dir}/{page_base_name}", "-l", "eng", "txt"], check=False, stderr=subprocess.DEVNULL)
        except Exception as e:
            handle_error(f"{timestamp()}: Error: Failed to convert {png_file} to {temp_text_file}: {e}", log_file, quiet, error_handling)
            error_count += 1
            file_had_error = True

        # Step 7: Handle text output (single file or separate)
        if os.path.isfile(temp_text_file):
            if single_file:
                if append_to_single_file(f"{page_base_name}.pdf", temp_text_file, single_file, log_file, quiet):
                    page_success += 1
                else:
                    page_fail += 1
                    file_had_error = True
            else:
                page_success += 1

            # Delete PNG file if text conversion succeeded (unless prevented)
            error_count += delete_png(png_file, log_file, quiet, no_delete, keep_pngs)
            if error_count > (len(png_files) + 1):  # Adjust based on prior errors
                file_had_error = True
        else:
            log_print(f"{timestamp()}: Skipping deletion of {png_file} due to text conversion failure.", log_file, quiet)
            page_fail += 1

    # Update counters and error tracking
    if page_fail == 0 and page_success > 0:
        log_print(f"{timestamp()}: Successfully processed {pdf_file} (all {page_success} pages)", log_file, quiet)
        success_count += 1
    else:
        log_print(f"{timestamp()}: Processing of {pdf_file} incomplete: {page_success} pages succeeded, {page_fail} pages failed", log_file, quiet)
        fail_count += 1
        if not file_had_error:  # Only add if not already added from earlier errors
            files_with_errors.append(pdf_file)

    if file_had_error and pdf_file not in files_with_errors:
        files_with_errors.append(pdf_file)

# Calculate duration
duration = int(time.time() - start_time)

# Final summary
log_print(f"{timestamp()}: Preprocessing complete!", log_file, quiet)
log_print(f"{timestamp()}: Summary:", log_file, quiet)
log_print(f"{timestamp()}:   Total files successfully processed: {success_count}", log_file, quiet)
log_print(f"{timestamp()}:   Total files not processed: {fail_count}", log_file, quiet)
log_print(f"{timestamp()}:   Total errors encountered: {error_count}", log_file, quiet)
log_print(f"{timestamp()}:   Script duration: {duration} seconds", log_file, quiet)
if files_with_errors:
    log_print(f"{timestamp()}: Files with errors:", log_file, quiet)
    for file in files_with_errors:
        log_print(f"{timestamp()}:   - {file}", log_file, quiet)
log_print(f"{timestamp()}: All output has been logged to {log_file}", log_file, quiet)
