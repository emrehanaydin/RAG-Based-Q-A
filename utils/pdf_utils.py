from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts text from a PDF file.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted text from the PDF file.
    """
    try:
        reader = PdfReader(pdf_path)
        text = ''

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text
        return text
    except Exception as e:
        raise RuntimeError(f"Error extracting text from PDF: {e}")

def chunk_text(text: str, chunk_size: int = 100) -> list:
    """Chunks the input text into smaller pieces.

    Args:
        text (str): The text to be chunked.
        chunk_size (int): Number of words per chunk.

    Returns:
        list: List of text chunks.
    """
    if not text:
        return []

    words = text.split()
    chunks = [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

    return chunks


def normalize_turkish(text: str) -> str:
    """
    Normalize Turkish characters in the given text.

    This function replaces specific Turkish characters with their normalized equivalents.

    Args:
        text (str): The text to be normalized.

    Returns:
        str: The text with Turkish characters replaced by their normalized counterparts.
    """
    tr_chars = 'ýÞþðÐÝçÇöÖüÜıİ'
    tr_mapping = str.maketrans(tr_chars, 'ıŞşğĞİçÇöÖüÜıİ')
    return text.translate(tr_mapping)
