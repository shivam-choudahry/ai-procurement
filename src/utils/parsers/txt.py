"""
Plain text / Markdown passthrough parser.
"""

import logging

logger = logging.getLogger(__name__)


def parse_txt(content: bytes) -> str:
    """
    Decode a plain text or markdown file to string.

    Args:
        content: Raw bytes

    Returns:
        Decoded string
    """
    encodings = ["utf-8", "latin-1", "cp1252"]
    for enc in encodings:
        try:
            text = content.decode(enc)
            logger.info(f"txt parser: decoded with {enc}, {len(text)} chars")
            return text
        except UnicodeDecodeError:
            continue
    return content.decode("utf-8", errors="replace")

