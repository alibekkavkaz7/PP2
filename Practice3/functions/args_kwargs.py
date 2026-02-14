def show(*args):
    print(args)

def show2(**kwargs):
    print(kwargs)

show(1, 2)
show2(name="Anna")
