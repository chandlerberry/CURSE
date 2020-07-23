# script to fill the db with 100 students, 10 instructors, and an admin from excel spreadsheets
# author: Chandler Berry

import sqlite3, openpyxl

# db connection 
db = sqlite3.connect('CURSE.db')

# students
filePath = 'G:\\gitrepos\\CURSE\\students.xlsx'
s = openpyxl.load_workbook(filePath)
students = s.active
maxRow = students.max_row
maxCol = students.max_column
getStudent = []
print('-----\nSTUDENTS\n-----')
for i in range(1, maxRow + 1):
    getStudent = []
    for j in range(1, maxCol + 1):
        getCell = students.cell(row = i, column = j)
        getStudent.append(getCell.value)
    insertStudent = 'INSERT INTO Student VALUES (' + str(getStudent[0]) + ', \'' + getStudent[1] + '\', \'' + getStudent[2] + '\', ' + str(getStudent[3]) + ', \'' + getStudent[4] + '\', \'' + getStudent[5] + '\', \'' + getStudent[6] + '\');'
    c = db.cursor()
    c.execute(insertStudent)
    print(getStudent[1] + ' ' + getStudent[2] + ' added to database')
    c.close()
    db.commit()

# instructors
filePath = 'G:\\gitrepos\\CURSE\\instructors.xlsx'
ins = openpyxl.load_workbook(filePath)
instructors = ins.active
maxRow = instructors.max_row
maxCol = instructors.max_column
getInstructor = []
print('-----\nINSTRUCTORS\n-----')
for i in range(1, maxRow + 1):
    getInstructor = []
    for j in range(1, maxCol + 1):
        getCell = instructors.cell(row = i, column = j)
        getInstructor.append(getCell.value)
    insertInstructor = 'INSERT INTO Instructor VALUES (' + str(getInstructor[0]) + ', \'' + getInstructor[1] + '\', \'' + getInstructor[2] + '\', \'' + getInstructor[3] + '\', \'' + getInstructor[4] + '\', \'' + getInstructor[5] + '\', \'' + getInstructor[6] + '\');'
    c = db.cursor()
    c.execute(insertInstructor)
    print(getInstructor[1] + ' ' + getInstructor[2] + ' added to database')
    c.close()
    db.commit()

# admin
print('-----\nADMIN\n-----')
c = db.cursor()
c.execute('INSERT INTO Admin VALUES (30001, \'Darth\', \'Vader\', \'vaderd\', \'luke_daddy_100\');')
c.close()
print('Darth Vader added to database')
db.commit()

# courses
print('-----\nCOURSES\n-----')
filePath = 'G:\\gitrepos\\CURSE\\courses.xlsx'
course = openpyxl.load_workbook(filePath)
courses = course.active
maxRow = courses.max_row
maxCol = courses.max_column
getCourse = []
for i in range(1, maxRow + 1):
    getCourse = []
    for j in range(1, maxCol + 1):
        getCell = courses.cell(row = i, column = j)
        getCourse.append(getCell.value)
    insertInstructor = 'INSERT INTO Course VALUES (' + str(getCourse[0]) + ', \'' + getCourse[1] + '\', \'' + getCourse[2] + '\', \'' + getCourse[3] + '\', \'' + getCourse[4] + '\', \'' + getCourse[5] + '\', \'' + getCourse[6] + '\', \'' + str(getCourse[7]) + '\', \'' + str(getCourse[8]) + '\');'
    c = db.cursor()
    c.execute(insertInstructor)
    print(getCourse[1] + ' added to database')
    c.close()
    db.commit()


fuckthis = db.cursor()
fuckthis.execute('INSERT INTO Schedule_Mapping VALUES (31799, 10011)')
fuckthis.execute('INSERT INTO Schedule_Mapping VALUES (31406, 10011)')
fuckthis.execute('INSERT INTO Schedule_Mapping VALUES (31047, 10011)')
fuckthis.execute('INSERT INTO Schedule_Mapping VALUES (31044, 10011)')
fuckthis.execute('INSERT INTO Schedule_Mapping VALUES (31799, 10010)')
fuckthis.execute('INSERT INTO Schedule_Mapping VALUES (31799, 10001)')
fuckthis.execute('INSERT INTO Schedule_Mapping VALUES (31799, 10067)')
fuckthis.execute('INSERT INTO Schedule_Mapping VALUES (31799, 10035)')
fuckthis.execute('INSERT INTO Schedule_Mapping VALUES (31799, 10090)')
fuckthis.execute('INSERT INTO Schedule_Mapping VALUES (31799, 10023)')
fuckthis.close()
db.commit()

db.close()