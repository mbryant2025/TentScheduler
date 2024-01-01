# Reads a csv file and returns a nicely formated dataframe

# Input csv format:

'''
Last Updated: ,,Michael Bryant,,,,,,,,,,,
,Sunday,,Monday,,Tuesday,,Wednesday,,Thursday,,Friday,,Saturday
7:00 - 7:30 AM,1,,1,,1,,1,,1,,1,,1
7:30 - 8:00 AM,1,,1,,1,,Q,,1,,1,,1
8:00 - 8:30 AM,1,,1,,1,,0,,1,,1,,1
8:30 - 9:00 AM,1,,1,,1,,0,,1,,1,,1
9:00 - 9:30 AM,1,,1,,1,,0,,1,,1,,1
...
1:30 - 2:00 AM,1,,1,,1,,1,,1,,1,,1
2:00 - 2:30 AM,1,,1,,1,,1,,1,,1,,1
NIGHT SHIFTS,1,,1,,1,,1,,1,,1,,1
'''

# Output format:

'''
    Sunday Monday Tuesday Wednesday Thursday Friday Saturday
7:00 AM 1      1      1        1         1       1       1
7:30 AM 1      1      1        Q         1       1       1
8:00 AM 1      1      1        0         1       1       1
8:30 AM 1      1      1        0         1       1       1
9:00 AM 1      1      1        0         1       1       1
...
1:30 AM 1      1      1        1         1       1       1
2:00 AM 1      1      1        1         1       1       1
NIGHT SHIFT 1      1      1        1         1       1       0
'''

# 1 = Available
# 0 = Unavailable
# Q = Questionable

import pandas as pd

# Define a function to parse the CSV
def parse_csv(file_path):
    # Read the CSV skipping the first two rows
    df = pd.read_csv(file_path, skiprows=2)

    # Remove the nan columns
    df = df.dropna(axis=1, how='all')

    name = pd.read_csv(file_path, nrows=1, header=None).iloc[0, 2]

    # Rename the columns by day of the week, Sunday = 0, Saturday = 6
    df.columns = [name, 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    return df

