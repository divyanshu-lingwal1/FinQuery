from docx import Document


def read_docx_file(file_path):
    document = Document(file_path)

    text = ""

    # Read normal paragraphs
    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text += paragraph.text + "\n"

    # Read tables
    for table in document.tables:
        for row in table.rows:
            row_data = []

            for cell in row.cells:
                row_data.append(cell.text.strip())

            text += " ".join(row_data) + "\n"

    return text