import json

def read_corpus(file_name):
    with open(file_name) as data_file:    
        data = json.load(data_file)
    return data

