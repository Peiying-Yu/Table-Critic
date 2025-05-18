import pickle

def read_pkl(pkl_file):
    with open(pkl_file, 'rb') as pkl_f:
        data = pickle.load(pkl_f)
    return data