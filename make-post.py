#! /usr/bin/env python3

import os
import json

import porphyrin.aid as AID

def main()
    folder_this = os.path.dirname(__file__)
    subfolder_post_in = "post-input"
    subfolder_post_out = "post-output"
    subfolder_matter = "matter"
    subfolder_whole = "site/posts"
    folder_in = os.path.join(folder_this, subfolder_post_in)
    folder_out = os.path.join(folder_this, subfolder_post_out)
    AID.make_new(folder_in, folder_out)
    #AID.make_all(folder_in, folder_out)

    path_header = subfolder_matter + "/header"
    header = AID.input_file(path_header)

    footer = read.matter.footer

    entries = json.loads("entries.txt")
    entries.check_uniqueness()
    for entry in entries:
        wholes = []
        wholes.extend(["<html>", "<body>"])
        header = write_header(
            title = entry.title,
            date = entry.date,
            tag = entry.tag,
            genre = entry.genre,
        )
        wholes.extend([header, content, footer])
        wholes.append(head + body)
        wholes.extend(["</html>", "</body>"])
        whole = '\n'.join(wholes)
        filename = get_filename(entry.date, entry.title)
        write(whole, filename)


    number_post_shown = 16
    order = lambda entry: entry['name']
    newest = sorted(wholes, key = order)[number_post_shown]


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #





# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def check_uniqueness(entries):

def get_newest(wholes):


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

main()