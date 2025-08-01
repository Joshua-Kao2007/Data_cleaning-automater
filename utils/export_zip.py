import streamlit as st
import zipfile
from io import BytesIO
import pandas as pd

# --- Import your KPI cleaning functions ---
from KPIs.csat import return_csat
from KPIs.nps import return_nps
from KPIs.itr import return_itr
from KPIs.tmv import return_tmv

# --- Import your Demographic cleaning functions ---
from Demographics.education import education_level
from Demographics.employment import return_employment
from Demographics.ethnicity import return_ethnicity
from Demographics.marital_status import return_marital_status
from Demographics.birth_year import return_birth_year
from Demographics.zip_code import home_zip_code
from Demographics.military import return_military
from Demographics.income_bracket import return_income_bracket

st.title("📦 Export Cleaned Data as ZIP")

def create_cleaned_data_zip() -> BytesIO:
    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        # --- KPIs ---
        kpi_funcs = {
            "CSAT_Cleaned.xlsx": return_csat,
            "NPS_Cleaned.xlsx": return_nps,
            "ITR_Cleaned.xlsx": return_itr,
            "TMV_Cleaned.xlsx": return_tmv,
        }

        for name, func in kpi_funcs.items():
            df = func()
            if df is not None:
                excel_buffer = BytesIO()
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False)
                zip_file.writestr(name, excel_buffer.getvalue())

        # --- Demographics that return single DataFrame ---
        demo_single_funcs = {
            "BirthYear_Cleaned.xlsx": return_birth_year,
            "HomeZipCode_Cleaned.xlsx": home_zip_code,
        }

        for name, func in demo_single_funcs.items():
            df = func()
            if df is not None:
                excel_buffer = BytesIO()
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False)
                zip_file.writestr(name, excel_buffer.getvalue())

        # --- Demographics that return dicts of DataFrames ---
        demo_dict_funcs = {
            "EducationLevel": education_level,
            "Employment": return_employment,
            "Ethnicity": return_ethnicity,
            "MaritalStatus": return_marital_status,
            "Military": return_military,
            "IncomeBracket": return_income_bracket,
        }

        for prefix, func in demo_dict_funcs.items():
            df_dict = func()
            if isinstance(df_dict, dict):
                for key, df in df_dict.items():
                    if df is not None:
                        fname = f"{prefix}_{key}.xlsx".replace(" ", "_")
                        excel_buffer = BytesIO()
                        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                            df.to_excel(writer, index=False)
                        zip_file.writestr(fname, excel_buffer.getvalue())

    zip_buffer.seek(0)
    return zip_buffer

# 🔘 UI Trigger
if st.button("Create ZIP"):
    zip_data = create_cleaned_data_zip()
    st.download_button(
        label="📥 Download All Cleaned Data (ZIP)",
        data=zip_data.getvalue(),
        file_name="All_Cleaned_Data.zip",
        mime="application/zip"
    )
