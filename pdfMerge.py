import streamlit as st
from PyPDF2 import PdfMerger, PdfReader
from io import BytesIO
import requests

def merge_pdfs(pdfFiles):
    merger = PdfMerger()
    
    for file in pdfFiles: 
        merger.append(file, 'rb')
        
    _byteIo = BytesIO()
    merger.write(_byteIo)    
    _byteIo.seek(0)
    
    return _byteIo

def download_file(file_url, file_name):
    response = requests.get(file_url)
    with open(file_name, 'wb') as file:
        file.write(response.content)

def main():
    st.title("PDF Document Edit APP")
    st.markdown("---")
    st.subheader("PDF Files Merge")
    # File upload
    uploaded_files = st.file_uploader("Upload PDF files", accept_multiple_files=True)

    if uploaded_files:
        # Sort files alphabetically
        sorted_files = sorted(uploaded_files, key=lambda file: file.name)

        # Combine PDFs
        merged_file = merge_pdfs(sorted_files)

        # Download button
        st.download_button("Download Merged PDF", data=merged_file, file_name="merged.pdf",mime='application/octet-stream')

    st.markdown("---")
    st.subheader("PDF Files to Images")




if __name__ == "__main__":
    main()
