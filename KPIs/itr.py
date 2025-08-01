import streamlit as st
import pandas as pd
from io import BytesIO


def return_itr(df, season):
    # 1) Drop first row if its Q198 value isn't one of the five valid options
    valid = {
        "Probably will attend",
        "Definitely will attend",
        "Might attend",
        "Probably will not attend",
        "Definitely will not attend",
    }
    if df.loc[0, "Q198"] not in valid:
        df = df.drop(index=0).reset_index(drop=True)

    # 2) Remove any rows missing RecordedDate, ExternalReference, or Q198
    df = df.dropna(subset=["RecordedDate", "ExternalReference", "Q198"])

    # 3) Map intent text → numeric score
    score_map = {
        "Definitely will attend":         5,
        "Probably will attend":       4,
        "Might attend":                 3,
        "Probably will not attend":     2,
        "Definitely will not attend":   1,
    }
    df["Q198"] = df["Q198"].map(score_map)

    # 4) Rename to your target names
    df = df.rename(columns={
        "RecordedDate":      "Issue Date",
        "ExternalReference": "Tess ID",
        "Q198":              "Notes",
    })
    # format date
    df["Issue Date"] = pd.to_datetime(df["Issue Date"]).dt.strftime("%m/%d/%Y")

    # 5) Rebuild with exact columns & placeholders
    out = pd.DataFrame({
        "Tess ID":               df["Tess ID"],
        "Issue Date":            df["Issue Date"],
        "Contact Method":        "Survey Response",   # will rename next
        "Category":              "Survey Scoring",
        "Activity Type":         "Intent to Return",
        "Origin":                df["Notes"].apply(
                                    lambda x: "Positive" if x >= 4
                                            else "Neutral" if x == 3
                                            else "Negative"
                                ),
        "Season":                None, # filled by dropdown
        "Performance":           "",   # blank
        "Notes":                 df["Notes"],
    })
    out["Season"] = season
    return out