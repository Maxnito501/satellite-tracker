import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(layout="wide")

st.title("🚀 Satellite Portfolio")
st.markdown("""
**หุ้นเล่นรอบ (Satellite)**  
- EDCA ซื้อเมื่อถูก ขายเมื่อกำไร  
- ธีมเฉพาะ: FDI, Data Center, Turnaround, XD รอบ  
- กลยุทธ์: ซื้อที่จุด EDCA, ขายที่จุดขาย
""")

# โหลดข้อมูล
@st.cache_data
def load_satellite():
    return pd.read_csv("data/satellite_portfolio.csv")

df = load_satellite()

# แสดงตารางเต็ม
st.subheader("📋 ข้อมูล Satellite Portfolio")
st.dataframe(
    df,
    column_config={
        "stock": "หุ้น",
        "sector": "หมวด",
        "entry_edca": "จุด EDCA",
        "exit_target": "จุดขาย",
        "dividend": "ปันผล",
        "theme": "ธีม"
    },
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# สถิติ
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("จำนวนหุ้น", f"{len(df)} ตัว")
with col2:
    avg_dividend = df["dividend"].str.replace("%", "").astype(float).mean()
    st.metric("ปันผลเฉลี่ย", f"{avg_dividend:.1f}%")
with col3:
    st.metric("ธีมเด่น", "FDI / Data Center / Turnaround")

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
    st.markdown(f"**จุด EDCA:** {stock_data['entry_edca']}")
    st.markdown(f"**จุดขาย:** {stock_data['exit_target']}")

with col2:
    st.markdown(f"**ปันผล:** {stock_data['dividend']}")
    st.markdown(f"**ธีม:** {stock_data['theme']}")

st.markdown("---")

# กราฟจำลองกลยุทธ์ EDCA
st.subheader(f"📈 กลยุทธ์ EDCA สำหรับ {selected}")

# แยกค่าตัวเลขจาก entry_edca และ exit_target
edca_range = stock_data['entry_edca'].split('-')
edca_low = float(edca_range[0])
edca_high = float(edca_range[1])

exit_range = stock_data['exit_target'].split('-')
exit_low = float(exit_range[0])
exit_high = float(exit_range[1]) if len(exit_range) > 1 else exit_low + 2

# สร้างข้อมูลราคาจำลอง 90 วัน (3 เดือน)
days = np.arange(1, 91)

# จำลองราคาที่ขึ้นลงเป็นรอบ
trend = np.sin(days / 20) * 1.5  # คลื่นไซน์จำลองรอบ
base_price = (edca_low + edca_high) / 2
prices = base_price + trend + np.random.normal(0, 0.2, 90).cumsum() * 0.1

fig = go.Figure()

# เส้นราคา
fig.add_trace(go.Scatter(
    x=days,
    y=prices,
    mode='lines',
    name=selected,
    line=dict(color='orange', width=2)
))

# เพิ่มโซน EDCA (ซื้อ)
fig.add_hrect(
    y0=edca_low, y1=edca_high,
    line_width=0,
    fillcolor="green",
    opacity=0.2,
    annotation_text="โซน EDCA (ซื้อ)"
)

# เพิ่มโซนขาย
fig.add_hrect(
    y0=exit_low, y1=exit_high,
    line_width=0,
    fillcolor="red",
    opacity=0.2,
    annotation_text="โซนขาย"
)

fig.update_layout(
    title=f"จำลองกลยุทธ์ EDCA: ซื้อโซนเขียว ขายโซนแดง",
    xaxis_title="วัน",
    yaxis_title="ราคา",
    height=500,
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# แสดงจุดสังเกต
st.info(f"""
**กลยุทธ์ {selected}**
- ซื้อเมื่อลงมาโซน {stock_data['entry_edca']} บาท
- ขายทำกำไรเมื่อขึ้นไปโซน {stock_data['exit_target']} บาท
- ปันผลระหว่างทาง {stock_data['dividend']}
""")

st.markdown("---")

# ตารางเปรียบเทียบจุดซื้อ-ขาย
st.subheader("📊 สรุปจุดซื้อ-ขายรายตัว")

# สร้างตารางใหม่สำหรับแสดงผล
summary = df[["stock", "entry_edca", "exit_target", "dividend", "theme"]].copy()
summary.columns = ["หุ้น", "จุดซื้อ (EDCA)", "จุดขาย", "ปันผล", "ธีม"]

st.dataframe(summary, use_container_width=True, hide_index=True)

st.caption("📌 หมายเหตุ: กราฟเป็นเพียงการจำลองเพื่อแสดงแนวคิด EDCA")
