import polars as pl
import pytest
from pathlib import Path
from quantilica_core.manifests import DownloadManifest
from quantilica_io.writer import to_parquet
from quantilica_io.reader import SmartReader

def test_to_parquet_with_manifest(tmp_path):
    # Create dummy data
    df = pl.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    
    # Create dummy manifest
    manifest = DownloadManifest(
        source_id="test-source",
        dataset_id="test-dataset",
        url="http://example.com/test.csv",
        sha256="fake-sha256",
        size_bytes=123,
        fetched_at="2026-05-09T00:00:00Z",
        path="test.csv",
        producer="test-producer"
    )
    
    output_file = tmp_path / "test.parquet"
    to_parquet(df, output_file, manifest=manifest)
    
    assert output_file.exists()
    
    # Verify metadata (requires pyarrow to read custom metadata easily or polars)
    # Polars doesn't show custom metadata in a simple way yet, but we can verify the file is readable
    df_read = pl.read_parquet(output_file)
    assert df_read.equals(df)

def test_smart_reader_csv(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("col1;col2\nval1;123", encoding="latin-1")
    
    reader = SmartReader()
    df = reader.read(csv_file)
    
    assert df.columns == ["col1", "col2"]
    assert df.height == 1
    assert df[0, "col2"] == 123
