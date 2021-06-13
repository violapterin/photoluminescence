#! /usr/bin/env python3

import os
import json
import re

import porphyrin.aid as AID


def main():
   folder_this = os.path.dirname(__file__)
   records = load_records(folder_this)
   matters = load_matters(folder_this)

   # # Convert posts into HTML article.
   AID.make_all(folder_cipher, folder_plain) # XXX
   # AID.make_new(folder_cipher, folder_plain)

   # # # # # # # # # # # # # # # #
   # # Write posts.
   for record in records:
      stamp = record.get("stamp")
      path_plain = search_path_plain(folder_plain, stamp)
      plain = AID.input_file(path_plain)
      base = os.path.basename(path_plain)
      path_post = os.path.join(folder_post, base + ".html")
      whole = write_post(matters, record, plain)
      AID.output_file(path_post, whole)

   # # # # # # # # # # # # # # # #
   # # Update catalogs.
   catalogs_stamp = {}
   for record in records:
      stamp = record.get("stamp")
      month = get_month(stamp)
      if month not in catalogs_stamp:
         catalogs_stamp[month] = [record]
         continue
      catalogs_stamp[month].append[record]
   for month, catalog in catalogs_stamp:
      catalog.sort()

   catalogs_series = {}
   for record in records:
      series = record.get("series")
      if series not in catalogs_series:
         catalogs_series[series] = [record]
         continue
      catalogs_series[series].append[record]
   for series, catalog in catalogs_series:
      catalog.sort()

   catalogs_genre = {}
   for record in records:
      genres = record.get("genre")
      for elision in genres:
         genre = get_genre(elision)
         if genre not in catalogs_genre:
            catalogs_genre[genre] = [record]
            continue
         catalogs_genre[genre].append[record]
   for genre, catalog in catalogs_genre:
      catalog.sort()

   catalogs_tag = {}
   for record in records:
      tags = record.get("tag")
      for tag in tags:
         if tag not in catalogs_tag:
            catalogs_tag[tag] = [record]
            continue
         catalogs_tag[tag].append[record]
   for tag, catalog in catalogs_tag:
      catalog.sort()

   # # # # # # # # # # # # # # # #
   # # Write pages.

   heading = "By date"
   whole = write_index(matters, records_index, heading):
   path_index = os.path.join(folder_site, "stamp.html")
   AID.output_file(path_index, whole)
   

   # # # # # # # # # # # # # # # #
   # # Write indices.
   number_post_max = 16
   number_post_shown = min(number_post_max, len(records))
   records_index = records[:number_post_shown]
   heading = "Newest"
   whole = write_index(matters, records_index, heading):
   path_index = os.path.join(folder_site, "index.html")
   AID.output_file(path_index, whole)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def load_matters(folder_this):
   folder_cipher = os.path.join(folder_this, "post-cipher")
   folder_plain = os.path.join(folder_this, "post-plain")
   folder_matter = os.path.join(folder_this, "matter")
   folder_site = os.path.join(folder_this, "site")
   folder_post = os.path.join(folder_site, "post")
   path_head = os.path.join(folder_matter, "head.html")
   head = AID.input_file(path_head)
   path_banner = os.path.join(folder_matter, "header-banner.html")
   header_banner = AID.input_file(path_banner)
   path_header_post = os.path.join(folder_matter, "header-post.html")
   header_post = AID.input_file(path_header_post)
   path_header_page = os.path.join(folder_matter, "header-page.html")
   header_page = AID.input_file(path_header_page)
   path_footer = os.path.join(folder_matter, "footer.html")
   footer = AID.input_file(path_footer)
   path_entry = os.path.join(folder_matter, "entry.html")
   entry = AID.input_file(path_entry)
   matters = {
      "head": head,
      "header_banner": header_banner,
      "header_post": header_post,
      "header_page": header_page,
      "footer": footer,
      "entry": entry,
   }
   return matters

def load_records(folder_this):
   path_records = os.path.join(folder_this, "record.json")
   records = json.loads(AID.input_file(path_records))
   records = [record for record in records if record is not None]
   records = sort_records_by_stamp(records)
   return records

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def write_page(matters, catalogs, heading):
   wholes = []
   head = matters.head.replace("$TITLE", heading)
   header_banner = matters.header_banner
   header_page = header_page.replace("$HEADING", heading)
   footer = matters.footer
   entry = matters.entry

   wholes.append("<html>")
   wholes.append(head)
   wholes.append("<body>")
   wholes.append(header_banner)
   wholes.append(header_post)
   for kind, catalog in catalogs:
      element = write_element_heading(kind, unify_link(kind))
      wholes.append(element)
      for record in catalog:
         stamp = record.get("stamp")
         name_post = search_path_plain(folder_post, stamp):
         display = write_entry(entry, record, name_post)
         wholes.append(display)
   wholes.append(footer)
   wholes.append("</body>")
   wholes.append("</html>")
   whole = '\n\n'.join(wholes)
   return whole

