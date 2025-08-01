import streamlit as st
import pandas as pd
from io import BytesIO
from utils.download_util import csv_download_button

def return_industry_code(df):
    # 0) Drop row 0 if its ExternalReference isn't an integer
    first_ref = df.loc[0, "ExternalReference"]
    try:
        int(first_ref)
    except Exception:
        df = df.drop(index=0).reset_index(drop=True)

    # 1) Select only ExternalReference & Q165, drop rows where Q165 is blank
    emp = df[["ExternalReference", "Q165"]].dropna(subset=["Q165"]).copy()
    emp = emp.rename(columns={"Q165": "Industry Code"})  # clearer header

    # 2) Loop through each unique industry code
    for code in emp["Industry Code"].unique():
        subdf = emp[emp["Industry Code"] == code]

        # a) Preview
        st.subheader(f"💼 {code} Responses")
        st.dataframe(subdf)

        # b) Build CSV in-memory
        csv_bytes = subdf.to_csv(index=False).encode("utf-8")

        # c) Download button
        filename = f"industry_{code.replace(' ', '_')}.csv"
        csv_download_button(
            subdf,
            label=f"📥 Download '{code}' CSV",
            filename=filename
        )