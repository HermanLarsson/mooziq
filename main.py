import json, os, csv, re

from loaders import get_names_ids, load_song_data, get_chosen_artist, get_artist_albums, filter_song_lyrics, get_artists

DIRECTORY = os.path.dirname(os.path.abspath(__file__)) # directory constat since the filepath up to dataset will always be the same


# Task 2

def format_albums(unprocessed_albums):

    list_months = [     #perhaps able to use datetime module for this
    "January", "February", "March", "April", 
    "May", "June", "July", "August", 
    "September", "October", "November", "December"
    ]
    all_albums = ""

    for i in range(len(unprocessed_albums)):
        
            album = unprocessed_albums[i]["name"]
            release_date = unprocessed_albums[i]["release_date"]

            if len(release_date) == 4:

                year = release_date[:4]

                all_albums += f"\n- \"{album}\" was released in {year}."

            elif len(release_date) == 7:

                year = release_date[:4]
                month = int(release_date[5:7])
                month = list_months[month - 1]

                all_albums += f"\n- \"{album}\" was released in {month} {year}."

            elif len(release_date) == 10:

                year = release_date[:4]
                month = int(release_date[5:7])
                month = list_months[month - 1]
                day = release_date[8:]


                if day[len(day) - 1] == "1" and day != "11":
                    suffix = "st"
                elif day[len(day) - 1] == "2" and day != "12":
                    suffix = "nd"
                elif day[len(day) - 1] == "3" and day != "13":
                    suffix = "rd"
                else:
                    suffix = "th"

                all_albums += f"\n- \"{album}\" was released in {month} {int(day)}{suffix} {year}."

            else: 

                all_albums += f"\n- \"{album}\" is not none when it was released."

    return all_albums


#Task 3

def get_tracks(names_ids, chosen_artist):
    
    folder_path = os.path.join(DIRECTORY, "dataset/top_tracks/")
    popularity_list = [] 

    with open(os.path.join(folder_path, names_ids[chosen_artist] + ".json"), "r", encoding="UTF-8") as jsonfile:
        data = json.load(jsonfile)
        
    
    for track in data["tracks"]:
        popularity_list.append((track["name"], track["popularity"]))

    return popularity_list
    

def format_tracks(popularity_list, chosen_artist):
    print(f"Listing top tracks for {chosen_artist}...")

    for song, popularity in popularity_list:
        if popularity <= 30:
            message = "No one knows this song."
        elif popularity <= 50:
            message = "Popular song."
        elif popularity <= 70:
            message = "It is quite popular now!"
        elif popularity >= 71:
            message = "It is made for the charts!"

        print(f'- "{song}" has a popularity score of {popularity}. {message}')


# Task 4

def get_top_tracks(names_ids, artist_info, chosen_artist):
    artist_popularity = get_tracks(names_ids, chosen_artist)
 
    for i in range(0, 2):
        artist_info.append(artist_popularity[i][0])


def get_genres(chosen_artist):
    genres_str = ""

    dict_artist_info = {}

    folder_path = os.path.join("dataset", "artists")
    for file_name in sorted(os.listdir(folder_path)):
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            dict_artist_info[data["name"]] = data["genres"]
                           
    genres = dict_artist_info[chosen_artist]

    if len(genres) > 0:
        for i in range(len(genres)):
            if i == 0:
                genres_str += genres[0]
            else:
                genres_str += f", {genres[i]}"
    else:
        genres_str = ""

    return genres_str


def get_artist_info(names_ids, chosen_artist):

    artist_info = list()
    artist_info.append(names_ids[chosen_artist])
    artist_info.append(chosen_artist)
    artist_info.append(len(get_artist_albums(names_ids, chosen_artist)))

    get_top_tracks(names_ids, artist_info, chosen_artist)

    artist_info.append(get_genres(chosen_artist))

    return artist_info

def read_write_csv(artist_info, chosen_artist):

    header = ["artist_id", "artist_name", "number_of_albums", "top_track_1", "top_track_2", "genres"]

    csv_path = os.path.join(".", "dataset", "artist-data.csv")
    if not os.path.isfile(csv_path):
        with open(csv_path, "w", encoding="UTF-8", newline="\n") as file:
            writer = csv.writer(file)
            writer.writerow(header)


    with open(csv_path, "r+", encoding="UTF-8", newline="\n") as file:
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
        #print(f"exporting \"{chosen_artist}\" datatocsvfile...datasuccessfullyupdated.")

    else:
        with open(csv_path, "a", encoding="UTF-8", newline="\n") as file:
            writer = csv.writer(file)    
            writer.writerow(artist_info)
        print(f"Exporting \"{chosen_artist}\" data to CSV file...\nData successfully appended.")
        #print(f"exporting \"{chosen_artist}\" datatocsvfile...datasuccessfullyappended.")

