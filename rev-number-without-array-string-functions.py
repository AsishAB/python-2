'''
Write a program to reverse a number without using String or Array methods

'''

number = 4567

def revNumber(num):
    revNum = 0

    while (num != 0):
        revNum = revNum * 10 + num % 10
        num = int(num / 10)
    return revNum


print(f"Number = {number}, Reversed Number = {revNumber(number)}")
