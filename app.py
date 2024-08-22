import streamlit as st
import pandas as pd
import pdfplumber

# Upload PDF file
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    # Save the uploaded PDF to a temporary file
    with open("/tmp/temp_pdf.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Extract tables using pdfplumber
    with pdfplumber.open("/tmp/temp_pdf.pdf") as pdf:
        all_tables = []
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)
                
        # Combine all tables into one DataFrame
        combined_df = pd.concat(all_tables, ignore_index=True)
    
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
