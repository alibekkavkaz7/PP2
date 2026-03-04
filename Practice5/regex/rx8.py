import re

text = input()

result = re.split(r"(?=[A-Z])", text)

print(result)