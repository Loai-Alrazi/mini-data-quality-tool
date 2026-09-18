import pandas as pd

from src.cleaner import (
    clean_column_names,
    clean_dataframe,
    handle_missing_values,
    remove_duplicate_rows,
)


def test_clean_column_names_normalizes_common_column_formats():
    data = pd.DataFrame(
        columns=[
            " Student Name ",
            "Age (Years)",
            "Score%",
            "",
        ]
    )

    result = clean_column_names(data)

    assert list(result.columns) == [
        "student_name",
        "age_years",
        "score",
        "unnamed_column",
    ]


def test_handle_missing_values_fills_numeric_and_text_columns():
    data = pd.DataFrame(
        {
            "name": ["Ahmed", None, "Sara"],
            "age": [20, None, 24],
        }
    )

    result, missing_count = handle_missing_values(data)

    assert missing_count == 2
    assert result.loc[1, "name"] == "unknown"
    assert result.loc[1, "age"] == 22
    assert not result.isna().any().any()


def test_handle_missing_values_fills_all_missing_numeric_column_with_zero():
    data = pd.DataFrame(
        {
            "score": pd.Series([None, None], dtype="float64"),
        }
    )

    result, missing_count = handle_missing_values(data)

    assert missing_count == 2
    assert result["score"].tolist() == [0, 0]


def test_remove_duplicate_rows_removes_duplicates_and_resets_index():
    data = pd.DataFrame(
        {
            "name": ["Ahmed", "Sara", "Sara"],
            "city": ["Sanaa", "Aden", "Aden"],
        }
    )

    result, duplicates_removed = remove_duplicate_rows(data)

    assert duplicates_removed == 1
    assert len(result) == 2
    assert result.index.tolist() == [0, 1]


def test_clean_dataframe_runs_all_cleaning_steps_and_returns_stats():
    data = pd.DataFrame(
        {
            " Student Name ": ["Ahmed", "Sara", "Sara"],
            "Age": [20, None, None],
            "City": ["Sanaa", "Aden", "Aden"],
        }
    )

    result, stats = clean_dataframe(data)

    assert list(result.columns) == ["student_name", "age", "city"]
    assert result.to_dict(orient="records") == [
        {"student_name": "Ahmed", "age": 20.0, "city": "Sanaa"},
        {"student_name": "Sara", "age": 20.0, "city": "Aden"},
    ]
    assert stats == {
        "rows_before": 3,
        "rows_after": 2,
        "duplicates_removed": 1,
        "missing_values_handled": 2,
    }
