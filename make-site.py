#! /usr/bin/env python3

import os
import json
import re

import porphyrin.aid as AID


def main():
   # Set constants.
   folder_this = os.path.dirname(__file__)
   folder_input = os.path.join(folder_this, "post-input")
   folder_output = os.path.join(folder_this, "post-output")
   folder_matter = os.path.join(folder_this, "matter")
   folder_site = os.path.join(folder_this, "site")
   folder_post = os.path.join(folder_site, "post")
   path_entries = os.path.join(folder_matter, "entries.json")
   entries = json.loads(AID.input_file(path_entries))
   entries = [entry for entry in entries if entry is not None]
   order = lambda entry: entry.get("stamp")
   entries.sort(key = order, reverse = True)

   path_head = os.path.join(folder_matter, "head.html")
   head = AID.input_file(path_head)
   path_banner = os.path.join(folder_matter, "header-post.html")
   header_banner = AID.input_file(path_banner)
   path_header_post = os.path.join(folder_matter, "header-post.html")
   header_post = AID.input_file(path_header_post)
   path_header_page = os.path.join(folder_matter, "header-page.html")
   header_page = AID.input_file(path_header_page)
   path_footer = os.path.join(folder_matter, "footer.html")
   footer = AID.input_file(path_footer)
   path_item = os.path.join(folder_matter, "item.html")
   item = AID.input_file(path_item)

   # # Convert posts into HTML article.
   # AID.make_all(folder_input, folder_output) # XXX
   AID.make_new(folder_input, folder_output)

   # # # # # # # # # # # # # # # #
   # # Combine HTML articles into HTML.
   for entry in entries:
      wholes = []
      path_output = ''
      path_post = ''
      for name in os.listdir(folder_output):
         if name.startswith(stamp):
            bare = name.split('.')[0]
            if not bare:
               continue
            path_output = os.path.join(folder_output, name)
            path_post = os.path.join(folder_post, bare + ".html")
            break
      if (path_output):
         continue
      output = AID.input_file(path_output)

      head_plugged = head.replace("$TITLE", entry.title)
      header_plugged = write_display(header, entry, None)
      wholes.extend(["<html>", head_plugged, "<body>"]
      wholes.extend([banner, header_plugged, output, footer])
      wholes.extend(["</body>", "</html>"])
      whole = '\n\n'.join(wholes)
      AID.output_file(path_post, whole)

   # # # # # # # # # # # # # # # #
   # # Write index.
   number_post_max = 16
   number_post_shown = min(number_post_max, len(entries))
   entries_newest = entries[:number_post_shown]
   wholes_home = []
   heading = "Newest"
   head_plugged = head.replace("$TITLE", heading)
   header_plugged = header_page.replace("$HEADING", heading)
   wholes.extend(["<html>", head_plugged, "<body>"]
   wholes.extend([banner, header_plugged])

   for entry in entries_newest:
      name_post = ''
      for name in os.listdir(folder_post):
         if name.startswith(entry.get("stamp")):
            name_post = name
            break
      if not name_post:
         continue
      item_plugged = write_display(item, entry, name_post)
      wholes_home.append(item)

   wholes_home.append(footer)
   wholes_home.append("</body>")
   wholes_home.append("</html>")
   whole_home = '\n\n'.join(wholes_home)
   path_index = os.path.join(folder_site, "index.html")
   AID.output_file(path_index, whole_home)

   # # # # # # # # # # # # # # # #
   # # Write page of stamp.
   


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


def write_element_heading(heading, link):
   if not heading:
      return None
   if not link:
      sinks = "<h1 class=\"heading-post\">{}</h1>".format(heading)
   else:
      sinks = (
         "<h1 class=\"heading-post\" + ' '
         + "href=\"/post/{}\">{}</h1>"
      ).format(link, heading)
   return sink

def write_element_stamp(stamp):
   if not stamp:
      return None
   sinks = (
      "<a class=\"data-stamp\"" + ' '
      + "href=\"/stamp/{}\">{}</a>"
   ).format(unify_link(get_month(stamp)), date)
   return sink

def write_element_genre(genre):
   if not genre:
      return None
   sink = (
      "<a class=\"data-genre\"" + ' '
      + "href=\"/genre/{}\">{}</a>"
   ).format(unify_link(genre), genre)
   return sink

def write_element_tag(tag):
   if not tag:
      return None
   sink = (
      "<a class=\"data-tag\"" + ' '
      + "href=\"/tag/{}\">{}</a>"
   ).format(unify_link(genre), genre)
   return sink

def write_element_series(series):
   if not series:
      return None
   sink = (
      "<a class=\"data-series\"" + ' '
      + "href=\"/series/{}\">{}</a>"
   ).format(unify_link(series), series)
   return sink

def unify_link(source):
   sink = lower(source)
   sink = sink.replace(' ', '-')
   return sink

def create_group(member):
   group = []
   if (isinstance(group, list)):
      group = member
   else:
      group = [member]
   return group

def write_display(source, entry, link):
      sink = source
      heading = entry.get("heading")
      stamp = entry.get("stamp")
      genres = create_group(entry.get("genre"))
      tags = create_group(entry.get("tag"))
      series = entry.get("series")
      if heading is not None:
         element = write_element_heading(heading, link)
         sink.replace("$HEADING", element)
      if stamp is not None:
         element = write_element_stamp(stamp)
         sink.replace("$STAMP", element)
      if genres is not [None]:
         elements = []
         for genre in genres:
            elements.append(write_element_genre(genre))
         element = '\n'.join(elements)
         sink.replace("$GENRE", element)
      if tags is not [None]:
         elements = []
         for tag in tags:
            elements.append(write_element_tag(tag))
         element = '\n'.join(elements)
         sink.replace("$TAG", element)
      if series is not None:
         element = write_element_stamp(stamp)
         sink.replace("$SERIES", element)
      return sink

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

main()