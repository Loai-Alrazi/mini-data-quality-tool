import re

import pandas as pd


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with normalized column names."""
    cleaned = df.copy()
    cleaned.columns = [
        _normalize_column_name(column)
        for column in cleaned.columns
    ]

    return cleaned


def handle_missing_values(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Fill missing values and return the number of handled values."""
    cleaned = df.copy()
    missing_count = int(cleaned.isna().sum().sum())

    for column in cleaned.columns:
        if not cleaned[column].isna().any():
            continue

        if pd.api.types.is_numeric_dtype(cleaned[column]):
            fill_value = cleaned[column].median()
            if pd.isna(fill_value):
                fill_value = 0
        else:
            fill_value = "unknown"

        cleaned[column] = cleaned[column].fillna(fill_value)

    return cleaned, missing_count


def remove_duplicate_rows(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Remove duplicate rows and return the number of removed rows."""
    rows_before = len(df)
    cleaned = df.drop_duplicates().reset_index(drop=True)
    duplicates_removed = rows_before - len(cleaned)

    return cleaned, duplicates_removed


def clean_dataframe(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    """Run all cleaning steps and return cleaned data with statistics."""
    rows_before = len(df)

    cleaned = clean_column_names(df)
    cleaned, missing_values_handled = handle_missing_values(cleaned)
    cleaned, duplicates_removed = remove_duplicate_rows(cleaned)

    stats = {
        "rows_before": rows_before,
        "rows_after": len(cleaned),
        "duplicates_removed": duplicates_removed,
        "missing_values_handled": missing_values_handled,
    }

    return cleaned, stats


def _normalize_column_name(column: object) -> str:
    name = str(column).strip().lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    name = re.sub(r"_+", "_", name).strip("_")

    return name or "unnamed_column"
