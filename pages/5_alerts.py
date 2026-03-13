import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

# โหลด environment variables จาก .env file
load_dotenv()

st.set_page_config(layout="wide")

st.title("🔔 ตั้งแจ้งเตือน LINE Messaging API")
st.markdown("""
รับการแจ้งเตือนเมื่อหุ้นถึงจุดซื้อหรือจุดขาย  
ผ่าน **LINE Messaging API** (ต้องมี LINE Official Account)

✅ **Token โหลดจากไฟล์ .env อัตโนมัติ**  
ไม่ต้องกรอกทุกครั้งที่เข้าแอป
""")

# ---------- โหลด Token จาก Environment ----------
CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
USER_ID = os.getenv("LINE_USER_ID")  # optional

# ---------- แสดงสถานะ Token ----------
st.subheader("🔐 สถานะ Token")

col1, col2 = st.columns(2)

with col1:
    if CHANNEL_ACCESS_TOKEN:
        masked_token = CHANNEL_ACCESS_TOKEN[:8] + "*" * 16 + CHANNEL_ACCESS_TOKEN[-4:]
        st.success("✅ Channel Access Token")
        st.code(masked_token)
    else:
        st.error("❌ ไม่พบ Channel Access Token ใน .env")

with col2:
    if CHANNEL_SECRET:
        masked_secret = CHANNEL_SECRET[:4] + "*" * 12 + CHANNEL_SECRET[-4:]
        st.success("✅ Channel Secret")
        st.code(masked_secret)
    else:
        st.error("❌ ไม่พบ Channel Secret ใน .env")

if USER_ID:
    masked_uid = USER_ID[:5] + "*" * 27 + USER_ID[-4:]
    st.info(f"📌 User ID: {masked_uid}")
else:
    st.info("📌 ไม่ได้ระบุ User ID (ส่งแบบ Broadcast)")

st.markdown("---")

# ---------- ฟังก์ชันส่ง LINE ----------
def send_line_message(access_token, message, user_id=None):
    """ส่งข้อความผ่าน LINE Messaging API"""
    url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    if user_id:
        url = "https://api.line.me/v2/bot/message/push"
        payload = {
            "to": user_id,
            "messages": [{"type": "text", "text": message}]
        }
    else:
        payload = {
            "messages": [{"type": "text", "text": message}]
        }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response.status_code in [200, 202], response.text
    except Exception as e:
        return False, str(e)

# ---------- ทดสอบส่งข้อความ ----------
if CHANNEL_ACCESS_TOKEN and CHANNEL_SECRET:
    st.subheader("📤 ทดสอบส่งข้อความ")
    
    test_message = st.text_input("ข้อความทดสอบ", value="📈 ทดสอบแจ้งเตือนจาก Satellite Tracker")
    
    if st.button("📤 ส่งทดสอบ"):
        success, response = send_line_message(
            CHANNEL_ACCESS_TOKEN,
            test_message,
            USER_ID
        )
        
        if success:
            msg_type = "เฉพาะบุคคล" if USER_ID else "Broadcast"
            st.success(f"✅ ส่ง {msg_type} สำเร็จ ตรวจสอบ LINE ของคุณ")
        else:
            st.error(f"❌ ส่งไม่สำเร็จ: {response}")
else:
    st.warning("⚠️ ไม่สามารถทดสอบส่งได้ กรุณาตั้งค่า Token ใน .env ให้ครบถ้วน")

st.markdown("---")

# ---------- โหลดข้อมูลหุ้น ----------
@st.cache_data
def load_stocks():
    core = pd.read_csv("data/core_portfolio.csv")
    satellite = pd.read_csv("data/satellite_portfolio.csv")
    
    core_data = core[["stock", "entry_dca", "entry_edca"]].copy()
    core_data["entry_exit"] = core_data["entry_dca"] + " / " + core_data["entry_edca"]
    
    satellite_data = satellite[["stock", "entry_edca", "exit_target"]].copy()
    satellite_data["entry_exit"] = satellite_data["entry_edca"] + " → " + satellite_data["exit_target"]
    
    all_stocks = pd.concat([
        core_data[["stock", "entry_exit"]],
        satellite_data[["stock", "entry_exit"]]
    ], ignore_index=True)
    
    return all_stocks

stocks = load_stocks()

# ---------- เลือกหุ้นที่จะแจ้งเตือน ----------
st.subheader("📊 เลือกหุ้นที่จะแจ้งเตือน")

if "alert_settings" not in st.session_state:
    st.session_state.alert_settings = {}

# ตั้งค่าเริ่มต้น
for idx, row in stocks.iterrows():
    stock = row["stock"]
    if stock not in st.session_state.alert_settings:
        st.session_state.alert_settings[stock] = {
            "buy_alert": True,
            "sell_alert": False
        }

# แสดงตารางหุ้น
for idx, row in stocks.iterrows():
    stock = row["stock"]
    
    cols = st.columns([1, 2, 1.5, 1.5])
    
    with cols[0]:
        st.write(f"**{stock}**")
    
    with cols[1]:
        st.write(f"`{row['entry_exit']}`")
    
    with cols[2]:
        buy = st.checkbox(
            "แจ้งซื้อ",
            value=st.session_state.alert_settings[stock]["buy_alert"],
            key=f"buy_{stock}"
        )
        st.session_state.alert_settings[stock]["buy_alert"] = buy
    
    with cols[3]:
        sell = st.checkbox(
            "แจ้งขาย",
            value=st.session_state.alert_settings[stock]["sell_alert"],
            key=f"sell_{stock}"
        )
        st.session_state.alert_settings[stock]["sell_alert"] = sell
    
    st.divider()

st.markdown("---")

# ---------- สรุป ----------
st.subheader("📋 สรุปการตั้งค่า")

col1, col2 = st.columns(2)

with col1:
    token_status = "✅ มี Token" if CHANNEL_ACCESS_TOKEN else "❌ ไม่มี Token"
    st.metric("สถานะ Token", token_status)

with col2:
    buy_count = sum(1 for s in st.session_state.alert_settings.values() if s["buy_alert"])
    sell_count = sum(1 for s in st.session_state.alert_settings.values() if s["sell_alert"])
    st.metric("แจ้งซื้อ/ขาย", f"{buy_count} / {sell_count}")

if st.button("💾 บันทึกการตั้งค่า"):
    st.success("✅ บันทึกการตั้งค่าเรียบร้อย")

st.info("""
💡 **หมายเหตุ:**
- Token อ่านจากไฟล์ `.env` โดยอัตโนมัติ
- การตั้งค่าหุ้นจะอยู่ใน Session (หายเมื่อปิดแอป)
- สำหรับ Production ควรใช้ Environment Variables + Database
""")
