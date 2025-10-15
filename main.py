import json, os
import re
from loaders import get_names_ids, load_song_data
DIRECTORY = os.path.dirname(os.path.abspath(__file__)) # directory constat since the filepath up to dataset will always be the same

'''
Hello evvryboda!
The get_files() and get_names_ids() are functions that can be used for multiple tasks 
so try to use them for as much as you can
PS, the get_names_ids() saves names as keys and ids as value. 
If you want to use the ids as filenames you need to include ".json" in the filepath ;)
'''
def get_files(folder): 

    folder_path = os.path.join(DIRECTORY, "dataset" , folder)

    all_filenames = []
    sorted_filenames = []

    for filename in os.listdir(folder_path): #iteratis over all the files in the directory and append them in a list
        all_filenames.append(filename)
    sorted_filenames = sorted(all_filenames)

    return sorted_filenames

def fix_capitalization(names_ids, chosen_artist):
    for key in names_ids:   #perhaps find different way since it doesnt need to iterate thru the whole list every time.
        if chosen_artist.lower() == key.lower():
            chosen_artist = key

    return chosen_artist

# Task 1

def get_artists(names_ids):
    print("Artists found in the database: \n")
    for artists in names_ids:
        print(f"- {artists}")
       
def get_artist_albums(names_ids, chosen_artist):  

    folder_path = os.path.join(DIRECTORY, "dataset/albums/")
    
    with open(os.path.join(folder_path, names_ids[chosen_artist] + ".json"), "r", encoding="UTF-8") as jsonfile:

        data = json.load(jsonfile)

    unprocessed_albums = data["items"]

    return unprocessed_albums

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

def get_top_tracks(names_ids):
    
    folder_path = os.path.join(DIRECTORY, "dataset/top_tracks/")
    user_artist = input(f"Please input the name of an artist: ")
    popularity_list = [] 
    artist_exists = False

    for artist_name in names_ids.keys():
        if artist_name.lower() == user_artist.lower():
            user_artist = artist_name
            artist_exists = True
            
    if artist_exists == True:
        with open(os.path.join(folder_path, names_ids[user_artist] + ".json"), "r", encoding="UTF-8") as jsonfile:
            data = json.load(jsonfile)
        
        print(f"Listing top tracks for {user_artist}...")

        for track in data['tracks']:
            popularity_list.append((track['name'], track['popularity']))

        for song, popularity in popularity_list:
            if popularity <= 30:
                text = "No one knows this song."
            elif popularity <= 50:
                text = "Popular song."
            elif popularity <= 70:
                text = "It is quite popular now!"
            elif popularity >= 71:
                text = "It is made for the charts!"

            print(f'- "{song}" has a popularity score of {popularity}. {text}')

    return popularity_list

# Task 5

def sort_albums_release(names_ids):
    search_year = input("What year?: ")
    print(f"Albums released in the year {search_year}:")
    reversed_dict = {value: key for key, value in names_ids.items()} # Reverses the dictionary so value (id) becomes key.
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



def main():

    main_menu = """
Welcome to Mooziq!
Choose one of the options bellow:

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
        menu_option = input("Type your option: ")

        if menu_option.isdigit():
            
            menu_option = int(menu_option)
            match menu_option:
                case 1:
                    names_ids = get_names_ids()
                    get_artists(names_ids)
                case 2:
                    names_ids = get_names_ids()
                    chosen_artist = input("Please input the name of an artist: ")
                    chosen_artist = fix_capitalization(names_ids, chosen_artist)

                
                    if chosen_artist in names_ids:
                        unprocessed_albums = get_artist_albums(names_ids, chosen_artist)
                        print(f"Listing all available albums from {chosen_artist}...{format_albums(unprocessed_albums)}")          
                case 3:
                    names_ids = get_names_ids()
                    get_artists(names_ids)
                    get_top_tracks(names_ids)
                case 4:
                    pass
                case 5:
                    names_ids = get_names_ids()
                    sort_albums_release(names_ids)
                case 6:
                    pass
                case 7:
                    get_longest_sequence()
                case 8:
                    pass
                case 9:
                    pass
                case 10:
                    print("Thank you for using Mooziq! Have a nice day :)")
                case _:
                    print("ERROR HANDLING")
        
        else:
            print("ERROR HANDLING")

if __name__ == "__main__":
    main()
    