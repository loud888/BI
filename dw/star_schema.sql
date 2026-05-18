-- Tạo Database
CREATE DATABASE student_bi;
\c student_bi

-- ==================== DIMENSION TABLES ====================

CREATE TABLE Dim_Student (
    StudentKey SERIAL PRIMARY KEY,
    Gender VARCHAR(10),
    Age INT,
    AgeGroup VARCHAR(10),
    Address VARCHAR(20),
    FamilySize VARCHAR(10),
    ParentStatus VARCHAR(10),
    MotherEdu VARCHAR(30),
    FatherEdu VARCHAR(30),
    Internet VARCHAR(10)
);

CREATE TABLE Dim_Time (
    TimeKey SERIAL PRIMARY KEY,
    Semester VARCHAR(20),
    AcademicYear VARCHAR(20)
);

CREATE TABLE Dim_Course (
    CourseKey SERIAL PRIMARY KEY,
    Subject VARCHAR(20),        -- Math or Portuguese
    CourseName VARCHAR(50)
);

CREATE TABLE Dim_Class (
    ClassKey SERIAL PRIMARY KEY,
    School VARCHAR(10),
    ClassName VARCHAR(50)
);

-- ==================== FACT TABLE ====================

CREATE TABLE Fact_StudentGrades (
    FactID SERIAL PRIMARY KEY,
    StudentKey INT REFERENCES Dim_Student(StudentKey),
    TimeKey INT REFERENCES Dim_Time(TimeKey),
    CourseKey INT REFERENCES Dim_Course(CourseKey),
    ClassKey INT REFERENCES Dim_Class(ClassKey),
    
    G1 DECIMAL(4,2),
    G2 DECIMAL(4,2),
    G3 DECIMAL(4,2),
    AverageScore DECIMAL(4,2),
    Absences INT,
    Failures INT,
    PassFlag INT CHECK (PassFlag IN (0,1))
);

-- Index
CREATE INDEX idx_student ON Fact_StudentGrades(StudentKey);
CREATE INDEX idx_time ON Fact_StudentGrades(TimeKey);
