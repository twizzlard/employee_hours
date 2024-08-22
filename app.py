import streamlit as st
import pandas as pd
import PyPDF2
import camelot

# Upload PDF file
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    # Save the uploaded PDF to a temporary file
    with open("/tmp/temp_pdf.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Extract tables using Camelot
    tables = camelot.read_pdf("/tmp/temp_pdf.pdf", pages='all', flavor='stream')
    
    # Combine all tables into one DataFrame
    combined_df = pd.concat([table.df for table in tables], ignore_index=True)
    
    # Display the DataFrame
    st.write("Extracted Table Data:")
    st.dataframe(combined_df)
    
    # Option to download the DataFrame as CSV
    csv = combined_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='extracted_tables.csv',
        mime='text/csv',
    )
