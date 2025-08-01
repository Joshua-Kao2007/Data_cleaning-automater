import streamlit as st
import pandas as pd
from utils.download_util import csv_download_button

def home_zip_code(df):
    # 0) Drop row 0 if its ExternalReference isn’t an integer
    first_ref = df.loc[0, "ExternalReference"]
    try:
        int(first_ref)
    except Exception:
        df = df.drop(index=0).reset_index(drop=True)

    # 1) Select only ExternalReference & Q30, drop blank zips
    subset = df[["ExternalReference", "Q30"]].dropna(subset=["Q30"]).copy()
    subset = subset.rename(columns={"Q30": "Home Zip Code"})

    # 2) Preview
    st.subheader("🏠 Home Zip Code Data")
    st.dataframe(subset)

    # 3) Single CSV download
    csv_download_button(
        subset,
        label="📥 Download Home Zip Codes CSV",
        filename="home_zip_codes.csv"
    )