def write_index(matters, records, heading):
   wholes = []
   head = matters.head.replace("$TITLE", heading)
   header_banner = matters.header_banner
   header_page = header_page.replace("$HEADING", heading)
   footer = matters.footer
   entry = matters.entry

   wholes.append("<html>")
   wholes.append(head)
   wholes.append("<body>")
   wholes.append(header_banner)
   wholes.append(header_post)
   for record in records:
      stamp = record.get("stamp")
      name_post = search_path_plain(folder_post, stamp):
      display = write_entry(entry, record, name_post)
      wholes.append(display)
   wholes.append(footer)
   wholes.append("</body>")
   wholes.append("</html>")
   whole = '\n\n'.join(wholes)
   return whole

def write_post(matters, record, plain):
   wholes = []
   title = record.get(title)
   head = matters.head.replace("$TITLE", title)
   header_banner = matters.header_banner
   header_post = write_entry(matters.header_post, record, None)
   footer = matters.footer

   wholes.append("<html>")
   wholes.append(head)
   wholes.append("<body>")
   wholes.append(header_banner)
   wholes.append(header_post)
   wholes.append(plain)
   wholes.append(footer)
   wholes.append("</body>")
   wholes.append("</html>")
   whole = '\n\n'.join(wholes)
   return whole

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def write_entry(source, record, link):
      sink = source
      heading = record.get("heading")
      stamp = record.get("stamp")
      genres = create_group(record.get("genre"))
      tags = create_group(record.get("tag"))
      series = record.get("series")
      if heading is not None:
         element = write_element_heading(heading, link)
         sink.replace("$HEADING", element)
      if stamp is not None:
         element = write_element_stamp(stamp)
         sink.replace("$STAMP", element)
      if series is not None:
         element = write_element_series(stamp)
         sink.replace("$SERIES", element)
      if (genres is not None) and (genres is not [None]):
         elements = []
         for elision in genres:
            elements.append(write_element_genre(elision))
         element = '\n'.join(elements)
         sink.replace("$GENRE", element)
      if (tags is not None) and (tags is not [None]):
         elements = []
         for tag in tags:
            elements.append(write_element_tag(tag))
         element = '\n'.join(elements)
         sink.replace("$TAG", element)
      return sink

def search_path_plain(folder_plain, stamp):
   path_plain = ''
   for name in os.listdir(folder_plain):
      if name.startswith(stamp):
         if not name.split('.')[0]:
            continue
         path_plain = os.path.join(folder_plain, name)
         break
   return path_plain

def search_path_plain(folder_post, stamp):
   name_post = ''
   for name in os.listdir(folder_post):
      if name.startswith(record.get("stamp")):
         name_post = name
         break
   return name_post

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

def write_element_genre(elision):
   genre = get_genre(elision)
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

def give_genres():
   genres = {
      "data": "Detailed data",
      "notes": "Negligible notes",
      "comments": "Contentious comments",
      "expositions": "Exotic expositions",
      "quests": "Quaint quests",
      "inventions": "Incongruous inventions",
      "readings": "Reflective readings",
      "satires": "Sincere satires",
      "memories": "Misleading memories",
      "fictions": "Fantastic fictions",
   }
   return genres

def get_genre(elision):
   genres = give_genres()
   genre = genres.get(elision)
   return genre

def unify_link(source):
   sink = source
   genres = give_genres()
   elisions = {value: key for key, value in genres}
   if sink in elisions:
      sink = elisions.get(sink)
      return sink

   sink = lower(sink)
   sink = sink.strip()
   values = {
      ' the ': ' ',
      ' a ': ' ',
      ', ': ' ',
      ': ': ' ',
      ' ': '-',
   }
   for key, value in values:
      sink = sink.replace(key, value)
   return sink

def sort_records_by_stamp(records):
   order = (lambda record: record.get("stamp"))
   result = records.sort(key = order, reverse = True)
   return result

def create_group(member):
   group = []
   if (isinstance(group, list)):
      group = member
   else:
      group = [member]
   return group

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

main()