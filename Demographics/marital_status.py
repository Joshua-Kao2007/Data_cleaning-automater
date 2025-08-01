import streamlit as st
import pandas as pd
from utils.download_util import csv_download_button

def return_marital_status(df):
    # 0) Drop row 0 if its ExternalReference isn’t an integer
    first_ref = df.loc[0, "ExternalReference"]
    try:
        int(first_ref)
    except Exception:
        df = df.drop(index=0).reset_index(drop=True)

    # 1) Select only ExternalReference, Q161, Q161_3_TEXT; drop rows where Q161 is blank
    ms = df[["ExternalReference", "Q161", "Q161_3_TEXT"]].dropna(
        subset=["Q161"]
    ).copy()

    # 2) Rename Q161 → Marital Status, Q161_3_TEXT → Other Text
    ms = ms.rename(columns={
        "Q161": "Marital Status",
        "Q161_3_TEXT": "Other Text"
    })

    # 3) Loop through each unique marital status
    for status in ms["Marital Status"].unique():
        subset = ms[ms["Marital Status"] == status]

        # a) Decide which columns to show
        if status.lower() == "other":
            display_df = subset[["ExternalReference", "Marital Status", "Other Text"]]
        else:
            display_df = subset[["ExternalReference", "Marital Status"]]

        # b) Preview in Streamlit
        st.subheader(f"💍 {status} Responses")
        st.dataframe(display_df)

        # c) Download CSV
        filename = f"marital_status_{status.replace(' ', '_').lower()}.csv"
        csv_download_button(
            display_df,
            label=f"📥 Download '{status}' CSV",
            filename=filename
        )
