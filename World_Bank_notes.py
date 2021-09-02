# list comprehension = [output expression for iterator variable in iterable]
#  [output expression +
# conditional on output for iterator variable in iterable +
# conditional on iterable]
avengers = ['hawkeye', 'iron man', 'thor', 'quicksilver']
names = ['barton', 'stark', 'odinson', 'maximoff']

# zip function accepts an arbritray number of iterables and returns an iterator
# of tuples. In this case a list of tuples. If one list or tuples contains more
# items than the other, then the other items are ignored. A single iterator
# object is returned.
z = zip(avengers, names)
print(type(z))
print(list(z))
# each tuple can be unpacked into a variable.
# The elements inside the tuples can be unpacked separetly since each element
# in each iterable/tuple is a separate parameter.
a, b, c, d, e = z
a
f, g = a
f


#
def raise_both(value1, value2):
    """Raise value1 to the power of value2 and vice versa."""
    new_value1 = value1 ** value2
    new_value2 = value2 ** value1
    new_tuple = (new_value1, new_value2)
    return new_tuple


x = ['user', 'gym', 'spy', 'auto']
n_vowel = map(lambda w: w.count('a'), x)
print(list(n_vowel))


def num_sequence(n):
    """Generate values from 0 to n."""
    i = 0
    while i < n:
        yield i
        i += 1


list(num_sequence(9))
