import csv
from datetime import datetime


def convert_date(date_value):
    date_value = date_value.strip()

    date_formats = [
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%d.%m.%Y"
    ]

    for date_format in date_formats:

        try:

            date_object = datetime.strptime(
                date_value,
                date_format
            )

            return date_object.strftime("%Y-%m-%d")

        except ValueError:
            continue

    raise ValueError(
        f"Invalid date format: {date_value}"
    )


def read_csv_file(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8-sig"
    ) as file:

        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError(
                "CSV file is empty or invalid"
            )

        reader.fieldnames = [
            column.strip()
            for column in reader.fieldnames
        ]

        required_columns = {
            "date",
            "description",
            "category",
            "amount"
        }

        if not required_columns.issubset(
            reader.fieldnames
        ):

            raise ValueError(
                "CSV file is missing required columns"
            )

        data = []

        for row in reader:

            if not any(row.values()):
                continue

            transaction = {
                "date": convert_date(
                    row["date"]
                ),
                "description": row["description"].strip(),
                "category": row["category"].strip(),
                "amount": row["amount"].strip()
            }

            data.append(transaction)

        return data