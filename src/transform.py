# src/transform.py
# Normalización y generación de capa Silver

from typing import Dict
import pandas as pd


def normalize_columns(df: pd.DataFrame, mapping: Dict[str, str]) -> pd.DataFrame:
    """
    Renombra columnas según mapping origen→canónico,
    normaliza fecha, partner y amount.
    """
    # Renombrar columnas
    df = df.rename(columns=mapping)

    # Fecha → datetime (ISO)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)

    # Partner → limpiar espacios y minúsculas
    if "partner" in df.columns:
        df["partner"] = df["partner"].astype(str).str.strip().str.lower()

    # Amount → quitar símbolos €, comas europeas y parsear float
    if "amount" in df.columns:
        df["amount"] = (
            df["amount"]
            .astype(str)
            .str.replace("€", "", regex=False)
            .str.replace(".", "", regex=False)  # quita separador de miles europeo
            .str.replace(",", ".", regex=False)  # coma → punto decimal
        )
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    return df


def to_silver(bronze: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega transacciones por partner y mes.
    Retorna DataFrame con columnas: partner, month, total_amount.
    """
    if "date" not in bronze.columns or "partner" not in bronze.columns or "amount" not in bronze.columns:
        raise ValueError("Bronze debe contener columnas canónicas: date, partner, amount")

    # Crear columna mes (usar Period luego convertir a timestamp inicio de mes)
    bronze["month"] = bronze["date"].dt.to_period("M").dt.to_timestamp()

    silver = (
        bronze.groupby(["partner", "month"], as_index=False)["amount"]
        .sum()
        .rename(columns={"amount": "total_amount"})
    )

    return silver
