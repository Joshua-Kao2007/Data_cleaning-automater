import streamlit as st
import pandas as pd
from utils.download_util import csv_download_button

def return_military(df):
    # 0) Drop row 0 if ExternalReference isn’t an integer
    first_ref = df.loc[0, "ExternalReference"]
    try:
        int(first_ref)
    except Exception:
        df = df.drop(index=0).reset_index(drop=True)

    # 1) Select only ExternalReference & Q197, drop rows where Q197 is blank
    sub = df[["ExternalReference", "Q197"]].dropna(subset=["Q197"]).copy()
    sub = sub.rename(columns={"Q197": "Military"})

    # 2) For each of the two possible answers, show & download
    for answer in ["Yes", "No"]:
        grp = sub[sub["Military"] == answer]

        st.subheader(f"🎖️ Military service: {answer}")
        st.dataframe(grp)

        filename = f"military_{answer.lower()}.csv"
        csv_download_button(
            grp,
            label=f"📥 Download '{answer}' CSV",
            filename=filename
        )
