import json

def read_file(file) -> dict:
    """ Reads a .json file and returns you a dict. """
    data = {}

    with open(file, 'r', encoding='utf-8') as f:
        for key, value in json.load(f).items():
            data[key] = value

    return data

def write_file(data: dict, file: str) -> bool:
    try:
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except:
        return False

    return True

def _key_exists(key, value) -> bool:
    try:
        key[value]
    except KeyError:
        return False

    return True

def validate_json(data: dict, max_users: int) -> dict:
    validated_data = {}

    idx = 0

    for key, value in data.items():
        if not _key_exists(value, 'done'): continue
        if value['done']: continue
        idx += 1
        validated_data[key] = value
        if idx == max_users - 1: break

    return validated_data
