import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.set_page_config(page_title="BI Sinh Viên", layout="wide")
st.title("📊 HỆ THỐNG BI - PHÂN TÍCH DỮ LIỆU SINH VIÊN")

# ==================== KẾT NỐI DATABASE ====================
engine = create_engine('postgresql://postgres:yourpassword@localhost:5432/student_bi')
# ←←← THAY "yourpassword" bằng mật khẩu PostgreSQL của bạn

# Load dữ liệu từ Staging (hoặc Fact nếu đã có)
df = pd.read_sql("SELECT * FROM staging_student_performance LIMIT 1000", engine)

# Tính Average Score
df['AverageScore'] = (df['G1'] + df['G2'] + df['G3']) / 3

st.success(f"✅ Kết nối Database thành công! Tổng sinh viên: **{len(df)}**")

# ==================== DASHBOARD ====================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Tổng sinh viên", len(df))
col2.metric("Điểm trung bình", f"{df['AverageScore'].mean():.2f}")
col3.metric("Tỷ lệ Pass", f"{(df['AverageScore'] >= 10).mean()*100:.1f}%")
col4.metric("Tỷ lệ Fail", f"{(df['AverageScore'] < 10).mean()*100:.1f}%")

st.subheader("📈 Điểm trung bình theo Giới tính")
st.bar_chart(df.groupby('sex')['AverageScore'].mean())

st.subheader("📍 Điểm trung bình theo Khu vực")
st.bar_chart(df.groupby('address')['AverageScore'].mean())

st.subheader("⏰ Điểm theo Thời gian học thêm")
st.bar_chart(df.groupby('studytime')['AverageScore'].mean())

st.subheader("Dữ liệu mẫu")
st.dataframe(df.head(10))
