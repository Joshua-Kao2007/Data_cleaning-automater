import streamlit as st
import pandas as pd
from io import BytesIO
from KPIs.csat import return_csat
from utils.download_util import excel_download_button
from KPIs.nps import return_nps
from KPIs.itr import return_itr
from KPIs.tmv import return_tmv


def main_kpis(df):
    season = st.selectbox(
    "Pick the Opera season to tag every row with:",
    [
        "2022/2023 Opera Season",
        "2023/2024 Opera Season",
        "2024/2025 Opera Season",
        "2025/2026 Opera Season",
    ],
    key="global_season")
    
    cleaned_csat = return_csat(df, season)
    st.subheader("Cleaned CSAT data preview")
    st.dataframe(cleaned_csat)
    excel_download_button(
        cleaned_csat,
        label="📥 Download cleaned CSAT Excel",
        sheet_name="CSAT",
        filename="csat_cleaned.xlsx"
    )

    cleaned_nps = return_nps(df, season)
    st.subheader("Cleaned NPS data preview")
    st.dataframe(cleaned_nps)
    excel_download_button(
        cleaned_nps,
        label="📥 Download cleaned NPS Excel",
        sheet_name="NPS",
        filename="nps_cleaned.xlsx"
    )

    cleaned_itr = return_itr(df, season)
    st.subheader("Cleaned Intent-to-Return data preview")
    st.dataframe(cleaned_itr)
    excel_download_button(
        cleaned_itr,
        label="📥 Download cleaned ITR Excel",
        sheet_name="ITR",
        filename="itr_cleaned.xlsx"
    )

    cleaned_tmv = return_tmv(df, season)
    st.subheader("Cleaned Time Money Value preview")
    st.dataframe(cleaned_tmv)
    excel_download_button(
        cleaned_tmv,
        label="📥 Download cleaned TMV Excel",
        sheet_name="TMV",
        filename="tmv_cleaned.xlsx"
    )
    st.success("All KPIs cleaned and ready for download!")