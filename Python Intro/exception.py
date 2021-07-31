import sys

try:
    a = int(input("a: "))
    b = int(input("b: "))

except ValueError:
    print("Error: Invalid Input")
    sys.exit(1)

try:
    c = a/b

except ZeroDivisionError:
    print("Error: Cannot divide by 0.")
    sys.exit(1)

print(f"{a}/{b} = {c}")
