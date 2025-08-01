import streamlit as st
import pandas as pd
from io import BytesIO


def return_nps(df, season):
    # 1) Drop first row if Q119 is text
    if isinstance(df.loc[0, "Q119"], str):
        df = df.drop(index=0).reset_index(drop=True)

    # 2) Remove rows with any blanks in the four key columns
    df = df.dropna(subset=[
        "RecordedDate",
        "ExternalReference",
        "Q119_NPS_GROUP",
        "Q119"
    ])

    # 3) Rename columns to your target names
    df = df.rename(columns={
        "RecordedDate":       "Issue Date",
        "ExternalReference":  "Tess ID",
        "Q119_NPS_GROUP":     "Origin",
        "Q119":               "Notes"
    })

    # 4) Build the new frame with the exact order & placeholders
    out = pd.DataFrame({
        "Tess ID":               df["Tess ID"],
        "Issue Date":            pd.to_datetime(df["Issue Date"]).dt.strftime("%m/%d/%Y"),
        "Contact Method":        "Survey Response",   # will be relabeled below
        "Category":              "Survey Scoring",
        "Activity Type":         "Net Promoter Score",
        "Origin":                df["Origin"],
        "Season":                None, # filled by dropdown
        "Performance":           "",   # left blank
        "Notes":                 df["Notes"],
    })
    out["Season"] = season

    return out