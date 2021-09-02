import pandas as pd
import matplotlib.pyplot as plt
# creates an iterable reader object so we can use next() on it.
df = pd.read_csv('/Users/mikemwimali/Documents/IT/Beginner_Projects/World_Bank/World_Bank_World_Development_Indicators.csv')

feature_names = list(df.columns)
print('List of column names : ', feature_names)

# getting the number of rows
len(df.loc[:])

# extracting the first row.
row_vals = list(df.loc[0])
print(row_vals)

zipped_lists = zip(feature_names, row_vals)
# Create a dictionary: rs_dict
rs_dict = dict(zipped_lists)
# Print the dictionary
print(rs_dict)


# this function creates dictionaries with required lists.
def lists2dict(list1, list2):
    """Return a dictionary where list1 provides
    the keys and list2 provides the values."""

    # Zip lists: zipped_lists
    zipped_lists = zip(list1, list2)

    # Create a dictionary: rs_dict
    rs_dict = dict(zipped_lists)

    # Return the dictionary
    return rs_dict


# Call lists2dict: rs_fxn
rs_fxn = lists2dict(feature_names, row_vals)

# Print rs_fxn
print(rs_fxn)

# creating our lists of lists where each sublist is a list of values of a row.
row_lists = [list(row) for row in df.values]

print(row_lists[0])
print(row_lists[1])

# Turn list of lists into list of dicts: list_of_dicts
list_of_dicts = [lists2dict(feature_names, sublist) for sublist in row_lists]

# Print the first two dictionaries in list_of_dicts
print(list_of_dicts[0])
print(list_of_dicts[1])

# Turn list of dicts into a DataFrame: df
df = pd.DataFrame(list_of_dicts)

# Print the head of the DataFrame
print(df.head())


# Open a connection to the file. This binds the csv file to the word 'file'.
# The with statement is a context manager.
with open('/Users/mikemwimali/Documents/IT/Beginner_Projects/World_Bank/World_Bank_World_Development_Indicators.csv') as file:

    # Skip the column names
    file.readline()

    # Initialize an empty dictionary: counts_dict
    counts_dict = {}

    # Process only the first 1000 rows
    for j in range(1000):

        # Split the current line into a list: line
        line = file.readline().split(',')

        # Get the value for the first column: first_col
        first_col = line[0]

        # If the column value is in the dict, increment its value
        if first_col in counts_dict.keys():
            counts_dict[first_col] += 1

        # Else, add to the dict and set value to 1
        else:
            counts_dict[first_col] = 1

# The resulting dictionary shows the number of times a country appears.
print(counts_dict)


# this generator function makes a generator object which yields a single line
# from a file with the next() function.
def read_large_file(file_object):
    """A generator function to read a large file lazily."""

    # Loop indefinitely until the end of the file
    while True:

        # Read a line from the file: data
        data = file_object.readline()

        # Break if this is the end of the file
        if not data:
            break

        # Yield the line of data
        yield data


# Openning a connection to a file, the resulting file object is already a
# generator. This allows us to deal chunks of data.
with open('/Users/mikemwimali/Documents/IT/Beginner_Projects/World_Bank/World_Bank_World_Development_Indicators.csv') as file:

    # Create a generator object for the file: gen_file
    gen_file = read_large_file(file)

    # Print the first three lines of the file
    print(next(gen_file))
    print(next(gen_file))
    print(next(gen_file))
# since a file object is already a generator, don't have to a make a generator
# with read_large_file() generator function.


counts_dict = {}

# Using the previous generator function to process the whole file line by line
# for every row to make a dictionary of the counts of country appearance.
# Open a connection to the file
with open('/Users/mikemwimali/Documents/IT/Beginner_Projects/World_Bank/World_Bank_World_Development_Indicators.csv') as file:

    # Use the for loop to iterate over the generator from read_large_file()
    for line in read_large_file(file):

        row = line.split(',')
        first_col = row[0]

        if first_col in counts_dict.keys():
            counts_dict[first_col] += 1
        else:
            counts_dict[first_col] = 1

