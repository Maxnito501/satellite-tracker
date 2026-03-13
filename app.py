import streamlit as st

# ต้องเป็นคำสั่งแรกของแอป
st.set_page_config(
    page_title="Satellite Tracker",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ส่วนนำ
st.title("📊 Satellite Tracker")
st.markdown("""
ติดตามหุ้น **Core + Satellite** พร้อมระบบแจ้งเตือน LINE  
แนวคิด: 
- **Core (ถือยาว)** — ปันผลดี ESG สูง  
- **Satellite (เล่นรอบ)** — EDCA ซื้อเมื่อถูก ขายเมื่อกำไร
""")

# แบ่งคอลัมน์สำหรับสถิติคร่าวๆ
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Core (ถือยาว)", "8 ตัว", "PTT, SCB, TISCO, AP, CPALL, ADVANC, BH, KTC")

with col2:
    st.metric("Satellite (เล่นรอบ)", "11 ตัว", "PTTEP, KTB, OR, GULF, BDMS, GPSC, BGRIM, WHA, CPAXT, SIRI, TU")

with col3:
    st.metric("กองทุนรวม", "8 กอง", "DCA + EDCA")

st.markdown("---")

# คำแนะนำเบื้องต้น
st.subheader("📌 วิธีใช้แอป")
st.markdown("""
- **แดชบอร์ด** – ดูภาพรวมพอร์ต
- **Core Portfolio** – หุ้นถือยาว จุด DCA/EDCA
- **Satellite Portfolio** – หุ้นเล่นรอบ จุดซื้อ-ขาย
- **กองทุนรวม** – DCA รายเดือน + EDCA ตามจังหวะ
- **ตั้งแจ้งเตือน** – รับ LINE เมื่อราคาถึงเป้าหมาย
""")

st.info("💡 ระบบแจ้งเตือนจะทำงานทุก 1 ชั่วโมง (เมื่อ Deploy แล้ว)")

# ส่วนท้าย
st.markdown("---")
st.caption("พัฒนาโดยคุณ — เพื่อการลงทุนระยะยาว 10 ปี")
