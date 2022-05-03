import json

def read_file(file) -> dict:
    """ Reads a .json file, filtrates it and returns you a dict. """
    data = {}

    with open(file, 'r') as f:
        for key, value in json.load(f).items():
            if not _key_exists(value, 'isFinished'): continue
            if value['isFinished']: continue
            data[key] = value

    return data

def _key_exists(key, value) -> bool:
    try:
        key[value]
    except KeyError:
        return False

    return True
