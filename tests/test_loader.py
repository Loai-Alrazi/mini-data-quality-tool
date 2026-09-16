from pathlib import Path

import pytest

from src.loader import load_csv


def test_load_csv_success(tmp_path):
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text(
        "name,age\nAlice,25\nBob,30\n",
        encoding="utf-8",
    )

    result = load_csv(csv_file)

    assert result == [
        {"name": "Alice", "age": "25"},
        {"name": "Bob", "age": "30"},
    ]


def test_load_csv_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_csv("data/missing.csv")


def test_load_csv_rejects_non_csv_file(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text(
        "name,age\nAlice,25\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="CSV"):
        load_csv(file_path)


def test_load_csv_rejects_file_without_extension(tmp_path):
    file_path = tmp_path / "sample"
    file_path.write_text(
        "name,age\nAlice,25\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="extension"):
        load_csv(file_path)


def test_load_csv_propagates_permission_error(tmp_path, monkeypatch):
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text(
        "name,age\nAlice,25\n",
        encoding="utf-8",
    )

    def raise_permission_error(*args, **kwargs):
        raise PermissionError("File cannot be read.")

    monkeypatch.setattr(Path, "open", raise_permission_error)

    with pytest.raises(PermissionError, match="cannot be read"):
        load_csv(csv_file)


def test_load_csv_rejects_empty_file(tmp_path):
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="empty"):
        load_csv(csv_file)


def test_load_csv_rejects_invalid_headers(tmp_path):
    csv_file = tmp_path / "invalid_headers.csv"
    csv_file.write_text(
        "name,\nAlice,25\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="column names"):
        load_csv(csv_file)


def test_load_csv_rejects_invalid_row_structure(tmp_path):
    csv_file = tmp_path / "invalid.csv"
    csv_file.write_text(
        "name,age\nAlice,25\nBob\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="row"):
        load_csv(csv_file)
