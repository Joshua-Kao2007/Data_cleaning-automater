from io import BytesIO
import streamlit as st

def excel_download_button(df, label, sheet_name, filename):
    buffer = BytesIO()
    df.to_excel(buffer, index=False, sheet_name=sheet_name, engine="openpyxl")
    buffer.seek(0)
    
    st.download_button(
        label=label,
        data=buffer,
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

def csv_download_button(df, label, filename):
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=label,
        data=csv_bytes,
        file_name=filename,
        mime="text/csv"
    )
