import camelot
import pdfplumber
import re
from typing import List, Dict


# -----------------------------
# Helpers
# -----------------------------

ARABIC_NUMBER_RE = re.compile(r'[۰-۹٬]+')

def normalize_cell(cell: str) -> str:
    """Clean cell text without collapsing structure."""
    if not cell:
        return ""
    cell = str(cell)
    cell = cell.replace("\n", " ").strip()
    cell = re.sub(r"\s+", " ", cell)
    return cell


def is_numeric(cell: str) -> bool:
    return bool(ARABIC_NUMBER_RE.fullmatch(cell))


def reconstruct_numbers(row: List[str]) -> List[str]:
    """
    Rebuild fragmented Arabic numbers WITHOUT merging columns.
    """
    rebuilt = []
    buffer = ""

    for cell in row:
        cell = cell.strip()
        if is_numeric(cell):
            buffer += cell
        else:
            if buffer:
                rebuilt.append(buffer)
                buffer = ""
            rebuilt.append(cell)

    if buffer:
        rebuilt.append(buffer)

    return rebuilt


def is_footnote_row(row: List[str]) -> bool:
    text = " ".join(row)
    return any(keyword in text for keyword in [
        "إن معلومات", "توزيع", "توجد", "تعتمد"
    ])


# -----------------------------
# 1. Camelot Lattice Tables
# -----------------------------

def extract_lattice_tables(pdf_path: str, pages: str) -> List[Dict]:
    tables = camelot.read_pdf(
        pdf_path,
        pages=pages,
        flavor="lattice",
        strip_text="\n"
    )

    results = []
    for table in tables:
        results.append({
            "page": table.page,
            "type": "lattice",
            "data": table.df.values.tolist()
        })

    return results


# -----------------------------
# 2. pdfplumber – SAFE STRUCTURED EXTRACTION
# -----------------------------

def extract_horizontal_line_tables(pdf_path: str, pages: List[int]) -> List[Dict]:
    results = []

    table_settings = {
        "vertical_strategy": "text",
        "horizontal_strategy": "lines",
        "snap_tolerance": 5,
        "text_tolerance": 6,
        "intersection_tolerance": 5,
        "min_words_vertical": 2,
        "min_words_horizontal": 1,
    }

    with pdfplumber.open(pdf_path) as pdf:
        for page_num in pages:
            page = pdf.pages[page_num - 1]
            tables = page.find_tables(table_settings)

            for table in tables:
                raw = table.extract()
                if not raw or len(raw) < 2:
                    continue

                # Normalize cells
                normalized = [
                    [normalize_cell(c) for c in row]
                    for row in raw
                ]

                # Remove fully empty rows
                normalized = [
                    row for row in normalized if any(row)
                ]

                # Rebuild fragmented numbers (row-safe)
                reconstructed = [
                    reconstruct_numbers(row)
                    for row in normalized
                ]

                # Determine dominant column count
                col_counts = [len(r) for r in reconstructed]
                target_cols = max(set(col_counts), key=col_counts.count)

                # Enforce fixed column width
                fixed = []
                for row in reconstructed:
                    if len(row) < target_cols:
                        row += [""] * (target_cols - len(row))
                    elif len(row) > target_cols:
                        row = row[:target_cols]
                    fixed.append(row)

                # Remove footnotes
                data_rows = [
                    row for row in fixed
                    if not is_footnote_row(row)
                ]

                if len(data_rows) < 2:
                    continue

                results.append({
                    "page": page_num,
                    "type": "horizontal_lines",
                    "data": data_rows,
                    "bbox": table.bbox,
                    "settings_used": table_settings
                })

    return results


# -----------------------------
# 3. Hybrid Extractor
# -----------------------------

def extract_tables_hybrid(pdf_path: str, pages: str) -> List[Dict]:
    if pages == "1-end":
        with pdfplumber.open(pdf_path) as pdf:
            page_numbers = list(range(1, len(pdf.pages) + 1))
    else:
        page_numbers = []
        for part in pages.split(","):
            if "-" in part:
                start, end = part.split("-")
                page_numbers.extend(range(int(start), int(end) + 1))
            else:
                page_numbers.append(int(part))

    lattice_tables = extract_lattice_tables(pdf_path, pages)
    horizontal_tables = extract_horizontal_line_tables(pdf_path, page_numbers)

    return lattice_tables + horizontal_tables


# -----------------------------
# Example
# -----------------------------
if __name__ == "__main__":
    pdf_file = "your_arabic_pdf.pdf"
    tables = extract_tables_hybrid(pdf_file, "98")

    for t in tables:
        print(f"\nPage {t['page']} | {t['type']}")
        for row in t["data"][:5]:
            print(row)
