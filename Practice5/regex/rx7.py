import re

text = input()

components = text.split("_")

camel = components[0] + ''.join(x.capitalize() for x in components[1:])

print(camel)