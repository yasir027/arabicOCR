from fastapi import FastAPI, UploadFile, File
import tempfile, os

from app.services.pdf_loader import get_page_count, extract_page_text
from app.services.table_extractor import extract_tables_hybrid

app = FastAPI(title="arabicOcr")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/debug/pdf-text")
async def debug_pdf_text(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        pdf_path = tmp.name

    pages = get_page_count(pdf_path)

    sample_text = extract_page_text(pdf_path, 1)

    os.unlink(pdf_path)

    return {
        "pages": pages,
        "sample_text": sample_text[:500]  # first 500 chars only
    }

@app.post("/extract/tables")
async def extract_pdf_tables(file: UploadFile = File(...), pages: str = "1"):
    import tempfile, os

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        pdf_path = tmp.name

    # Extract tables
    result = extract_tables_hybrid(pdf_path, pages)

    # Delete temp filed
    os.unlink(pdf_path)

    return {"tables": result}

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()
