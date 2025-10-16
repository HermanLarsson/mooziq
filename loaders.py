import os, json, re, string

DIRECTORY = os.path.dirname(os.path.abspath(__file__)) # directory constat since the filepath up to dataset will always be the same

# All tasks ish
def get_names_ids():

    dict_artist_info = {}
    folder_path = os.path.join("dataset", "artists")
    for file_name in sorted(os.listdir(folder_path)):
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            dict_artist_info[data["name"]] = data["id"] 
    return dict_artist_info

# Task 1

def get_artists(names_ids):

    for artists in names_ids:
        print(f"- {artists}")


# Task 2, 3, 4

def get_chosen_artist(names_ids):
    chosen_artist = input("Please input the name of one of the following artists:\n")
    
    names = list(names_ids.keys())
    counter = 0
    while counter < len(names):
        name = names[counter] 
        if chosen_artist.lower() == name.lower():
            chosen_artist = name
            counter = len(names)
        else:
            counter += 1
    
    return chosen_artist


def get_artist_albums(names_ids, chosen_artist):  

    folder_path = os.path.join(DIRECTORY, "dataset/albums/")
    
    with open(os.path.join(folder_path, names_ids[chosen_artist] + ".json"), "r", encoding="UTF-8") as jsonfile:

        data = json.load(jsonfile)

    unprocessed_albums = data["items"]

    return unprocessed_albums


# Task 5

def load_song_data():
    index = 1
    matches_dict = {}
    folder_path = os.path.join("dataset", "songs")
    print(f"Available songs: ")
    for file_names in sorted(os.listdir(folder_path)):
        file_path = os.path.join(folder_path, file_names)
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            matches_dict[index] = {"title": data["title"], "lyrics": data["lyrics"]}
            print(f"{index}. {data["title"]} by {data["artist"]}")
            index += 1
    return matches_dict


# Task 7

def filter_song_lyrics(song_choice, matches_dict):
    try:
        if song_choice in matches_dict:
            lyrics = matches_dict[song_choice]["lyrics"]
            lower_lyrics = lyrics.lower()
            lower_lyrics_filtered = re.sub(f"[{re.escape(string.punctuation)}]", "", lower_lyrics)
            lower_lyrics_split = lower_lyrics_filtered.split()
        return lower_lyrics_split
    except UnboundLocalError:
        print("")