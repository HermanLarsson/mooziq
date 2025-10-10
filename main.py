import json, os



def get_artist_info(info_one, info_two): # Maybe change names. Cant think of anything else now

    directory = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(directory, "dataset/artists/")

    all_filenames = []
    sorted_filenames = []
    dict_artist_info = {}

    for filename in os.listdir(folder_path): #iteratis over all the files in the directory and append them in a list
        all_filenames.append(filename)

    sorted_filenames = sorted(all_filenames)

    for filename in sorted_filenames: 
        with open(os.path.join(folder_path, filename),"r") as file: 
            data = json.load(file)

            dict_artist_info[data[info_one]] = data[info_two] + ".json" #add the info_one as key and the info_two as value

    return dict_artist_info




def fix_capitalization(names_ids, chosen_artist):
    for key in names_ids:   #perhaps find different way since it doesnt need to iterate thru the whole list every time.
        if chosen_artist.lower() == key.lower():
            chosen_artist = key
    #while chosen_artist not in names.ids:
    #    if chosen_artist.lower() == names.ids.lower()
    #       chosen_artist = names.ids
    return chosen_artist
    
def get_albums(names_ids, chosen_artist):  

    directory = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(directory, "dataset/albums/")
    

    with open(os.path.join(folder_path, names_ids[chosen_artist]), "r", encoding="UTF-8") as jsonfile:

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
        if unprocessed_albums[i]["album_type"] == "album":
            album = unprocessed_albums[i]["name"]
            release_date = unprocessed_albums[i]["release_date"]
#make the release date to function

            if len(release_date) == 4:

                year = release_date[:4]

                all_albums += f"\n\"{album}\" was released in {year}"

            elif len(release_date) == 7:

                year = release_date[:4]
                month = int(release_date[5:7])
                month = list_months[month - 1]

                all_albums += f"\n\"{album}\" was released in {month} {year}"

            elif len(release_date) == 10:

                year = release_date[:4]
                month = int(release_date[5:7])
                month = list_months[month - 1]
                day = int(release_date[8:])

                all_albums += f"\n\"{album}\" was released in {month} {day}th {year}"

            else: 

                all_albums += f"\n\"{album}\" is not none when it was released"


    return all_albums

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
                    names_ids = get_artist_info("name", "id") #pass two parameters
                    #function to print names from names_ids :)
                case 2:
                    names_ids = get_artist_info("name", "id")
                    chosen_artist = input("Please input the name of an artist: ")
                    chosen_artist = fix_capitalization(names_ids, chosen_artist)

                    unprocessed_albums = get_albums(names_ids, chosen_artist)
                
                    if chosen_artist in names_ids:
                        print(f"Listing all available albums from {chosen_artist}...{format_albums(unprocessed_albums)}")          

                case 3:
                    pass
                case 4:
                    pass
                case 5:
                    pass
                case 6:
                    pass
                case 7:
                    pass
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
    