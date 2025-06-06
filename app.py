import streamlit as st
import pandas as pd
from utils.parser import parse_bank_statement

st.title("📊 Smart Expense Predictor")

uploaded_file = st.file_uploader("Upload your bank statement (CSV)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Raw Uploaded Data")
    st.dataframe(df.head())

    parsed_df = parse_bank_statement(df)

    if parsed_df is not None:
        st.subheader("Parsed & Cleaned Data")
        st.dataframe(parsed_df.head())
    else:
        st.error("Could not detect necessary columns. Please check your file.")
