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
            # add new tuple to the db that indicates that the student is now registered for this course
            addTuple = 'INSERT INTO Schedule_Mapping VALUES (' + str(getCRN) + ', ' + str(studentID) + ')'
            c = database.cursor()
            c.execute(addTuple)
            c.close()
            database.commit()
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

    # author: Sterling
    # student menu function
    def studentMenu(self, sID, sEmail):
        choice=""

        while 1:
            choice = input("Welcome to the CURSE registration system.\n1. Add a course\n2. Drop a course\n3. Search courses\n4. View/print schedule\n5. Check conflicts\n6. Logout\nEnter choice : ")
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
                #printSchedule()
            elif choice == '5':
                print("Checking schedule for conflicts.")
                #checkConflict()
            elif choice == '6':
                print("Logging out...")
                logout()

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
        print('\n')
   
    # author: Naomi
    # printing instructor schedule
    def printInstructorSchedule(self, username, upassword):
        c = database.cursor()

        #getting first and last name of instructor
        c.execute("""SELECT FirstName FROM Instructor WHERE Password = '""" + upassword + """' AND Email = '""" + username + """';""")
        fName = c.fetchall()
        for i in fName:
            FName = i[0]

        c.execute("""SELECT LastName FROM Instructor WHERE Password = '""" + upassword + """' AND Email = '""" + username + """';""")
        lName = c.fetchall()
        for i in lName:
            LName = i[0]

        fullName = FName + " " + LName

        #getting courses where instructor matches first and last name of instructor
        c.execute("""SELECT Title from Course WHERE Instructor ='""" + fullName + """';""")
        qr = c.fetchall()
        c.close()

        if (qr is not None):
            print("\nYou are not teaching any courses at the moment.\n")
        else:
            print("Here is your schedule: \n")
            for i in qr:
                print(i[0])

    # author: Sterling
    # instructor menu function
    def instructorMenu(self, username, upassword):
        choice=""

        while 1:
            choice = input("Welcome to the CURSE registration system.\n1. Search courses\n2. View/print schedule\n3. Print roster\n4. Logout\nEnter choice : ")
            if choice == '1': 
                print("Searching courses.")
                self.searchCourses()
            elif choice == '2':
                self.printInstructorSchedule(username, upassword)
            elif choice == '3': 
                self.printRoster()
            elif choice == '4':
                print("Logging out...")
                logout()

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
            print("Error : CRN already exists.")
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
            roster = 'NULL'
            # inserting new info into database
            c = database.cursor()
            c.execute("""INSERT INTO Course VALUES(""" + CRN + """, '""" + title + """', '""" + dept + """', '""" + iName + """', '""" + time + """', '""" + day + """', '""" + semester + """', """ + year + """, """ + cred + """, """ + roster + """);""")
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
            choice = input("Are you sure you want to remove this? y/n : ")
            if (choice == 'y'):
                c = database.cursor()
                c.execute("""DELETE FROM COURSE WHERE CRN = """ + removeCRN + """;""")
                c.close()
                print("Success.")
            else:
                print("Canceled. No changes have been made.")

        # commit changes to db
        database.commit()    

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

                c.execute("""INSERT INTO STUDENT VALUES(""" + sID + """,'""" + sFirstName + """','""" + sLastName + """',""" + gYear + """,'""" + m + """','""" + sEmail + """','""" + sPassword + """',  NULL);""") 
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

                c.execute("""INSERT INTO INSTRUCTOR VALUES(""" + iID + """,'""" + iFirstName + """','""" + iLastName + """','""" + title + """','""" + dept + """','""" + iEmail + """','""" + iPassword + """',  NULL);""")
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
            choice = input("Welcome to the CURSE registration system.\n1. Add a course to system\n2. Remove a course from system\n3. Search courses\n4. Link/unlink user from course\n5. Add user\n6. Logout\nEnter choice : ")
            if choice == '1':
                self.addCourseSys()
            elif choice == '2':
                self.removeCourseSys()
            elif choice == '3':
                print("Searching courses.")
                self.searchCourses()
            elif choice == '4':
                print("Link/unlink student or instructor to course.")
            #linkUnlink
            elif choice == '5':
                self.addStudentInstructor()
            elif choice == '6':
                print("Logging out...")
                logout()

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

