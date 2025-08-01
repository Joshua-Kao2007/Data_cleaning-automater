import streamlit as st
import pandas as pd
from io import BytesIO
from utils.download_util import csv_download_button

def education_level(df):
    first_ref = df.loc[0, "ExternalReference"]
    try:
        float(first_ref)  # will succeed for numeric strings/ints/floats
    except Exception:
        df = df.drop(index=0).reset_index(drop=True)
    # 1) Select only ExternalReference & Q126, drop blanks
    edu = df[["ExternalReference", "Q126"]].dropna(
        subset=["ExternalReference", "Q126"]
    ).copy()
    # 2) Rename Q126 → Education Level
    edu = edu.rename(columns={"Q126": "Education Level"})

    # 3) Loop through each unique level
    for level in edu["Education Level"].unique():
        subdf = edu[edu["Education Level"] == level]

        st.subheader(f"🎓 {level} Responses")
        st.dataframe(subdf)

        # Build CSV
        csv_data = subdf.to_csv(index=False).encode("utf-8")

        # Download CSV button
        filename = f"education_{level.replace(' ', '_')}.csv"

        csv_download_button(
            subdf,
            label=f"📥 Download '{level}' CSV",
            filename=filename
        )
