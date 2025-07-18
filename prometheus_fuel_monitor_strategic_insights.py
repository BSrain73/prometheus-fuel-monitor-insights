# prometheus_fuel_monitor_strategic_insights.py

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Prometheus Fuel Monitor Insights", layout="wide")

st.title("🚍 Prometheus Fuel Monitor – Strategic Insights")
st.markdown("Visualización de consumo, pasajeros y CO₂eq para flotas de transporte.")

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_csv("prometheus_fuel_dataset_1000x10.csv", parse_dates=["fecha"])
    return df

try:
    df = load_data()

    st.success("✅ Datos cargados correctamente.")

    # Indicadores clave
    total_km = df["km"].sum()
    total_litros = df["litros"].sum()
    total_pasajeros = df["pasajeros"].sum()
    total_co2 = df["co2_kg"].sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total KM", f"{total_km:,.0f}")
    col2.metric("Total Litros", f"{total_litros:,.0f}")
    col3.metric("Total Pasajeros", f"{total_pasajeros:,.0f}")
    col4.metric("Total CO₂ eq (kg)", f"{total_co2:,.0f}")

    # Gráfico simple de evolución diaria
    df_daily = df.groupby("fecha").agg({"litros": "sum", "pasajeros": "sum", "co2_kg": "sum"}).reset_index()

    st.plotly_chart(
        px.line(df_daily, x="fecha", y=["litros", "pasajeros", "co2_kg"],
                labels={"value": "Cantidad", "variable": "Indicador"},
                title="📈 Evolución diaria de indicadores")
    )

except Exception as e:
    st.error(f"❌ Error al cargar o procesar los datos: {e}")

