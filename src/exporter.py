
from pathlib import Path

import pandas as pd


DEFAULT_OUTPUT_DIR = Path("output")
DEFAULT_FILENAME = "cleaned.csv"


def export_clean_data(
    data: pd.DataFrame,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    filename: str = DEFAULT_FILENAME,
) -> Path:
    """
    Export cleaned data to a CSV file.

    Parameters
    ----------
    data : pd.DataFrame
        Cleaned dataset to export.

    output_dir : Path
        Directory where the CSV file will be saved.

    filename : str
        Name of the output CSV file.

    Returns
    -------
    Path
        Path to the generated CSV file.

    Raises
    ------
    TypeError
        If data is not a pandas DataFrame.

    ValueError
        If filename is empty or does not have a CSV extension.

    OSError
        If the output file cannot be written.
    """

    if not isinstance(data, pd.DataFrame):
        raise TypeError("data must be a pandas DataFrame")

    if not filename:
        raise ValueError("filename cannot be empty")

    if not filename.lower().endswith(".csv"):
        raise ValueError("filename must have a .csv extension")

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / filename

    try:
        data.to_csv(output_path, index=False)
    except OSError as exc:
        raise OSError(
            f"Failed to export data to '{output_path}'"
        ) from exc

    return output_path