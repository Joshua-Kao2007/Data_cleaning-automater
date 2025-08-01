import streamlit as st
import pandas as pd
from io import BytesIO


def return_csat(df, season):
    # identify your Q3 column (change this if your header is different)
    q3 = "Q3"

    # 1) Drop first row if its Q3 cell is text (i.e. not numeric)
    if isinstance(df.loc[0, q3], str):
        df = df.drop(index=0).reset_index(drop=True)

    # 2) Keep only rows with no blanks in RecordedDate, ExternalDataReference, Q3
    df = df.dropna(subset=["RecordedDate", "ExternalReference", q3])

    # 3) Map satisfaction text → scores
    mapping = {
        "Extremely satisfied": 5,
        "Somewhat satisfied":   4,
        "Neither satisfied nor dissatisfied": 3,
        "Somewhat dissatisfied": 2,
        "Extremely dissatisfied": 1,
    }
    df[q3] = df[q3].map(mapping)

    # 4) Format RecordedDate → MM/DD/YYYY
    df["RecordedDate"] = pd.to_datetime(df["RecordedDate"]).dt.strftime("%m/%d/%Y")

    # 5) Rename to your target schema
    df = df.rename(columns={
        "RecordedDate":      "Issue Date",
        "ExternalReference": "Tess ID",
        q3:                  "Notes"
    })

    # 6) Build the new frame with all the headers you want
    out = pd.DataFrame({
        "Tess ID":               df["Tess ID"],
        "Issue Date":            df["Issue Date"],
        # placeholder columns to be renamed next
        "Contact Method":        "Survey Response", 
        "Category":              "Survey Scoring",  
        "Activity Type":         "Customer Satisfaction", 
        "Origin":                df["Notes"].apply(
                                    lambda x: "Positive" if x >= 4
                                            else "Neutral" if x == 3
                                            else "Negative"
                                ),
        "Season":                None,
        "Performance":           "",    # blank
        "Notes":                 df["Notes"],
    })
    out["Season"] = season

    return out