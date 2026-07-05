"""
Document Parser Agent — orchestrates parsing of uploaded vendor documents.
This agent wraps the parser/ module for use in the agent pipeline.
"""

import logging
from src.utils.parsers import parse_document
from langfuse import observe

logger = logging.getLogger(__name__)

@observe
def parse_vendor_document(
    vendor_id: str,
    vendor_name: str,
    filename: str,
    content: bytes,
) -> dict:
    """
    Parse a vendor document to plain text.

    Args:
        vendor_id: Vendor identifier
        vendor_name: Vendor display name
        filename: Original filename with extension
        content: Raw file bytes

    Returns:
        ParsedDoc dict with text and metadata
    """
    text = parse_document(filename, content)
    ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else "txt"
    method_map = {
        "pdf": "pdfplumber",
        "docx": "python-docx",
        "doc": "python-docx",
        "txt": "plaintext",
        "md": "plaintext",
        "markdown": "plaintext",
    }

    result = {
        "vendor_id": vendor_id,
        "vendor_name": vendor_name,
        "filename": filename,
        "text": text,
        "parse_method": method_map.get(ext, "unknown"),
        "char_count": len(text),
        "success": not text.startswith("["),  # Error messages start with [
    }
    logger.info(f"Parsed {filename}: {result['char_count']} chars via {result['parse_method']}")
    return result

