import pytest

from src.report import generate_report


def test_generate_report_contains_basic_statistics():
    report = generate_report(
        rows_before=100,
        rows_after=90,
        duplicates_removed=10,
    )

    assert "Data Cleaning Report" in report
    assert "Rows before cleaning: 100" in report
    assert "Rows after cleaning: 90" in report
    assert "Duplicate rows removed: 10" in report


def test_generate_report_includes_missing_values_when_provided():
    report = generate_report(
        rows_before=100,
        rows_after=95,
        duplicates_removed=5,
        missing_values_handled=12,
    )

    assert "Missing values handled: 12" in report


def test_generate_report_excludes_missing_values_when_not_provided():
    report = generate_report(
        rows_before=100,
        rows_after=95,
        duplicates_removed=5,
    )

    assert "Missing values handled:" not in report


def test_generate_report_returns_string():
    report = generate_report(
        rows_before=10,
        rows_after=8,
        duplicates_removed=2,
    )

    assert isinstance(report, str)


def test_generate_report_preserves_report_structure():
    report = generate_report(
        rows_before=50,
        rows_after=45,
        duplicates_removed=5,
        missing_values_handled=3,
    )

    expected = "\n".join(
        [
            "Data Cleaning Report",
            "====================",
            "",
            "Rows before cleaning: 50",
            "Rows after cleaning: 45",
            "Duplicate rows removed: 5",
            "Missing values handled: 3",
        ]
    )

    assert report == expected


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("rows_before", "50"),
        ("rows_after", 45.5),
        ("duplicates_removed", None),
        ("missing_values_handled", True),
    ],
)
def test_generate_report_rejects_non_integer_statistics(field, value):
    statistics = {
        "rows_before": 50,
        "rows_after": 45,
        "duplicates_removed": 5,
        "missing_values_handled": 3,
    }
    statistics[field] = value

    with pytest.raises(TypeError, match=f"{field} must be an integer"):
        generate_report(**statistics)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("rows_before", -1),
        ("rows_after", -1),
        ("duplicates_removed", -1),
        ("missing_values_handled", -1),
    ],
)
def test_generate_report_rejects_negative_statistics(field, value):
    statistics = {
        "rows_before": 50,
        "rows_after": 45,
        "duplicates_removed": 5,
        "missing_values_handled": 3,
    }
    statistics[field] = value

    with pytest.raises(ValueError, match=f"{field} cannot be negative"):
        generate_report(**statistics)


def test_generate_report_rejects_rows_after_greater_than_rows_before():
    with pytest.raises(
        ValueError,
        match="rows_after cannot be greater than rows_before",
    ):
        generate_report(
            rows_before=50,
            rows_after=51,
            duplicates_removed=0,
        )


def test_generate_report_rejects_duplicates_greater_than_rows_before():
    with pytest.raises(
        ValueError,
        match="duplicates_removed cannot be greater than rows_before",
    ):
        generate_report(
            rows_before=50,
            rows_after=45,
            duplicates_removed=51,
        )
