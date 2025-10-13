import os, json

DIRECTORY = os.path.dirname(os.path.abspath(__file__)) # directory constat since the filepath up to dataset will always be the same


def get_names_ids():

    dict_artist_info = {}
    folder_path = os.path.join("dataset", "artists")
    for file_name in sorted(os.listdir(folder_path)):
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            dict_artist_info[data["name"]] = data["id"] 
    return dict_artist_info