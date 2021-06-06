#! /usr/bin/env python3

import os
import json
import re

import porphyrin.aid as AID


def main():
   # Set folders.
   folder_this = os.path.dirname(__file__)
   folder_input = os.path.join(folder_this, "post-input")
   folder_output = os.path.join(folder_this, "post-output")
   folder_matter = os.path.join(folder_this, "matter")
   folder_site = os.path.join(folder_this, "site")
   folder_post = os.path.join(folder_site, "post")

   # Set entries.
   path_entries = os.path.join(folder_matter, "entries.json")
   text_entries = AID.input_file(path_entries)
   entries = json.loads(text_entries)
   entries = [entry for entry in entries if entry is not None]
   #order = (lambda entry: entry.get("date"))
   entries.sort(key = lambda entry: entry.get("date"), reverse = True)

   # # Convert posts into HTML article.
   AID.make_new(folder_input, folder_output)

   # # Combine HTML articles into HTML.
   for entry in entries:
      wholes = []
      date = entry.get("date")
      title = entry.get("title")
      genres = entry.get("genres")
      tags = entry.get("tags")
      series = entry.get("series")
      data = {
         "date": date,
         "title": title,
         "genres": genres,
         "tags": tags,
         "series": series,
      }

      path_post = ''
      for name in os.listdir(folder_output):
         if name.startswith(date):
            path_post = os.path.join(folder_output, name)
            break
      if not path_post:
         continue
      path_head = os.path.join(folder_matter, "head.html")
      path_header = os.path.join(folder_matter, "header.html")
      path_footer = os.path.join(folder_matter, "footer.html")

      post = AID.input_file(path_post)
      head = AID.input_file(path_head)
      header = AID.input_file(path_header)
      footer = AID.input_file(path_footer)

      data = {
         "$DATE_POST": get_text_date(date),
         "$TITLE_POST": title,
         "$GENRES_POST": join_with_comma(genres),
         "$TAGS_POST": join_with_comma(tags),
         "$SERIES_POST": join_with_comma(series),
      }
      head = plug_head(head, data)
      header = plug_header(header, data)

      wholes.append("<html>")
      wholes.append(head)
      wholes.append("<body>")
      wholes.append(header)
      wholes.append(post)
      wholes.append(footer)
      wholes.append("</body>")
      wholes.append("</html>")
      whole = '\n'.join(wholes)
      AID.output_file(path_post, whole)

   # # Write index.
   number_post_shown = min(16, len(entries))
   entries_newest = entries[:number_post_shown]
   wholes_home = []
   for entry in entries_newest:
      date = entry.get("date")
      title = entry.get("title")
      name_post = ''
      for name in os.listdir(folder_output):
         if name.startswith(date):
            name_post = os.path.join(folder_output, name)
            break
      if not name_post:
         continue
      item_class = "class=\"item-newest\""
      item_href = "<a  href=\"/post/{}\">".format(name_post)
      item_format = "<a {} {}>{}</a>"
      item = item_format.format(item_class, item_href, title)
      wholes_home.append(item)
   whole_home = '\n'.join(wholes_home)
   print("whole_home:", whole_home) # XXX
   path_index = os.path.join(folder_site, "index.html")
   AID.output_file(path_index, whole_home)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def get_text_date(date):
   months = {
      "01": "January", "02": "February", "03": "March",
      "04": "April", "05": "May", "06": "June",
      "07": "July", "08": "August", "09": "September",
      "10": "October", "11": "November", "12": "December",
   }
   year = "20" + date[0:2]
   month = months.get(date[2:4])
   day = date[4:6]
   if (day[0] == '0'):
      day = day[1]
   text = ' '.join([month, day + ',', year])
   return text

def join_with_comma(items):
   item = ''
   if (isinstance(items, list)):
      item = ", ".join(items)
   else:
      item = items
   return item


def plug_header(source, values):
   keys = {
      "$DATE_POST",
      "$TITLE_POST",
      "$GENRES_POST",
      "$TAGS_POST",
      "$SERIES_POST",
   }
   values_part = [{key: values.get(key)} for key in keys]
   sink = plug_value(source, values_part)
   return sink

def plug_head(source, values):
   keys = {
      "$TITLE_POST",
   }
   values_part = [{key: values.get(key)} for key in keys]
   sink = plug_value(source, values_part)
   return sink

def plug_value(source, values):
   print(values)
   sink = source
   for key, value in values:
      if not key:
         continue
      sink = sink.replace(key, value)
   return sink

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

main()