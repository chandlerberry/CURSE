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

#adding values to student table 
c.execute('''INSERT INTO STUDENT VALUES(10001, 'Isaac', 'Newton', 1668, 'BSAS', 'newtoni', 'pass1');''') 
c.execute('''INSERT INTO STUDENT VALUES(10002, 'Marie', 'Curie', 1903, 'BSAS', 'curiem', 'pass2');''') 
c.execute('''INSERT INTO STUDENT VALUES(10003, 'Nikola', 'Tesla', 1878, 'BSEE', 'telsan', 'pass3');''') 
c.execute('''INSERT INTO STUDENT VALUES(10004, 'Thomas', 'Edison', 1879, 'BSEE', 'notcool', 'pass4');''') 
c.execute('''INSERT INTO STUDENT VALUES(10005, 'John', 'von Neumann', 1923, 'BSCO', 'vonneumannj', 'pass5');''') 
c.execute('''INSERT INTO STUDENT VALUES(10006, 'Grace', 'Hopper', 1928, 'BCOS', 'hopperg', 'pass6');''') 
c.execute('''INSERT INTO STUDENT VALUES(10007, 'Mae', 'Jemison', 1981, 'BSCH', 'jemisonm', 'pass7');''') 
c.execute('''INSERT INTO STUDENT VALUES(10008, 'Mark', 'Dean', 1979, 'BSCO', 'deanm', 'pass8');''') 
c.execute('''INSERT INTO STUDENT VALUES(10009, 'Michael', 'Faraday', 1812, 'BSAS', 'faradaym', 'pass9');''') 
c.execute('''INSERT INTO STUDENT VALUES(10010, 'Ada', 'Lovelace', 1832, 'BCOS', 'lovelacea', 'pass10');''') 

#adding values to instructor table
c.execute('''INSERT INTO INSTRUCTOR VALUES(20001, 'Joseph', 'Fourier', 'Full Prof.', 'BSEE', 'fourierj', 'word1');''') 
c.execute('''INSERT INTO INSTRUCTOR VALUES(20002, 'Nelson', 'Mandela', 'Full Prof.', 'HUSS', 'mandelan', 'word2');''') 
c.execute('''INSERT INTO INSTRUCTOR VALUES(20003, 'Galileo', 'Galilei', 'Full Prof.', 'BSAS', 'galileig', 'word3');''') 
c.execute('''INSERT INTO INSTRUCTOR VALUES(20004, 'Alan', 'Turing', 'Associate Prof.', 'BSCO', 'turinga', 'word4');''') 
c.execute('''INSERT INTO INSTRUCTOR VALUES(20005, 'Katie', 'Bouman', 'Assistant Prof.', 'BCOS', 'boumank', 'word5');''') 
c.execute('''INSERT INTO INSTRUCTOR VALUES(20006, 'Daniel', 'Bernoulli', 'Associate Prof.', 'BSME', 'bernoullid', 'word6');''') 

#adding value to admin table
c.execute('''INSERT INTO ADMIN VALUES(30001, 'Malala', 'Yousafzai', 'yousafzaim', 'password1');''') 

#adding values to course table
c.execute('''INSERT INTO COURSE VALUES(31799, 'Applied Programming Concepts','BSEE', 'Joseph Fourier', '9:30am-10:50am', 'TR', 'Summer', 2020, 4);''') 
c.execute('''INSERT INTO COURSE VALUES(31406, 'Signals and Systems', 'HUSS', 'Nelson Mandela', '10:00am-11:50am', 'MW', 'Summer', 2020, 4);''') 
c.execute('''INSERT INTO COURSE VALUES(31290, 'Computer Architecture', 'BSAS', 'Galileo Galilei', '9:30am-10:50am', 'TR', 'Summer', 2020, 4);''') 
c.execute('''INSERT INTO COURSE VALUES(31047, 'Advanced Digital Circuit Design', 'BSCO', 'Alan Turing', '8:00am-9:20am','WF', 'Summer', 2020, 4);''') 
c.execute('''INSERT INTO COURSE VALUES(31044, 'Computer Networks', 'BCOS', 'Katie Bouman', '8:00am-9:20am', 'TR', 'Summer', 2020, 4);''')

#testing the schedule mapping1
c.execute('''INSERT INTO Schedule_Mapping VALUES (31799, 10002)''')
c.execute('''INSERT INTO Schedule_Mapping VALUES (31799, 10003)''')
c.execute('''INSERT INTO Schedule_Mapping VALUES (31799, 10004)''')
c.execute('''INSERT INTO Schedule_Mapping VALUES (31799, 10005)''')
c.execute('''INSERT INTO Schedule_Mapping VALUES (31799, 10006)''')
c.execute('''INSERT INTO Schedule_Mapping VALUES (31799, 10007)''')

c.execute('''INSERT INTO Schedule_Mapping VALUES (31406, 10001)''')
c.execute('''INSERT INTO Schedule_Mapping VALUES (31406, 10010)''')
c.execute('''INSERT INTO Schedule_Mapping VALUES (31406, 10009)''')
c.execute('''INSERT INTO Schedule_Mapping VALUES (31406, 10008)''')
c.execute('''INSERT INTO Schedule_Mapping VALUES (31406, 10007)''')

c.execute('''INSERT INTO Schedule_Mapping VALUES (31290, 10001)''')
c.execute('''INSERT INTO Schedule_Mapping VALUES (31047, 10001)''')
c.execute('''INSERT INTO Schedule_Mapping VALUES (31044, 10001)''')

#printing student table
print('Student table:')
c.execute('''SELECT * FROM Student''')
query_result = c.fetchall()
  
for i in query_result:
	print(i)

#printing instructor table
print('Instructor table:')
c.execute('''SELECT * FROM Instructor''')
query_result = c.fetchall()
  
for i in query_result:
	print(i)

#printing admin table
print('Admin table:')
c.execute('''SELECT * FROM Admin''')
query_result = c.fetchall()
  
for i in query_result:
	print(i)

#printing course table    
print('Course table:')
c.execute('''SELECT * FROM Course''')
query_result = c.fetchall()
  
for i in query_result:
	print(i)
    
# Saving changes in the file
database.commit() 
c.close()
database.close()