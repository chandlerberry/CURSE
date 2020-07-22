import sqlite3
import sys

database = sqlite3.connect('CURSE.db')

# base class User
class User:

    # constructor
    def __init__(self, firstName, lastName, ID):
        self.firstName = firstName
        self.lastName = lastName
        self.ID = ID

    # author: Naomi Torre
    # search all courses function
    def searchAllCourses(self):
        print("\nHere are all the courses: \n")
        c = database.cursor()
        c.execute("""SELECT * from Course """)
        qr = c.fetchall()
        c.close()
        for i in qr:
            print(i)

    # author: Naomi Torre
    # search courses with parameters
    def searchCoursesByParam(self):
        print("Here are the parameters to search by: \n1 to search by semester \n2 to search title \n3 to search by CRN \n4 to search by department \n5 to search by instructor \n6 to search by time \n7 to search by days \n8 to search by credits")
        choice = input("Enter number that corresponds to parameter of choice: ")
        
        if choice == '1':
            term = input("\nEnter the semester in which you would like to search courses for: ")
            yr = input("\nEnter the year of the semester: ")
            c = database.cursor()
            c.execute("""SELECT * from Course WHERE Semester = '""" + term + """' AND Year = '""" + yr + """';""")
            qr = c.fetchall()
            c.close()
            
            print("\nHere are all the courses in " + term + " " + yr + ":\n")
            for i in qr:
                print(i)
        
        elif choice == '2':
            title = input("Enter title to search by: ")
            c = database.cursor()
            c.execute("""SELECT * from Course WHERE Title = '""" + title + """';""")
            qr = c.fetchall()
            c.close()
            
            print("\nHere are all the courses titled " + title + ":\n")
            for i in qr:
                print(i)
        
        elif choice == '3':
            crn = input("Enter CRN to search by: ")
            c = database.cursor()
            c.execute("""SELECT * from Course WHERE CRN = '""" + crn + """';""")
            qr = c.fetchall()
            c.close()
            
            print("\nHere are all the courses with " + crn + " as a CRN:\n")
            for i in qr:
                print(i)
            
        elif choice == '4':
            department = input("Enter department to search by: ")
            c = database.cursor()
            c.execute("""SELECT * from Course WHERE Department = '""" + department + """';""")
            qr = c.fetchall()
            c.close()
            
            print("\nHere are all the courses in the department " + department + ":\n")
            for i in qr:
                print(i)
            
        elif choice == '5':
            instructor = input("Enter instructor to search by: ")
            c = database.cursor()
            c.execute("""SELECT * from Course WHERE Instructor = '""" + instructor + """';""")
            qr = c.fetchall()
            c.close()

            print("\nHere are all the courses taught by " + instructor + ":\n")
            for i in qr:
                print(i)
            
        elif choice == '6':
            time = input("Enter time to search by: ")
            c = database.cursor()
            c.execute("""SELECT * from Course WHERE Times = '""" + time + """';""")
            qr = c.fetchall()
            c.close()
            
            print("\nHere are all the courses taught at  " + time + ":\n")
            for i in qr:
                print(i)
            
        elif choice == '7':
            days = input("Enter days to search by: ")
            c = database.cursor()
            c.execute("""SELECT * from Course WHERE DaysOfWeek = '""" + days + """';""")
            qr = c.fetchall()
            c.close()
            
            print("\nHere are all the courses taught on " + days + ":\n")
            for i in qr:
                print(i)
        
        elif choice == '8':
            creds = input("Enter number of credits to search by: ")
            c = database.cursor()
            c.execute("""SELECT * from Course WHERE Credits = '""" + creds + """';""")
            qr = c.fetchall()
            c.close()
            
            print("\nHere are all the courses with " + creds + " credits: \n")
            for i in qr:
                print(i)
        else: 
            print('invalid choice! \n Please try again.')
            self.searchCoursesByParam()

    # author: Naomi Torre
    # search courses function           
    def searchCourses(self):
        num = input("\nEnter 1 to search all courses or 2 to search with parameters: ")
        if num == '1':
            self.searchAllCourses()
        elif num == '2':
            self.searchCoursesByParam()
        else:
            print("invalid choice! \n Please try again.")
            self.searchCourses()

    # returns a list of schedule conflict notifications to the user, if any are found
    # author: Chandler Berry
    def checkConflicts(self, studentID, courseID):
        # get year and semester info
        year = input('Enter Year: ')
        semester = input('Enter Semester: ')

        # queries
        getCourse = 'SELECT Title, Times, DaysOfWeek FROM Course WHERE CRN = ' + str(courseID) + ' AND Year = \'' + str(year) + '\' AND Semester = \'' + str(semester) + '\''
        getSched = 'SELECT Course.Title, Course.Times, Course.DaysOfWeek FROM Course INNER JOIN Schedule_Mapping ON Schedule_Mapping.CourseID = Course.CRN WHERE Schedule_Mapping.StudentID = ' + str(studentID) + ' AND Course.Year = \'' + str(year) + '\' AND Course.Semester = \'' + str(semester) + '\''
        
        # get info of course being compared
        c = database.cursor()
        c.execute(getCourse)
        newCourse = c.fetchone()
        c.close()

        # split string values of time and day info for the new course
        newCourseTimes = newCourse[1].split('-')
        newCourseDays = list(newCourse[2])

        # get course start and end times into an int format to be compared with the student's existing schedule
        unwantedChars = [':', 'a', 'm', 'p']
        for c in unwantedChars:
            newCourseTimes[0] = newCourseTimes[0].replace(c, '')
            newCourseTimes[1] = newCourseTimes[1].replace(c, '')
        newCourseTimes[0] = int(newCourseTimes[0])
        newCourseTimes[1] = int(newCourseTimes[1])

        # get student schedule to compare
        c = database.cursor()
        c.execute(getSched)
        sched = c.fetchall()
        c.close()

        # empty list of conflicts that will be filled with strings if any conflicts are found
        conflictList = []

        # iterate through each course in the student's existing schedule
        for course in sched:
            # split string values of time and day info for each course in the student's existing schedule
            times = course[1].split('-')
            days = list(course[2])

            # get each course's start and end time in int format
            for c in unwantedChars:
                times[0] = times[0].replace(c, '')
                times[1] = times[1].replace(c, '')
            times[0] = int(times[0])
            times[1] = int(times[1])

            # compare new course info with course in existing student schedule, return true/false if conflict is found/not found
            for day in days:
                for newDay in newCourseDays:
                    # if date matches, compare times
                    if day == newDay:
                        #   start times match                  end times match                    starts in the middle of other class                                ends in the middle of other class
                        if (newCourseTimes[0] == times[0]) or (newCourseTimes[1] == times[1]) or (newCourseTimes[0] > times[0] and newCourseTimes[0] < times[1]) or (newCourseTimes[1] > times[0] and newCourseTimes[1] < times[1]):
                            conflict = 'CONFLICT FOUND WITH COURSE ' + course[0] + ' ON DAY: ' + day
                            conflictList.append(conflict)
                        else:
                            continue
                    else:
                        continue

        return conflictList