###############################################
################### warning ###################
###### you have entered the shadow realm ######
###############################################

    # # add courses to student schedule
    # # author: Chandler Berry
    # def addCourse(self, studentID, studentEmail):

    #     # prompt user to enter CRN
    #     getCRN = input('enter CRN of course you want to add: ')

    #     # get ID of student adding the course to their schedule
    #     c = database.cursor()
    #     getStudentID = 'SELECT Student.ID FROM Student WHERE Student.Email = \'' + studentEmail + '\''
    #     c.execute(getStudentID)
    #     studentResult = list(c.fetchall())
    #     c.close()

    #     # get initial student schedule
    #     c = database.cursor()
    #     getSched = 'SELECT Student.Schedule FROM Student WHERE Student.ID = ' + studentID
    #     c.execute(getSched)
    #     schedule = list(c.fetchall())
    #     c.close()

    #     # get initial course roster
    #     c = database.cursor()
    #     getRoster = 'SELECT Course.Roster FROM Course WHERE Course.CRN = ' + getCRN
    #     c.execute(getRoster)
    #     roster = list(c.fetchall())
    #     c.close()

    #     # add student ID to course roster in Course table
    #     newRoster = ''
    #     for row in roster:
    #         if row[0] == None:
    #             for value in studentResult:
    #                 newRoster = value[0]
    #         elif row[0] != None:
    #             for value in studentResult:
    #                 newRoster = str(row[0]) + '-' + str(value[0])
    #     c = database.cursor()
    #     updateRoster = 'UPDATE Course SET Roster = \'' + str(newRoster) + '\' WHERE Course.CRN = ' + str(getCRN)
    #     c.execute(updateRoster)
    #     c.close()

    #     # add course to student schedule
    #     newSchedule = ''
    #     for row in schedule:
    #         if row[0] == None:
    #             for value in studentResult:
    #                 newSchedule = str(getCRN)
    #         elif row[0] != None:
    #             for value in studentResult:
    #                 newSchedule = str(row[0]) + '-' + str(getCRN)
    #     c = database.cursor()
    #     updateSched = 'UPDATE Student SET Schedule = \'' + newSchedule + '\' WHERE Student.ID = ' + studentID
    #     c.execute(updateSched)
    #     print('\nCourse Added to Schedule\n')
    #     c.close()
        
    #     # commit changes to db
    #     database.commit()

    # # remove courses from student schedule
    # # author: Chandler Berry
    # def rmCourse(self, studentID, studentEmail):

    #     # prompt user to enter CRN
    #     getCRN = input('enter CRN of course you want to remove: ')

    #     # get ID of student removing the course from their schedule
    #     c = database.cursor()
    #     getStudentID = 'SELECT Student.ID FROM Student WHERE Student.Email = \'' + studentEmail + '\''
    #     c.execute(getStudentID)
    #     studentResult = list(c.fetchall())

    #     # get initial student schedule
    #     c = database.cursor()
    #     getSched = 'SELECT Student.Schedule FROM Student WHERE Student.ID = ' + studentID
    #     c.execute(getSched)
    #     schedule = list(c.fetchall())
    #     c.close()

    #     # get initial course roster
    #     c = database.cursor()
    #     getRoster = 'SELECT Course.Roster FROM Course WHERE Course.CRN = ' + getCRN
    #     c.execute(getRoster)
    #     roster = list(c.fetchall())
    #     c.close()

    #     # remove student ID from course roster in Course table
    #     newRoster = ''
    #     for row in roster:
    #         if row[0] == None:
    #             print('you aren\'t registered in this course')
    #         elif row[0] != None:
    #             findID = ''
    #             for value in studentResult:
    #                 findID = row[0]
    #                 if str(value[0]) in findID:
    #                     newRoster = findID
    #                     if '-' in newRoster:
    #                         rosterList = newRoster.split('-')
    #                         rosterList.remove(str(value[0]))
    #                         s = '-'
    #                         newRoster = s.join(rosterList)
    #                     else:
    #                         newRoster = ''
    #                 else:
    #                     print('you aren\'t registered in this course')
    #     c = database.cursor()
    #     # quick fix for preventing an empty space from being input into the Course table, this was causing a couple issues that can be nipped in the bud right here.
    #     updateRoster = 'UPDATE Course SET Roster = \'' + newRoster + '\' WHERE Course.CRN = ' + getCRN
    #     if not newRoster:
    #         updateRoster = 'UPDATE Course SET Roster = NULL WHERE Course.CRN = ' + getCRN
    #     c.execute(updateRoster)
    #     c.close()

    #     # remove course from student schedule
    #     newSched = ''
    #     for row in schedule:
    #         if row[0] == None:
    #             print('you aren\'t registered in this course')
    #         elif row[0] != None:
    #             findCRN = ''
    #             for value in schedule:
    #                 findCRN = row[0]
    #                 if str(value[0]) in findCRN:
    #                     newSched = findCRN
    #                     if '-' in newRoster:
    #                         schedList = newSched.split('-')
    #                         schedList.remove(str(value[0]))
    #                         s = '-'
    #                         newSched = s.join(schedList)
    #                     else:
    #                         newSched = ''
    #                 else:
    #                     print('you aren\'t registered in this course')
    #     c = database.cursor()
    #     updateSched = 'UPDATE Student SET Schedule = \'' + newSched + '\' WHERE Student.ID = ' + studentID
    #     if not newSched:
    #         updateSched = 'UPDATE Student SET Schedule = NULL WHERE Student.ID = ' + studentID
    #     c.execute(updateSched)
    #     print('\nCourse Removed from Schedule\n')
    #     c.close()
        
    #     # commit changes to db
    #     database.commit()