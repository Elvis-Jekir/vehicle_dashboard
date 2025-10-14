# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import time

# --- CONFIG DA PÁGINA (sem ícone) ---
st.set_page_config(
    page_title="Condição e Preço dos Veículos",
    layout="wide"
)

# --- TEMA ESCURO ---
st.markdown("""
<style>
  .stApp { background-color: #0e1117; }
  body, .stMarkdown, .stText, .stDataFrame { color: #ffffff; }
  h1, h2, h3, h4, h5, h6 { color: #fafafa; }
  .block-container { padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)

# --- HEADER (somente texto) ---
st.markdown("<h1 style='text-align:center;'>Condição e Preço dos Veículos</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray;'>Entendendo como o ano do modelo, tipo e condição impactam os preços</p>", unsafe_allow_html=True)
st.write("---")

# --- CARREGAR DADOS (com cache) ---
@st.cache_data(ttl=600)
def load_data():
    time.sleep(0.5)
    df = pd.read_csv("vehicles.csv")

    # tratar colunas categóricas
    for col in ["type", "condition", "fuel", "transmission", "paint_color", "model"]:
        if col in df.columns:
            df[col] = df[col].fillna("unknown")

    # converter numéricas com segurança
    for col in ["price", "model_year", "odometer", "cylinders", "is_4wd", "days_listed"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # remover linhas sem preço
    if "price" in df.columns:
        df = df.dropna(subset=["price"])

    return df

df = load_data()

# 1) VISUALIZADOR DE DADOS
st.header("Visualizador de Dados")
min_count = 100
show_small = st.checkbox(f"Incluir tipos com menos de {min_count} anúncios", value=True)

if not show_small and "type" in df.columns:
    counts = df["type"].value_counts()
    keep = counts[counts >= min_count].index
    df_view = df[df["type"].isin(keep)]
else:
    df_view = df

st.dataframe(df_view.head(50), use_container_width=True)

# 2) TIPOS POR COMBUSTÍVEL (barras empilhadas)
st.header("Tipos de Veículos por Combustível")
if {"type", "fuel"}.issubset(df_view.columns):
    fig1 = px.histogram(
        df_view, x="fuel", color="type", barmode="stack",
        title="Distribuição de tipos por combustível"
    )
    fig1.update_layout(template="plotly_dark", xaxis_title="Combustível", yaxis_title="Quantidade")
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.info("Colunas necessárias para este gráfico não estão disponíveis (type/fuel).")

# 3) HISTOGRAMA: condição x ano do modelo
st.header("Histograma: Condição x Ano do Modelo")
if {"condition", "model_year"}.issubset(df_view.columns):
    fig2 = px.histogram(
        df_view, x="model_year", color="condition", nbins=40,
        title="Distribuição de condição por ano do modelo"
    )
    fig2.update_layout(template="plotly_dark", xaxis_title="Ano do Modelo", yaxis_title="Quantidade")
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("Colunas necessárias para este gráfico não estão disponíveis (condition/model_year).")

# 4) Comparar distribuição de preços entre tipos
st.header("Comparar Distribuição de Preços entre Tipos")
if {"type", "price"}.issubset(df.columns):
    types = sorted([t for t in df["type"].dropna().unique() if t != "unknown"])
    if len(types) >= 2:
        col1, col2 = st.columns(2)
        with col1:
            t1 = st.selectbox("Selecione o Tipo 1", types, index=0)
        with col2:
            t2 = st.selectbox("Selecione o Tipo 2", types, index=min(1, len(types)-1))

        normalize = st.checkbox("Normalizar histograma")

        subset = df[df["type"].isin([t1, t2])]
        fig3 = px.histogram(
            subset, x="price", color="type", barmode="overlay",
            histnorm="percent" if normalize else None, nbins=50,
            title=f"Distribuição de Preços: {t1} vs {t2}"
        )
        fig3.update_layout(
            template="plotly_dark",
            xaxis_title="Preço",
            yaxis_title="Percentual" if normalize else "Quantidade"
        )
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.warning("Dados insuficientes de tipos para comparação.")
else:
    st.info("Colunas necessárias para este gráfico não estão disponíveis (type/price).")


