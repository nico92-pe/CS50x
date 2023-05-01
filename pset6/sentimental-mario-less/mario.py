from cs50 import get_int

# Prompt the Height
while True:
    height = get_int("Height: ")
    if height > 0 and height < 9:
        break

# Drawing the pyramid
for i in range(height):
    print(" "*(height - 1 - i) + "#"*(i + 1))