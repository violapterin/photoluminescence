#! /usr/bin/env python3

import os
import json

import porphyrin.aid as AID
import support as SUPPORT



def main()
   # Set constants.
   folder_this = os.path.dirname(__file__)
   folder_in = os.path.join(folder_this, "post-input")
   folder_out = os.path.join(folder_this, "post-output")
   folder_matter = os.path.join(folder_this, "asset")
   folder_site = os.path.join(folder_this, "site")
   folder_site_post = os.path.join(folder_site, "post")
   path_entries = os.path.join(folder_matter, "entries.txt")
   entries = json.loads(path_entries)

   # # Convert posts into HTML.
   # AID.make_new(folder_in, folder_out)
   AID.make_all(folder_in, folder_out)

   # # Combine posts into the body element.
   for entry in entries:
      wholes = []
      date, title = give_date_and_title(entry.name)
      data = {
         date = date,
         title = title,
         tag = entry.tag,
         genre = entry.genre,
      }

      head = write_head(**data)
      header_site = write_header_site(**data)
      write_header_post(**data)
      write_footer(**data)
      wholes.extend(["<html>", "<body>"])
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

def write_head()
   folder_this = os.path.dirname(__file__)
   path_head = os.path.join(folder_this, "asset/head")
   header = AID.input_file(path_header)

def write_header_site()

def write_header_post()

def write_footer()


def get_newest(entries):

def give_date_and_title(name):
   fragments = name.split('-')
   date = ''
   title = ''
   if fragments[0]:
      date = fragments[0]
   if fragments[1]:
      date = fragments[1]
   return date, title

def plug_value(source, values):
   sink = source
   for name, value in values:
      sink = sink.replace(name, value)
    return sink

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

main()