from cs50 import get_string
import re

# Source: https://stackoverflow.com/questions/15228054/how-to-count-the-amount-of-sentences-in-a-paragraph-in-python

# Get text from user
text = get_string("Text: ")

# Calculate words, letters and sentences
number_words = len(text.split())
number_letters = 0
for c in text:
    if ord(c.upper()) >= 65 and ord(c.upper()) <= 90:
        number_letters += 1
number_sentences = len(re.split(r'[.!?]+', text))-1

# Calculate the parameters
l = number_letters / number_words * 100
s = number_sentences / number_words * 100

# Calculate the index
index = round((0.0588 * l - 0.296 * s - 15.8), 0)

# Output the answer based on the index
if index < 2:
    print("Before Grade 1")
elif index >= 16:
    print("Grade 16+")
else:
    print(f"Grade {index}")