# Operator Overloading

class BookX:
    def __init__(self, pages):
        self.pages = pages
    def __add__(self, other):
        return self.pages + other.pages
    def __gt__(self, other):
        if self.pages > other.pages:
            return True
        else:
            return False
    def __eq__(self, other):
        if self.pages == other.pages:
            return True
        else:
            return False

class BookY:
    def __init__(self, pages):
        self.pages = pages
    def __add__(self, other):
        return self.pages + other.pages
    def __gt__(self, other):
        if self.pages > other.pages:
            return True
        else:
            return False
    def __eq__(self, other):
        if self.pages == other.pages:
            return True
        else:
            return False


b1 = BookX(100)
b2 = BookY(20)
print(b2 < b1)