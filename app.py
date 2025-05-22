import os
import numpy as np
import pandas as pd
import streamlit as st
from google.cloud import bigquery, storage
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt

# === CONFIGURAÇÃO: autenticação com chave de serviço ===
ADC_PATH = r"cred_GCP\centering-abode-460412-c7-1a78da5e810c.json"  # ajuste o caminho conforme necessário
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ADC_PATH
os.environ["GOOGLE_CLOUD_PROJECT"] = "centering-abode-460412-c7"

# === CONFIGURAÇÃO: modelo ===
BUCKET_NAME = "lstn_model"
BLOB_NAME = "model_lstm1.h5"
MODEL_LOCAL_PATH = r"models\model_lstm1.keras"

# === Baixar e carregar modelo LSTM ===
@st.cache_resource
def load_lstm_model():
    if not os.path.exists(MODEL_LOCAL_PATH):
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(BLOB_NAME)
        blob.download_to_filename(MODEL_LOCAL_PATH)
        st.info(f"Modelo baixado do GCS para {MODEL_LOCAL_PATH}")
    return load_model(MODEL_LOCAL_PATH)

# === Buscar dados mais recentes do BigQuery ===
def get_data():
    client = bigquery.Client()
    query = """
        SELECT Datetime, Close
        FROM `centering-abode-460412-c7.finance_data.nvda_prices_yf2`
        ORDER BY Datetime DESC
        LIMIT 90
    """
    df = client.query(query).to_dataframe().sort_values("Datetime")
    return df

# === Interface Streamlit ===
st.set_page_config(layout="centered")
st.title("📈 Previsão de Fechamento NVDA com LSTM")

if st.button("🔁 Rodar Previsão"):
    try:
        df = get_data()

        x_input = df["Close"].values.reshape(-1, 1)
        x_input = np.expand_dims(x_input, axis=0)  # (1, 90, 1)

        model = load_lstm_model()
        prediction = model.predict(x_input)[0][0]

        st.metric("📊 Previsão do Próximo Fechamento", f"${prediction:.2f}")
        st.line_chart(df.set_index("Datetime")["Close"])

    except Exception as e:
        st.error(f"Erro durante predição: {e}")