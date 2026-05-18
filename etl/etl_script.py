import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# Kết nối database
engine = create_engine('postgresql://postgres:yourpassword@localhost:5432/student_bi')

# Đọc dữ liệu
mat = pd.read_csv('data/raw/student-mat.csv', sep=';')
por = pd.read_csv('data/raw/student-por.csv', sep=';')

# Hợp nhất dữ liệu
df = pd.concat([mat, por], ignore_index=True)

# Transform
df['AverageScore'] = (df['G1'] + df['G2'] + df['G3']) / 3.0
df['PassFlag'] = np.where(df['AverageScore'] >= 10, 1, 0)
df['AgeGroup'] = pd.cut(df['age'], bins=[0,16,18,22], labels=['<=16','17-18','19+'])

# Load vào Staging
df.to_sql('staging_student', engine, if_exists='replace', index=False)

print("ETL hoàn thành! Dữ liệu đã được load vào database.")
