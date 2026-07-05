"""Document parser package — PDF, DOCX, XLSX, TXT/MD."""
from src.utils.parsers.pdf import parse_pdf
from src.utils.parsers.docx import parse_docx
from src.utils.parsers.txt import parse_txt
from src.utils.parsers.xlsx import parse_xlsx


def parse_document(filename: str, content: bytes) -> str:
    """
    Route a document to the appropriate parser based on file extension.

    Args:
        filename: Original filename with extension
        content: Raw bytes of the file

    Returns:
        Normalized plain text
    """
    ext = filename.lower().split(".")[-1]
    if ext == "pdf":
        return parse_pdf(content)
    elif ext in ("docx", "doc"):
        return parse_docx(content)
    elif ext in ("xlsx", "xls"):
        return parse_xlsx(content)
    elif ext in ("txt", "md", "markdown"):
        return parse_txt(content)
    else:
        return content.decode("utf-8", errors="replace")


__all__ = ["parse_document", "parse_pdf", "parse_docx", "parse_xlsx", "parse_txt"]

