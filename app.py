# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# --- Load data ---
@st.cache_data
def load_data():
    # Use your file name here
    return pd.read_csv("vehicles.csv")

df = load_data()

# --- UI header ---
st.header("Car Sales Dashboard (Sprint 5)")

# --- Controls ---
st.write("Choose a chart to display:")

# Buttons version (meets project requirement)
col1, col2 = st.columns(2)
with col1:
    if st.button("Show Histogram"):
        st.write("Histogram: Vehicle Odometer")
        fig = px.histogram(df, x="odometer")
        st.plotly_chart(fig, use_container_width=True)

with col2:
    if st.button("Show Scatter Plot"):
        st.write("Scatter: Odometer vs Price")
        fig = px.scatter(df, x="odometer", y="price")
        st.plotly_chart(fig, use_container_width=True)

# Optional: checkbox version (either buttons or checkboxes is fine)
with st.expander("Optional: use checkboxes instead"):
    show_hist = st.checkbox("Histogram (odometer)")
    show_scatter = st.checkbox("Scatter (odometer vs price)")
    if show_hist:
        fig = px.histogram(df, x="odometer")
        st.plotly_chart(fig, use_container_width=True)
    if show_scatter:
        fig = px.scatter(df, x="odometer", y="price")
        st.plotly_chart(fig, use_container_width=True)
