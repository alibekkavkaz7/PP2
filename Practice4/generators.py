

# 1
def squares_to_n(n):
    for i in range(n + 1):
        yield i * i


# 2
def even_numbers(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i


# 3
def div_3_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i


# 4
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i


# 5
def reverse_numbers(n):
    while n >= 0:
        yield n
        n -= 1



n = int(input())

# 1
for x in squares_to_n(n):
    print(x, end=" ")
print()

# 2
for x in even_numbers(n):
    print(x, end=",")
print()

# 3
for x in div_3_4(n):
    print(x, end=" ")
print()

# 4
a = int(input())
b = int(input())

for x in squares(a, b):
    print(x, end=" ")
print()

# 5
for x in reverse_numbers(n):
    print(x, end=" ")
