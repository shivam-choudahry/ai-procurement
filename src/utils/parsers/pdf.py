"""
PDF parser using pdfplumber (primary) with PyPDF2 fallback.
"""

import io
import logging

logger = logging.getLogger(__name__)


def parse_pdf(content: bytes) -> str:
    """
    Extract text from a PDF file.

    Args:
        content: Raw PDF bytes

    Returns:
        Normalized plain text, page-separated
    """
    # Primary: pdfplumber (better layout handling)
    try:
        import pdfplumber
        pages = []
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    pages.append(f"[Page {i + 1}]\n{text.strip()}")
        if pages:
            logger.info(f"pdfplumber: extracted {len(pages)} pages")
            return "\n\n".join(pages)
    except ImportError:
        logger.warning("pdfplumber not available, falling back to PyPDF2")
    except Exception as e:
        logger.warning(f"pdfplumber failed: {e}, falling back to PyPDF2")

    # Fallback: PyPDF2
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(content))
        pages = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                pages.append(f"[Page {i + 1}]\n{text.strip()}")
        if pages:
            logger.info(f"PyPDF2: extracted {len(pages)} pages")
            return "\n\n".join(pages)
    except Exception as e:
        logger.error(f"PyPDF2 also failed: {e}")

    return "[PDF parse error: could not extract text from this document]"

