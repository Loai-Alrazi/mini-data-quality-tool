# 
def generate_report(
    rows_before,
    rows_after,
    duplicates_removed,
    missing_values_handled=None,
):
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

