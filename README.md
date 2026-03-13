# Satellite Tracker

แอปติดตามหุ้น Core + Satellite พร้อมระบบแจ้งเตือน LINE

## วิธีติดตั้ง
1. clone repo นี้
2. ติดตั้ง packages: `pip install -r requirements.txt`
3. รัน: `streamlit run app.py`

## ฟีเจอร์
- แสดงข้อมูลหุ้น Core (ถือยาว) + Satellite (เล่นรอบ)
- ดึงราคาปัจจุบันจาก Google Finance
- ตั้งแจ้งเตือน LINE เมื่อราคาถึงเป้าหมาย
