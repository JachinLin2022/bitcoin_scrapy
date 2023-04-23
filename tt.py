import ast

header = {}

with open('header.txt', 'r') as file:
    for line in file:
        if line.startswith('cookie') or line.startswith('authorization') or line.startswith('x-csrf-token'):
            key, value = line.strip().split(": ")
            header[key] = value


print(header)