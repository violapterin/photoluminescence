#! /usr/bin/env python3

import os
import json

import porphyrin.aid as AID


def main()
   # Set constants.
   folder_this = os.path.dirname(__file__)
   folder_input = os.path.join(folder_this, "post-input")
   folder_output = os.path.join(folder_this, "post-output")
   folder_matter = os.path.join(folder_this, "matter")
   folder_site = os.path.join(folder_this, "site")
   folder_post = os.path.join(folder_site, "post")
   path_entries = os.path.join(folder_matter, "entries.txt")
   entries = json.loads(path_entries)

   # # Convert posts into HTML article.
   # AID.make_new(folder_in, folder_out)
   AID.make_all(folder_input, folder_output)

   # # Combine HTML articles into HTML.
   for entry in entries:
      wholes = []
      date = entry.date
      tags = entry.tags
      genre = entry.genre
      title = entry.title
      data = {
         date = date,
         tags = tags,
         genre = genre,
         title = title,
      }

      name_post = give_name(date, title)
      path_post = os.path.join(folder_output, name_post)
      path_head = os.path.join(folder_matter, "head")
      path_header = os.path.join(folder_matter, "head")
      path_footer = os.path.join(folder_matter, "head")
      values_head = {
         "$TITLE_POST": title,
      }
      values_header = {
         "$TITLE_POST": title,
         "$DATE_POST": get_text_date(date),
         "$TAGS_POST": tags,
         "$GENRE_POST": genre,
      }
      post = AID.input_file(whole, path_post)
      head = AID.input_file(path_head)
      header = AID.input_file(path_header)
      footer = AID.input_file(path_footer)
      head = plug_values(head, values_head)
      header = plug_values(head, values_header)

      wholes.append("<html>")
      wholes.append(head)
      wholes.append("<body>")
      wholes.append(header)
      wholes.append("<article class=\"post\">")
      wholes.append(post)
      wholes.append("</article>")
      wholes.append(footer)
      wholes.append("</body>")
      wholes.append("</html>")
      whole = '\n'.join(wholes)
      AID.output_file(whole, path_post)

   # # Write index.
   number_post_shown = 16
   order = lambda entry: entry['name']
   newest = sorted(entries, key = order)[number_post_shown]
   wholes_home = []
   for entry in newest:
      date, title = give_date_and_title(entry.name)
      name_post = give_name(date, title)
      item_class = "class=\"item-newest\""
      item_href = "<a  href=\"/post/{}\">".format(name_post)
      item_format = "<a {} {}> {} </a>"
      item = item_format.format(item_class, item_href, name_post)
      print("item:", item) # XXX
      wholes_home.append(item)
   whole_home = '\n'.join(wholes_home)
   path_index = os.path.join(folder_site, "index.html")
   AID.output_file(whole_home, path_index)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

   '''
def write_head(**data, head)
   date = data.date
   title = data.title
   tag = data.tag
   genre = data.genre

def write_header(**data, header)
   date = data.date
   title = data.title
   tag = data.tag
   genre = data.genre

def write_footer(**data, footer)
   date = data.date
   title = data.title
   tag = data.tag
   genre = data.genre
   '''

def give_text_date(date):
   months = {
      "01": "January", "02": "February", "03": "March",
      "04": "April", "05": "May", "06": "June",
      "07": "July", "08": "August", "09": "September",
      "10": "October", "11": "November", "12": "December",
   }
   month = months.get(date[0:2])
   day = date[2:4]
   if (day[0] = '0'):
      day = day[1]
   year = "20" + date[4:6]
   text = ' '.join([month, day + ',', year])
   return text

def get_name(date, title)
   fragments = title.split(/[^A-Za-z0-9]/)
   fragments.extend(['', '', ''])
   sink = '-'.join(fragments[0:3])
   return sink

def plug_value(source, values):
   sink = source
   for name, value in values:
      sink = sink.replace(name, value)
    return sink

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

main()