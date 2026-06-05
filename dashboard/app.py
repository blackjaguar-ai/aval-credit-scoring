"""
dashboard/app.py
Placeholder del Día 1. El dashboard real se construye en el Día 19.
El contenedor levanta y pasa el health check. Eso es todo lo que necesita hoy.
"""

import os
import streamlit as st

st.set_page_config(
    page_title="AVAL — Credit Scoring",
    page_icon="📊",
    layout="centered",
)

st.title("AVAL — Scoring Crediticio Alternativo")
st.caption("Sistema en construcción · Semana 3")

api_url = os.getenv("API_URL", "http://localhost:8000")

st.info(
    f"Dashboard en construcción. "
    f"API disponible en: `{api_url}`\n\n"
    "El dashboard completo se despliega en el Día 19 con: "
    "score por solicitud, factores SHAP, explicación del agente "
    "y factor wow (thin-file aprobado vs. rechazo tradicional)."
)

with st.expander("Estado del sistema"):
    try:
        import requests
        r = requests.get(f"{api_url}/health", timeout=3)
        if r.status_code == 200:
            st.success(f"API operativa — {api_url}")
        else:
            st.warning(f"API respondió {r.status_code}")
    except Exception as e:
        st.error(f"API no disponible: {e}")