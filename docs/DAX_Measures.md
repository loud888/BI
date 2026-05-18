# DAX Measures - Power BI

## KPI Cards
Total Students = COUNTROWS(Dim_Student)
Average Score = AVERAGE(Fact_StudentGrades[AverageScore])
Pass Rate = DIVIDE(CALCULATE(COUNTROWS(Fact_StudentGrades), Fact_StudentGrades[PassFlag]=1), [Total Students])
Fail Rate = 1 - [Pass Rate]

## Phân tích
Avg Score by Gender = CALCULATE([Average Score], ALLEXCEPT(Dim_Student, Dim_Student[Gender]))
Pass Rate Urban = CALCULATE([Pass Rate], Dim_Student[Address] = "U")
Avg Score by Parent Education = CALCULATE([Average Score], ALLEXCEPT(Dim_Student, Dim_Student[MotherEdu]))

## Top & Bottom
Top 10 Students Score = TOPN(10, Dim_Student, [Average Score], DESC)
