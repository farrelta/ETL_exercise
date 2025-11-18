import pandas as pd
from pathlib import Path
import pandas.testing as pdt
import pytest
from utils.load import save_csv

def test_save_csv_default_filename_prints_name(tmp_path, capsys, monkeypatch):
    # ensure cwd is tmp_path; expect printed message to include the filename at least
    monkeypatch.chdir(tmp_path)
    df = pd.DataFrame({"n": [10, 20]})
    default_name = "products.csv"
    save_csv(df)  # should write to ./products.csv
    out = Path(tmp_path) / default_name
    assert out.exists()
    loaded = pd.read_csv(out)
    pdt.assert_frame_equal(loaded, df)
    captured = capsys.readouterr()
    # accept messages that include the filename (relative) — more lenient than requiring absolute path
    assert "Saved to " in captured.out
    assert default_name in captured.out

def test_save_csv_accepts_pathlib_path(tmp_path, capsys):
    df = pd.DataFrame({"a": [1]})
    out = tmp_path / "pathlib.csv"
    # pass a Path object as filename
    save_csv(df, out)
    assert out.exists()
    loaded = pd.read_csv(out)
    pdt.assert_frame_equal(loaded, df)
    captured = capsys.readouterr()
    # printing should reflect the path passed (string form of Path)
    assert str(out) in captured.out

def test_save_csv_passes_index_false_to_to_csv(monkeypatch, tmp_path):
    df = pd.DataFrame({"z": [0]})
    target = tmp_path / "called_index.csv"
    recorded = {}

    def fake_to_csv(self, filename, index=True, **kwargs):
        # record the index argument and the filename received
        recorded["index"] = index
        recorded["filename"] = filename
        setattr(self, "_saved_to", filename)

    monkeypatch.setattr(pd.DataFrame, "to_csv", fake_to_csv)
    save_csv(df, str(target))
    assert getattr(df, "_saved_to") == str(target)
    # ensure the index argument was forwarded as False
    assert recorded.get("index") is False
    assert recorded.get("filename") == str(target)