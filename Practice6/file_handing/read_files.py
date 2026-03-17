with open("example.txt", "r") as file:
    content = file.read()
    print(content)

with open("example.txt", "r") as file:
    for line in file:
        print(line.strip())