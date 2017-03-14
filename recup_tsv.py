is_associated_91_91 = {}
is_associated_91_182 = {}
is_associated_test = {}

with open('training/training_set_91_91.tsv', 'r') as tsv:
    for line in tsv:
        current = line.strip().split('\t')
        is_associated_91_91[(current[0], current[1])] = current[2]

with open('training/training_set_91_182.tsv', 'r') as tsv:
    for line in tsv:
        current = line.strip().split('\t')
        is_associated_91_182[(current[0], current[1])] = current[2]

with open('training/testing_set.tsv', 'r') as tsv:
    for line in tsv:
        current = line.strip().split('\t')
        is_associated_test[(current[0], current[1])] = current[2]
