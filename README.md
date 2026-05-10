# quantilica-io 📊

**Analytical data processing and conversion layer for Quantilica.**

`quantilica-io` is the specialized layer for reading, validating, and converting raw data into analytical formats (Parquet).

## 🚀 Features

- **Multi-format Reader**: Unified interface for CSV, Excel, DBF, and JSON.
- **Parquet Converter**: High-performance conversion using Polars and PyArrow.
- **Data Contracts**: Schema validation and column standardization.
- **Provenance Injection**: Embeds `quantilica-core` manifest metadata directly into Parquet headers.

## 📦 Installation

`quantilica-io` is published from this GitHub repository (not on PyPI). Add
it to your project as a git dependency:

```bash
uv add "quantilica-io @ git+https://github.com/Quantilica/quantilica-io.git"
```

Or with pip:

```bash
pip install "quantilica-io @ git+https://github.com/Quantilica/quantilica-io.git"
```

## 🛠️ Usage

```python
from quantilica_io.writer import to_parquet
from quantilica_core.manifests import DownloadManifest

# Load a manifest from a download
manifest = DownloadManifest.read_json("data/raw/dataset.csv.manifest.json")

# Convert to Parquet with provenance
to_parquet(manifest, "data/processed/dataset.parquet")
```

---

## ⚖️ License

Copyright (c) 2026 Komesu, D.K. (Quantilica)  
Licensed under the [MIT License](LICENSE).
