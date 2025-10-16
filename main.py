import re, string

from data_loader import *

DIRECTORY = os.path.dirname(os.path.abspath(__file__)) # directory constat since the filepath up to dataset will always be the same

# Task 1

def get_artists(names_ids):

    for artists in names_ids:
        print(f"- {artists}")

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
            release_date_precision = unprocessed_albums[i]["release_date_precision"]

            if release_date_precision == "year":

                year = release_date[:4]

                all_albums += f"\n- \"{album}\" was released in {year}."

            elif release_date_precision == "month":

                year = release_date[:4]
                month = int(release_date[5:7])
                month = list_months[month - 1]

                all_albums += f"\n- \"{album}\" was released in {month} {year}."

            elif release_date_precision == "day":

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

                all_albums += f"\n- \"{album}\" has no release date."

    return all_albums

#Task 3
    
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

        print(f"- \"{song}\" has a popularity score of {popularity}. {message}")

# Task 4

def get_num_tracks(names_ids, artist_info, chosen_artist, amount_tracks):
    track_popularity = get_tracks(names_ids, chosen_artist)
 
    for i in range(0, amount_tracks):
        artist_info.append(track_popularity[i][0])

def get_artist_info(names_ids, chosen_artist):

    artist_info = list()
    artist_info.append(names_ids[chosen_artist])
    artist_info.append(chosen_artist)
    artist_info.append(len(get_artist_albums(names_ids, chosen_artist)))

    get_num_tracks(names_ids, artist_info, chosen_artist, 2)

    artist_info.append(get_genres(chosen_artist))

    return artist_info

# Task 5

def load_albums_year(names_ids):
    try:
        search_year = int(input("Please enter a year: \n"))
        albums_list = sort_albums(names_ids, search_year)
        if search_year >= 0:
            print(f"Albums released in the year {search_year}:")
            if len(albums_list) == 0:
                print(f"No albums were released in the year {search_year}.")
            else:  
                for albums, artist in albums_list:
                    print(f"- \"{albums}\" by {artist}.")
        else:
            print("Invalid input. Please type a positive integer as year.")
    except ValueError:
        print("Invalid input. Please input a positive integer as year.")

# Task 6

def get_moosed(matches_dict):
    try:
        user_song = int(input(f"Please select one of the following songs (number): "))
    
        if user_song <= len(matches_dict) and user_song > 0:
            lyric = matches_dict[user_song]["lyrics"]

            pattern = "mo"
            repl = "moo"
            lyric = re.sub(pattern, repl, lyric)

            lyric = re.sub(r"\b\w+(?=[!?])", repl, lyric)

            if matches_dict[user_song]["lyrics"] == lyric:
                print(f"{matches_dict[user_song]["title"]} by {matches_dict[user_song]["artist"]} is not moose-compatible!")
            else:
                print(f"{matches_dict[user_song]["title"]} by {matches_dict[user_song]["artist"]} has been moos-ified!")
            
            try:
                os.mkdir("./moosified")
            except:
                moosed_folder_exists = True
            
            song_path = matches_dict[user_song]["title"]+" Moosified.txt"
            file_path = os.path.join("moosified", song_path)
                        
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(lyric)

            print(f"File saved at ./moosified/{matches_dict[user_song]["title"]} Moosified.txt")
            print(" ___            ___")
            print("/   \\          /   \\")
            print("\\_   \\        /  __/")
            print(" _\\   \\      /  /__")
            print(" \\___  \\____/   __/")
            print("     \\_       _/")
            print("       | @ @  \\__")
            print("       |")
            print("     _/     /\\")
            print("    /o)  (o/\\ \\__")
            print("    \\_____/ /")
            print("      \\____/")
    
    except ValueError:
        print()

    return

# Task 7

def filter_song_lyrics(song_choice, matches_dict):
    if song_choice not in matches_dict:
        lower_lyrics_split = None

    else:
        lyrics = matches_dict[song_choice]["lyrics"]
        lower_lyrics = lyrics.lower()
        lower_lyrics_filtered = re.sub(f"[{re.escape(string.punctuation)}]", "", lower_lyrics)
        lower_lyrics_split = lower_lyrics_filtered.split()
        return lower_lyrics_split
    
def get_longest_sequence(matches_dict, song_choice, lyrics):
    sequence_start = 0
    longest_sequence = 0
    index_mapping = {}
    for i in range(len(lyrics)):
        if lyrics[i] in index_mapping:
            if index_mapping[lyrics[i]] + 1 > sequence_start:
                sequence_start = index_mapping[lyrics[i]] + 1
        index_mapping[lyrics[i]] = i

        current_length = i - sequence_start + 1
        if current_length > longest_sequence:
            longest_sequence = current_length
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
                    try:
                        unprocessed_albums = get_artist_albums(names_ids, chosen_artist)
                        print(f"Listing all available albums from {chosen_artist}...{format_albums(unprocessed_albums)}")
                    except KeyError:
                        print()
                case 3:
                    names_ids = get_names_ids()
                    get_artists(names_ids)
                    chosen_artist = get_chosen_artist(names_ids)
                    try:
                        track_popularity = get_tracks(names_ids, chosen_artist)
                        format_tracks(track_popularity, chosen_artist)
                    except KeyError:
                        print("error handling")
                case 4:
                    names_ids = get_names_ids()
                    get_artists(names_ids)
                    try:
                        chosen_artist = get_chosen_artist(names_ids)
                        artist_info = get_artist_info(names_ids, chosen_artist)
                        read_write_csv(artist_info, chosen_artist)
                    except KeyError:
                        print("error handling")
                case 5:
                    names_ids = get_names_ids()
                    load_albums_year(names_ids)
                case 6:
                    matches_dict = load_song_data()
                    get_moosed(matches_dict)
                case 7:
                    matches_dict = load_song_data()
                    try:
                        song_choice = int(input("Please select one of the following songs (number): \n"))
                        lyrics = filter_song_lyrics(song_choice, matches_dict)
                        if lyrics == None:
                            print("Error. Please input a number from the list of songs above.")
                        else:
                            get_longest_sequence(matches_dict, song_choice, lyrics)
                    except ValueError:
                        print("Error. Please input a positive integer instead.")
                case 8:
                    pass
                case 9:
                    pass
                case 10:
                    print("Thank you for using Mooziq! Have a nice day :)")
                case _:
                    print("error handling")

        except ValueError:
            print("error handling")
        except TypeError:
            print("error handling")

if __name__ == "__main__":
    main()
    