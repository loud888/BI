-- Tạo Database
CREATE DATABASE student_bi;
\c student_bi

-- ==================== DIMENSION TABLES ====================

CREATE TABLE Dim_Student (
    StudentKey SERIAL PRIMARY KEY,
    Gender VARCHAR(10),
    Age INT,
    AgeGroup VARCHAR(10),
    Address VARCHAR(20),           -- U = Urban, R = Rural
    FamilySize VARCHAR(10),
    ParentStatus VARCHAR(10),
    MotherEdu INT,
    FatherEdu INT,
    StudyTime INT
);

CREATE TABLE Dim_Course (
    CourseKey SERIAL PRIMARY KEY,
    Subject VARCHAR(20),           -- Math or Portuguese
    CourseName VARCHAR(50)
);

CREATE TABLE Dim_Time (
    TimeKey SERIAL PRIMARY KEY,
    Semester VARCHAR(20)
);

-- Fact Table
CREATE TABLE Fact_StudentGrades (
    FactID SERIAL PRIMARY KEY,
    StudentKey INT REFERENCES Dim_Student(StudentKey),
    CourseKey INT REFERENCES Dim_Course(CourseKey),
    TimeKey INT REFERENCES Dim_Time(TimeKey),
    
    G1 DECIMAL(4,2),
    G2 DECIMAL(4,2),
    G3 DECIMAL(4,2),
    AverageScore DECIMAL(4,2),
    Absences INT,
    Failures INT,
    PassFlag INT
);
-- Index
CREATE INDEX idx_student ON Fact_StudentGrades(StudentKey);
CREATE INDEX idx_time ON Fact_StudentGrades(TimeKey);
