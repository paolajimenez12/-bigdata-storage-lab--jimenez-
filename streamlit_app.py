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
col_date = st.sidebar.text_input("Columna origen → date", "date")
col_partner = st.sidebar.text_input("Columna origen → partner", "partner")
col_amount = st.sidebar.text_input("Columna origen → amount", "amount")

mapping = {
    col_date: "date",
    col_partner: "partner",
    col_amount: "amount",
}

# -------------------------------------------------------
# Subida de archivos
# -------------------------------------------------------
uploaded_files = st.file_uploader(
    "Sube uno o más archivos CSV",
    type=["csv"],
    accept_multiple_files=True
)

bronze_frames = []

if uploaded_files:
    for file in uploaded_files:
        try:
            df = pd.read_csv(file, encoding="utf-8")
        except UnicodeDecodeError:
            df = pd.read_csv(file, encoding="latin-1")

        # Normalizar y etiquetar linaje
        df_norm = normalize_columns(df, mapping)
        df_tagged = tag_lineage(df_norm, source_name=file.name)
        bronze_frames.append(df_tagged)

    # Concatenar todo en Bronze
    bronze = concat_bronze(bronze_frames)

    st.subheader("📂 Datos Bronze (unificados)")
    st.dataframe(bronze.head(100), use_container_width=True)

    # ---------------------------------------------------
    # Validación
    # ---------------------------------------------------
    st.subheader("✅ Validación de datos")
    errors = basic_checks(bronze)

    if errors:
        st.error("Se encontraron problemas en los datos:")
        for e in errors:
            st.write(f"- {e}")
    else:
        st.success("Los datos cumplen con las validaciones mínimas.")

        # -----------------------------------------------
        # Transformación → Silver
        # -----------------------------------------------
        silver = to_silver(bronze)

        st.subheader("🥈 Datos Silver (partner × mes)")
        st.dataframe(silver, use_container_width=True)

        # KPIs simples
        st.subheader("📌 KPIs")
        total_amount = silver["total_amount"].sum()
        total_partners = silver["partner"].nunique()
        st.metric("Monto total (EUR)", f"{total_amount:,.2f}")
        st.metric("Número de partners", total_partners)

        # Visualización
        st.subheader("📈 Distribución mensual")
        st.bar_chart(
            silver.set_index("month")["total_amount"],
            use_container_width=True
        )

        # -----------------------------------------------
        # Descarga de resultados
        # -----------------------------------------------
        st.subheader("⬇️ Descarga de resultados")

        bronze_csv = bronze.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Descargar Bronze CSV",
            data=bronze_csv,
            file_name="bronze.csv",
            mime="text/csv"
        )

        silver_csv = silver.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Descargar Silver CSV",
            data=silver_csv,
            file_name="silver.csv",
            mime="text/csv"
        )
else:
    st.info("Sube al menos un archivo CSV para comenzar.")
