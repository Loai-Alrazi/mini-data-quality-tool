def generate_report(
    rows_before,
    rows_after,
    duplicates_removed,
    missing_values_handled=None,
):
    rows_before = _validate_count("rows_before", rows_before)
    rows_after = _validate_count("rows_after", rows_after)
    duplicates_removed = _validate_count(
        "duplicates_removed",
        duplicates_removed,
    )

    if missing_values_handled is not None:
        missing_values_handled = _validate_count(
            "missing_values_handled",
            missing_values_handled,
        )

    if rows_after > rows_before:
        raise ValueError("rows_after cannot be greater than rows_before")

    if duplicates_removed > rows_before:
        raise ValueError("duplicates_removed cannot be greater than rows_before")

    report = [
        "Data Cleaning Report",
        "====================",
        "",
        f"Rows before cleaning: {rows_before}",
        f"Rows after cleaning: {rows_after}",
        f"Duplicate rows removed: {duplicates_removed}",
    ]

    if missing_values_handled is not None:
        report.append(
            f"Missing values handled: {missing_values_handled}"
        )

    return "\n".join(report)


def _validate_count(name, value):
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")

    if value < 0:
        raise ValueError(f"{name} cannot be negative")

    return value

