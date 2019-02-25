""""
The program gets 2 arrays X and Y.
Usage:
1st line - number of elements in X-array
next X lines - lines one by one
next line - number of queries Y
next Y lines - separate queries, each in separate line

The program counts how many times each query of Y can be found among the elements of X.
Example:

Input:
6
one
two
three
four
one
one
3
one
four
five

Output:
3
1
0
"""


import collections

def get_input():
    return get_strings('X'), get_strings('Y')

def get_strings(name):                  #gets number of elements in array and then gets array's strings
    strings = []
    length = int(raw_input('Input number of elements {}:'.format(name)))
    for _ in range(length):
        strings.append(raw_input('Input string:'))
    return strings

def count(a, b):                       #counts how many times each word of a can be found among the elements of b
    return [collections.Counter(a)[word] for word in b]


selection = int(raw_input('User input - press(1), read from file - press(2)'))
if selection == 1:
    X, Y = get_input()
if selection == 2:
    f = open('strings.txt', 'r')
    strings = f.read().splitlines()
    number_X = strings[0]
    if not number_X.isdigit():
        raise ValueError('Invalid limit value.')
    X = strings[1:int(number_X) + 1]
    Y = strings[int(number_X) + 2:]
output = count(X, Y)
for element in output:
print (element)
