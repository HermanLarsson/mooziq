import os, json, csv

DIRECTORY = os.path.dirname(os.path.abspath(__file__)) # constat since the filepath up to dataset will always be the different for users


def get_names_ids():

    dict_artist_info = {}
    folder_path = os.path.join("dataset", "artists")

    for file_name in sorted(os.listdir(folder_path)):
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            dict_artist_info[data["name"]] = data["id"] 

    return dict_artist_info


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


def get_tracks(names_ids, chosen_artist):
    
    folder_path = os.path.join(DIRECTORY, "dataset/top_tracks/")
    track_popularity = [] 

    with open(os.path.join(folder_path, names_ids[chosen_artist] + ".json"), "r", encoding="UTF-8") as jsonfile:
        data = json.load(jsonfile)
        
    
    for track in data["tracks"]:
        track_popularity.append((track["name"], track["popularity"]))

    return track_popularity


def get_genres(chosen_artist):

    artist_genres_str = ""
    dict_artist_info = {}
    folder_path = os.path.join("dataset", "artists")

    for file_name in sorted(os.listdir(folder_path)):
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            dict_artist_info[data["name"]] = data["genres"]
                           
    artist_genres = dict_artist_info[chosen_artist]

    if len(artist_genres) > 0:
        for i in range(len(artist_genres)):
            if i == 0:
                artist_genres_str += artist_genres[0]
            else:
                artist_genres_str += f", {artist_genres[i]}"
    else:
        artist_genres_str = ""

    return artist_genres_str


def write_artist_csv(artist_info, chosen_artist):

    header = ["artist_id", "artist_name", "number_of_albums", "top_track_1", "top_track_2", "genres"]
    csv_path = os.path.join(".", "dataset", "artist-data.csv")

    if not os.path.isfile(csv_path):
        with open(csv_path, "w", encoding="UTF-8", newline="\n") as file:
            writer = csv.writer(file)
            writer.writerow(header)

    with open(csv_path, "r", encoding="UTF-8") as file:
        data = list(csv.reader(file))

    found_artist = False    
    for i in range(1, len(data)):
        if data[i][1] == chosen_artist:
            data[i] = artist_info
            found_artist = True

    if found_artist:
        with open(csv_path, "w", encoding="UTF-8", newline="\n") as file:
            writer = csv.writer(file)    
            writer.writerows(data)
        print(f"Exporting \"{chosen_artist}\" data to CSV file...\nData successfully updated.")

    else:
        with open(csv_path, "a", encoding="UTF-8", newline="\n") as file:
            writer = csv.writer(file)    
            writer.writerow(artist_info)
        print(f"Exporting \"{chosen_artist}\" data to CSV file...\nData successfully appended.")


def load_song_data():

    index = 1
    matches_dict = {}
    folder_path = os.path.join("dataset", "songs")
    print(f"Available songs: ")

    for file_names in sorted(os.listdir(folder_path)):
        file_path = os.path.join(folder_path, file_names)
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            matches_dict[index] = {"title": data["title"], "lyrics": data["lyrics"], "artist": data["artist"]}
            print(f"{index}. {data["title"]} by {data["artist"]}")
            index += 1

    return matches_dict


def sort_albums(names_ids, search_year):

    reversed_dict = {value: key for key, value in names_ids.items()} 
    albums_list = []    
    folder_path = os.path.join("dataset", "albums")

    for file_name in sorted(os.listdir(folder_path)):
        file_path = os.path.join(folder_path, file_name)
        artist_id = os.path.splitext(file_name)[0]    

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            albums_info = data["items"]    

            for item in albums_info:
                release_date = item["release_date"]
                release_year = release_date[:4]
                album_name = item["name"]
                artist_name = reversed_dict.get(artist_id)

                if int(release_year) == search_year:
                    albums_list.append((album_name, artist_name))

            albums_list.sort()
    
    return albums_list