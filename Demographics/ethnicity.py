import streamlit as st
import pandas as pd
from io import BytesIO
from utils.download_util import csv_download_button

def return_ethnicity(df):
    first_ref = df.loc[0, "ExternalReference"]
    try:
        int(first_ref)
    except Exception:
        df = df.drop(index=0).reset_index(drop=True)

    # 1) Select only ExternalReference & Q26, drop rows where Q26 is blank
    eth = df[["ExternalReference", "Q26"]].dropna(subset=["Q26"]).copy()
    eth = eth.rename(columns={"Q26": "Ethnicity"})  # clearer column name

    # 2) Loop through each unique ethnicity
    for group in eth["Ethnicity"].unique():
        subdf = eth[eth["Ethnicity"] == group]

        # a) Preview
        st.subheader(f"🌐 {group} Responses")
        st.dataframe(subdf)

        # b) Build CSV in‐memory
        csv_bytes = subdf.to_csv(index=False).encode("utf-8")

        # c) Download button
        filename = f"ethnicity_{group.replace(' ', '_')}.csv"
        csv_download_button(
            subdf,
            label=f"📥 Download '{group}' CSV",
            filename=filename
        )