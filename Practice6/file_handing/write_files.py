with open("example.txt", "w") as file:
    file.write("Hello, this is new content!")

with open("example.txt", "a") as file:
    file.write("\nThis line is appended.")