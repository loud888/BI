import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# ====================== CONFIG ======================
engine = create_engine('postgresql://postgres:yourpassword@localhost:5432/student_bi')

# ====================== EXTRACT ======================
mat = pd.read_csv('data/raw/student-mat.csv', sep=';')
por = pd.read_csv('data/raw/student-por.csv', sep=';')

print("Math shape:", mat.shape)
print("Portuguese shape:", por.shape)

# ====================== TRANSFORM ======================
# Hợp nhất 2 bảng
df = pd.concat([mat, por], axis=0, ignore_index=True)

# Tạo các cột mới
df['AverageScore'] = (df['G1'] + df['G2'] + df['G3']) / 3
df['PassFlag'] = np.where(df['AverageScore'] >= 10, 1, 0)

df['AgeGroup'] = pd.cut(df['age'], bins=[0, 16, 18, 22], labels=['<=16', '17-18', '19+'])
df['ScoreLevel'] = pd.cut(df['AverageScore'], 
                          bins=[0, 8, 10, 12, 15, 20], 
                          labels=['Weak', 'Average', 'Good', 'Very Good', 'Excellent'])

# Thêm cột Subject
df['Subject'] = np.where(df.index < len(mat), 'Math', 'Portuguese')

# Chọn cột quan trọng
final_df = df[['school', 'sex', 'age', 'address', 'famsize', 'Pstatus', 'Medu', 'Fedu',
               'studytime', 'failures', 'absences', 'G1', 'G2', 'G3', 'AverageScore',
               'PassFlag', 'AgeGroup', 'ScoreLevel', 'Subject']]

# Load vào database
final_df.to_sql('staging_student_performance', engine, if_exists='replace', index=True, index_label='StudentKey')

print("✅ ETL hoàn thành! Dữ liệu đã load vào Staging table.")
