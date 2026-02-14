class A:
    def __init__(self, x):
        self.x = x

class B(A):
    def __init__(self, x):
        super().__init__(x)

b = B(5)
print(b.x)
