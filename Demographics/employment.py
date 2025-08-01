import streamlit as st
import pandas as pd
from io import BytesIO
from utils.download_util import csv_download_button

def return_employment(df):
    # 0) Drop row 0 if its ExternalReference isn’t an integer
    first_ref = df.loc[0, "ExternalReference"]
    try:
        int(first_ref)
    except Exception:
        df = df.drop(index=0).reset_index(drop=True)

    # 1) Select only ExternalReference, Q162, Q162_3_TEXT; drop rows where Q162 is blank
    emp = df[["ExternalReference", "Q162", "Q162_3_TEXT"]].dropna(
        subset=["Q162"]
    ).copy()

    # 2) Rename Q162 → Employment for clarity
    emp = emp.rename(columns={"Q162": "Employment"})

    # 3) Loop through each unique Employment response
    for role in emp["Employment"].unique():
        subset = emp[emp["Employment"] == role]

        # a) Decide which columns to show
        if role == "Other":
            display_df = subset[["ExternalReference", "Employment", "Q162_3_TEXT"]] \
                         .rename(columns={"Q162_3_TEXT": "Other Text"})
        else:
            display_df = subset[["ExternalReference", "Employment"]]

        # b) Preview in Streamlit
        st.subheader(f"💼 {role} Responses")
        st.dataframe(display_df)

        # c) Build CSV in memory
        csv_bytes = display_df.to_csv(index=False).encode("utf-8")

        # d) Download button
        safe_role = role.replace(" ", "_")
        filename = f"employment_{safe_role}.csv"
        csv_download_button(
            display_df,
            label=f"📥 Download '{role}' CSV",
            filename=filename
        )