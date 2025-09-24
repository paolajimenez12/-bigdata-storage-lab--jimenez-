# streamlit_app.py
# Aplicación Streamlit para el laboratorio:
# De CSVs heterogéneos a un almacén analítico confiable

import io
import pandas as pd
import streamlit as st

from src.ingest import tag_lineage, concat_bronze
from src.validate import basic_checks
from src.transform import normalize_columns, to_silver


# -------------------------------------------------------
# Configuración de página
# -------------------------------------------------------
st.set_page_config(
    page_title="Big Data Storage Lab",
    layout="wide"
)

st.title("📊 Laboratorio: De CSVs heterogéneos a un almacén analítico confiable")

st.markdown(
    "Carga múltiples archivos CSV, mapea columnas al esquema canónico "
    "(`date`, `partner`, `amount`) y genera un almacén confiable (bronze → silver)."
)

# -------------------------------------------------------
# Barra lateral: configuración de columnas
# -------------------------------------------------------
st.sidebar.header("⚙️ Configuración de columnas")
col_date = st.sidebar.text_input("Columna orig
