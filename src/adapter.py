"""Adapt the loader's string records to the cleaner's DataFrame input."""

import pandas as pd


def rows_to_dataframe(rows: list[dict[str, str]]) -> pd.DataFrame:
    """Recognize blank cells and columns containing only numeric values."""
    if not rows:
        raise ValueError("CSV file must contain at least one data row.")

    data = pd.DataFrame(rows, dtype=object).replace(r"^\s*$", float("nan"), regex=True)
    for column in data.columns:
        values = data[column]
        numeric = pd.to_numeric(values, errors="coerce")
        if values.notna().any() and numeric.notna().equals(values.notna()):
            data[column] = numeric

    return data
