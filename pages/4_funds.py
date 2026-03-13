import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(layout="wide")

st.title("📦 กองทุนรวม")
st.markdown("""
**กลยุทธ์ลงทุนในกองทุนรวม**  
- **DCA รายเดือน:** SCB, RSP500, RMNDQ100, RMF  
- **EDCA ตามจังหวะ:** KKP, GEQ, SCBSEMI, SCBGQUAL
""")

# โหลดข้อมูล
@st.cache_data
def load_funds():
    return pd.read_csv("data/funds.csv")

df = load_funds()

# แยกประเภทกองทุน
dca_funds = df[df["strategy"] == "DCA รายเดือน"]
edca_funds = df[df["strategy"] == "EDCA"]

# แสดงตารางรวม
st.subheader("📋 ข้อมูลกองทุนทั้งหมด")
st.dataframe(
    df,
    column_config={
        "fund": "กองทุน",
        "strategy": "กลยุทธ์",
        "note": "หมายเหตุ"
    },
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# แสดงสถิติ
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("กองทุน DCA รายเดือน", f"{len(dca_funds)} กอง")

with col2:
    st.metric("กองทุน EDCA", f"{len(edca_funds)} กอง")

with col3:
    st.metric("กลยุทธ์หลัก", "DCA + EDCA")

st.markdown("---")

# ส่วน DCA รายเดือน
st.subheader("📅 กองทุน DCA รายเดือน")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **หลักการ DCA รายเดือน:**
    - ลงทุนเท่ากันทุกเดือน
    - ไม่สนจังหวะตลาด
    - เหมาะกับกองทุนแกนหลัก
    """)

with col2:
    # จำลองผล DCA
    months = np.arange(1, 13)
    investment_per_month = 2500
    cumulative = investment_per_month * months
    # จำลองผลตอบแทนสมมติ 8% ต่อปี
    returns = cumulative * (1 + 0.08/12) ** months

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=months,
        y=cumulative,
        mode='lines',
        name='เงินลงทุน',
        line=dict(color='blue')
    ))
    fig.add_trace(go.Scatter(
        x=months,
        y=returns,
        mode='lines',
        name='มูลค่ายกตัวอย่าง 8%',
        line=dict(color='green', dash='dash')
    ))
    fig.update_layout(
        title="จำลอง DCA รายเดือน 2,500 บาท",
        xaxis_title="เดือน",
        yaxis_title="บาท",
        height=300
    )
    st.plotly_chart(fig, use_container_width=True)

# แสดงตาราง DCA Funds
st.subheader("📊 กองทุน DCA แนะนำ")
dca_display = dca_funds[["fund", "note"]].copy()
dca_display.columns = ["กองทุน", "รายละเอียด"]
st.dataframe(dca_display, use_container_width=True, hide_index=True)

st.markdown("---")

# ส่วน EDCA
st.subheader("⏱️ กองทุน EDCA (ตามจังหวะ)")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **หลักการ EDCA:**
    - รอจังหวะตลาดย่อตัว
    - ซื้อเมื่อถูก ขายเมื่อกำไร
    - เหมาะกับกองทุนธีมเฉพาะ
    """)

with col2:
    # จำลอง EDCA
    days = np.arange(1, 91)
    prices = 100 + np.sin(days / 20) * 15 + np.random.normal(0, 2, 90)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=days,
        y=prices,
        mode='lines',
        name='ราคาจำลอง',
        line=dict(color='orange')
    ))
    
    # เพิ่มโซนซื้อ (ต่ำกว่า 90)
    fig.add_hrect(
        y0=70, y1=90,
        fillcolor="green",
        opacity=0.2,
        line_width=0,
        annotation_text="โซน EDCA"
    )
    
    fig.update_layout(
        title="จำลองจังหวะ EDCA: ซื้อเมื่อลง",
        xaxis_title="วัน",
        yaxis_title="ราคา",
        height=300
    )
    st.plotly_chart(fig, use_container_width=True)

# แสดงตาราง EDCA Funds
st.subheader("📊 กองทุน EDCA แนะนำ")
edca_display = edca_funds[["fund", "note"]].copy()
edca_display.columns = ["กองทุน", "รายละเอียด"]
st.dataframe(edca_display, use_container_width=True, hide_index=True)

st.markdown("---")

# ส่วนวางแผนการลงทุน
st.subheader("💰 ตัวอย่างการจัดสรรเงินรายเดือน")

# ตัวเลื่อนปรับเงินลงทุน
monthly_investment = st.slider(
    "เงินลงทุนต่อเดือน (บาท)",
    min_value=5000,
    max_value=50000,
    value=20000,
    step=1000
)

# คำนวณสัดส่วน
dca_amount = int(monthly_investment * 0.7)  # 70% สำหรับ DCA
edca_amount = monthly_investment - dca_amount  # 30% เก็บรอ EDCA

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("รวมต่อเดือน", f"{monthly_investment:,.0f} บาท")

with col2:
    st.metric("DCA รายเดือน (70%)", f"{dca_amount:,.0f} บาท")

with col3:
    st.metric("เก็บรอ EDCA (30%)", f"{edca_amount:,.0f} บาท")

st.info("""
💡 **คำแนะนำ:**
- แบ่งเงิน DCA รายเดือนออกเป็น 4 กองทุนหลัก (SCB, RSP500, RMNDQ100, RMF)
- เงิน EDCA เก็บไว้ในบัญชี รอจังหวะตลาดย่อตัว
""")

st.markdown("---")
st.caption("📌 หมายเหตุ: กราฟเป็นเพียงการจำลองเพื่อแสดงแนวคิด")
