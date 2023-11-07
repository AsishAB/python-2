'''
   Write a code that will take input of the total number of students
   Then, ask for the roll number, name and total mark of each student
   Then write the details of each student in a file called Marks.txt
      in the form student_roll_number, student_name, student_marks
   And then, read from the same file and display the output
'''

roll_number = []
names = []
marks = []
file_name = "Marks.txt"
error_valid_number_message = "Error !! Please enter a valid number"

class EmptyStringException(Exception):
    def __init__(self, msg):
        if msg == '':
            msg = "Empty Student List"
        self.msg = msg
    def printErrorMessage(self):
        print(self.msg)

def getMaxNumberOfStudents():
    max_students = 0
    while True:
        try:
            max_students = int(input("Enter the Maximum Number of Students "))
        except ValueError:
            print(error_valid_number_message)
            continue
        else:
            return max_students


def updateMarks(max_students):
    student = ''
    for i in range(0,max_students):
        # j = i + 1 # --> i remains same till for loop is called
        while True:
            j = i + 1 # --> i remains same till for loop is called
            try:
                roll = int(input(f"Enter Roll Number of student {j} "))
                roll_number.append(roll)
                name = input(f"Enter Name of Student {j} ")
                names.append(name)
                mark = int(input(f"Enter Marks of Student {j} "))
                marks.append(mark)
                student += f"{roll_number[i]}, {names[i]}, {marks[i]} \n"
            except ValueError:
                print(error_valid_number_message)
                continue
            else:
                break

    return student


def writeToAndReadFromFile(student_list, file_name):
    try:
        f = open(file_name, "w+")
        if student_list == '':
            raise EmptyStringException
        f.write(student_list)
        f.seek(0)  # --> 0 means from the start of the file
        print("\n")
        print(f.read())
        f.close()
    except EmptyStringException as e:
        e.printErrorMessage()
    except Exception as otherExceptions:
        print(otherExceptions)


max_no_of_students = getMaxNumberOfStudents()
student_list = updateMarks(max_no_of_students)
writeToAndReadFromFile(student_list, file_name)
