class Rectangle:
    # length = 0
    # breadth = 0
    def __init__(self, l, b):
        self.length = l
        self.breadth = b

    def area(self):
        area =  self.length * self.breadth
        return area

    def perimeter(self):
        per = 2 * (self.length + self.breadth)
        return per

    @staticmethod
    def help():
        print("All angles of rectangle are right angles (90%)")


rect1 = Rectangle(10, 5)
print(f"Area of Rectangle = {rect1.area()}")
print(f"Perimeter of Rectangle = {rect1.perimeter()}")
rect1.help()


