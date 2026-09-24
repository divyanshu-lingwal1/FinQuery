import csv


def read_csv_file(file_path):
    with open(file_path, "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        reader.fieldnames = [column.strip() for column in reader.fieldnames]

        required_columns = {
            "date",
            "description",
            "category",
            "amount"
        }

        if not required_columns.issubset(reader.fieldnames):
            raise ValueError("CSV file is missing required columns")

        data = []

        for row in reader:

            if not any(row.values()):
                continue

            transaction = {
                "date": row["date"],
                "description": row["description"],
                "category": row["category"],
                "amount": row["amount"]
            }

            data.append(transaction)

        return data