import re

text = input()

if re.fullmatch(r"ab*", text):
    print("Match")
else:
    print("No match")