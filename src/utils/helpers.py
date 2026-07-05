"""Utility helpers for the RFQ prototype."""

import io
import json


def parse_uploaded_file(uploaded_file) -> str:
    """Extract text from an uploaded file (txt, md, pdf, docx)."""
    filename = uploaded_file.name.lower()

    if filename.endswith((".txt", ".md")):
        return uploaded_file.read().decode("utf-8", errors="replace")

    elif filename.endswith(".pdf"):
        try:
            import PyPDF2
            reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as e:
            return f"[PDF parse error: {e}]"

    elif filename.endswith(".docx"):
        try:
            from docx import Document
            doc = Document(io.BytesIO(uploaded_file.read()))
            return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
        except Exception as e:
            return f"[DOCX parse error: {e}]"

    elif filename.endswith(".json"):
        try:
            data = json.loads(uploaded_file.read().decode("utf-8"))
            if isinstance(data, dict):
                return data.get("response_text", json.dumps(data, indent=2))
            return json.dumps(data, indent=2)
        except Exception as e:
            return f"[JSON parse error: {e}]"

    return f"[Unsupported file format: {filename}]"


def status_badge(status: str) -> str:
    """Return an emoji badge for a status value."""
    badges = {
        "present": "✅",
        "partial": "🟡",
        "missing": "🔴",
        "unclear": "⚠️",
        "conflicting": "🚨",
        "HIGH": "🔴 HIGH",
        "MEDIUM": "🟡 MEDIUM",
        "LOW": "🟢 LOW",
        "PASS": "✅ PASS",
        "FAIL": "❌ FAIL",
        "PARTIAL": "🟡 PARTIAL",
        "UNKNOWN": "❓ UNKNOWN",
    }
    return badges.get(status, status)


def risk_color(risk_level: str) -> str:
    """Return a color hex for risk level."""
    colors = {"HIGH": "#ff4b4b", "MEDIUM": "#ffa500", "LOW": "#21c354"}
    return colors.get(risk_level, "#888888")


def score_to_stars(score) -> str:
    """Convert a numeric score to star display."""
    if score == "N/A" or score is None:
        return "N/A"
    try:
        n = int(score)
        return "★" * n + "☆" * (5 - n)
    except (ValueError, TypeError):
        return str(score)


def truncate(text: str, max_len: int = 200) -> str:
    """Truncate text to max_len characters."""
    if not text:
        return ""
    return text[:max_len] + ("..." if len(text) > max_len else "")
