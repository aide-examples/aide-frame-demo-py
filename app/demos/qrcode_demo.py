"""Demo: QR Code generation."""

from aide_frame import qrcode_utils

TITLE = "QR Code"
DESCRIPTION = "Generate QR codes from text or URLs"


def run(data: dict) -> dict:
    """
    Generate a QR code from input text.

    Input: {"text": "https://example.com"}
    Output: {"image": "data:image/png;base64,...", "text": "https://example.com"}
    """
    text = data.get('text', '').strip()
    if not text:
        return {"error": "Text is required"}, 400

    if not qrcode_utils.is_available():
        return {"error": "qrcode library not installed. Run: pip install qrcode[pil]"}, 500

    try:
        data_url = qrcode_utils.generate_qr_base64(text)
        if data_url is None:
            return {"error": "Failed to generate QR code"}, 500

        return {
            "text": text,
            "image": data_url,
            "size": len(text)
        }
    except Exception as e:
        return {"error": str(e)}, 500
