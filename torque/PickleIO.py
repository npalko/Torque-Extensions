import pickle


def write(obj, file=None):
    if file is None:
        file = obj.name + '.torque'
    with open(file, 'w') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)        
def load(file):
    with open(file, 'r') as f:
        obj = pickle.load(f)
        return obj