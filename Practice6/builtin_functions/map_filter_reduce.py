from functools import reduce

numbers = [1, 2, 3, 4]

squared = list(map(lambda x: x**2, numbers))
print(squared)

even = list(filter(lambda x: x % 2 == 0, numbers))
print(even)

total = reduce(lambda x, y: x + y, numbers)
print(total)