import math

# 1. 
degree = float(input("Input degree: "))
radian = degree * (math.pi / 180)
print("Output radian:", round(radian, 6))


# 2. 
height = float(input("Height: "))
base1 = float(input("Base, first value: "))
base2 = float(input("Base, second value: "))

area_trapezoid = (base1 + base2) / 2 * height
print("Area of trapezoid:", area_trapezoid)


# 3. 
n = int(input("Input number of sides: "))
side = float(input("Input the length of a side: "))

area_polygon = (n * side * side) / (4 * math.tan(math.pi / n))
print("The area of the polygon is:", round(area_polygon))


# 4. 
base = float(input("Length of base: "))
height_para = float(input("Height of parallelogram: "))

area_para = base * height_para
print("Area of parallelogram:", area_para)
