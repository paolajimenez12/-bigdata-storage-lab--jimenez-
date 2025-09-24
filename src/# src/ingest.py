# src/ingest.py
# Ingesta de datos y etiquetado de linaje

from typing import List
import pandas as pd
from datetime import datetime, timezone


def tag_lineage(df: pd.DataFrame, source_name: str) -> pd.DataFrame:
    """
    Añade metadatos de linaje:
    - source_file: nombre lógico de la fuente
    - ingested_at: timestamp UTC ISO
    """
    df = df.copy()
    df["source_file"] = source_name
    df["ingested_at"] = datetime.now(timezone.utc).isoformat()
    return df


def concat_bronze(frames: List[pd.DataFrame]) -> pd.DataFrame:
    """
    Concatena múltiples DataFrames a un esquema estándar:
    date, partner, amount, source_file, ingested_at
    """
    if not frames:
        return pd.DataFrame(columns=["date", "partner", "amount", "source_file", "ingested_at"])

    bronze = pd.concat(frames, ignore_index=True)
    expected_cols = ["date", "partner", "amount", "source_file", "ingested_at"]
    # Garantizar que todas las columnas estén presentes
    for col in expected_cols:
        if col not in bronze.columns:
            bronze[col] = None

    return bronze[expected_cols]
