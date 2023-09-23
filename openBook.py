import os
import json

def open_book(vault_path, note_path, epubcfi, json_path, book_path):

    # Open the JSON file
    with open(json_path, 'r') as f:
        # Load the contents of the file into a Python object
        data = json.load(f)
    lastloc = data['lastLocation']
    data['lastLocation'] = epubcfi

    # put a bookmark at the last location
    # check if 'bookmarks' is a key in the json file
    if 'bookmarks' in data.keys():
        bookmarks = data['bookmarks']
        if lastloc not in bookmarks:
            data['bookmarks'].append(lastloc)
    else:
        data['bookmarks'] = [lastloc]
    
    # Overwrite the json file
    with open(json_path, "w") as outfile:
        json.dump(data, outfile)

    # get the path to Foliate
    with open('folder_locations.json', 'r') as f:
        folder_locations = json.load(f)
    run_foliate_path = folder_locations['run_foliate_path']

    # run Foliate
    command = run_foliate_path + " \"" + book_path + "\""  # bash command
    os.system(command)
    #/usr/bin/com.github.johnfactotum.Foliate /home/ondrej/OneDrive/Documents/test_vault/No%20treason-Spooner.epub
                                              #/home/ondrej/OneDrive/Documents/test_vault


if __name__ == '__main__':
    import sys
    #print(sys.argv)
    vault_path, note_path, epubcfi, json_path, book_path = sys.argv[1:]
    open_book(vault_path=vault_path, note_path=note_path, epubcfi=epubcfi, json_path=json_path, book_path=book_path)