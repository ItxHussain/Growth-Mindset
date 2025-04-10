# Import
import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout="wide")
st.title("Data Sweeper")
st.write("Transform Your files between CSV and Excel formats with built-in data cleaning and visualization!")



uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "excel"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == '.csv':
            df = pd.read_csv(file)
        elif file_ext == '.xlsx':
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue
        
        # Display info about the file
        st.write(f"*File Name:* {file.name}")
        st.write(f"*File Size:* {file.size/1024}")

        # Display the first 5 rows of the dataframe
        st.write("Preview the Head of the Dataframe")
        st.dataframe(df.head())

      
        # Perform data cleaning
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates removed successfully!")

                    with col2:
                        if st.button(f"Fill Missing Values for {file.name}"):
                            numeric_col = df.select_dtypes(include=["number"]).columns
                            df[numeric_col] = df[numeric_col].fillna(df[numeric_col].mean())
                            st.write("Missing values filled with mean successfully!")


                            # Choose Specific Column to keep or Convert 
                            st.subheader("Select Columns to Convert")
                            columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
                            df = df[columns]


                            # Create Some Visualizations
                            st.subheader("Data Visualizations")
                            if st.checkbox(f"Show visualization for {file.name}"):
                                st.bar_chart(df.select_dtypes(include="number").iloc[:,:2])


                            # Convert the file => CSV to Excel format
                            st.subheader("Conversion Options")
                            conversion_type = st.radio(f"Convert {file.name} to:", ["csv", "Excel"], key=file.name)
                            if st.button(f"Convert {file.name}"):
                                buffer = BytesIO()
                                if conversion_type == "CSV":
                                    df.to_csv(buffer, index=False)
                                    file_name = file.name.replace(file.name, ".csv")
                                    mime_type = "text/csv"

                                elif conversion_type == "Excel":
                                    df.to_excel(buffer, index=False)
                                    file_name = file.name.replace(file.name, ".xlsx")
                                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                buffer.seek(0)


                                # Download the converted file
                                st.download_button(
                                     label=f"Download {file_name} as {conversion_type}",
                                     data=buffer,
                                     file_name=file_name,
                                     mime=mime_type
                                )

                    st.success("Data processing completed successfully!")