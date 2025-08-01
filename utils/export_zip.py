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
from Demographics.education import education_level             # returns dict[level]→DataFrame
from Demographics.employment import return_employment          # returns dict[role]→DataFrame
from Demographics.ethnicity import return_ethnicity            # returns dict[eth]→DataFrame
from Demographics.marital_status import return_marital_status  # returns dict[status]→DataFrame
from Demographics.birth_year import return_birth_year          # returns single DataFrame
from Demographics.zip_code import home_zip_code                # returns single DataFrame
from Demographics.military import return_military              # returns dict["Yes"/"No"]→DataFrame
from Demographics.income_bracket import return_income_bracket  # returns dict[bracket]→DataFrame

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
            excel_buffer = BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            zip_file.writestr(name, excel_buffer.getvalue())

        # --- Demographics that return single DataFrame ---
        demo_single = {
            "BirthYear_Cleaned.xlsx": return_birth_year(),
            "HomeZipCode_Cleaned.xlsx": home_zip_code(),
        }

        for name, df in demo_single.items():
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
            for key, df in df_dict.items():
                fname = f"{prefix}_{key}.xlsx".replace(" ", "_")
                excel_buffer = BytesIO()
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False)
                zip_file.writestr(fname, excel_buffer.getvalue())

    st.download_button(
        label="📥 Download All Cleaned Data (ZIP)",
        data=zip_buffer.getvalue(),
        file_name="All_Cleaned_Data.zip",
        mime="application/zip"
    )
