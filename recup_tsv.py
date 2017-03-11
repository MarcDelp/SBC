is_associated = {}

with open('training/training_set_91_91.tsv', 'r') as tsv:
    for line in tsv:
        current = line.strip().split('\t')
        is_associated[(current[0], current[1])] = current[2]

print is_associated
