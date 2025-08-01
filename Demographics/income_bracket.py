import streamlit as st
import pandas as pd
from utils.download_util import csv_download_button

def return_income_bracket(df):
    # 0) Drop row 0 if ExternalReference isn’t an integer
    first_ref = df.loc[0, "ExternalReference"]
    try:
        int(first_ref)
    except Exception:
        df = df.drop(index=0).reset_index(drop=True)

    print(df.columns.tolist())

    # 1) Select only ExternalReference & Q28, drop rows where Q28 is blank
    ib = df[["ExternalReference", "Q28"]].dropna(subset=["Q28"]).copy()
    ib = ib.rename(columns={"Q28": "Income Bracket"})

    # 2) Loop through each unique income bracket
    for bracket in ib["Income Bracket"].unique():
        subdf = ib[ib["Income Bracket"] == bracket]

        # a) Preview
        st.subheader(f"💰 {bracket} Responses")
        st.dataframe(subdf)

        # b) Build CSV in-memory
        csv_bytes = subdf.to_csv(index=False).encode("utf-8")

        # c) Download button
        filename = f"income_bracket_{bracket.replace(' ', '_')}.csv"
        csv_download_button(
            subdf,
            label=f"📥 Download '{bracket}' CSV",
            filename=filename
        )
