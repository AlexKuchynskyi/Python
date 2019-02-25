"""
The program gets integer N and N strings in format <first_name>, <second_name>, <sex>, <age>
and returns sorted by age list with prefixes "Mr." and "Mrs."
Input:
4
Ivan Petrov M 34
Sergey Terehov M 25
Alexandra Kac F 23
Semen Burdenko M 25

Output:
Mrs. Alexandra Kac
Mr. Sergey Terehov
Mr. Semen Burdenko
Mr. Ivan Petrov
"""


import collections

Processed_String = collections.namedtuple('Processed_String', ['first_name', 'second_name', 'sex', 'age'])
POSSIBLE_SEX = {'female': 'F', 'male': 'M'}

def process_string(input_string):    # Splits the input string and gets separate components of the splitted string
    components = input_string.split()
    if len(components) != 4:
        print('Invalid number of components in input string!')
    sex = components[2]
    if sex not in POSSIBLE_SEX.values():
        print ('Invalid sex component!')
    age = components[3]
    if not age.isdigit():
        print('Invalid age component!')
    components[3] = int(age)
    return Processed_String._make(components)

def process_data(func):               #Decorator for data processing

    def wrapper(*args, **kwargs):
        data = func(*args, **kwargs)
        for index, input_string in enumerate(data):
            data[index] = process_string(input_string)
        return data
    return wrapper

def main(data):
    data.sort(key=lambda input_string: input_string.age)
    for index, input_string in enumerate(data):
        data[index] = make_output(input_string)
    return data

def make_output(input_string):       # Set an output string in the form needed
    return '{prefix} {first_name} {second_name}'.format(
        prefix = put_prefix(input_string.sex),
        first_name = input_string.first_name,
        second_name = input_string.second_name)

@process_data
def get_input():
    data = []
    limit = int(raw_input('Input number of lines please:'))
    for _ in range(limit):
        data.append(raw_input('Input a line in format "<Name> <Surname> <Sex M/F> <Age>":'))
    return data

def put_prefix(sex):
    if sex == "F":
        return 'Ms.'
    if sex == "M":
        return 'Mr.'


selection = int(raw_input('User input - press(1), read from file - press(2)'))
if selection == 1:
    user_input = get_input()
    output = main(user_input)
    for element in output:
        print (element)
if selection == 2:
    f = open('names.txt', 'r')
    lines = f.read().splitlines()
    limit = lines[0]
    if not limit.isdigit():
        raise ValueError('Invalid limit value.')
data = lines[1:int(limit) + 1]