# class Student derived from User
class Student(User):

    # constructor
    def __init__(self, firstName, lastName, ID):
        super().__init__(firstName, lastName, ID)
        print('Student {} {} [{}] created'.format(self.firstName, self.lastName, self.ID))

    # add courses to student schedule
    # author: Chandler Berry
    def addCourse(self, studentID):
        # prompt user to enter CRN
        getCRN = input('Enter CRN of course you want to add: ')
        # check if student is already in the class they are trying to add
        c = database.cursor()
        checkSchedMapping = 'SELECT StudentID FROM Schedule_Mapping WHERE StudentID = ' + str(studentID) + ' AND CourseID = ' + str(getCRN)
        c.execute(checkSchedMapping)
        result = c.fetchone()
        c.close()
        if not result:
            # determine if course being registered does not conflict with the rest of the student's schedule
            conflicts = self.checkConflicts(studentID, getCRN)
            # if no conflict(s) found, add the course
            if len(conflicts) == 0:
                # add new tuple to the db that indicates that the student is now registered for this course
                addTuple = 'INSERT INTO Schedule_Mapping VALUES (' + str(getCRN) + ', ' + str(studentID) + ')'
                c = database.cursor()
                c.execute(addTuple)
                c.close()
                database.commit()
            # if conflict(s) are found, print them to the user
            else:
                print(*conflicts, sep = '\n')
            print('The course has been added to your schedule.')
        else:
            if result[0] == studentID:
                print('You are already registered in this course.')
            else:
                pass

    # remove courses from student schedule
    # author: Chandler Berry
    def rmCourse(self, studentID):
        # prompt user to enter CRN
        getCRN = input('Enter CRN of course you want to remove: ')
        # check if student is actually in the class they are trying to remove
        c = database.cursor()
        checkSchedMapping = 'SELECT StudentID FROM Schedule_Mapping WHERE StudentID = ' + str(studentID) + ' AND CourseID = ' + str(getCRN)
        c.execute(checkSchedMapping)
        result = c.fetchone()
        c.close()
        if not result:
            print('You are not registered in this course.')
        else:
            if result[0] == studentID:
                # remove the tuple from the db that indicates this student is registered in this course
                deleteTuple = 'DELETE FROM Schedule_Mapping WHERE StudentID = ' + str(studentID) + ' AND CourseID = ' + str(getCRN)
                c = database.cursor()
                c.execute(deleteTuple)
                c.close()
                database.commit()
                print('The course has been removed from your schedule.')
            else:
                pass

    # print student's schedule provided with the year and semester
    # author: Chandler Berry
    def printSched(self, studentID):
        getYear = input('Enter Year: ')
        getSemester = input('Enter Semester: ')
        checkSchedMapping = 'SELECT Course.Title, Course.Times, Course.DaysOfWeek FROM Course INNER JOIN Schedule_Mapping ON Schedule_Mapping.CourseID = Course.CRN WHERE Schedule_Mapping.StudentID = ' + str(studentID) + ' AND Course.Semester = \'' + getSemester + '\' AND Course.Year = \'' + str(getYear) + '\''
        c = database.cursor()
        c.execute(checkSchedMapping)
        schedResult = c.fetchall()
        c.close()
        if not schedResult:
            print('\nNo Schedule found for ' + getSemester + ' ' + str(getYear) + '.\n')
        else:
            print('\nYour Schedule for ' + getSemester + ' ' + str(getYear) + ':')
            for course in schedResult:
                print(course[1] + '\t\t' + course[2] + '\t' + course[0])
            print()

    # author: Sterling
    # student menu function
    def studentMenu(self, sID, sEmail):
        choice=""

        while 1:
            choice = input("\nWelcome to the CURSE registration system.\n1. Add a course\n2. Drop a course\n3. Search courses\n4. View/print schedule\n5. Check conflicts\n6. Logout\nEnter choice : ")
            if choice == '1':
                print("Add a course to your schedule.")
                self.addCourse(sID)
            elif choice == '2':
                print("Drop a course from your schedule.")
                self.rmCourse(sID)
            elif choice == '3':
                print("Searching courses.")
                self.searchCourses()
            elif choice == '4':
                print("Please select a semester and year : ")
                self.printSched(sID)
            elif choice == '5':
                print("Logging out...")
                logout()
            else:
                print("¯\_(ツ)_/¯ Invalid input.")

