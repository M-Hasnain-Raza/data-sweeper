# Import
import streamlit as st;
import pandas as pd;
import os;
from io import BytesIO

# Set up aur app
st.set_page_config(page_title="Data Sweeper", layout="wide")
st.title("Data sweeper")
st.write("transform my CSV file into Excel formate built-in data cleaning and visualization!")

uploaded_files = st.file_uploader("Upload my files (CSV to Excel):", type=["csv","xlsx"],
accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file, engine="calamine") #engine="openpyxl"
        else:
            st.error(f"unsupported file type: {file_ext}")
            continue

         # display info about the file 
    
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size/1024}")

         #show 5 rows of our data frame 

        st.write("Preview of our data frame")
        st.dataframe(df.head())

       #options for data cleaning
        st.subheader("Data cleaning options")
        if st.checkbox(f"clean data for {file.name}"):
         col1, col2 = st.columns(2)

         with col1:
            if st.button(f"Remove duplicate from {file.name}"):
                 df.drop_duplicates(inplace=True)
                 st.write("Duplicates Removed!")

         with col2:
           if st.button(f"fil missing value for {file.name}"):
                numeric_cols = df.select_dtypes(include=['number']).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.write("Missing Values have been filed!")

      # choose specific column to keep or convert
        st.subheader("select columns to convert")
        columns = st.multiselect(f"choose column for {file.name}", df.columns, default=df.columns.to_list())
        df = df[columns]
       


     # create some visualization
        st.subheader("Data visualization")
        if st.checkbox(f"show Visualization for {file.name}"):
           st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])
  
         #convert csv to Excel

        st.subheader("Conversion Option")
        conversion_type = st.radio(f"convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
              df.to_csv(buffer, index=False)
              file_name = file.name.replace(file_ext,".csv")
              mime_type = "text/csv"

            elif conversion_type == "Excel":
              df.to_excel(buffer, index=False)
              file_name = file.name.replace(file_ext,".xlsx")
              mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" 
            buffer.seek(0)

            #Download button
            st.download_button(
               label=f"download {file.name} as {conversion_type}",
               data=buffer,
               file_name=file_name,
               mime=mime_type
            )
st.success("all files processed succesfully!")
