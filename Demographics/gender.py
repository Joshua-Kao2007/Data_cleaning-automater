import streamlit as st
import pandas as pd
from utils.download_util import csv_download_button

def return_gender(df):
    # 0) Drop row 0 if ExternalReference isn’t an integer
    first_ref = df.loc[0, "ExternalReference"]
    try:
        int(first_ref)
    except Exception:
        df = df.drop(index=0).reset_index(drop=True)

    # 1) Select only ExternalReference & Q29, drop rows where Q29 is blank
    gd = df[["ExternalReference", "Q29"]].dropna(subset=["Q29"]).copy()
    gd = gd.rename(columns={"Q29": "Gender"})

    # 2) Loop through each unique gender
    for g in gd["Gender"].unique():
        subdf = gd[gd["Gender"] == g]

        # a) Preview
        st.subheader(f"🚻 {g} Responses")
        st.dataframe(subdf)

        # b) Build CSV in-memory
        csv_bytes = subdf.to_csv(index=False).encode("utf-8")

        # c) Download button
        filename = f"gender_{g.replace(' ', '_').lower()}.csv"
        csv_download_button(
            subdf,
            label=f"📥 Download '{g}' CSV",
            filename=filename
        )
