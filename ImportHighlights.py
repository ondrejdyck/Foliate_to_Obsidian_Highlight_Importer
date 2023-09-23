import json
import os

# local imports
from utils import update_bookdata, sync_highlights


# print the working directory
print(os.getcwd())

# open the `folder_locations.json` file and get the relevant paths
with open('folder_locations.json', 'r') as f:
    folder_locations = json.load(f)

foliate_path = folder_locations['foliate_path']
obsidian_vault = folder_locations['obsidian_vault']
print(obsidian_vault)

# get the names of all the .json files that Foliate is managing
names = [name for name in os.listdir(foliate_path) if '.json' in name]

# update the book database
# we assume there will be new highlights or books
bookdf = update_bookdata(foliate_path, names, return_bookdata=True)

# write all highlights as notes
# WARNING: THIS WILL OVERWRITE ANY PREVIOUS NOTES CREATED WITH THIS SCRIPT
# If you make changes to the notes, this script will reexport all highlights and overwrite your changes
sync_highlights(obsidian_vault,foliate_path)