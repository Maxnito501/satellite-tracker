import os
from dotenv import load_dotenv
import streamlit as st

# โหลด environment variables จาก .env file (เฉพาะ local development)
load_dotenv()

def get_line_config():
    """
    ดึงการตั้งค่า LINE จาก environment variables หรือ Streamlit secrets
    เรียงลำดับความสำคัญ:
    1. st.secrets (สำหรับ Streamlit Cloud)
    2. environment variables (สำหรับ local development)
    """
    
    # พยายามโหลดจาก Streamlit secrets ก่อน (ถ้ามี)
    try:
        if "line" in st.secrets:
            return {
                "access_token": st.secrets["line"]["channel_access_token"],
                "channel_secret": st.secrets["line"]["channel_secret"],
                "user_id": st.secrets["line"].get("user_id")
            }
    except:
        pass
    
    # ถ้าไม่มี secrets ให้โหลดจาก environment variables
    return {
        "access_token": os.getenv("LINE_CHANNEL_ACCESS_TOKEN"),
        "channel_secret": os.getenv("LINE_CHANNEL_SECRET"),
        "user_id": os.getenv("LINE_USER_ID")
    }

def save_line_config_to_env(access_token, channel_secret, user_id=None):
    """
    บันทึกการตั้งค่า LINE ลงใน session state (ไม่บันทึกลงไฟล์จริง)
    ใช้สำหรับกรณีต้องการเปลี่ยนค่าเฉพาะ session
    """
    if "line_config" not in st.session_state:
        st.session_state.line_config = {}
    
    st.session_state.line_config.update({
        "access_token": access_token,
        "channel_secret": channel_secret,
        "user_id": user_id
    })

def get_active_config():
    """
    ดึงการตั้งค่าที่กำลังใช้งานอยู่
    - ถ้ามีใน session state ให้ใช้ค่านั้น
    - ถ้าไม่มี ให้ใช้จาก environment/secrets
    """
    if "line_config" in st.session_state and st.session_state.line_config.get("access_token"):
        return st.session_state.line_config
    return get_line_config()
