class student:
    def __init__(self, roll, grade):
        self.roll = roll
        self.grade= grade

    def display(self):
        print(f"Roll = {self.roll}, grade = {self.grade}")

stud1= student(34,"S")
stud1.age = 7
stud1.display()