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
student = ''
error = False

while True:
    try:
        max_students = int(input("Enter the Maximum Number of Students "))
    except ValueError:
        print("Error !! Please enter a valid integer")
        error = True
        continue
    else:
        error = False
        break

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
            print("Error !! Please enter a valid integer")
            error = True
            continue
        else:
            error = False
            break


print("\n")
f = open("Marks.txt", "w+")
f.write(student)
f.seek(0) # --> 0 means from the start of the file
print(f.read())
f.close()

