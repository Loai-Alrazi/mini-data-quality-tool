import pandas as pd
import pytest

from src.exporter import export_clean_data


def test_export_clean_data_creates_csv_file(tmp_path):
    data = pd.DataFrame(
        {
            "name": ["Ali", "Ahmed"],
            "age": [25, 30],
        }
    )

    output_path = export_clean_data(
        data=data,
        output_dir=tmp_path,
    )

    assert output_path.exists()
    assert output_path.name == "cleaned.csv"


def test_exported_csv_contains_correct_data(tmp_path):
    data = pd.DataFrame(
        {
            "name": ["Ali", "Ahmed"],
            "age": [25, 30],
        }
    )

    output_path = export_clean_data(
        data=data,
        output_dir=tmp_path,
    )

    exported_data = pd.read_csv(output_path)

    pd.testing.assert_frame_equal(
        exported_data,
        data,
    )


def test_exporter_creates_output_directory(tmp_path):
    output_dir = tmp_path / "output"

    data = pd.DataFrame(
        {
            "name": ["Ali"],
        }
    )

    output_path = export_clean_data(
        data=data,
        output_dir=output_dir,
    )

    assert output_dir.exists()
    assert output_path.exists()


def test_exporter_rejects_non_dataframe(tmp_path):
    with pytest.raises(TypeError):
        export_clean_data(
            data=["Ali", "Ahmed"],
            output_dir=tmp_path,
        )


def test_exporter_rejects_non_csv_filename(tmp_path):
    data = pd.DataFrame(
        {
            "name": ["Ali"],
        }
    )

    with pytest.raises(ValueError):
        export_clean_data(
            data=data,
            output_dir=tmp_path,
            filename="cleaned.txt",
        )