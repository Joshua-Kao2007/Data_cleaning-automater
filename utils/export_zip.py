import streamlit as st
import pandas as pd
import zipfile
from io import BytesIO

# --- KPI cleaning functions ---
from KPIs.csat import return_csat
from KPIs.nps import return_nps
from KPIs.itr import return_itr
from KPIs.tmv import return_tmv

# --- Demographic functions ---
from Demographics.education import education_level
from Demographics.employment import return_employment
from Demographics.ethnicity import return_ethnicity
from Demographics.marital_status import return_marital_status
from Demographics.birth_year import return_birth_year
from Demographics.zip_code import home_zip_code
from Demographics.military import return_military
from Demographics.income_bracket import return_income_bracket

st.title("📦 Export Cleaned Data as ZIP")

uploaded_file = st.file_uploader("Upload your survey Excel file", type=["xlsx"])
season = st.selectbox("Select a season", ["2023-24", "2024-25", "Spring 2025"])

def create_cleaned_data_zip(df: pd.DataFrame, season: str) -> BytesIO:
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:

        # --- KPI functions that require df + season ---
        kpi_funcs = {
            "CSAT.xlsx": lambda: return_csat(df, season),
            "NPS.xlsx":  lambda: return_nps(df, season),
            "ITR.xlsx":  lambda: return_itr(df, season),
            "TMV.xlsx":  lambda: return_tmv(df, season),
        }

        for filename, func in kpi_funcs.items():
            try:
                result_df = func()
                excel_buffer = BytesIO()
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    result_df.to_excel(writer, index=False)
                zip_file.writestr(filename, excel_buffer.getvalue())
            except Exception as e:
                print(f"[KPI ERROR] {filename}: {e}")

        # --- Demographic: Single-DF return ---
        single_df_funcs = {
            "BirthYear.xlsx": return_birth_year,
            "ZipCode.xlsx": home_zip_code,
        }

        for filename, func in single_df_funcs.items():
            try:
                result_df = func(df)
                excel_buffer = BytesIO()
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    result_df.to_excel(writer, index=False)
                zip_file.writestr(filename, excel_buffer.getvalue())
            except Exception as e:
                print(f"[DEMO SINGLE ERROR] {filename}: {e}")

        # --- Demographic: Dict-of-DF return ---
        dict_df_funcs = {
            "Education": education_level,
            "Employment": return_employment,
            "Ethnicity": return_ethnicity,
            "MaritalStatus": return_marital_status,
            "Military": return_military,
            "Income": return_income_bracket,
        }

        for prefix, func in dict_df_funcs.items():
            try:
                df_dict = func(df)
                for key, result_df in df_dict.items():
                    filename = f"{prefix}_{key}.xlsx".replace(" ", "_")
                    excel_buffer = BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                        result_df.to_excel(writer, index=False)
                    zip_file.writestr(filename, excel_buffer.getvalue())
            except Exception as e:
                print(f"[DEMO DICT ERROR] {prefix}: {e}")

    zip_buffer.seek(0)
    return zip_buffer

# --- UI Action ---
if uploaded_file and season:
    df = pd.read_excel(uploaded_file)

    if st.button("Create ZIP"):
        zip_data = create_cleaned_data_zip(df, season)
        st.download_button(
            label="📥 Download All Cleaned Data",
            data=zip_data.getvalue(),
            file_name="cleaned_data.zip",
            mime="application/zip"
        )
