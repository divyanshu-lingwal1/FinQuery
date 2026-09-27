from pypdf import PdfReader


def read_pdf_file(file_path):
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text

import re
from pypdf import PdfReader


def read_pdf_file(file_path):
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def parse_pdf_transactions(text):
    transactions = []

    pattern = re.compile(
        r"Date:\s*(.*?)\s*"
        r"Description:\s*(.*?)\s*"
        r"Category:\s*(.*?)\s*"
        r"Amount:\s*([\d,]+(?:\.\d+)?)",
        re.IGNORECASE
    )

    matches = pattern.findall(text)

    for match in matches:

        transaction = {
            "date": match[0].strip(),
            "description": match[1].strip(),
            "category": match[2].strip(),
            "amount": match[3].replace(",", "").strip()
        }

        transactions.append(transaction)

    return transactions