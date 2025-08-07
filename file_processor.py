# file_processor.py
import fitz  # PyMuPDF
import streamlit as st
import io

def convert_pdf_to_image_bytes(uploaded_pdf_file):
    """
    Chuyển đổi tất cả các trang của file PDF thành danh sách các byte ảnh PNG.
    """
    try:
        doc = fitz.open(stream=uploaded_pdf_file.read(), filetype="pdf")
        img_bytes_list = []
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(dpi=300)
            img_bytes = pix.tobytes("png")
            img_bytes_list.append(img_bytes)
        doc.close()
        return img_bytes_list
    except Exception as e:
        st.error(f"Lỗi khi xử lý file PDF: {e}")
        return None