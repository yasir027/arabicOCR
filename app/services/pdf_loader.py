import pdfplumber

def get_page_count(pdf_path: str) -> int:
    print("Opening PDF for page count...")
    with pdfplumber.open(pdf_path) as pdf:
        print("PDF opened successfully")
        return len(pdf.pages)

def extract_page_text(pdf_path: str, page_number: int) -> str:
    print("Opening PDF for text extraction...")
    with pdfplumber.open(pdf_path) as pdf:
        print("PDF opened, extracting page...")
        page = pdf.pages[page_number - 1]
        text = page.extract_text()
        print("Text extracted")
        return text or ""
