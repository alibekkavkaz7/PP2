class A:
    def f(self):
        print("A")

class B(A):
    def f(self):
        print("B")

b = B()
b.f()
