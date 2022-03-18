import pickle

def save_object(path_file, object):
    with open(path_file, 'wb')as f:
        pickle.dump(object, f)

def read_file(path_file):
    object = None
    with open(path_file, 'rb') as f:
        object = pickle.load(f)
        print(object)
    return object

