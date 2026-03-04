import re

text = input()

if re.search(r"a.*b", text):
    print("Match")
else:
    print("No match")