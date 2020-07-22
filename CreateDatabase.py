import sqlite3

database = sqlite3.connect('CURSE.db')
c = database.cursor()

c.execute('DROP TABLE IF EXISTS Student')
c.execute('DROP TABLE IF EXISTS Instructor')
c.execute('DROP TABLE IF EXISTS Admin')
c.execute('DROP TABLE IF EXISTS Course')
c.execute('DROP TABLE IF EXISTS Schedule_Mapping')

createStudentTable = '''
CREATE TABLE Student (  
    ID 			INT 	    PRIMARY KEY NOT NULL,
    FirstName	TEXT	    NOT NULL,
    LastName	TEXT 	    NOT NULL,
    GradYear	INT 	    NOT NULL,
    Major		CHAR(4)     NOT NULL,
    Email		TEXT	    NOT NULL,
    Password    TEXT        NOT NULL
);
'''
c.execute(createStudentTable)

createInstructorTable = '''
CREATE TABLE Instructor (
    ID          INT         PRIMARY KEY NOT NULL,
    FirstName   TEXT        NOT NULL,
    LastName    TEXT        NOT NULL,
    Title       TEXT        NOT NULL,
    Department  CHAR(4)     NOT NULL,
    Email       TEXT        NOT NULL,
    Password    TEXT        NOT NULL
);
'''
c.execute(createInstructorTable)

createAdminTable = '''
CREATE TABLE Admin (
    ID          INT         PRIMARY KEY NOT NULL,
    FirstName   TEXT        NOT NULL,
    LastName    TEXT        NOT NULL,
    Email       TEXT        NOT NULL,
    Password    TEXT        NOT NULL
);
'''
c.execute(createAdminTable)

createCourseTable = '''
CREATE TABLE Course (
    CRN         INT         PRIMARY KEY NOT NULL,
    Title       TEXT        NOT NULL,
    Department  CHAR(4)     NOT NULL,
    Instructor  TEXT        NOT NULL,
    Times       TEXT        NOT NULL,
    DaysOfWeek  TEXT        NOT NULL,
    Semester    TEXT        NOT NULL,
    Year        TEXT        NOT NULL,
    Credits     TEXT        NOT NULL
);
'''
c.execute(createCourseTable)

createSchedMappingTable = '''
CREATE TABLE Schedule_Mapping (
    CourseID    INT     REFERENCES Course (ID),
    StudentID   INT     REFERENCES Student (ID)
);
'''
c.execute(createSchedMappingTable)

# Saving changes in the file
database.commit() 
c.close()
database.close()

print('created CURSE db')