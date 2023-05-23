CREATE DATABASE IF NOT EXISTS pyUniversity;
USE pyuniversity;

CREATE TABLE IF NOT EXISTS Students(
    id INT PRIMARY KEY AUTO_INCREMENT,
    member_property VARCHAR(12) DEFAULT 'Student',
    first_name VARCHAR(20),
    last_name VARCHAR(20),
    fathers_name VARCHAR(20),
    mothers_name VARCHAR(20),
    birth_date DATE,
    country VARCHAR(20) DEFAULT 'Greece',
    city VARCHAR(20) CHECK (LENGTH(city)>=4),
    email VARCHAR(40) UNIQUE CHECK (LENGTH(email)>=4),
    register_date DATETIME DEFAULT NOW(),
    update_state_date DATETIME DEFAULT NOW(),
    save_state_date DATETIME DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS Subjects(
   id INT PRIMARY KEY AUTO_INCREMENT,
   subject_name VARCHAR(30) UNIQUE NOT NULL CHECK (LENGTH(subject_name)>=5),
   professor_fullname VARCHAR(31) CHECK (LENGTH(professor_fullname)>=9),
   lesson_type TINYINT -- 0 means optional and 1 means obligatory
);


CREATE TABLE IF NOT EXISTS grades(
    student_id INT,
    subject_id INT,
    CONSTRAINT stud_grades_id FOREIGN KEY (student_id) REFERENCES Students(id) ON DELETE CASCADE,
    CONSTRAINT subj_grades_id FOREIGN KEY (subject_id) REFERENCES Subjects(id) ON DELETE CASCADE,
    grade DECIMAL(4,2) DEFAULT NULL,
    modified_grade_date DATE DEFAULT NULL
);




  -- DROP TABLE IF EXISTS grades;
  -- DROP TABLE IF EXISTS Subjects;
  -- DROP TABLE Students;
