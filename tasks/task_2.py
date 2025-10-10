import json, os

#rel_path = "../dataset/artists" #relative path from tasks, needs to be changed for main.py
#all_filenames = []
#sorted_filenames = []
#names_ids = {}
#names_formatted = ""
#
#for filename in os.listdir(rel_path): #iteratis over all the files in the directory and save them
#    all_filenames.append(filename)
#
#sorted_filenames = sorted(all_filenames)
#
#for filename in sorted_filenames:
#    with open(os.path.join(rel_path, filename),"r") as jsonfile: 
#        data = json.load(jsonfile)
#
#        names_ids[data["name"]] = data["id"] + ".json" #add the names as key and the id as value to make the later tasks easier
#
#for name in names_ids:
#    names_formatted += f"\n- {name}"



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

    for i in range(len(all_albums)):
        if all_albums[i]["album_type"] == "album":
            album = all_albums[i]["name"]
            release_date = all_albums[i]["release_date"]
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



chosen_artist = input("Please input the name of an artist: ")
chosen_artist = fix_capitalization(names_ids, chosen_artist)

unprocessed_albums = get_albums(names_ids, chosen_artist)
format_albums(unprocessed_albums)

if chosen_artist in names_ids:
    print(f"Listing all available albums from {chosen_artist}...{format_albums(unprocessed_albums)}")


