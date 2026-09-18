import subprocess
import sys
from pathlib import Path

import pandas as pd
import pytest

import main as cli
from src.adapter import rows_to_dataframe


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_main_cleans_sample_and_reports_results(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    result = cli.main([str(PROJECT_ROOT / "data" / "sample.csv")])

    assert result == 0
    cleaned = pd.read_csv(tmp_path / "output" / "cleaned.csv")
    expected = pd.DataFrame({
        "student_name": ["Ahmed", "Sara", "Mohammed", "Ali", "Noor", "Huda", "Omar"],
        "age": [22.0, 21.0, 22.0, 24.0, 23.0, 22.0, 22.0],
        "city": ["Sanaa", "Aden", "Taiz", "Sanaa", "unknown", "Aden", "Taiz"],
        "score": [85.0, 90.0, 78.0, 88.0, 88.0, 92.0, 75.0],
    })
    pd.testing.assert_frame_equal(cleaned, expected)
    captured = capsys.readouterr()
    assert captured.err == ""
    assert "Cleaned CSV saved to:" in captured.out
    assert "Rows before cleaning: 8" in captured.out
    assert "Rows after cleaning: 7" in captured.out
    assert "Duplicate rows removed: 1" in captured.out
    assert "Missing values handled: 4" in captured.out


@pytest.mark.parametrize(("filename", "content", "message"), [
    ("missing.csv", None, "missing.csv"),
    ("input.txt", "name\nAli\n", "CSV"),
    ("empty.csv", "", "empty"),
    ("headers.csv", "name,age\n", "at least one data row"),
    ("invalid.csv", "name,age\nAli\n", "structure"),
    ("encoding.csv", b"name\n\xff\n", "decode"),
])
def test_main_reports_invalid_input(
    tmp_path, monkeypatch, capsys, filename, content, message
):
    monkeypatch.chdir(tmp_path)
    source = tmp_path / filename
    if isinstance(content, bytes):
        source.write_bytes(content)
    elif content is not None:
        source.write_text(content, encoding="utf-8")

    assert cli.main([str(source)]) == 1

    captured = capsys.readouterr()
    assert "Error:" in captured.err
    assert message in captured.err
    assert "Traceback" not in captured.err
    assert "Data Cleaning Report" not in captured.out
    assert not (tmp_path / "output").exists()


def test_main_reports_export_failure(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "output").write_text("directory is blocked", encoding="utf-8")

    assert cli.main([str(PROJECT_ROOT / "data" / "sample.csv")]) == 1

    captured = capsys.readouterr()
    assert "Error:" in captured.err
    assert "Cleaned CSV saved" not in captured.out


def test_adapter_recognizes_blanks_and_preserves_mixed_text():
    rows = [
        {"number": "10", "mixed": "10", "text": "NA", "empty": ""},
        {"number": " ", "mixed": "word", "text": "NULL", "empty": "\t"},
        {"number": "30", "mixed": "", "text": "nan", "empty": ""},
    ]

    data = rows_to_dataframe(rows)

    assert data["number"].iloc[[0, 2]].tolist() == [10.0, 30.0]
    assert pd.isna(data.loc[1, "number"])
    assert data["mixed"].iloc[:2].tolist() == ["10", "word"]
    assert pd.isna(data.loc[2, "mixed"])
    assert data["text"].tolist() == ["NA", "NULL", "nan"]
    assert data["empty"].isna().all()
    assert rows[1]["number"] == " "


@pytest.mark.parametrize(("arguments", "returncode", "message"), [
    (["--help"], 0, "usage:"),
    ([], 2, "required"),
    (["missing.csv"], 1, "Error:"),
])
def test_command_line_exit_status(tmp_path, arguments, returncode, message):
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "main.py"), *arguments],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == returncode
    assert message in result.stdout + result.stderr
    assert "Traceback" not in result.stderr
