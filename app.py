import streamlit as st
import requests

# === CONFIG ===
st.set_page_config(page_title="Previsão NVDA com LSTM", layout="centered")
st.title("📈 Previsão da Ação NVDA com LSTM")

# === URL da Cloud Function ===
CLOUD_FUNCTION_URL = "https://southamerica-east1-centering-abode-460412-c7.cloudfunctions.net/predict_lstm"

if st.button("🔁 Rodar Previsão"):
    try:
        response = requests.get(CLOUD_FUNCTION_URL)
        if response.status_code == 200:
            result = response.json()
            st.metric("📊 Fechamento Previsto", f"${result['prediction']:.2f}")
            st.caption(f"Baseado nos dados até {result['last_date']}")
        else:
            st.error(f"Erro: {response.status_code}")
    except Exception as e:
        st.error(f"Erro ao conectar com a API: {e}")
