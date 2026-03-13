import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(layout="wide")

st.title("🏆 Core Portfolio")
st.markdown("""
**หุ้นแกนหลัก (ถือยาว)**  
- ปันผลสูง 5-8%  
- ESG Rating A ขึ้นไป  
- Beta ต่ำ ผันผวนน้อยกว่าตลาด  
- กลยุทธ์: DCA รายเดือน / EDCA เมื่อลง
""")

# โหลดข้อมูล
@st.cache_data
def load_core():
    return pd.read_csv("data/core_portfolio.csv")

df = load_core()

# แสดงตารางเต็ม
st.subheader("📋 ข้อมูล Core Portfolio")
st.dataframe(
    df,
    column_config={
        "stock": "หุ้น",
        "sector": "หมวด",
        "entry_dca": "จุด DCA",
        "entry_edca": "จุด EDCA",
        "dividend": "ปันผล",
        "esg": "ESG",
        "note": "หมายเหตุ"
    },
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# แสดงรายละเอียดทีละตัว
st.subheader("🔍 วิเคราะห์รายตัว")

# เลือกหุ้นจาก dropdown
selected = st.selectbox(
    "เลือกหุ้นเพื่อดูรายละเอียด",
    df["stock"].tolist()
)

# ดึงข้อมูลหุ้นที่เลือก
stock_data = df[df["stock"] == selected].iloc[0]

# แสดงข้อมูล
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"**หมวด:** {stock_data['sector']}")
    st.markdown(f"**จุด DCA:** {stock_data['entry_dca']}")
    st.markdown(f"**จุด EDCA:** {stock_data['entry_edca']}")

with col2:
    st.markdown(f"**ปันผล:** {stock_data['dividend']}")
    st.markdown(f"**ESG:** {stock_data['esg']}")
    st.markdown(f"**หมายเหตุ:** {stock_data['note']}")

# กราฟจำลอง (ตามหุ้นที่เลือก)
st.markdown("---")
st.subheader(f"📈 กราฟราคาจำลอง {selected}")

# สร้างข้อมูลจำลองตามราคาเป้าหมาย
import numpy as np

# แยกค่าตัวเลขจาก entry_dca (เช่น "32-34" -> [32,34])
dca_range = stock_data['entry_dca'].split('-')
dca_low = float(dca_range[0])
dca_high = float(dca_range[1])

# สร้างข้อมูลราคาจำลอง 30 วัน
days = np.arange(1, 31)
base_price = (dca_low + dca_high) / 2
prices = base_price + np.random.normal(0, 1, 30).cumsum() * 0.1

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=days,
    y=prices,
    mode='lines',
    name=selected,
    line=dict(color='royalblue', width=2)
))

# เพิ่มเส้น DCA zone
fig.add_hline(
    y=dca_low,
    line_dash="dash",
    line_color="green",
    annotation_text=f"DCA ต่ำ {dca_low}"
)
fig.add_hline(
    y=dca_high,
    line_dash="dash",
    line_color="red",
    annotation_text=f"DCA สูง {dca_high}"
)

fig.update_layout(
    title=f"จำลองราคา {selected} 30 วัน",
    xaxis_title="วัน",
    yaxis_title="ราคา",
    height=400
)

st.plotly_chart(fig, use_container_width=True)

st.caption("📌 หมายเหตุ: กราฟเป็นเพียงการจำลองเพื่อแสดงแนวคิด")
