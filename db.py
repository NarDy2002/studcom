import json


def get_db(file_name: str):
    with open(file_name, "r") as read_file:
        data = json.load(read_file)
    return data


def push_db(file_name: str, new_data: dict):
    data = get_db(file_name)
    data.update(new_data)
    set_db(file_name, data)


def pop_db(file_name: str, id1: str):
    data = get_db(file_name)
    data.pop(id1)
    set_db(file_name, data)


def set_db(file_name: str, db: dict):
    f = open(file_name, "w")
    f.write(str(json.dumps(db)))
    f.close()
