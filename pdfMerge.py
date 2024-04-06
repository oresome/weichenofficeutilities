import streamlit as st
from PyPDF2 import PdfMerger, PdfReader
from io import BytesIO
import requests
import fitz
import os
import shutil
from zipfile import ZipFile
import glob

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

def pdf_to_images_with_resolution(pdf_path, output_folder, resolution):
    with open("temp_file.pdf", "wb") as f:
        f.write(pdf_path.getbuffer())
    pdf_document = fitz.open("temp_file.pdf")
    #st.markdown(pdf_document)
    #st.markdown(pdf_document.page_count)
    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        #st.markdown(page)
        # Calculate the image size based on the specified resolution
        zoom_x = resolution / 72  # 1 point (pt) is equal to 1/72 inch
        zoom_y = resolution / 72
        trans = fitz.Matrix(zoom_x, zoom_y)
        pixmap = page.get_pixmap(matrix=trans)
        image_path = f"page{page_number}_res{resolution}.png"
        #st.markdown(image_path)
        pixmap.pil_save(image_path)


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


    ##############################################################################################################

    st.markdown("---")
    st.subheader("PDF Files to Images")
    # File upload
    uploaded_files_image = st.file_uploader("Upload a PDF file", accept_multiple_files=False)
    #st.markdown(uploaded_files_image)

    # resolution options
    RESoption = st.selectbox(
                        'Please Select the Image Resolution',
                        ('150', '100', '300', '600'))

    st.write('You Selected:', RESoption)

    if uploaded_files_image:
        # convert PDF
        pdf_to_images_with_resolution(uploaded_files_image, "/", resolution=int(RESoption))
        
        imageList = glob.glob('page*.png')
        # create a ZipFile object
        zipObj = ZipFile('imageResults.zip', 'w')
        # Add multiple files to the zip
        for image in imageList:
            zipObj.write(image)
        zipObj.close()  
        
        # Download button
        with open("imageResults.zip", "rb") as fp:
            btn = st.download_button(
                label="Download Converted Images",
                data=fp,
                file_name="imageResults.zip",
                mime="application/zip"
            )
        
        # remove then recreate "imageResults/"
        #shutil.rmtree("imageResults/")
        os.remove("imageResults.zip")
        for image in imageList:
            os.remove(image)
        #os.makedirs("imageResults/")



if __name__ == "__main__":
    main()
