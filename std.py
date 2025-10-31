
import datetime
import re

# Importing built-in func for date, time handling & email validation

class User:                                     #Base class for a user
    def __init__(self, name, user_id, email):
        try:
            self.name = str(name)
            self.user_id = int(user_id)
            self.email = str(email)
        except ValueError:
            raise TypeError("Invalid data type")

        if not validate_email(self.email):
            raise ValueError("Invalid email format.")

class Student(User):             #Inherits from user & represent student class
    def __init__(self, name, user_id, email):
        super().__init__(name, user_id, email)
        self.courses_enrolled = []

class Course:                     # Class course along with id, name and grade
    def __init__(self, course_id, name):
        try:
            self.course_id = str(course_id)
            self.name = str(name)
        except ValueError:
            raise TypeError("Course ID must be int and name must be str.")

        self.enrolled_students = []
        self.attendance = {}                 # Dict date: set of student_ids
        self.grades = {}                    # Dict student_id: list of grades

#Global Lists

students = []   #list to hold all the student
courses = {}    #Dict to hold all courses

#Helper Functions

def get_student_id(student_id):           #Search & return student obj by id
    for student in students:
        if student.user_id == student_id:
            return student
    return None

def validate_email(email):                  #Validates an email using regex
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def calculate_average(grades):                 #Calculate the avg of grade
    return sum(grades) / len(grades) if grades else 0.0


def add_student(name, user_id, email):            #Method to add new student
    if get_student_id(user_id):                   #Checks for duplicate id
        print("Student ID already exists.")
        return
    students.append(Student(name, user_id, email))  #Add student to list
    print(f"Student added successfully: {name} | {email}")

def add_course(course_id, name):    #Method to add new course
    if course_id in courses:         #Checks if the course id to avoid duplication
        print("Course ID already exists.")
        return
    courses[course_id] = Course(course_id, name)    # Create a new Course & add it to the courses dict
    print("Course added successfully.")

def enroll_student_to_course(student_id, course_id):   #Enroll the student to a course
    student = get_student_id(student_id)   # Access the student object using the ID
    course = courses.get(course_id)        # Access the course object using the ID
    if not student:                        # Look up the course and student by their IDs
        print("Student not found.")
        return
    if not course:
        print("Course not found.")
        return
    if student_id in course.enrolled_students:   # Ensure the student is enrolled in the specified course
        print("Student already enrolled in this course.")
        return
    course.enrolled_students.append(student_id)   #Update the student id
    student.courses_enrolled.append(course_id)    #Update the course id
    print("Student enrolled in course.")

def mark_attendance(course_id, student_id):   # Mark today's attendance for a student in a course
    course = courses.get(course_id)           # Look up the course object & student id
    student = get_student_id(student_id)
    today = datetime.date.today().isoformat()   # Get today's date in 'YYYY-MM-DD' format
    if not course:                                # Look up the course and student by their IDs
        print("Course not found.")
        return
    if not student:
        print("Student not found.")
        return
    if student_id not in course.enrolled_students:     # Ensure the student is enrolled in the specified course
        print("Student not enrolled in this course.")
        return
    if today not in course.attendance:
        course.attendance[today] = set()
        course.attendance[today].add(student_id)    #Record attendance
    if student_id not in course.attendance[today]:   # Add student ID to today's attendance if not already marked
        course.attendance[today].add(student_id)
        print(f"Attendance marked for {today}.")
    else:
        print(f"Attendance already marked for {today}.")

def add_grade(course_id, student_id, mark): # Add a grade for a student in a course
    if not (0 <= mark <= 100):               # Validate that the mark is within the acceptable range
        print("Marks should be between 0 and 100.")
        return
    course = courses.get(course_id)       # Look up the course and student by their IDs
    student = get_student_id(student_id)
    if not course:                         # Check if the course and student exist
        print("Course not found.")
        return
    if not student:
        print("Student not found.")
        return
    if student_id not in course.enrolled_students:   # Ensure student is enrolled in the specified course
        print("Student not enrolled in this course.")
        return
    if student_id not in course.grades:
        course.grades[student_id] = []
    course.grades[student_id].append(mark)  # Add the mark to the student's grade list
    print("Grade recorded.")