# Task 5

def sort_albums_release(names_ids):
    search_year = input("Please enter a year:\n")
    print(f"Albums released in the year {search_year}:")
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
                if release_year == search_year:
                    albums_list.append((album_name, artist_name))
                albums_list.sort()
    if len(albums_list) == 0:
        print(f"No albums were released in the year {search_year}.")
    else:  
        for albums, artist in albums_list:
            print(f"- \"{albums}\" by {artist}.")

# Task 6

def get_moosed(names_ids):
    pass

# Task 7
def get_longest_sequence():
    matches_dict = load_song_data()
    song_choice = int(input("Please select one of the following songs (number): "))
    if song_choice in matches_dict:
        lyrics = matches_dict[song_choice]["lyrics"]
        lower_lyrics = lyrics.lower()
        filtered_lyrics = re.split(r'[,.\'\n\r ]', lower_lyrics)
        word_list = []
        for words in filtered_lyrics:
            if words not in word_list:
                word_list.append(words)

        print(f"The length of the longest unique word sequence in {matches_dict[song_choice]["title"]} is {len(word_list)} ")
            
        print(word_list)  

def get_longest_sequence(matches_dict, song_choice, lyrics):
    # Sliding window algorithm to get longest sequence
    sequence_start = 0
    longest_sequence = 0
    index_mapping = {}
    for i in range(len(lyrics)):
        if lyrics[i] in index_mapping:
            sequence_start = max(sequence_start, index_mapping[lyrics[i]] + 1)
        index_mapping[lyrics[i]] = i
        longest_sequence = max(longest_sequence, i - sequence_start + 1)
    print(f"The length of the longest unique sequence in {matches_dict[song_choice]["title"]} is {(longest_sequence)}")



def main():
    print("""Welcome to Mooziq!
Choose one of the options bellow:""")
    
    main_menu = """
1. Get All Artists
2. Get All Albums By An Artist
3. Get Top Tracks By An Artist
4. Export Artist Data
5. Get Released Albums By Year
6. Analyze Song Lyrics
7. Calculate Longest Unique Word Sequence In A Song
8. Weather Forecast For Upcoming Concerts
9. Search Song By Lyrics
10. Exit
"""
    menu_option = None

    while menu_option != 10:
        
        print(main_menu)
        try:
            menu_option = int(input("Type your option:\n"))

            match menu_option:
                case 1:
                    names_ids = get_names_ids()
                    print("Artists found in the database:")
                    get_artists(names_ids)
                case 2:
                    names_ids = get_names_ids()
                    get_artists(names_ids)
                    chosen_artist = get_chosen_artist(names_ids)
                    if chosen_artist in names_ids:
                        unprocessed_albums = get_artist_albums(names_ids, chosen_artist)
                        print(f"Listing all available albums from {chosen_artist}...{format_albums(unprocessed_albums)}")
                case 3:
                    names_ids = get_names_ids()
                    get_artists(names_ids)
                    chosen_artist = get_chosen_artist(names_ids)
                    try:
                        popularity_list = get_tracks(names_ids, chosen_artist)
                        format_tracks(popularity_list, chosen_artist)
                    except KeyError:
                        print()
                case 4:
                    names_ids = get_names_ids()
                    get_artists(names_ids)
                    try:
                        chosen_artist = get_chosen_artist(names_ids)
                        artist_info = get_artist_info(names_ids, chosen_artist)
                        read_write_csv(artist_info, chosen_artist)
                    except KeyError:
                        print()
                case 5:
                    names_ids = get_names_ids()
                    sort_albums_release(names_ids)
                case 6:
                    names_ids = get_names_ids()
                    get_moosed(names_ids)
                case 7:
                    matches_dict = load_song_data()
                    try:
                        song_choice = int(input("Please select one of the following songs (number): "))
                        lyrics = filter_song_lyrics(song_choice, matches_dict)
                        get_longest_sequence(matches_dict, song_choice, lyrics)
                    except ValueError:
                        print("")
                    except TypeError:
                        print("")
                case 8:
                    pass
                case 9:
                    pass
                case 10:
                    print("Thank you for using Mooziq! Have a nice day :)")
                case _:
                    pass

        except ValueError:
            pass
        except TypeError:
            pass

if __name__ == "__main__":
    main()
    