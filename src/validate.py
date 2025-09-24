# src/validate.py
# Validación básica de datos canónicos

from typing import List
import pandas as pd


def basic_checks(df: pd.DataFrame) -> List[str]:
    """
    Revisa calidad mínima:
    - Columnas canónicas presentes
    - amount numérico y ≥ 0
    - date tipo datetime
    Devuelve lista de errores encontrados.
    """
    errors: List[str] = []

    required = ["date", "partner", "amount"]
    for col in required:
        if col not in df.columns:
            errors.append(f"Columna requerida faltante: {col}")

    if "amount" in df.columns:
        if not pd.api.types.is_numeric_dtype(df["amount"]):
            errors.append("amount no es numérico")
        elif (df["amount"] < 0).any():
            errors.append("amount contiene valores negativos")

    if "date" in df.columns:
        if not pd.api.types.is_datetime64_any_dtype(df["date"]):
            errors.append("date no está en formato datetime")

    return errors