print(counts_dict)


# Initialize reader object: urb_pop_reader
urb_pop_reader = pd.read_csv('/Users/mikemwimali/Documents/IT/Beginner_Projects/World_Bank/World_Bank_World_Development_Indicators.csv', chunksize=1000)

# Get the first DataFrame chunk: df_urb_pop
df_urb_pop = next(urb_pop_reader)

# Check out the head of the DataFrame
print(df_urb_pop.head())

# selecting only the rows of df_urb_pop that equal 'CEB'(central europe baltic)
df_pop_ceb = df_urb_pop[df_urb_pop['CountryCode'] == 'CEB']

# makes a list of tuples from zip object for total pop and urban pop columns.
pops = zip(df_pop_ceb['Total Population'], df_pop_ceb['Urban population (% of total)'])

# Turn zip object into list: pops_list
pops_list = list(pops)

# Print pops_list
print(pops_list)


# Writing a list comprehension to make a list of values to assign to the new
# column 'Total Urban'. Output expression is product of urban pop percentage
# by the total population. Multiply by .01 to remove percentage figure. Use
# the int() function to make sure that 'total urban' is an integer.
df_pop_ceb['Total Urban Population'] = [int(tup[0] * tup[1] * 0.01) for tup in pops_list]

# Plot urban population data
df_pop_ceb.plot(kind='scatter', x='Year', y='Total Urban Population')

plt.show()


# Aggregating the results over all the DataFrame chunks in the data set.
# Initialize empty DataFrame: data
data = pd.DataFrame()

# Iterate over each DataFrame chunk
for df_urb_pop in urb_pop_reader:

    # Check out specific country: df_pop_ceb
    df_pop_ceb = df_urb_pop[df_urb_pop['CountryCode'] == 'CEB']

    # Zip DataFrame columns of interest: pops
    pops = zip(df_pop_ceb['Total Population'], df_pop_ceb['Urban population (% of total)'])

    # Turn zip object into list: pops_list
    pops_list = list(pops)

    # Use list comprehension to create new DataFrame column 'Total Urban Population'
    df_pop_ceb['Total Urban Population'] = [int(tup[0] * tup[1] * 0.01) for tup in pops_list]

    # Append DataFrame chunk to data: data
    data = data.append(df_pop_ceb)

# Plot urban population data
data.plot(kind='scatter', x='Year', y='Total Urban Population')

plt.show()


# Code for processing data into one function. Can reuse the code else where.
def plot_pop(filename, country_code):

    # Initialize reader object: urb_pop_reader
    urb_pop_reader = pd.read_csv(filename, chunksize=1000)

    # Initialize empty DataFrame: data
    data = pd.DataFrame()

    # Iterate over each DataFrame chunk
    for df_urb_pop in urb_pop_reader:
        # Check out specific country: df_pop_ceb
        df_pop_ceb = df_urb_pop[df_urb_pop['CountryCode'] == country_code]

        # Zip DataFrame columns of interest: pops
        pops = zip(df_pop_ceb['Total Population'], df_pop_ceb['Urban population (% of total)'])

        # Turn zip object into list: pops_list
        pops_list = list(pops)

        # Use list comprehension to create new DataFrame column 'Total Urban Population'
        df_pop_ceb['Total Urban Population'] = [int(tup[0] * tup[1] * 0.01) for tup in pops_list]

        # Append DataFrame chunk to data: data
        data = data.append(df_pop_ceb)

    # Plot urban population data
    data.plot(kind='scatter', x='Year', y='Total Urban Population')
    plt.show()


# Set the filename: fn
fn = '/Users/mikemwimali/Documents/IT/Beginner_Projects/World_Bank/World_Bank_World_Development_Indicators.csv'

# Call plot_pop for country code 'CEB'
plot_pop(fn, 'CEB')

# Call plot_pop for country code 'ARB'
plot_pop(fn, 'ARB')