def generate_full_report(course_id):
    course = courses.get(course_id)
    if not course:
        print("Course not found.")
        return

    print(f"\n=== Report for Course: {course.name} (ID: {course.course_id}) ===")
    print("Enrolled Students:")

    total_sessions = len(course.attendance)
    all_grades = [g for grades in course.grades.values() for g in grades]
    course_avg = calculate_average(all_grades)

    for sid in course.enrolled_students:
        student = get_student_id(sid)
        print(f"- {student.name} (ID: {student.user_id}, Email: {student.email})")

        # Grades
        grades = course.grades.get(sid, [])
        avg_grade = calculate_average(grades)
        print(f"  Grades: {grades if grades else 'None'} | Avg: {avg_grade:.2f}")

        # Attendance
        attended_days = [date for date, ids in course.attendance.items() if sid in ids]
        print(f"  Attendance Days: {len(attended_days)} | Dates: {', '.join(attended_days) if attended_days else 'None'}")

        # Attendance Percentage
        if total_sessions > 0:
            attendance_percent = (len(attended_days) / total_sessions) * 100
        else:
            attendance_percent = 0.0

        print(f"  Attendance Percentage: {attendance_percent:.2f}%")

        # Highlight students with good scores
        if avg_grade > 85:
            print("  [Grade abv 85%]")

        if attendance_percent > 75:
            print("  [Attd abv 75% ]")

    print(f"\nTotal Sessions Held: {total_sessions}")
    print(f"Overall Course Average Grade: {course_avg:.2f}")
    print("=== End of Report ===\n")

# ------------   Menu System CLI based  -----------

def menu():
    while True:
        print("\n========= Student Course Management =========")
        print("1. Add Student")
        print("2. Add Course")
        print("3. Enroll Student in Course")
        print("4. Mark Attendance")
        print("5. Add Grade")
        print("6. Generate Report")
        print("7. Exit")
        choice = input("Choose an option (1–7): ")     #user input for menu selection

        try:
            if choice == '1':                            #Add a new student
                full_name = input("Enter full name: ")
                user_id = int(input("Enter student ID: "))
                email = input("Enter email: ").strip()
                add_student(full_name, user_id, email)

            elif choice == '2':                            #Add a new course
                cid = input("Enter course ID: ")
                cname = input("Enter course name: ")
                add_course(cid, cname)

            elif choice == '3':                            #Enroll student in a course
                sid = int(input("Enter student ID: "))
                cid = input("Enter course ID: ")
                enroll_student_to_course(sid, cid)

            elif choice == '4':                          #Mark attendance for a student
                cid = input("Enter course ID: ")
                sid = int(input("Enter student ID: "))
                mark_attendance(cid, sid)

            elif choice == '5':                          #Add grades
                cid = input("Enter course ID: ")
                sid = int(input("Enter student ID: "))
                mark = int(input("Enter grade (0–100): "))
                add_grade(cid, sid, mark)

            elif choice == '6':                               #Generate full report
                cid = input("Enter course ID for report: ")
                generate_full_report(cid)

            elif choice == '7':                       #Exit the menu
                print("Exiting program.")
                break

            else:
                print("Invalid option. Please choose 1–7.")
        except Exception as b:                                  #To Catch any error
            print(f"Error: {b}")

# --------  Testing with predefined input  -----------

if __name__ == "__main__":

       # Adding sample students
    add_student("Balu", 101, "balu@ymail.com")
    add_student("Veena", 102, "veena@trymail.com")
    add_student("trish",103,"trish@gmail.com")
    add_student("max",104,"maxi@gmail.com")
    add_student("harry",105,"harry@gmail.com")
    add_student("ron", 106, "ron@gmail.com")
    add_student("shri", 107, "shrik@rkmail.com")
    add_student("vikz", 108, "vikz@supermail.com")

       # Adding sample courses
    add_course("CS101", "Computer Science")
    add_course("MATH101", "Calculus I")
    add_course("PYTH101", "Python")
    add_course("ENG101", "English")
    add_course("DRW101", "Drawing")


       # Enrolling students in courses
    enroll_student_to_course(101, "CS101")
    enroll_student_to_course(102, "MATH101")
    enroll_student_to_course(103, "PYTH101")
    enroll_student_to_course(104, "MATH101")
    enroll_student_to_course(105, "PYTH101")
    enroll_student_to_course(106, "PYTH101")
    enroll_student_to_course(106, "ENG101")
    enroll_student_to_course(107, "MATH101")
    enroll_student_to_course(108, "DRW101")
    enroll_student_to_course(104, "DRW101")


       # Marking attendance for today
    mark_attendance("CS101", 101)
    mark_attendance("ENG101", 101)
    mark_attendance("MATH101", 102)
    mark_attendance("PYTH101", 103)
    mark_attendance("MATH101", 104)
    mark_attendance("PYTH101", 105)
    mark_attendance("PYTH101", 106)
    mark_attendance("MATH101", 107)
    mark_attendance("DRW101", 108)
    mark_attendance("DRW101", 104)


       # Adding grades
    add_grade("CS101", 101, 95)
    add_grade("MATH101", 102, 88)
    add_grade("PYTH101", 103, 95)
    add_grade("MATH101", 104, 95)
    add_grade("PYTH101", 105, 70)
    add_grade("PYTH101", 106, 68)
    add_grade("MATH101", 107, 20)
    add_grade("DRW101", 108, 55)
    add_grade("ENG101", 101, 69)

       # Generating reports
    generate_full_report("CS101")
    generate_full_report("MATH101")
    generate_full_report("PYTH101")
    generate_full_report("ENG101")
    generate_full_report("DRW101")


    #Uncomment this to run the interactive menu

