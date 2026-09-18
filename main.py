"""Command-line entry point for the CSV cleaning workflow."""

import argparse
import sys

from src.adapter import rows_to_dataframe
from src.cleaner import clean_dataframe
from src.exporter import export_clean_data
from src.loader import load_csv
from src.report import generate_report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Clean a local CSV file.")
    parser.add_argument("input_csv", help="Path to a UTF-8 CSV file")
    args = parser.parse_args(argv)

    try:
        print(f"Loading CSV: {args.input_csv}")
        rows = load_csv(args.input_csv)
        data = rows_to_dataframe(rows)
        cleaned, stats = clean_dataframe(data)
        report = generate_report(**stats)
        output_path = export_clean_data(cleaned)
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Cleaned CSV saved to: {output_path}")
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
