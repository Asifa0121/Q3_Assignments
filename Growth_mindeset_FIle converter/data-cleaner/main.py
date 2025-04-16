import streamlit as st
import pandas as pd
from io import BytesIO 

st.set_page_config(page_title="File converter& CLeaner", layout="wide")
st.title("File converter🗂️ & Cleaner🧹")
st.write("Ulpload your CSV and Excel Files to clean the data convert format effortlessly")

files = st.file_uploader("Upload CSV or Excel files", type=["csv", "xlxs"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split(".")[-1]
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

        st.subheader(f"🔍{file.name} - Preview")
        st.dataframe(df.head())

        if st.checkbox(f"Fill Missing Values - {file.name}"):
            df.fillna(df.select_dtypes(include="number").mean(), inplace=True) 
            st.success("Missing Values Filled Successfully!🎉")
            st.dataframe(df.head())

        seleceted_columns = st.multiselect(f"Select Columns, {file.name}", df.columns, default=df.columns)
        df = df [seleceted_columns]
        st.dataframe(df.head())

        if st.checkbox(f"📊 Show Chart - {file.name}") and not df.select_dtypes(include="number").empty:
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        format_choice = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"Download {file.name} as {format_choice}"):
            output = BytesIO()
            if format_choice == "CSV":
                df.to_csv(output, index=False)
                mime = "text/csv"
                new_name = file.name.replace(ext, "csv")
            else:
                df.to_excel(output, index=False)
                mime = "application/vnd.openxmlformats.office document.spreadsheetml.sheet"
                new_name = file.name.replace(ext, "xlsx")
            output.seek(0)
            st.download_button("⬇️Download File", file_name=new_name, data=output, mime=mime)
        st.success("Processing Completed🎉")

        