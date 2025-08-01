import streamlit as st
from io import BytesIO
import pandas as pd
from utils.download_util import csv_download_button

def return_birth_year(df):
    # 0) Drop row 0 if its ExternalReference isn’t an integer
    first_ref = df.loc[0, "ExternalReference"]
    try:
        int(first_ref)
    except Exception:
        df = df.drop(index=0).reset_index(drop=True)

    # 1) Select only ExternalReference & Q166, drop rows where Q166 is blank
    subset = df[["ExternalReference", "Q166"]].dropna(subset=["Q166"]).copy()
    subset = subset.rename(columns={"Q166": "Birth Year"})
    subset = subset[subset["Birth Year"].astype(str).str.match(r"^\d{4}$")]
    # 2) Preview the cleaned data
    st.subheader("🎂 Birth Year Responses")
    st.dataframe(subset)

    # 3) Offer one CSV download for the full set
    csv_download_button(
        subset,
        label="📥 Download Birth Year CSV",
        filename="birth_year.csv"
    )
