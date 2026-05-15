"""Smart file reading integrated with Quantilica manifests."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import polars as pl
from quantilica_core.manifests import DownloadManifest


class SmartReader:
    """A reader that understands Quantilica manifests and optimizes Polars loading."""

    def __init__(self, default_encoding: str = "utf-8"):
        self.default_encoding = default_encoding

    def read(
        self,
        path_or_manifest: str | Path | DownloadManifest,
        **kwargs: Any,
    ) -> pl.DataFrame:
        """Read a file into a Polars DataFrame, optionally guided by a manifest."""
        if isinstance(path_or_manifest, DownloadManifest):
            path = Path(path_or_manifest.path)
        else:
            path = Path(path_or_manifest)

        suffix = path.suffix.lower()

        if suffix == ".csv":
            # Brazilian Gov data: default to semicolon and latin-1
            if "separator" not in kwargs:
                kwargs["separator"] = ";"
            if "encoding" not in kwargs:
                kwargs["encoding"] = "latin-1"
            return pl.read_csv(path, **kwargs)
        
        if suffix == ".parquet":
            return pl.read_parquet(path, **kwargs)
        
        if suffix == ".json":
            return pl.read_json(path, **kwargs)

        if suffix in (".xlsx", ".xls"):
            return pl.read_excel(path, **kwargs)

        raise ValueError(f"Unsupported file format: {suffix}")

    def scan(
        self,
        path_or_manifest: str | Path | DownloadManifest,
        **kwargs: Any,
    ) -> pl.LazyFrame:
        """Lazily scan a file (optimized for large CSVs/Parquet)."""
        if isinstance(path_or_manifest, DownloadManifest):
            path = Path(path_or_manifest.path)
        else:
            path = Path(path_or_manifest)

        suffix = path.suffix.lower()

        if suffix == ".csv":
            if "separator" not in kwargs:
                kwargs["separator"] = ";"
            if "encoding" not in kwargs:
                kwargs["encoding"] = "latin-1"
            return pl.scan_csv(path, **kwargs)
        
        if suffix == ".parquet":
            return pl.scan_parquet(path, **kwargs)

        raise ValueError(f"Lazy scanning not supported for: {suffix}")
