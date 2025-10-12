import json, os

def fix_capitalization(names_ids, chosen_artist):
    for key in names_ids:   #perhaps find different way since it doesnt need to iterate thru the whole list every time.
        if chosen_artist.lower() == key.lower():
            chosen_artist = key
    #while chosen_artist not in names.ids:
    #    if chosen_artist.lower() == names.ids.lower()
    #       chosen_artist = names.ids
    return chosen_artist
    
def get_artist_albums(names_ids, chosen_artist):  

    directory = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(directory, "dataset/albums/")
    

    with open(os.path.join(folder_path, names_ids[chosen_artist] + ".json"), "r", encoding="UTF-8") as jsonfile: # + ".json" because the value if just the id without the .json

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

                all_albums += f"\n\"{album}\" was released in {year}."

            elif len(release_date) == 7:

                year = release_date[:4]
                month = int(release_date[5:7])
                month = list_months[month - 1]

                all_albums += f"\n\"{album}\" was released in {month} {year}."

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

                all_albums += f"\n\"{album}\" is not none when it was released."


    return all_albums



names_ids = get_artist_info("name", "id")
chosen_artist = input("Please input the name of an artist: ")
chosen_artist = fix_capitalization(names_ids, chosen_artist)

if chosen_artist in names_ids:
    unprocessed_albums = get_artist_albums(names_ids, chosen_artist)
    print(f"Listing all available albums from {chosen_artist}...{format_albums(unprocessed_albums)}")  


