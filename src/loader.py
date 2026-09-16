import csv
from pathlib import Path


def load_csv(file_path: str) -> list[dict[str, str]]:
    """Load and validate a CSV file."""
    path = Path(file_path)

    if not path.suffix:
        raise ValueError("Input file must have a .csv extension.")

    if path.suffix.lower() != ".csv":
        raise ValueError("Input file must be a CSV file.")

    try:
        with path.open("r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)

            try:
                headers = next(reader)
            except StopIteration as exc:
                raise ValueError("CSV file is empty.") from exc

            if not headers or any(not header.strip() for header in headers):
                raise ValueError("CSV file must contain valid column names.")

            rows = []

            for row_number, row in enumerate(reader, start=2):
                if len(row) != len(headers):
                    raise ValueError(
                        f"Invalid CSV structure at row {row_number}."
                    )

                rows.append(dict(zip(headers, row)))

    except csv.Error as exc:
        raise ValueError("Invalid CSV content.") from exc

    return rows
