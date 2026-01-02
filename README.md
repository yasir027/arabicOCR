Arabic OCR & Table Extraction Application
Overview

This application is a Python-based backend service for extracting structured tables from Arabic-language PDF documents.
It is built to safely handle complex Arabic financial statements and reports where tables are often:

Partially bordered or irregular

Containing fragmented Arabic numerals

Mixed with explanatory footnotes

Visually aligned but not structurally tagged

The system focuses on accuracy, column integrity, and data reliability, rather than aggressive extraction.

The system focuses on accuracy, column integrity, and data reliability,
rather than aggressive extraction.


Project Directory Structure

arabicOcr/
│
├── app/                         # Application source code
│   └── main.py                  # FastAPI entry point (Uvicorn app)
│
├── tests/                       # Test cases (unit / integration)
│
├── venv/                        # Python virtual environment
│
├── Sabek Financial Statement.pdf  # Sample Arabic financial PDF
│
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
└── .gitignore                   # Git ignore rules


What the Application Does

- Extracts structured tables from Arabic-language PDF documents
- Preserves column alignment and row integrity
- Reconstructs fragmented Arabic numerals safely
- Filters narrative rows and explanatory footnotes
- Provides a FastAPI-based backend for integration and automation


Core Extraction Strategy
1. Lattice (Grid-Based) Extraction

Uses Camelot

Applied when tables have clear borders

Minimal cleanup required

2. Line-Based Structured Extraction

Uses pdfplumber

Detects rows via horizontal lines and text alignment

Handles partially bordered and irregular tables

Includes:

Arabic numeral reconstruction

Fixed column enforcement

Footnote removal

3. Hybrid Output

Results from both methods are combined

No forced deduplication to avoid data loss

Output Format

Each extracted table contains:

Page number

Extraction method (lattice or horizontal_lines)

Table data as a 2D list (rows × columns)

Bounding box (for debugging/validation)

Extraction settings used

This output can be directly converted to:

JSON

CSV

Pandas DataFrame

Database records

Requirements
System Requirements

Python 3.8+

Ghostscript (required for Camelot)

Python Dependencies

All dependencies are defined in:

requirements.txt

How to Run the Application
1. Create a Virtual Environment

From the project root:

python -m venv venv


Activate it:

venv\Scripts\activate        # Windows
source venv/bin/activate    # macOS/Linux

2. Install Dependencies
pip install -r requirements.txt


⚠️ Make sure Ghostscript is installed and available in your system PATH.

3. Start the Application Server

Run the FastAPI application using Uvicorn:

python -m uvicorn app.main:app


The API will start on the default address:

http://127.0.0.1:8000

Typical Usage

Upload or reference an Arabic PDF (e.g. financial statements)

Specify page ranges for extraction

Receive structured table data as API responses

Use extracted data for analytics, reporting, or storage

Design Principles

Data integrity over extraction volume

No unsafe column merging

Row-safe numeric reconstruction

Arabic-aware processing

Fail-safe filtering of unreliable rows

If a row or table cannot be confidently reconstructed, it is intentionally excluded.

Intended Use Cases

Arabic financial statements

Government and regulatory reports

Statistical publications

Research and compliance workflows

OCR and data ingestion pipelines

Known Limitations

Does not perform OCR on scanned images (OCR must be pre-applied)

Heavily malformed tables may be skipped

Footnote detection is keyword-based and may require tuning for new document formats

Summary

This application provides a production-ready backend for extracting structured tables from Arabic PDFs, with a strong emphasis on correctness, safety, and maintainability.


