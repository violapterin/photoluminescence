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
   order = lambda entry: entry.get("stamp")
   entries.sort(key = order, reverse = True)

   # # Convert posts into HTML article.
   # AID.make_all(folder_input, folder_output) # XXX
   AID.make_new(folder_input, folder_output)

   # # # # # # # # # # # # # # # #
   # # Combine HTML articles into HTML.
   path_head = os.path.join(folder_matter, "head.html")
   path_header = os.path.join(folder_matter, "header.html")
   path_footer = os.path.join(folder_matter, "footer.html")
   path_item = os.path.join(folder_matter, "item.html")
   head = AID.input_file(path_head)
   header = AID.input_file(path_header)
   footer = AID.input_file(path_footer)
   item = AID.input_file(path_item)

   for entry in entries:
      wholes = []
      heading = entry.get("heading")
      stamp = entry.get("stamp")
      genres = create_group(entry.get("genre"))
      tags = create_group(entry.get("tag"))
      series = entry.get("series")

      items = []
      if stamp is not None:
         items.append(write_element_stamp(stamp))
      if genres is not [None]:
         elements = [write_element_genre(genre) for genre in genres]
         items.extend(elements)
      if tags is not [None]:
      items.extend([write_element_tag(tag) for tag in tags])
      if series is not None:
         items.append(write_element_series(series))
      item = '\n'.join(items)

      element_heading = "<heading>{}</heading>".format(heading)
      head_plugged = head.replace("$TITLE", element_heading)

      month = get_month()

      path_output = ''
      path_post = ''
      for name in os.listdir(folder_output):
         if name.startswith(stamp):
            path_output = os.path.join(folder_output, name)
            bare = name.split('.')[0]
            if not bare:
               continue
            path_post = os.path.join(folder_post, bare + ".html")
            break
      output = AID.input_file(path_output)

      wholes.append("<html>")
      wholes.append(head_plugged)
      wholes.append("<body>")
      wholes.append(header_plugged)
      wholes.append(output)
      wholes.append(footer)
      wholes.append("</body>")
      wholes.append("</html>")
      whole = '\n\n'.join(wholes)
      AID.output_file(path_post, whole)

   # # # # # # # # # # # # # # # #
   # # Write index.
   number_post_max = 16
   number_post_shown = min(number_post_max, len(entries))
   entries_newest = entries[:number_post_shown]
   wholes_home = []
   wholes_home.append("<html>")
   wholes_home.append(head)
   wholes_home.append("<body>")
   wholes_home.append(banner)

   for entry in entries_newest:
      stamp = entry.get("stamp")
      heading = entry.get("heading")
      genres = entry.get("genres")
      tags = entry.get("tags")
      series = entry.get("series")
      name_post = ''
      for name in os.listdir(folder_post):
         if name.startswith(stamp):
            name_post = name
            break

      plug_item(item, data)
      wholes_home.append(plug_item(item, data))

   wholes_home.append(footer)
   wholes_home.append("</body>")
   wholes_home.append("</html>")
   whole_home = '\n\n'.join(wholes_home)
   path_index = os.path.join(folder_site, "index.html")
   AID.output_file(path_index, whole_home)

   # # # # # # # # # # # # # # # #
   # # Update pages.


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def get_day(stamp):
   day = stamp[4:6]
   if (day[0] == '0'):
      day = day[1]
   return day

def get_month(stamp):
   months = {
      "01": "January", "02": "February", "03": "March",
      "04": "April", "05": "May", "06": "June",
      "07": "July", "08": "August", "09": "September",
      "10": "October", "11": "November", "12": "December",
   }
   month = months.get(stamp[2:4])
   return month

def get_year(stamp):
   year = "20" + stamp[0:2]
   return year

def get_date(stamp):
   month = get_month(stamp)
   day = get_day(stamp)
   year = get_year(stamp)
   date = ' '.join([month, day + ',', year])
   return date


def write_heading_post(heading):
   if not heading:
      return None
   sinks = "<h1 class=\"heading-post\">{}</h1>".format(heading)
   return sink

def write_element_stamp(stamp):
   if not stamp:
      return None
   sinks = (
      "<a class=\"data-stamp\"" + ' '
      "href=\"/stamp/{}\">{}</a>"
   ).format(unify_link(get_month(stamp)), date)
   return sink

def write_element_genre(genre):
   if not genre:
      return None
   sink = (
      "<a class=\"data-genre\"" + ' '
      "href=\"/genre/{}\">{}</a>"
   ).format(unify_link(genre), genre)
   return sink

def write_element_tag(tag):
   if not tag:
      return None
   sink = (
      "<a class=\"data-tag\"" + ' '
      "href=\"/tag/{}\">{}</a>"
   ).format(unify_link(genre), genre)
   return sink

def write_element_series(series):
   if not series:
      return None
   sink = (
      "<a class=\"data-series\"" + ' '
      "href=\"/series/{}\">{}</a>"
   ).format(unify_link(series), series)
   return sink

def unify_link(source):
   sink = lower(source)
   sink = sink.replace(' ', '-')
   return sink

def create_group(item):
   group = []
   if (isinstance(group, list)):
      group = item
   else:
      group = [item]
   return group


'''
def join_with_comma(items):
   item = ''
   if (isinstance(items, list)):
      item = ", ".join(items)
   else:
      item = items
   return item

def plug_item(source, values):
   keys = {
      "$NAME",
      "$STAMP",
      "$TITLE",
      "$GENRES",
      "$TAGS",
      "$SERIES",
   }
   values_part = {key: values.get(key) for key in keys}
   sink = plug_value(source, values_part)
   return sink

def plug_header(source, values):
   keys = {
      "$STAMP",
      "$TITLE",
      "$GENRES",
      "$TAGS",
      "$SERIES",
   }
   values_part = {key: values.get(key) for key in keys}
   sink = plug_value(source, values_part)
   return sink

def plug_head(source, values):
   keys = {
      "$TITLE",
   }
   values_part = {key: values.get(key) for key in keys}
   sink = plug_value(source, values_part)
   return sink

def plug_value(source, values):
   sink = source
   for key, value in values.items():
      if not key:
         continue
      if not value:
         sink = sink.replace(key, '')
      else:
         sink = sink.replace(key, value)
   return sink
'''

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

main()