# How to run this script: 
# $ python3 -m scripts.db-helper

import os
from db import DB


def show_numbers_of_audio_stored_in_db(db: DB):
    os.system('clear')
    all_records = db.get_all()
    print(f"Number of audio stored in the DB: {len(all_records)}\n")
    input("Press Enter to continue...")

def print_command_menu():
    os.system('clear')
    print("How can I help you?")
    print("(1) Show numbers of audio stored in the DB.")
    print("(*) Exit")

def main():
    db = DB()
    print_command_menu()
    
    while True:
        print_command_menu()
        command = input()
        match command:
            case '1':
                show_numbers_of_audio_stored_in_db(db)
            case _:
                break
        

if __name__ == "__main__":
    main()