# class Instructor derived from User
class Instructor(User):

    # constructor
    def __init__(self, firstName, lastName, ID):
        super().__init__(firstName, lastName, ID)
        print('Instructor {} {} [{}] created'.format(self.firstName, self.lastName, self.ID))

    # print course roster for instructor
    # author: Chandler Berry
    def printRoster(self):
        # get course ID to view roster
        getCRN = input('Enter CRN to view roster: ')
        # check if CRN exists in db
        findCRN = 'SELECT CRN FROM Course where CRN = ' + str(getCRN)
        c = database.cursor()
        c.execute(findCRN)
        result = c.fetchone()
        c.close()
        if not result:
            print('Course does not exist for this CRN')
        else:
            # get roster from the db
            getRoster = 'SELECT Student.FirstName, Student.LastName, Course.Title FROM Student INNER JOIN Schedule_Mapping ON StudentID = Student.ID INNER JOIN Course ON Course.CRN = Schedule_Mapping.CourseID WHERE CourseID = ' + str(getCRN) + ' ORDER BY LastName ASC'
            c = database.cursor()
            c.execute(getRoster)
            rosterList = c.fetchall()
            c.close()
            # print roster to instructor
            print('\nRoster for ' + rosterList[0][2] + ':')
            for student in rosterList:
                print(student[0] + ' ' + student[1])
            print()
    
    # search a course roster for a particular student, given the course number and student ID
    # author: Chandler Berry
    def searchRoster(self):
        getCRN = input('Enter CRN of course you want to search: ')
        findCRN = 'SELECT CRN FROM Course where CRN = ' + str(getCRN)
        c = database.cursor()
        c.execute(findCRN)
        result = c.fetchone()
        c.close()
        if not result:
            print('Course does not exist for this CRN')
        else:
            getStudentID = input('Enter student ID to find the student in the course: ')
            searchSchedMapping = 'SELECT Student.FirstName, Student.LastName FROM Student INNER JOIN Schedule_Mapping ON StudentID = Student.ID WHERE Schedule_Mapping.CourseID = ' + str(getCRN) + ' AND Student.ID = ' + str(getStudentID)
            c = database.cursor()
            c.execute(searchSchedMapping)
            result = c.fetchall()
            c.close()
            if not result:
                print('No student found registered for this course with ID: ' + str(getStudentID))
            else:
                studentMatch = result[0][0] + ' ' + result[0][1]
                print(studentMatch)
   
    # author: Naomi
    # printing instructor schedule
    def printInstructorSchedule(self, username, upassword):
        c = database.cursor()
        term = input("Enter the semester you would like to search in: ")
        yr = input("Enter the year of the semester you would like to search in: ")    

        #getting first and last name of instructor
        c.execute("""SELECT FirstName, LastName FROM Instructor WHERE Password = '""" + upassword + """' AND Email = '""" + username + """';""")
        fName = c.fetchall()
        for i in fName:
            FName = i[0]
            LName = i[1]

        fullName = FName + " " + LName

        #getting courses where instructor matches first and last name of instructor
        c.execute("""SELECT Title, Times, DaysOfWeek from Course WHERE Instructor ='""" + fullName + """' AND Semester = '""" + term + """' AND Year = '""" + yr + """';""")
        qr = c.fetchall()
        c.close()
        if not qr:
            print("\nYou do not have a schedule at the moment with the entered criterias. Please try again.")
        else:
            print("\nHere is your " + term + " " + yr + " schedule: ")
            for i in qr:
                print(i[0] + "    " + i[2] + "    " + i[1])

            

    # author: Sterling
    # instructor menu function
    def instructorMenu(self, username, upassword):
        choice=""

        while 1:
            choice = input("\nWelcome to the CURSE registration system.\n1. Search courses\n2. View/print schedule\n3. Print roster\n4. Search roster\n5. Logout\nEnter choice : ")
            if choice == '1': 
                print("Searching courses.")
                self.searchCourses()
            elif choice == '2':
                self.printInstructorSchedule(username, upassword)
            elif choice == '3': 
                self.printRoster()
            elif choice == '4':
                self.searchRoster()
            elif choice == '5':
                print("Logging out...")
                logout()
            else:
                print("¯\_(ツ)_/¯ Invalid input.")

