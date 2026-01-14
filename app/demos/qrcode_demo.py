"""Demo: QR Code generation."""

import base64
import io

TITLE = "QR Code"
DESCRIPTION = "Generate QR codes from text or URLs"

# Try to import qrcode library
try:
    import qrcode
    QRCODE_AVAILABLE = True
except ImportError:
    QRCODE_AVAILABLE = False


def run(data: dict) -> dict:
    """
    Generate a QR code from input text.

    Input: {"text": "https://example.com"}
    Output: {"image": "data:image/png;base64,...", "text": "https://example.com"}
    """
    text = data.get('text', '').strip()
    if not text:
        return {"error": "Text is required"}, 400

    if not QRCODE_AVAILABLE:
        return {"error": "qrcode library not installed. Run: pip install qrcode[pil]"}, 500

    try:
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=2,
        )
        qr.add_data(text)
        qr.make(fit=True)

        # Create image
        img = qr.make_image(fill_color="black", back_color="white")

        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        return {
            "text": text,
            "image": f"data:image/png;base64,{img_base64}",
            "size": len(text)
        }
    except Exception as e:
        return {"error": str(e)}, 500
