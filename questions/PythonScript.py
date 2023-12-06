import os
import csv

# Get the current script's directory
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the path to the CSV file
csv_path = os.path.join(script_dir, 'Ex1', 'test_outputs', 'test_1.csv')

# Read the expected output from the CSV file
with open(csv_path, 'r') as csv_file:
    reader = csv.reader(csv_file)
    expected_output = next(reader)[0]

# Your code to print the nursery rhyme
your_output = "Twinkle, twinkle, little star, How I wonder what you are! Up above the world so high, Like a diamond in the sky. Twinkle, twinkle, little star, How I wonder what you are."

# Compare the expected output with your output
if your_output == expected_output:
    print("Test passed!")
else:
    print("Test failed. Expected output and your output do not match.")
