import re

text = input()

if re.fullmatch(r"ab{2,3}", text):
    print("Match")
else:
    print("No match")