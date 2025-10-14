# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Condição e Preço dos Veículos",
    page_icon="🚐",
    layout="wide"
)

# --- ESTILO ESCURO PERSONALIZADO ---
st.markdown("""
    <style>
        body { background-color: #0e1117; color: #ffffff; }
        .stApp { background-color: #0e1117; }
        h1, h2, h3, h4, h5, h6 { color: #fafafa; }
        .block-container { padding-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

# --- CABEÇALHO ---
st.markdown("<h1 style='text-align:center;'>Condição e Preço dos Veículos</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray;'>Entendendo como o ano do modelo, tipo e condição impactam os preços</p>", unsafe_allow_html=True)
st.write("---")

# --- CARREGAR DADOS COM CACHE ---
@st.cache_data(ttl=600)
def load_data():
    time.sleep(1)  # simula tempo de carregamento
    df = pd.read_csv("vehicles.csv")
    df.dropna(subset=["price", "manufacturer"], inplace=True)
    return df

df = load_data()

# --- VISUALIZADOR DE DADOS ---
st.header("Visualizador de Dados")
include_small = st.checkbox("Incluir fabricantes com menos de 1000 anúncios")

if not include_small:
    df = df.groupby("manufacturer").filter(lambda x: len(x) >= 1000)

st.dataframe(df.head(50), use_container_width=True)

# --- TIPOS DE VEÍCULOS POR FABRICANTE ---
st.header("Tipos de Veículos por Fabricante")
fig1 = px.histogram(
    df,
    x="manufacturer",
    color="type",
    barmode="stack",
    title="Tipos de veículos por fabricante"
)
fig1.update_layout(
    xaxis_title="Fabricante",
    yaxis_title="Quantidade",
    template="plotly_dark"
)
st.plotly_chart(fig1, use_container_width=True)

# --- HISTOGRAMA CONDIÇÃO VS ANO DO MODELO ---
st.header("Histograma: Condição x Ano do Modelo")
fig2 = px.histogram(
    df,
    x="model_year",
    color="condition",
    nbins=40,
    title="Distribuição de condição por ano do modelo"
)
fig2.update_layout(
    xaxis_title="Ano do Modelo",
    yaxis_title="Quantidade",
    template="plotly_dark"
)
st.plotly_chart(fig2, use_container_width=True)

# --- COMPARAR DISTRIBUIÇÃO DE PREÇOS ENTRE FABRICANTES ---
st.header("Comparar Distribuição de Preços entre Fabricantes")

manufacturers = sorted(df["manufacturer"].dropna().unique())
col1, col2 = st.columns(2)

with col1:
    man1 = st.selectbox("Selecione o Fabricante 1", manufacturers)
with col2:
    man2 = st.selectbox("Selecione o Fabricante 2", manufacturers)

normalize = st.checkbox("Normalizar histograma")

subset = df[df["manufacturer"].isin([man1, man2])]
fig3 = px.histogram(
    subset,
    x="price",
    color="manufacturer",
    barmode="overlay",
    histnorm="percent" if normalize else None,
    nbins=50,
    title=f"Distribuição de Preços: {man1} vs {man2}"
)
fig3.update_layout(
    xaxis_title="Preço",
    yaxis_title="Percentual" if normalize else "Quantidade",
    template="plotly_dark"
)
st.plotly_chart(fig3, use_container_width=True)

