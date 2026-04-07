import itertools

for numbers in itertools.product([0, 1], repeat=5):
    print(list(numbers))