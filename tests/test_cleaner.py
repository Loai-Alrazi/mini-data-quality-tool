import pandas as pd
import pytest

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


def test_clean_column_names_handles_blank_and_non_string_names():
    data = pd.DataFrame([[1, 2, 3]], columns=["  ", "!!!", 42])

    assert list(clean_column_names(data).columns) == [
        "unnamed_column", "unnamed_column", "42"
    ]


def test_handle_missing_values_fills_entirely_missing_text_column():
    data = pd.DataFrame({"name": pd.Series([None, None], dtype="object")})

    cleaned, count = handle_missing_values(data)

    assert cleaned["name"].tolist() == ["unknown", "unknown"]
    assert count == 2


def test_handle_missing_values_preserves_complete_data():
    data = pd.DataFrame({"score": [0, 10], "name": ["Ali", "Sara"]})

    cleaned, count = handle_missing_values(data)

    pd.testing.assert_frame_equal(cleaned, data)
    assert count == 0


def test_remove_duplicate_rows_keeps_first_occurrence_and_resets_index():
    data = pd.DataFrame(
        {"name": ["Ali", "Sara", "Ali", "Ali"], "score": [10, 20, 10, 30]},
        index=[4, 6, 8, 10],
    )

    cleaned, count = remove_duplicate_rows(data)

    expected = pd.DataFrame({"name": ["Ali", "Sara", "Ali"], "score": [10, 20, 30]})
    pd.testing.assert_frame_equal(cleaned, expected)
    assert count == 1


def test_remove_duplicate_rows_preserves_unique_rows():
    data = pd.DataFrame({"name": ["Ali", "Sara"]})

    cleaned, count = remove_duplicate_rows(data)

    pd.testing.assert_frame_equal(cleaned, data)
    assert count == 0


def test_clean_dataframe_fills_before_removing_duplicates_and_reports_counts():
    data = pd.DataFrame(
        {" Name ": ["Ali", "Ali", None], " Score ": [10.0, None, 10.0]}
    )

    cleaned, stats = clean_dataframe(data)

    expected = pd.DataFrame({"name": ["Ali", "unknown"], "score": [10.0, 10.0]})
    pd.testing.assert_frame_equal(cleaned, expected)
    assert stats == {
        "rows_before": 3,
        "rows_after": 2,
        "duplicates_removed": 1,
        "missing_values_handled": 2,
    }


def test_clean_dataframe_handles_empty_data_with_columns():
    data = pd.DataFrame(
        {" Name ": pd.Series(dtype="object"), "Score": pd.Series(dtype="float64")}
    )

    cleaned, stats = clean_dataframe(data)

    assert cleaned.empty
    assert list(cleaned.columns) == ["name", "score"]
    assert stats == {
        "rows_before": 0,
        "rows_after": 0,
        "duplicates_removed": 0,
        "missing_values_handled": 0,
    }


@pytest.mark.parametrize(
    "clean",
    [clean_column_names, handle_missing_values, remove_duplicate_rows, clean_dataframe],
)
def test_cleaning_does_not_mutate_input(clean):
    data = pd.DataFrame(
        {" Name ": ["Ali", None, "Ali"], "Score": [10.0, None, 10.0]},
        index=[2, 4, 6],
    )
    original = data.copy(deep=True)

    clean(data)

    pd.testing.assert_frame_equal(data, original)