# class admin derived from user
class Admin(User):  
    # constructor
    def __init__(self, firstName, lastName, ID):
        super().__init__(firstName, lastName, ID)
        print('Admin {} {} [{}] created'.format(self.firstName, self.lastName, self.ID)) 

    # author: Sterling
    # add courses to system function
    def addCourseSys(self):
        print("Adding a course to the system.")
        title = input("Title : ")
        CRN = input("CRN : ")
        
        #checking if the CRN already exists
        c = database.cursor()
        c.execute("""SELECT * FROM COURSE WHERE CRN = """ + CRN + """;""")
        # fetchone() returns a 0 if nothing was found
        query_result = c.fetchone()
        c.close()

        #result that returned 
        if (query_result is not None):
            print("\nError : CRN already exists.")
            for i in query_result:
                print(i)
                
        else:
            dept = input("Department : ")
            iName = input("Instructor: ")
            time = input("Time slot : ")
            day = input("Days (MTWRF) : ")
            semester = input("Semester (Fall, Spring, Summer) : ")
            year = input("Year : ")
            cred = input("# of credits : ")
            # inserting new info into database
            c = database.cursor()
            c.execute("""INSERT INTO Course VALUES(""" + CRN + """, '""" + title + """', '""" + dept + """', '""" + iName + """', '""" + time + """', '""" + day + """', '""" + semester + """', """ + year + """, """ + cred + """);""")
            c.execute("""SELECT * FROM Course WHERE CRN = """ + CRN + """;""")
            query_result = c.fetchone()
            c.close()
            for i in query_result:
                print(str(i))
            print("Success! Course added to system.")

        # commit changes to db
        database.commit()    
        

    # author: Sterling
    # remove courses from system
    def removeCourseSys(self):
        print("Removing a course from the system.")
        removeCRN = input("Enter CRN of course to remove : ")
        c = database.cursor()
        c.execute("""SELECT * FROM COURSE WHERE CRN = """ + removeCRN + """;""")
        query_result = c.fetchone()
        c.close()
        if (query_result is None):
            print("Error: CRN entered does not match a course in the database.")
        else:
            for i in query_result:
                print(i)
            choice = input("Are you sure you want to remove this? (y for yes, any other key for no) : ")
            if (choice == 'y'):
                c = database.cursor()
                c.execute("""DELETE FROM COURSE WHERE CRN = """ + removeCRN + """;""")
                c.close()
                print("Success.")
            else:
                print("Canceled. No changes have been made.")

        # commit changes to db
        database.commit()  

    def linkStudent(self):
        # Getting info from user
        try:
            getCRN = input("Enter CRN of course you want to add a student to : ")
            c = database.cursor()
            # Printing out the results so user knows they're choosing the right course and student
            c.execute("""SELECT * FROM COURSE WHERE CRN = """ + getCRN + """;""")
            qr1 = c.fetchone()
            c.close()
            if qr1 is None:
                print("CRN does not exist in system.")
            else:
                for i in qr1:
                    print(i)
                getFName = input("First Name of Student : ")
                getLName = input("Last Name : ")
                getStudentID = input("ID of Student : ")
                c = database.cursor()
                c.execute("""SELECT * FROM STUDENT WHERE ID = '""" + getStudentID + """' AND FirstName = '""" + getFName + """' AND LastName = '""" + getLName + """';""")
                qr1 = c.fetchone()
                c.close()
                if qr1 is None:
                    print("Student does not exist in system.")
                else:
                    # checking for conflicting course in student schedule
                    for i in qr1:
                        print(i)
                    # Check if student is already registered for course
                    c = database.cursor()
                    c.execute("""SELECT StudentID FROM Schedule_Mapping WHERE StudentID = '""" + str(getStudentID) + """' AND CourseID = '""" + str(getCRN) + """';""")
                    qr1 = c.fetchone()
                    c.close()
                    if qr1 is not None:
                        for i in qr1:
                            print(i)
                        print("Student " + getFName + " " + getLName + " is already registered for " + getCRN + "." )
                    else:
                        # checking for conflicting course in student schedule
                        conflicts = self.checkConflicts(getStudentID, getCRN)
                        # if the length of the conflicts list is zero, that means there were no conflicts
                        if len(conflicts) == 0:
                            confirm = input("Confirm link (y/n) : ")
                            if confirm == 'y':
                                c = database.cursor()
                                c.execute("""INSERT INTO Schedule_Mapping VALUES (""" + str(getCRN) + """, """ + str(getStudentID) + """);""")
                                database.commit()
                                print("Success.")
                            else:
                                print("No changes have been made.")
                        else:
                            print(*conflicts, sep = '\n')
        except:
            print("( ͡ʘ ͜ʖ ͡ʘ) Invalid criteria. Please enter data again.")
        
    def unlinkStudent(self):
        try:
            # Getting info from user
            getCRN = input("Enter CRN of course you want to remove a student from : ")
            c = database.cursor()
            c.execute("""SELECT * FROM Schedule_Mapping WHERE CourseID = '""" + getCRN + """';""")
            qr1 = c.fetchone()
            c.close()
            if qr1 is None:
                print("Cannot unlink Student because Course Roster is empty, or CRN doesn't exist.")
            else:
                getStudentID = input("Input ID of Student to unlink from Course : ")
                # Checking if student is actually registered to course
                c = database.cursor()
                c.execute("""SELECT * FROM Schedule_Mapping WHERE CourseID = '""" + getCRN + """' AND StudentID = '""" + getStudentID + """';""")
                qr1 = c.fetchone()
                c.close()
                if qr1 is None:
                    print("Student is not already registered for " + getCRN + ", or Student does not exist in system.")
                else:
                    print("Removing : ")
                    c = database.cursor()
                    c.execute("""SELECT * FROM Student WHERE ID = '""" + getStudentID + """';""")
                    qr1 = c.fetchone()
                    c.close()
                    for i in qr1:
                        print(i)
                    print("From : ")
                    c = database.cursor()
                    c.execute("""SELECT * FROM Course WHERE CRN = '""" + getCRN + """';""")
                    qr1 = c.fetchone()
                    c.close()
                    for i in qr1:
                        print(i)
                    confirm = input("Confirm y/n : ")
                    if confirm == 'y':
                        c = database.cursor()
                        c.execute("""DELETE FROM Schedule_Mapping WHERE CourseID = '""" + getCRN + """' AND StudentID = '""" + getStudentID + """';""")
                        qr1 = c.fetchone()
                        c.close()
                        database.commit()
                        print("Success.")
                    else:
                        print("No changes have been made.")
        except:
            print("( ͡ʘ ͜ʖ ͡ʘ) Invalid criteria. Please enter data again.")

    def linkInstructor(self):
        try:
            getCRN = input("Enter CRN of course to add instructor to : ")
            c = database.cursor()
            # Printing out the results so user knows they're choosing the right course and student
            c.execute("""SELECT * FROM COURSE WHERE CRN = """ + getCRN + """;""")
            qr1 = c.fetchone()
            c.close()
            if qr1 is None:
                print("CRN does not exist in system.")
            else:
                getFirstName = input("Enter First Name of Instructor : ")
                getLastName = input("Enter Last Name : ")
                getID = input("Enter Instructor ID : ")
                c = database.cursor()
                c.execute("""SELECT FirstName, LastName FROM Instructor WHERE Firstname = '""" + getFirstName + """' AND LastName = '""" + getLastName + """' AND ID  = """ + getID + """;""")
                Name = c.fetchall()
                for i in Name:
                    FName = i[0]
                    LName = i[1]
                fullName = FName + " " + LName
                c.close()
                c = database.cursor()
                c.execute("""SELECT Instructor FROM Course WHERE Instructor = '""" + fullName + """' AND CRN = """ + getCRN + """;""")
                qr1 = c.fetchone()
                if qr1 is not None:
                    print(fullName + " is already teaching this Course " + getCRN + ".")
                else:    
                    c = database.cursor()
                    c.execute("""SELECT Instructor FROM Course WHERE Instructor = 'TBA' AND CRN = """ + getCRN + """;""")
                    qr1 = c.fetchone()
                    c.close()
                    # if it finds the TBA (course is available for teaching)
                    if qr1 is not None:
                        insertName = getFirstName + " " + getLastName
                        confirmInsert = input(insertName + " will be teaching " + getCRN + "\nConfirm (y for yes, anything else for no) : ")
                        if confirmInsert == 'y':
                            c = database.cursor()                  
                            c.execute("""UPDATE Course SET Instructor = '""" + insertName + """' WHERE CRN = """ + getCRN + """;""")
                            c.close()
                            print("Success.")
                            database.commit()
                        else:
                            print("No changes have been made.")
                    else: # if there is already a name here
                        print("Course is already being taught by another Instructor.")
        except:
            print("( ͡ʘ ͜ʖ ͡ʘ) Invalid criteria. Please enter data again.")

    def unlinkInstructor(self):
        try:
            # Get CRN from user
            getCRN = input("Enter CRN of Course to unlink Instructor : ")
            c = database.cursor()
            # Checking if CRN exists in system
            c.execute("""SELECT * FROM COURSE WHERE CRN = """ + getCRN + """;""")
            qr1 = c.fetchone()
            c.close()
            if qr1 is None:
                print("CRN does not exist in system.")
            else:
                c = database.cursor()
                # Seeing who is teaching
                c.execute("""SELECT Instructor FROM Course WHERE CRN = """ + getCRN + """;""")
                qr1 = c.fetchall()
                c.close()

                for i in qr1:
                    inst = i[0]

                confirm3 = input("Would you like to remove " + inst + " from course " + getCRN + " (y for yes, anything else for no) : ")

                if confirm3 == 'y':
                    c = database.cursor()                  
                    c.execute("""UPDATE Course SET Instructor = 'TBA' WHERE CRN = """ + getCRN + """;""")
                    c.close()
                    print("Success.")
                    database.commit()
                else:
                    print("No changes have been made.")
        except:
            print("( ͡ʘ ͜ʖ ͡ʘ) Invalid criteria. Please enter data again.")

    # author: Naomi
    # add instructor or student to system
    def addStudentInstructor(self):
        c = database.cursor()

        uType = input("Do you want to add a Student or Instructor? ")

        if uType == "Student":
            sID = input("\nEnter the student's id: ")
            sEmail = input("Enter the student's email: ")

            c.execute("""SELECT * FROM Student WHERE ID = """ + sID + """ OR Email = '""" + sEmail + """';""")
            # fetchone() returns a 0 if nothing was found
            query_result = c.fetchone()

            #result that returned 
            if (query_result is not None):
                print("Error : Student already in system.")

            else:
                sFirstName = input("Enter the student's first name: ")
                sLastName = input("Enter the student's last name: ")
                gYear = input("enter the student's graduation year: ")
                m = input("Enter the student's major: ")
                sPassword = input("Enter the student's password: ")

                c.execute("""INSERT INTO STUDENT VALUES(""" + sID + """,'""" + sFirstName + """','""" + sLastName + """',""" + gYear + """,'""" + m + """','""" + sEmail + """','""" + sPassword + """');""") 
                print("\nStudent has been added!\n")
                c.close()

        elif uType == "Instructor":
            iID = input("\nEnter the instructor's id: ")
            iEmail = input("Enter the instructor's email: ")

            c.execute("""SELECT * FROM Instructor WHERE ID = """ + iID + """ OR Email = '""" + iEmail + """';""")
            # fetchone() returns a 0 if nothing was found
            query_result = c.fetchone()

            #result that returned 
            if (query_result is not None):
                print("Error : Instructor already in system.")

            else:
                iFirstName = input("Enter the instructor's first name: ")
                iLastName = input("Enter the instructor's last name: ")
                title = input("enter the instructor's title: ")
                dept = input("Enter the department the instructor belongs to: ")
                iPassword = input("Enter the instructor's password: ")

                c.execute("""INSERT INTO INSTRUCTOR VALUES(""" + iID + """,'""" + iFirstName + """','""" + iLastName + """','""" + title + """','""" + dept + """','""" + iEmail + """','""" + iPassword + """');""")
                print("\nInstructor has been added!\n")
                c.close()
        else: 
            print("\nWrong user type. Please enter correct user type to add.")
            self.addStudentInstructor()

        # commit changes to db
        database.commit() 


    # author: Sterling
    # admin menu function
    def adminMenu(self):
        choice = ""

        while 1:
            choice = input("\nWelcome to the CURSE registration system.\n1. Add a course to system\n2. Remove a course from system\n3. Search courses\n4. Link/unlink user from course\n5. Add user\n6. Logout\nEnter choice : ")
            if choice == '1':
                self.addCourseSys()
            elif choice == '2':
                self.removeCourseSys()
            elif choice == '3':
                print("Searching courses.")
                self.searchCourses()
            elif choice == '4':
                print("Link/unlink student or instructor to course.")
                linkChoice = input("1. Link or 2. Unlink? : ")
                if linkChoice == '1':
                    StOrI = input("1. Student or 2. Instructor? : ")
                    if StOrI == '1':
                        self.linkStudent()
                    elif StOrI == '2':
                        self.linkInstructor()
                    else:
                        print("¯\_(ツ)_/¯ Invalid input.")
                elif linkChoice == '2':
                    StOrI = input("1. Student or 2. Instructor? : ")
                    if StOrI == '1':
                        self.unlinkStudent()
                    elif StOrI == '2':
                        self.unlinkInstructor()
                    else:
                        print("¯\_(ツ)_/¯ Invalid input.")
            elif choice == '5':
                self.addStudentInstructor()
            elif choice == '6':
                print("Logging out...")
                logout()
            else:
                print("¯\_(ツ)_/¯ Invalid input.")

