import easyocr


# Create the reader only once (faster for repeated use)
reader = easyocr.Reader(['en'])


def extract_text_from_receipt(image_path):
    """
    Extracts all text from a receipt image.

    Args:
        image_path (str): Path to the receipt image.

    Returns:
        dict: Extracted text
    """

    result = reader.readtext(image_path)

    extracted_text = ""

    for detection in result:
        extracted_text += detection[1] + "\n"

    return {
        "message": "Text extracted successfully.",
        "text": extracted_text.strip()
    }