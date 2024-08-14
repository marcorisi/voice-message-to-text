# How to run this script: 
# $ (venv/bin/)python3 -m scripts.cli-helper

import os
from db import DB


def show_numbers_of_audio_stored_in_db(db: DB):
    os.system('clear')
    all_records = db.get_all()
    print(f"Number of audio stored in the DB: {len(all_records)}\n")
    input("Press Enter to continue...")

def show_all_items_stored_in_db(db: DB):
    os.system('clear')
    all_records = db.get_all()
    if not all_records:
        print("DB is empty.\n")
        print("Press Enter to continue...")
        input()
        return
    
    print("Printing all the items stored in the DB.\n")
    print("Press Enter to continue or x to exit.\n")
    for record in all_records:
        print(record)
        key = input()
        if key == 'x':
            break

def truncate_db(db: DB):
    os.system('clear')
    print("Are you sure you want to delete all the items stored in the DB? (y/N)")
    answer = input()
    if answer.lower() != 'y':
        return
    db.truncate()
    input("DB cleared. Press Enter to continue...")

def clean_up_storage_folder():
    os.system('clear')
    print("Are you sure you want to delete all the files in the storage folder? (y/N)")
    answer = input()
    if answer.lower() != 'y':
        return
    # Remove all the files in the storage folder, but keep the .gitkeep file
    os.system("find ./storage ! -name '.gitkeep' -type f -exec rm -f {} +")
    input("Storage folder cleaned up. Press Enter to continue...")

def print_command_menu():
    os.system('clear')
    print("How can I help you?")
    print("(1) Show numbers of audio stored in the DB.")
    print("(2) Show all the items stored in the DB.")
    print("(3) Truncate the DB.")
    print("(4) Clean up the storage folder.")
    print("(*) Exit")

def main():
    db = DB()
    
    while True:
        print_command_menu()
        command = input()
        match command:
            case '1':
                show_numbers_of_audio_stored_in_db(db)
            case '2':
                show_all_items_stored_in_db(db)
            case '3':
                truncate_db(db)
            case '4':
                clean_up_storage_folder()
            case _:
                break
        

if __name__ == "__main__":
    main()
