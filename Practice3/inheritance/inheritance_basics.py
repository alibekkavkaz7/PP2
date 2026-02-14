class A:
    def f(self):
        print("A")

class B(A):
    pass

b = B()
b.f()
