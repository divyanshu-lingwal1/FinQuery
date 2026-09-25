import pytesseract
from PIL import Image


def read_image_file(file_path):
    image = Image.open(file_path)

    text = pytesseract.image_to_string(image)

    return text
