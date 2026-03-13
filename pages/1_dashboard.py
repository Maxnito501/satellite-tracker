import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ต้องเป็นคำสั่งแรกของหน้า
st.set_page_config(layout="wide")

st.title("📊 แดชบอร์ดรวม")
st.markdown("ภาพรวมพอร์ต Core + Satellite + กองทุน")

# โหลดข้อมูลจาก CSV
@st.cache_data
def load_data():
    core = pd.read_csv("data/core_portfolio.csv")
    satellite = pd.read_csv("data/satellite_portfolio.csv")
    funds = pd.read_csv("data/funds.csv")
    return core, satellite, funds

core, satellite, funds = load_data()

# แถวที่ 1: สถิติรวม
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Core (ถือยาว)", f"{len(core)} ตัว", "ปันผล 5-8%")

with col2:
    st.metric("Satellite (เล่นรอบ)", f"{len(satellite)} ตัว", "EDCA + ขายทำกำไร")

with col3:
    st.metric("กองทุนรวม", f"{len(funds)} กอง", "DCA + EDCA")

with col4:
    st.metric("สถานะ", "พร้อมลุย", "รอจังหวะ")

st.markdown("---")

# แถวที่ 2: กราฟตัวอย่าง (จำลอง)
st.subheader("📈 ตัวอย่างกราฟราคา (จำลอง)")

# สร้างกราฟตัวอย่าง
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=("PTT", "SCB", "WHA", "CPAXT"),
    vertical_spacing=0.12
)

# เพิ่มข้อมูลจำลอง
fig.add_trace(
    go.Scatter(x=[1,2,3,4,5], y=[32,33,34,33,34], mode="lines", name="PTT"),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(x=[1,2,3,4,5], y=[135,138,140,142,144], mode="lines", name="SCB"),
    row=1, col=2
)

fig.add_trace(
    go.Scatter(x=[1,2,3,4,5], y=[4.0,4.1,4.2,4.1,4.0], mode="lines", name="WHA"),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(x=[1,2,3,4,5], y=[15.0,15.5,16.0,15.5,15.0], mode="lines", name="CPAXT"),
    row=2, col=2
)

fig.update_layout(height=600, showlegend=False)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# แถวที่ 3: แสดงข้อมูลแบบย่อ
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Core Portfolio (ถือยาว)")
    st.dataframe(core[["stock", "sector", "dividend", "esg"]], use_container_width=True)

with col2:
    st.subheader("🚀 Satellite Portfolio (เล่นรอบ)")
    st.dataframe(satellite[["stock", "sector", "dividend", "theme"]], use_container_width=True)

st.markdown("---")

# ส่วนท้าย
st.caption("📌 ข้อมูล ณ วันที่ 11 มีนาคม 2569")
