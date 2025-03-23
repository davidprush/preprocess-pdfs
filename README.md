# preprocess_pdfs.py

## Overview

`preprocess_pdfs.py` is a Python 3 script that processes multi-page PDF files by converting them to PNG images using ImageMagick and extracting text from those images using Tesseract OCR. The script handles all pages of each PDF, logs progress and errors to both the terminal and a log file, and provides a summary of results including successful processes, failures, errors, and runtime duration. It offers flexible options to customize input/output directories, logging behavior, and file deletion preferences.

## Features

- Converts multi-page PDFs to individual PNGs per page.
- Extracts text from PNGs into separate `.txt` files.
- Logs all actions with timestamps to a file and terminal.
- Provides a summary with counts of successful files, failed files, errors, and script duration.
- Supports options to keep PDFs, PNGs, or all files instead of deleting them.
- Customizable input directory, output directory, log file name, and verbosity.

## Prerequisites

- **Python 3**: Version 3.6 or higher.
- **ImageMagick**: For converting PDFs to PNGs.
- **Tesseract OCR**: For extracting text from PNGs.

### Installation

1. **Install Python 3**:
   - On macOS: `brew install python`
   - On Linux: `sudo apt-get install python3` (Ubuntu/Debian) or `sudo dnf install python3` (Fedora)
   - On Windows: Download from [python.org](https://www.python.org/downloads/)

2. **Install ImageMagick**:
   - On macOS: `brew install imagemagick`
   - On Linux: `sudo apt-get install imagemagick` or `sudo dnf install imagemagick`
   - On Windows: Download from [ImageMagick](https://imagemagick.org/script/download.php)

3. **Install Tesseract**:
   - On macOS: `brew install tesseract`
   - On Linux: `sudo apt-get install tesseract-ocr` or `sudo dnf install tesseract`
   - On Windows: Download from [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)

4. **Make the Script Executable** (optional):
   ```bash
   chmod +x preprocess_pdfs.py
   ```

## Usage

Run the script from the command line in a directory containing PDF files, or specify an input directory with options.

## Basic Command

```bash
python3 preprocess_pdfs.py
```
- Processes PDFs in the current directory.
- Saves text files to extracted-text/.
- Deletes PDFs and PNGs after successful processing.
- Logs all output to a timestamped file (e.g., preprocess_log_20250323_143045.txt).

## Options
| Option | Description | Default |
| ------- | ------------ | --------|
| `-h, --help` | Show help message with description, options, and examples | N/A |
| `-i, --input-dir` | Directory containing PDF files to process | Current directory `(.)` |
| `-o, --output-dir` | Directory where extracted text files will be saved | extracted-text |
| `-q, --quiet` | Limit output and log to errors only (verbose otherwise) | False (verbose) |
| `-l, --log-file` | Custom name for the log file | `preprocess_log_YYYYMMDD_HHMMSS.txt` |
| `-k, --keep-pdfs` | Prevent deletion of original PDF files| False (delete PDFs) |
| `-p, --keep-pngs` | Prevent deletion of intermediate PNG files | False (delete PNGs) |
| `-n, --no-delete` | Prevent deletion of any files (PDFs and PNGs), overrides `-k` and `-p` | False (delete all) |
| `-e, --error-handling` | `{exit,continue}` Action on error: 'exit' to stop script, 'continue' to proceed | continue |

## Examples

- Default run:
```bash
python3 preprocess_pdfs.py
```
- Specify input directory:
```bash
python3 preprocess_pdfs.py -i ./pdfs
```
- Custom output directory:
```bash
python3 preprocess_pdfs.py -o ./text_files
```
- Quiet mode with custom log:
```bash
python3 preprocess_pdfs.py -q -l errors.log
```
- Keep PDFs:
```bash
python3 preprocess_pdfs.py -k
```
- Keep PNGs:
```bash
python3 preprocess_pdfs.py -p
```
- Keep all files:
```bash
python3 preprocess_pdfs.py -n
```
- Combined options:
```bash
python3 preprocess_pdfs.py -i ./pdfs -o ./text -q -l mylog.txt -n
```

## Output

### Help

```
usage: preprocess_pdfs.py [-h] [-i INPUT_DIR] [-o OUTPUT_DIR] [-q] [-l LOG_FILE] [-k] [-p] [-n] [-e {exit,continue}]

A script to preprocess multi-page PDF files by converting them to PNGs and extracting text using ImageMagick and Tesseract. Processes all pages of each PDF, logs progress and errors, and provides a summary of results.

options:
  -h, --help            show this help message and exit
  -i INPUT_DIR, --input-dir INPUT_DIR
                        Directory containing PDF files to process (default: current directory '.')
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Directory where extracted text files will be saved (default: 'extracted-text')
  -q, --quiet           Limit terminal output and log file entries to errors only (default: verbose output)
  -l LOG_FILE, --log-file LOG_FILE
                        Custom name for the log file (default: 'preprocess_log_YYYYMMDD_HHMMSS.txt')
  -k, --keep-pdfs       Prevent deletion of original PDF files (default: delete PDFs)
  -p, --keep-pngs       Prevent deletion of intermediate PNG files (default: delete PNGs)
  -n, --no-delete       Prevent deletion of any files (PDFs and PNGs), overrides --keep-pdfs and --keep-pngs
  -e {exit,continue}, --error-handling {exit,continue}
                        Action on error: 'exit' to stop script, 'continue' to proceed (default: 'continue')

Examples:
  python3 preprocess_pdfs.py                    # Process PDFs with default settings
  python3 preprocess_pdfs.py -i ./pdfs          # Process PDFs from './pdfs'
  python3 preprocess_pdfs.py -o ./text          # Save text to './text'
  python3 preprocess_pdfs.py -q -l errors.log   # Quiet mode, log to 'errors.log'
  python3 preprocess_pdfs.py -k                 # Keep PDFs
  python3 preprocess_pdfs.py -p                 # Keep PNGs
  python3 preprocess_pdfs.py -n                 # Keep all files
  python3 preprocess_pdfs.py -e exit            # Exit on first error
  python3 preprocess_pdfs.py -i pdfs -o text -q -l mylog.txt -n -e continue  # Combined options
```
The script outputs to both the terminal and a log file with timestamps. Example (default mode):

```
2025-03-23 14:30:45: Directory 'extracted-text' already exists.
2025-03-23 14:30:45: Converting doc1.pdf to PNGs...
2025-03-23 14:30:45: Deleting doc1.pdf...
2025-03-23 14:30:46: Converting doc1-0.png to extracted-text/doc1-0.txt...
2025-03-23 14:30:46: Deleting doc1-0.png...
2025-03-23 14:30:46: Successfully processed doc1.pdf (all 1 pages)
2025-03-23 14:30:46: Preprocessing complete!
2025-03-23 14:30:46: Summary:
2025-03-23 14:30:46:   Total files successfully processed: 1
2025-03-23 14:30:46:   Total files not processed: 0
2025-03-23 14:30:46:   Total errors encountered: 0
2025-03-23 14:30:46:   Script duration: 1 seconds
2025-03-23 14:30:46: All output has been logged to preprocess_log_20250323_143045.txt
```
With `-q` (quiet mode), only errors and the summary appear:

```
2025-03-23 14:30:45: Error: Failed to convert doc1-0.png to extracted-text/doc1-0.txt
2025-03-23 14:30:46: Preprocessing complete!
2025-03-23 14:30:46: Summary:
2025-03-23 14:30:46:   Total files successfully processed: 0
2025-03-23 14:30:46:   Total files not processed: 1
2025-03-23 14:30:46:   Total errors encountered: 1
2025-03-23 14:30:46:   Script duration: 1 seconds
```

## Notes
- Multi-page PDFs: Each page is processed into a separate text file (e.g., doc-0.txt, doc-1.txt).
- Error Handling: Errors (e.g., conversion failures) are logged but do not stop the script; it continues to the next file or page.
- File Deletion: By default, PDFs and PNGs are deleted after successful processing unless -k, -p, or -n is used.
- Log File: Created in the current directory unless a full path is specified with -l.
- Verbose Errors: To see detailed error messages (e.g., from convert or tesseract), remove stderr=subprocess.DEVNULL from the script.

## Troubleshooting
Command not found: Ensure convert and tesseract are in your PATH.
Permissions: Run with sudo or adjust file permissions if deletion fails.
No PDFs found: Check the input directory specified with -i.

## License
This script is provided as-is under the MIT License. Feel free to modify and distribute it as needed.
```
Copyright 2025 David Rush

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
