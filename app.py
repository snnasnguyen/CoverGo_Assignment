# app.py
import streamlit as st
from file_processor import convert_pdf_to_image_bytes
from api_handler import extract_info_from_image

def main():
    """
    Hàm chính của ứng dụng Streamlit.
    """
    st.set_page_config(
        page_title="Demo OCR Bảo hiểm",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("📄 Demo OCR cho Mẫu đơn Yêu cầu Bồi thường Bảo hiểm")

    uploaded_file = st.file_uploader(
        "Tải lên một file PDF hoặc Hình ảnh",
        type=["pdf", "png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:
        file_type = uploaded_file.type
        # Khởi tạo một từ điển duy nhất để lưu trữ toàn bộ dữ liệu tổng hợp
        combined_data = {}

        # Hiển thị trạng thái tải lên và xử lý
        with st.spinner("File đã được tải lên thành công. Đang xử lý..."):
            if file_type == "application/pdf":
                img_bytes_list = convert_pdf_to_image_bytes(uploaded_file)
                if img_bytes_list:
                    # Lặp qua từng trang để trích xuất thông tin
                    for i, img_bytes in enumerate(img_bytes_list):
                        st.image(img_bytes, caption=f"Trang {i+1} của tài liệu")
                        extracted_data_page = extract_info_from_image(img_bytes)
                        st.json(extracted_data_page)
                        # Hợp nhất dữ liệu với logic ưu tiên trang đầu
                        if i == 0:
                            combined_data = extracted_data_page
                        else:
                            # Chỉ cập nhật nếu key chưa tồn tại, hoặc giá trị hiện tại đang là None/không hợp lệ
                            for key, value in extracted_data_page.items():
                                if key not in combined_data or combined_data[key] in ["NULL"]:
                                    if value not in ["NULL"]:
                                        combined_data[key] = value

            elif file_type.startswith("image"):
                img_bytes = uploaded_file.read()
                st.image(img_bytes, caption="Hình ảnh đã tải lên")
                extracted_data_page = extract_info_from_image(img_bytes)
                if extracted_data_page:
                    combined_data.update(extracted_data_page) # Với 1 ảnh, update là đủ
            
            else:
                st.error("Định dạng file không được hỗ trợ.")

        # Hiển thị kết quả sau khi xử lý xong
        if combined_data:
            st.success("✅ Trích xuất dữ liệu thành công!")
            st.subheader("Thông tin được trích xuất và tổng hợp:")
            st.json(combined_data)
        
        elif uploaded_file:
            st.warning("Không thể trích xuất thông tin. Vui lòng thử lại với một tài liệu khác.")


if __name__ == "__main__":
    main()