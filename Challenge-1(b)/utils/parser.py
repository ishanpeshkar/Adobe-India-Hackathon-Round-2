import fitz  # PyMuPDF

def extract_text_from_pdf(file_path):
    """
    Extracts text from each page of the given PDF.

    Returns a list of dictionaries containing:
    - page_number (starting from 1)
    - text (full page text)
    """
    pdf_document = fitz.open(file_path)
    page_data = []

    for page_index in range(len(pdf_document)):
        current_page = pdf_document.load_page(page_index)
        page_text = current_page.get_text()

        if page_text.strip():  # Skip empty pages
            page_data.append({
                "page_number": page_index + 1,
                "text": page_text
            })

    pdf_document.close()
    return page_data