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
                    pass
                case 2:
                    pass
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
    