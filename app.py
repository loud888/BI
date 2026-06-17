import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine

# ==================== 1. CẤU HÌNH HỆ THỐNG (UI/UX) ====================
st.set_page_config(
    page_title="Hệ thống BI Phân tích Học tập Sinh viên",
    layout="wide",
    page_icon="🎓",
    initial_sidebar_state="expanded"
)

# Khởi tạo CSS tùy chỉnh để giao diện "sạch" và chuyên nghiệp hơn
st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    div[data-testid="stMetricValue"] {font-size: 28px; font-weight: 700; color: #1E3A8A;}
    div[data-testid="stMetricLabel"] {font-size: 14px; font-weight: 600; color: #4B5563;}
    .reportview-container .main .block-container{padding-top: 2rem;}
    </style>
""", unsafe_allow_html=True)

# ==================== 2. KẾT NỐI & XỬ LÝ DỮ LIỆU (ETL nhẹ) ====================
@st.cache_data(ttl=600) # Cache dữ liệu 10 phút để tối ưu hiệu năng
def load_data():
    try:
        engine = create_engine('postgresql://postgres:123@localhost:5432/student_bi')
        # Đọc dữ liệu gốc từ DB
        df = pd.read_sql("SELECT * FROM staging_student_performance", engine)
        
        # Tạo dữ liệu chuẩn hóa cho Khoa/Học kỳ theo yêu cầu bài toán BI chuyên sâu
        if 'department' not in df.columns:
            df['department'] = df['address'].map({'U': 'Công nghệ thông tin', 'R': 'Kinh tế số'})
        if 'semester' not in df.columns:
            df['semester'] = df['studytime'].map({1: 'Học kỳ I', 2: 'Học kỳ II', 3: 'Học kỳ I', 4: 'Học kỳ II'})
            
        # Tính toán các chỉ số nghiệp vụ (Business Metrics)
        df['AverageScore'] = (df['G1'] + df['G2'] + df['G3']) / 3.0
        df['Status'] = df['AverageScore'].apply(lambda x: 'Pass' if x >= 10 else 'Fail')
        return df
    except Exception as e:
        # Cơ chế dự phòng khi mất kết nối DB đột ngột
        st.error(f"Lỗi kết nối cơ sở dữ liệu: {e}. Vui lòng kiểm tra lại PostgreSQL.")
        return pd.DataFrame()

df_raw = load_data()

if df_raw.empty:
    st.warning("Ứng dụng tạm thời dừng do không thể truy vấn dữ liệu từ PostgreSQL.")
    st.stop()

# ==================== 3. THANH BỘ LỌC (SIDEBAR) ====================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3449/3449614.png", width=80)
    st.title("BỘ LỌC DỮ LIỆU")
    st.caption("Hệ thống quản trị và hỗ trợ quyết định v1.0")
    st.divider()
    
    # Bộ lọc động lấy trực tiếp từ trường dữ liệu của DB
    list_departments = ["Tất cả"] + list(df_raw['department'].unique())
    selected_dept = st.selectbox("Chọn Khoa / Khối ngành", list_departments)
    
    list_semesters = ["Tất cả"] + list(df_raw['semester'].unique())
    selected_sem = st.selectbox("Học kỳ", list_semesters)
    
    list_gender = ["Tất cả", "Nam (M)", "Nữ (F)"]
    selected_gender = st.selectbox("Giới tính", list_gender)

# Áp dụng bộ lọc động vào tập dữ liệu hiện hành
df = df_raw.copy()
if selected_dept != "Tất cả":
    df = df[df['department'] == selected_dept]
if selected_sem != "Tất cả":
    df = df[df['semester'] == selected_sem]
if selected_gender != "Tất cả":
    gender_code = 'M' if "Nam" in selected_gender else 'F'
    df = df[df['sex'] == gender_code]

# ==================== 4. TIÊU ĐỀ CHÍNH ====================
st.title("🎓 EXECUTIVE DASHBOARD - HỆ THỐNG BI SINH VIÊN")
st.caption(f"Dữ liệu được khai thác từ Kho dữ liệu (Data Warehouse) | Đang hiển thị: **{len(df):,}** / **{len(df_raw):,}** hồ sơ sinh viên.")
st.divider()

# ==================== 5. KHU VỰC KPI CHỦ CHỐT ====================
total_students = len(df)
avg_score = df['AverageScore'].mean() if total_students > 0 else 0
pass_rate = (df['Status'] == 'Pass').mean() * 100 if total_students > 0 else 0
fail_rate = 100 - pass_rate if total_students > 0 else 0

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric(label="TỔNG SỐ SINH VIÊN", value=f"{total_students:,} SV")
with kpi2:
    st.metric(label="ĐIỂM TRUNG BÌNH (GPA)", value=f"{avg_score:.2f} / 20")
with kpi3:
    st.metric(label="TỶ LỆ ĐẠT (PASS RATE)", value=f"{pass_rate:.1f}%")
with kpi4:
    st.metric(label="TỶ LỆ TRƯỢT MÔN", value=f"{fail_rate:.1f}%")

st.write("") 

# ==================== 6. PHÂN TÍCH CHUYÊN SÂU (TABS) ====================
tab_overview, tab_demographics, tab_behavior = st.tabs([
    "📈 TỔNG QUAN KẾT QUẢ", 
    "👥 PHÂN TÍCH THEO PHÂN KHÚC", 
    "📊 PHÂN TÍCH HÀNH VI & ĐIỂM SỐ"
])

# --- TAB 1: TỔNG QUAN ---
with tab_overview:
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("📊 Điểm trung bình theo Khoa & Học kỳ")
        df_dept_sem = df.groupby(['department', 'semester'])['AverageScore'].mean().reset_index()
        fig1 = px.bar(
            df_dept_sem, 
            x='department', 
            y='AverageScore', 
            color='semester',
            barmode='group',
            labels={'department': 'Khoa', 'AverageScore': 'Điểm TB'},
            color_discrete_sequence=px.colors.qualitative.Plotly
        )
        fig1.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=350)
        st.plotly_chart(fig1, use_container_width=True)
        
    with col_chart2:
        st.subheader("📉 Cơ cấu Tỷ lệ Đạt / Trượt môn")
        status_counts = df['Status'].value_counts().reset_index()
        fig2 = px.pie(
            status_counts, 
            values='count', 
            names='Status',
            hole=0.4,
            color='Status',
            color_discrete_map={'Pass': '#10B981', 'Fail': '#EF4444'}
        )
        fig2.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=350)
        st.plotly_chart(fig2, use_container_width=True)

# --- TAB 2: ĐẶC ĐIỂM NHÂN KHẨU HỌC ---
with tab_demographics:
    col_demo1, col_demo2 = st.columns(2)
    
    with col_demo1:
        st.subheader("⚖️ So sánh Biến thiên Điểm số theo Giới tính")
        fig_sex = px.box(
            df, 
            x='sex', 
            y='AverageScore', 
            points="all",
            labels={'sex': 'Giới tính (F: Nữ, M: Nam)', 'AverageScore': 'Phân bổ điểm'},
            color='sex',
            color_discrete_sequence=['#EC4899', '#3B82F6']
        )
        st.plotly_chart(fig_sex, use_container_width=True)
        
    with col_demo2:
        st.subheader("📍 Phân bổ Điểm theo Khu vực cư trú")
        df_address = df.groupby('address')['AverageScore'].mean().reset_index()
        df_address['address'] = df_address['address'].map({'U': 'Thành thị (Urban)', 'R': 'Nông thôn (Rural)'})
        fig_addr = px.bar(
            df_address, 
            x='address', 
            y='AverageScore',
            color='address',
            text_auto='.2f',
            color_discrete_sequence=['#475569', '#94A3B8']
        )
        st.plotly_chart(fig_addr, use_container_width=True)

# --- TAB 3: HÀNH VI HỌC TẬP ---
with tab_behavior:
    st.subheader("🕵️ Phân tích tương quan đa chiều")
    col_beh1, col_beh2 = st.columns([6, 4])
    
    with col_beh1:
        fig_scatter = px.scatter(
            df, 
            x='absences', 
            y='AverageScore', 
            color='Status',
            size='studytime',
            labels={'absences': 'Số buổi vắng học', 'AverageScore': 'Điểm số trung bình'},
            title="Mối quan hệ giữa Tỷ lệ vắng - Thời gian tự học - Kết quả cuối kỳ",
            color_discrete_map={'Pass': '#10B981', 'Fail': '#EF4444'}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    with col_beh2:
        st.markdown("#### 💡 THÔNG TIN BIẾN ĐỘNG (DYNAMIC INSIGHTS)")
        
        if total_students > 0:
            # Thuật toán tính toán Insight tự động dựa trên tập dữ liệu đã lọc
            high_absence_fail = df[df['absences'] > 10]['Status'].value_counts(normalize=True).get('Fail', 0) * 100
            avg_study_high = df[df['studytime'] >= 3]['AverageScore'].mean()
            avg_study_low = df[df['studytime'] < 3]['AverageScore'].mean()
            diff_study = avg_study_high - avg_study_low if (pd.notna(avg_study_high) and pd.notna(avg_study_low)) else 0
            
            st.info(f"📌 **Rủi ro chuyên cần:** Nhóm sinh viên nghỉ **trên 10 buổi** hiện có tỷ lệ trượt môn lên tới **{high_absence_fail:.1f}%**. Khuyến nghị Khoa tăng cường nhắc nhở quản lý.")
            st.success(f"📌 **Tác động tự học:** Sinh viên duy trì tự học $\ge$ 3 giờ/tuần ghi nhận mức điểm trung bình **cao hơn {diff_study:.1f} điểm** so với nhóm còn lại.")
        else:
            st.write("Không tìm thấy dữ liệu khả dụng cho phân khúc bộ lọc này.")

st.divider()

# ==================== 7. TRUY XUẤT DỮ LIỆU CHI TIẾT (DRILL-DOWN) ====================
st.subheader("📋 Kiểm toán Dữ liệu Chi tiết (Granular Data)")
with st.expander("Nhấp để hiển thị danh sách chi tiết"):
    all_columns = df.columns.tolist()
    selected_cols = st.multiselect("Tùy chỉnh cấu trúc cột hiển thị", all_columns, default=['sex', 'address', 'studytime', 'absences', 'AverageScore', 'Status'])
    
    st.dataframe(
        df[selected_cols].sort_values(by='AverageScore', ascending=False), 
        use_container_width=True
    )

# Chân trang hệ thống doanh nghiệp
st.caption("🔒 Hệ thống thông tin quản trị nội bộ | Trường Đại học • Trung tâm Phân tích dữ liệu & BI")
