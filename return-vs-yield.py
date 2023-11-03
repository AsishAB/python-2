def mygenerator():
    print("Line 1")
    yield 1
    print("Line 2")
    yield 2
    print("Line 3")
    yield 3


x= mygenerator()

for i in x:
    print(i)