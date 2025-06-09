import pickle

class Human:
    def __init__(self, name):
        self.name = name

with open('instance.pickle', 'rb') as f:
    instance = pickle.load(f)

print(instance.name)

with open('data.pickle', 'rb') as fh:
    data = pickle.load(fh)

print(data)