# author: Naomi Torre
# login function
def login():
    user = input("Are you a Student, Admin or Instructor? ")
    if user == 'Student' or user == 'Admin' or user == 'Instructor':
        username = input("Enter username: ")
        upassword = input("Enter password: ") 

        #Checking credentials
        c = database.cursor()
        c.execute("""SELECT Email from '""" + user + """' WHERE '""" + user + """'.Email = '""" + username + """';""")
        qr1 = c.fetchall()
        c.close()

        for i in qr1:
            result1 = i[0]

        c = database.cursor()
        c.execute("""SELECT Password from '""" + user + """' WHERE Password = '""" + upassword + """' AND Email = '""" + username + """';""")
        qr2= c.fetchall()
        c.close()

        for i in qr2:
            result2 = i[0]

        try:
            if username == result1 and upassword == result2 :
                print("\nLogin successful!")
                
                c = database.cursor()
                c.execute('SELECT ID, FirstName, LastName FROM '+user+' WHERE '+user+'.Email = \''+username+'\'')
                userInfo = list(c.fetchall())
                c.close()
                for row in userInfo:
                    fName = row[1]
                    lName = row[2]
                    uID = row[0]
                if user == 'Student':
                    sUser = Student(str(fName), str(lName), str(uID))
                    sUser.studentMenu(str(uID), username)
                elif user == 'Instructor':
                    iUser = Instructor(str(fName), str(lName), str(uID))
                    iUser.instructorMenu(username, upassword)
                elif user == 'Admin':
                    aUser = Admin(str(fName), str(lName), str(uID))
                    aUser.adminMenu()

        except UnboundLocalError:
            print("\ninvalid credentials.")
            again = input("Would you like to try again? \nEnter 1 to go back to login \nEnter 2 to exit\n")
            if again == '1':
                login()
            elif again == '2': 
                sys.exit()
    else: 
        print('\nPlease enter a correct user type.')
        login()

# author: Naomi Torre
# logout function    
def logout():
    print(" \nYou have successfully logged out. \nFor security reasons, exit your web browser.")
    sys.exit()