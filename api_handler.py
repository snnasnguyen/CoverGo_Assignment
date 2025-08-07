# api_handler.py
import google.generativeai as genai
from PIL import Image
import streamlit as st
import io
import json

def initialize_gemini():
    """
    Cấu hình và khởi tạo mô hình Gemini từ Streamlit Secrets.
    """
    try:
        genai.configure(api_key="AIzaSyCS7vSDj8YCt16yCRxF64om0HQs4jbOebs")
        return genai.GenerativeModel('gemini-2.5-flash')
    except KeyError:
        st.error("Lỗi: Không tìm thấy Gemini API Key. Vui lòng kiểm tra file .streamlit/secrets.toml.")
        st.stop()
    except Exception as e:
        st.error(f"Lỗi khi cấu hình Gemini API: {e}")
        st.stop()


def extract_info_from_image(image_bytes):
    """
    Sử dụng Gemini API để trích xuất thông tin từ ảnh và trả về JSON.
    """
    model = initialize_gemini()
    
    # Chuyển đổi byte ảnh sang đối tượng PIL Image
    page_image = Image.open(io.BytesIO(image_bytes))
    prompt =[
                "You are a professional AI assistant specializing in processing insurance documents. Based on the following text content, please extract key information from the claim form and categorize them into distinct sections: 'Personal and Policy Information', 'Medical Information', and 'Payment Information'.",
                "Present the results in the following structured format and response JSON format:",
                "---",
                "### **Personal and Policy Information**",
                "* **Insured / Policy Owner Personal Details**:",
                "    * Name:",
                "    * ID / Passport No.:",
                "    * Date of Birth:",
                "    * Gender:",
                "    * Occupation:",
                "* **Policy Details**:",
                "    * Policy No. / Cert No.:",
                "    * Product Type:",
                "    * Claimed Benefits:",
                "---",
                "### **Medical Information**",
                "* **Inpatient Details**:",
                "    * Patient Name:",
                "    * Admission Date:",
                "    * Discharge Date:",
                "    * Final Diagnosis:",
                "    * Surgical Procedures Performed:",
                "    * Is this an emergency case?:",
                "    * Is this due to an accident?:",
                "---",
                "### **Payment Information**",
                "* **Payment Method**:",
                "    * e-Payout or Cheque",
                "* **Bank Account Details**:",
                "    * Account Holder Name:",
                "    * Bank Name:",
                "    * Account Number:",
                "If any information field is not found, leave it blank or state 'NULL'.",
                "Image content for analysis:",
                page_image
            ]
    try:
        response = model.generate_content(prompt)
        print(response.text)
        extracted_json_str = response.text.strip('` \n').replace('json', '')
        data = json.loads(extracted_json_str)
        return data
    except Exception as e:
        st.error(f"Lỗi khi gọi Gemini API: {e}")
        return None

