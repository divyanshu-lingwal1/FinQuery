import pytesseract
from PIL import Image


def read_image_file(file_path):
    image = Image.open(file_path)

    text = pytesseract.image_to_string(image)

    return text

import re


def parse_image_transactions(text):
    transactions = []

    date_matches = list(
        re.finditer(
            r"Date\s*[:.]?\s*(\d{4}-\d{2}-\d{2})",
            text,
            re.IGNORECASE
        )
    )

    for index, match in enumerate(date_matches):

        start = match.start()

        if index + 1 < len(date_matches):
            end = date_matches[index + 1].start()
        else:
            end = len(text)

        block = text[start:end]

        description_match = re.search(
            r"Description\s*[:.]?\s*(.*?)(?=\n|Category|Amount|$)",
            block,
            re.IGNORECASE
        )

        category_match = re.search(
            r"Category\s*[:.]?\s*(.*?)(?=\n|Amount|$)",
            block,
            re.IGNORECASE
        )

        amount_match = re.search(
            r"Amount\s*[:.]?\s*([\d,]+(?:\.\d+)?)",
            block,
            re.IGNORECASE
        )

        if description_match and category_match and amount_match:

            transaction = {
                "date": match.group(1).strip(),
                "description": description_match.group(1).strip(),
                "category": category_match.group(1).strip(),
                "amount": amount_match.group(1).replace(",", "").strip()
            }

            transactions.append(transaction)

    return transactions
