import datetime, csv, os

DIRECTORY = os.path.dirname(os.path.abspath(__file__)) # constat since the filepath up to dataset will always be the different for users

def get_performing_artists():


    with open(os.path.join(DIRECTORY, "dataset", "concerts", "concerts.csv"), "r", encoding="UTF-8") as file:
        all_concerts = csv.DictReader(file)
        artists = list()

        for row in all_concerts:
            if row["artist"] not in artists:
                artists.append(row["artist"])
        
        for i in range(len(artists)):
            print(artists[i])
                
                 

def get_concerts():
    artist_concerts = list()
    chosen_artist = input("Please input the name of one of the following artists: ")

    with open(os.path.join(DIRECTORY, "dataset", "concerts", "concerts.csv"), "r", encoding="UTF-8") as file:
        all_concerts = csv.DictReader(file)

        for row in all_concerts:
            if row["artist"].lower() == chosen_artist.lower():
                 artist_concerts.append(row)
    
    return artist_concerts

def get_weather(artist_concerts):
    with open(os.path.join(DIRECTORY, "dataset", "weather", "weather.csv"), "r", encoding="UTF-8") as file:
        data = csv.reader(file)
        header = next(data)
        weather_info = list(data)

        for concert in artist_concerts:

            concert_date = str(datetime.date(int(concert["year"]), int(concert["month"]), int(concert["day"])))
            for row in weather_info:
                if concert_date == row[1]:
                    if concert["city_code"] == row[3]:
                        concert["weather"] = row
    
    return artist_concerts
                             

def format_date(date, date_precision):

    month_names = {   
    1: "January", 2: "February", 3: "March", 
    4: "April", 5: "May", 6: "June", 
    7: "July", 8: "August", 9: "September", 
    10: "October", 11: "November", 12: "December"
    }
    formatted_date = tuple()
    if date_precision == "year":

        year = date[:4]
        formatted_date = (year)

    elif date_precision == "month":

        year = date[:4]
        month = int(date[5:7])
                    
        formatted_date = (year, month_names[month])

    elif date_precision == "day":
    
        year = date[:4]
        month = int(date[5:7])
        day = date[8:]

        if day[len(day) - 1] == "1" and day != "11":
            suffix = "st"
        elif day[len(day) - 1] == "2" and day != "12":
            suffix = "nd"
        elif day[len(day) - 1] == "3" and day != "13":
            suffix = "rd"
        else:
            suffix = "th"

        day = int(day)    #To remove the zero it starts with zero
        
        day = str(day) + suffix

        formatted_date = (year, month_names[month], day)

    else: 
        formatted_date = None

    return formatted_date


#If the minimum temperature is lower or equal than 10°C, append “Wear warm clothes.”.
#If precipitation is greater or equal than 2.3mm and the wind speed is less than 15 km/h, 
#	append “Bring an umbrella.”
#If precipitation is greater or equal than 2.3mm and the wind speed is greater or equal than 15 km/h,  append “Bring a rain jacket.”
#If the minimum temperature is greater than 10°C and the precipitation is less than 2.3mm, append “Perfect weather!”.

#Gothenburg, September 22nd 2025. Wear warm clothes. Bring an umbrella.

def check_weather(concerts):
    all_concerts = ""
    for concert in concerts:
        formatted_date = format_date(concert["weather"][1], "day")
        message = ""

        if int(concert["weather"][6]) <= 10:
            message += "Wear warm clothes. "

        elif int(concert["weather"][6]) > 10 and float(concert["weather"][0]) < 2.3:
            message += "Perfect weather!"

        if float(concert["weather"][0]) >= 2.3 and int(concert["weather"][8]) < 15:
            message += "Bring an umbrella."

        elif float(concert["weather"][0]) >= 2.3 and int(concert["weather"][8]) >= 15:
            message += "Bring an rain jacket."

        all_concerts += f"\n- {concert["weather"][2]}, {formatted_date[1]} {formatted_date[2]} {formatted_date[0]}. {message}"

    return all_concerts


#case 8:
get_performing_artists()
artist_concerts = get_concerts()
concerts_weather = get_weather(artist_concerts)
print(f"Fetching weather forecast for \"{artist_concerts[0]["artist"]}\" concerts...")
print(f"{artist_concerts[0]["artist"]} has {len(artist_concerts)} upcoming concerts: {check_weather(concerts_weather)}")