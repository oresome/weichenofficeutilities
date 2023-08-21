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

    st.markdown("---")
    st.markdown("Demo video download")
    st.video("Bisalloy_demo.mp4")

    file_url = 'https://webify-1306024390.cos.ap-shanghai.myqcloud.com/Download/Bisalloy_UH-RFID_Wear_Sensor_Demo.mp4'
    #file_name = 'Bisalloy_demo.mp4'
    file_data = requests.get(file_url).content
    st.download_button('Download This Demo', data=file_data, file_name="Bisalloy_demo.mp4", mime='application/octet-stream')




if __name__ == "__main__":
    main()
