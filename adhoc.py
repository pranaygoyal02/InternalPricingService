# Find natural numbers for a natural number till 10
# Add this number to count
class A:
    def __init__(self):
        sum = 0
    def findnaturalnumber(self,x):
        if ( (x%3 == 0) or ( x % 5 == 0 )):
            return x
        else:
            return None

    def addnaturalnumber(self):
        pass
