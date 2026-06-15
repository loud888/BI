# Hệ thống BI Phân tích Dữ liệu Sinh viên

## Giới thiệu
Hệ thống Business Intelligence giúp phân tích kết quả học tập của sinh viên dựa trên dataset UCI. Đề tài bao gồm ETL, thiết kế Data Warehouse và trực quan hóa dữ liệu.

## Công nghệ sử dụng
- Database: PostgreSQL
- ETL: Python (pandas + SQLAlchemy)
- Dashboard: HTML + Chart.js
- Công cụ quản lý: DBeaver

## Cấu trúc dự án
- `data/raw/` : Chứa 2 file CSV gốc
- `etl/` : Script ETL
- `dw/` : Script tạo Star Schema
- `dashboard.html` : Dashboard trực quan

## Hướng dẫn chạy
```bash
git clone https://github.com/loud888/BI.git
cd BI
python3 etl/etl_script.py
