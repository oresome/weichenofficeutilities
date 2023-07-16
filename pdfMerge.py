import streamlit as st
from PyPDF2 import PdfMerger, PdfReader
from io import BytesIO

def merge_pdfs(pdfFiles):
    merger = PdfMerger()
    
    for file in pdfFiles: 
        merger.append(file, 'rb')
        
    _byteIo = BytesIO()
    merger.write(_byteIo)    
    _byteIo.seek(0)
    
    return _byteIo

def main():
    st.title("PDF Document Merge APP")

    # File upload
    uploaded_files = st.file_uploader("Upload PDF files", accept_multiple_files=True)

    if uploaded_files:
        # Sort files alphabetically
        sorted_files = sorted(uploaded_files, key=lambda file: file.name)

        # Combine PDFs
        merged_file = merge_pdfs(sorted_files)

        # Download button
        st.download_button("Download Merged PDF", data=merged_file, file_name="merged.pdf",mime='application/octet-stream')


if __name__ == "__main__":
    main()
