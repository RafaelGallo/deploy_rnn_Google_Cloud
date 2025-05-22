import streamlit as st
import requests

# === Configurações da interface ===
st.set_page_config(page_title="Previsão NVDA com LSTM", layout="centered")
st.title("📈 Previsão de Fechamento da NVDA com LSTM")

# === URL da sua Cloud Function ===
CLOUD_FUNCTION_URL = "https://southamerica-east1-centering-abode-460412-c7.cloudfunctions.net/predict_lstm"  # 🔁 Substitua pela URL real

# === Interface com botão ===
if st.button("🔁 Rodar previsão agora"):
    try:
        response = requests.get(CLOUD_FUNCTION_URL)

        if response.status_code == 200:
            result = response.json()
            prediction = result.get("prediction")
            last_date = result.get("last_date")

            st.metric("📊 Fechamento Previsto", f"${prediction:.2f}")
            st.caption(f"📅 Baseado nos dados até: {last_date}")
        else:
            st.error(f"Erro na API: {response.status_code}")
    except Exception as e:
        st.error(f"Erro ao conectar com a API: {e}")
