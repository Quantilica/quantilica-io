"""Data contracts and schema validation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import polars as pl


@dataclass(frozen=True)
class Field:
    """A field in a data contract."""
    name: str
    dtype: pl.DataType
    required: bool = True
    description: str | None = None


@dataclass(frozen=True)
class DataContract:
    """A contract defining the expected structure and types of a dataset."""
    dataset_id: str
    fields: list[Field]
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self, df: pl.DataFrame | pl.LazyFrame) -> None:
        """Validate a DataFrame against this contract."""
        schema = df.collect_schema() if isinstance(df, pl.LazyFrame) else df.schema
        
        for field in self.fields:
            if field.required and field.name not in schema:
                raise ValueError(f"Missing required field: {field.name}")
            
            if field.name in schema:
                actual_type = schema[field.name]
                if actual_type != field.dtype:
                    # Polars types can be complex, this is a basic check
                    raise TypeError(
                        f"Field '{field.name}' has type {actual_type}, "
                        f"expected {field.dtype}"
                    )

    def cast(self, df: pl.DataFrame) -> pl.DataFrame:
        """Cast a DataFrame to match the contract types."""
        expressions = []
        for field in self.fields:
            if field.name in df.columns:
                expressions.append(pl.col(field.name).cast(field.dtype))
        return df.with_columns(expressions)
