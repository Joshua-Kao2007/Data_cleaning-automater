import streamlit as st
import pandas as pd
from io import BytesIO
from KPIs.kpi_dashboard import main_kpis
from Demographics.education import education_level
from Demographics.employment import return_employment
from Demographics.ethnicity import return_ethnicity
from Demographics.industry_code import return_industry_code
from Demographics.marital_status import return_marital_status
from Demographics.birth_year import return_birth_year
from Demographics.military import return_military
from Demographics.income_bracket import return_income_bracket
from Demographics.gender import return_gender
from Demographics.zip_code import home_zip_code
from utils.export_zip import create_cleaned_data_zip

st.set_page_config(page_title="Survey Data Cleaner", layout="wide")
st.title("📊 Survey Data Cleaning Dashboard")
uploaded_file = st.file_uploader("Upload your survey Excel file", type=["xlsx", "xls"])

if not uploaded_file:
    st.stop()
try:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()
except Exception:
    st.error("Failed to read the Excel file. Ensure it's a valid .xlsx/.xls format.")
    st.stop()

page = st.sidebar.radio(
    "Choose view:",
    ["KPIs", "Highest Education Level", "Gender", "Employment Level", "Industry Code", "Marital Status", "Race/Ethnicity", "Birth Year", "Military Status", "Income Bracket", "Zip Code", "Full Zip File"]
)

if page == "KPIs":
    main_kpis(df)
elif page == "Gender":
    return_gender(df)
elif page == "Highest Education Level":
    education_level(df)
elif page == "Employment Level":
    return_employment(df)
elif page == "Industry Code":
    return_industry_code(df)
elif page == "Marital Status":
    return_marital_status(df)
elif page == "Race/Ethnicity":
    return_ethnicity(df)
elif page == "Birth Year":
    return_birth_year(df)
elif page == "Military Status":
    return_military(df)
elif page == "Income Bracket":
    return_income_bracket(df)
elif page == "Zip Code":
    home_zip_code(df)
elif page == "Full Zip File":
    create_cleaned_data_zip(df, season)