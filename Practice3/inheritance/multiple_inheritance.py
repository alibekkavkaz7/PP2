class A:
    def f(self):
        print("A")

class B:
    def g(self):
        print("B")

class C(A, B):
    pass

c = C()
c.f()
c.g()
