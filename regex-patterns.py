import re

mystring = "Jessa and Kelly"

# Define the regex pattern to match spaces between words
pattern = r'\b\s+\b'

# Replace spaces with "@"
modified_string = re.sub(pattern, '@', mystring)

print(modified_string)

import re

mystring = "Jessa@and@Kelly"

# Define the regex pattern to match "@"
pattern = r'@'

# Split the string using "@" as the delimiter
split_strings = re.split(pattern, mystring)

# Convert the result to an array
result_array = list(filter(None, split_strings))

print(result_array)

