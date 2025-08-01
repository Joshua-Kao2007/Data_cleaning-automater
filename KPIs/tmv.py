import streamlit as st
import pandas as pd
from io import BytesIO


def return_tmv(df, season):
    # Valid agree/disagree responses
    valid = {
        "Strongly agree",
        "Somewhat agree",
        "Neither agree nor disagree",
        "Somewhat disagree",
        "Strongly disagree",
    }

    # 1) Drop first row if its Q157 isn't valid
    if df.loc[0, "Q157"] not in valid:
        df = df.drop(index=0).reset_index(drop=True)

    # 2) Drop rows with any blanks in the three key columns
    df = df.dropna(subset=["RecordedDate", "ExternalReference", "Q157"])

    # 3) Map text → numeric scores
    score_map = {
        "Strongly agree":                5,
        "Somewhat agree":                4,
        "Neither agree nor disagree":    3,
        "Somewhat disagree":             2,
        "Strongly disagree":             1,
    }
    df["Q157"] = df["Q157"].map(score_map)

    # 4) Rename columns to your schema
    df = df.rename(columns={
        "RecordedDate":      "Issue Date",
        "ExternalReference": "Tess ID",
        "Q157":              "Notes",
    })
    df["Issue Date"] = pd.to_datetime(df["Issue Date"]).dt.strftime("%m/%d/%Y")

    # 5) Build the output frame with placeholders
    out = pd.DataFrame({
        "Tess ID":               df["Tess ID"],
        "Issue Date":            df["Issue Date"],
        "Contact Method":        "Survey Response",    # placeholder for Contact Method
        "Category":              "Survey Scoring",    # placeholder for Category
        "Activity Type":         "Time Money Value",  # fixed label for this metric
        "Origin":                df["Notes"].apply(
                                    lambda x: "Positive" if x >= 4
                                            else "Neutral" if x == 3
                                            else "Negative"
                                ),
        "Season":                None,  # filled below
        "Performance":           "",    # blank
        "Notes":                 df["Notes"],
    })
    out["Season"] = season

    return out