import json
import pandas as pd
import os
import re
import urllib.parse

def update_bookdata(folder, names, return_bookdata=False):
    book_metadata = {'title':[], 'author':[], 'identifier':[], 'name':[], 'has_highlights':[]}

    # Get the Foliate library data
    # This has the ebpub identifier and path location
    with open(folder+'/library/uri-store.json', 'r') as f:
        libdata = json.load(f)
    

    # Gather data we are interested in
    for name in names:
        # Open the JSON file
        with open(folder+'/'+name, 'r') as f:
            # Load the contents of the file into a Python object
            data = json.load(f)

        book_metadata['title'].append(data['metadata']['title'])
        book_metadata['author'].append(data['metadata']['creator'])
        book_metadata['identifier'].append(data['metadata']['identifier'])
        book_metadata['name'].append(name)

        # Check if annotations are present
        if 'annotations' in data:
            # The field is present
            book_metadata['has_highlights'].append('True')
        else:
            # The field is not present
            book_metadata['has_highlights'].append('False')

    df = pd.DataFrame(book_metadata)

    df['path'] = float('nan')
    for item in libdata['uris']:
        # Remove 'file://' prefix from item[1] string
        path = item[1].replace('file://', '')
        path = urllib.parse.unquote(path)
        df.loc[df['identifier'] == item[0], 'path'] = path
    df.to_csv('bookData.csv', index=False)

    if return_bookdata:
        return df
    else:
        return

def get_highlights(path):
    with open(path, 'r') as f:
        json_data = json.load(f)

    if 'annotations' not in json_data.keys():
        return 0
    else:
        return json_data['annotations']
    
def sync_highlights(vault_path, foliate_path, bookdf=0):
    if bookdf==0:
        filename = 'bookData.csv'
        if os.path.exists(filename):
            bookdf = pd.read_csv(filename)
        else:
            raise FileNotFoundError('The bookData.csv file has not been created yet.')
            

    highlights_path = os.path.join(vault_path, 'highlights')

    # Check if the 'highlights' directory exists, and create it if it doesn't
    if not os.path.exists(highlights_path):
        os.makedirs(highlights_path)
        print("Created 'highlights' directory in 'vault' folder.")


    for index, row in bookdf.iterrows():
        if row['has_highlights']==True:
            #print(row)
            # remove any characters that are not letters or numbers
            title = re.sub(r'[^a-zA-Z0-9]+', '_', row['title'])
            book_path = os.path.join(highlights_path, title)
            if not os.path.exists(book_path):
                os.makedirs(book_path)

            fname = row['name']
            p = os.path.join(foliate_path, fname)
            highlights = get_highlights(p)
            for i, highlight in enumerate(highlights):
                epubcfi = highlight['value']
                text = highlight['text']

                # write markdown note
                fname = book_path+'/'+str(i)+'-'+title+'.md'
                with open(fname, 'w') as f:
                    f.write('Title: '+row['title']+'\n')
                    #print(index)
                    #print(row['author'])
                    f.write('Author: '+str(row['author'])+'\n')
                    #f.write('Location: '+loc+'\n')
                    f.write('\n')
                    f.write('> '+text)
                    f.write('\n')
                    f.write('\n')
                    f.write('Click `run` below to open the quote in the book.\n')
                    f.write('```run-shell\n')
                    f.write('cd @vault_path/.scripts\n')#/home/ondrej/OneDrive/Documents/test_vault\n')
                    json_path = os.path.join(foliate_path, row['name'])
                    f.write('python openBook.py @vault_path @note_path \"'+epubcfi+'\" '+json_path+' \"'+row['path']+'\"')
                    f.write('\n```')
                    f.write('\n')
                    f.write('#review')