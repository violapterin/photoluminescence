#! /usr/bin/env python3

import os
import json

import porphyrin.aid as AID

def main():
   # Load constants.
   folder_this = os.path.dirname(__file__)
   folder_cipher = os.path.join(folder_this, "post-cipher")
   folder_plain = os.path.join(folder_this, "post-plain")
   folder_matter = os.path.join(folder_this, "matter")
   folder_site = os.path.join(folder_this, "site")
   folder_post = os.path.join(folder_site, "post")
   folder_page = os.path.join(folder_site, "page")
   records = load_record(folder_this)
   matter = load_matter(folder_matter)

   # # # # # # # # # # # # # # # #
   # # Convert posts into HTML article.
   # AID.make_all(folder_cipher, folder_plain) # XXX
   AID.make_new(folder_cipher, folder_plain)

   # # # # # # # # # # # # # # # #
   # # Write posts.
   for record in records:
      stamp = record.get("stamp")
      path_plain = search_path_plain(folder_plain, stamp)
      plain = AID.input_file(path_plain)
      base = os.path.basename(path_plain).split('.')[0]
      path_post = os.path.join(folder_post, base + ".html")
      whole = write_post(matter, plain, record)
      AID.output_file(path_post, whole)

   # # # # # # # # # # # # # # # #
   # # Update catalogs.
   catalogs_stamp = {}
   for record in records:
      stamp = record.get("stamp")
      month = get_month(stamp)
      if not month:
         continue
      if month not in catalogs_stamp:
         catalogs_stamp[month] = [record]
         continue
      catalogs_stamp[month].append(record)
   heading = "By date"
   whole = write_catalog(matter, catalogs_stamp, folder_post, heading)
   path_stamp = os.path.join(folder_site, "stamp.html")
   AID.output_file(path_stamp, whole)

   catalogs_genre = {}
   for record in records:
      elision = record.get("genre")
      genre = get_genre(elision)
      if not genre:
         continue
      if genre not in catalogs_genre:
         catalogs_genre[genre] = [record]
         continue
      catalogs_genre[genre].append(record)
   heading = "By genre"
   whole = write_catalog(matter, catalogs_genre, folder_post, heading)
   path_genre = os.path.join(folder_site, "genre.html")
   AID.output_file(path_genre, whole)

   catalogs_tag = {}
   for record in records:
      tags = check_group(record.get("tag"))
      for tag in tags:
         if not tag:
            continue
         if tag not in catalogs_tag:
            catalogs_tag[tag] = [record]
            continue
         catalogs_tag[tag].append(record)
   heading = "By tag"
   whole = write_catalog(matter, catalogs_tag, folder_post, heading)
   path_tag = os.path.join(folder_site, "tag.html")
   AID.output_file(path_tag, whole)

   catalogs_series = {}
   for record in records:
      series = record.get("series")
      if not series:
         continue
      if series not in catalogs_series:
         catalogs_series[series] = [record]
         continue
      catalogs_series[series].append(record)
   heading = "By series"
   whole = write_catalog(matter, catalogs_series, folder_post, heading)
   path_series = os.path.join(folder_site, "series.html")
   AID.output_file(path_series, whole)
   
   # # # # # # # # # # # # # # # #
   # # Write pages.
   number_post_max = 16
   number_post_shown = min(number_post_max, len(records))
   records_index = records[:number_post_shown]
   heading = "Newest"
   whole = write_page(matter, records_index, folder_post, heading)
   path_index = os.path.join(folder_site, "index.html")
   AID.output_file(path_index, whole)

   for month, catalog in catalogs_stamp.items():
      heading = month
      name = unify_name(month) + ".html"
      whole = write_page(matter, catalog, folder_post, heading)
      path_stamp = os.path.join(folder_page, name)
      AID.output_file(path_stamp, whole)

   for genre, catalog in catalogs_genre.items():
      heading = genre
      name = unify_name(genre) + ".html"
      whole = write_page(matter, catalog, folder_post, heading)
      path_genre = os.path.join(folder_page, name)
      AID.output_file(path_genre, whole)

   for tag, catalog in catalogs_tag.items():
      heading = tag
      name = unify_name(tag) + ".html"
      whole = write_page(matter, catalog, folder_post, heading)
      path_tag = os.path.join(folder_page, name)
      AID.output_file(path_tag, whole)

   for series, catalog in catalogs_series.items():
      heading = series
      name = unify_name(series) + ".html"
      whole = write_page(matter, catalog, folder_post, heading)
      path_series = os.path.join(folder_page, name)
      AID.output_file(path_series, whole)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def load_matter(folder_matter):
   path_head = os.path.join(folder_matter, "head.html")
   path_banner = os.path.join(folder_matter, "header-banner.html")
   path_header_post = os.path.join(folder_matter, "header-post.html")
   path_header_page = os.path.join(folder_matter, "header-page.html")
   path_footer = os.path.join(folder_matter, "footer.html")
   path_entry = os.path.join(folder_matter, "entry.html")
   head = AID.input_file(path_head)
   header_banner = AID.input_file(path_banner)
   header_post = AID.input_file(path_header_post)
   header_page = AID.input_file(path_header_page)
   footer = AID.input_file(path_footer)
   entry = AID.input_file(path_entry)
   matter = {
      "head": head,
      "header_banner": header_banner,
      "header_post": header_post,
      "header_page": header_page,
      "footer": footer,
      "entry": entry,
   }
   return matter

def load_record(folder_this):
   path_records = os.path.join(folder_this, "record.json")
   records = json.loads(AID.input_file(path_records))
   records = [record for record in records if record is not None]
   order = (lambda record: record.get("stamp"))
   records.sort(key = order, reverse = True)
   return records

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def write_catalog(matter, catalogs, folder_post, heading):
   wholes = []
   head = matter["head"].replace("$TITLE", write_title(heading))
   header_banner = matter["header_banner"]
   header_page = matter["header_page"].replace(
      "$HEADING",
      write_element_display(heading, None)
   )
   footer = matter["footer"]
   entry = matter["entry"]

   wholes.append("<!DOCTYPE html>")
   wholes.append("<html lang=\"en\">")
   wholes.append(head)
   wholes.append("<body>")
   wholes.append(header_banner)
   wholes.append(header_page)
   for kind, catalog in catalogs.items():
      display = write_element_display(kind, unify_name(kind))
      wholes.append("<p class=\"title-catalog\">")
      wholes.append(display)
      wholes.append("</p>")
      for record in catalog:
         stamp = record.get("stamp")
         name_post = search_path_post(folder_post, stamp)
         display = write_entry(entry, record, name_post)
         wholes.append(display)
   wholes.append(footer)
   wholes.append("</body>")
   wholes.append("</html>")
   whole = '\n\n'.join(wholes)
   return whole

def write_page(matter, records, folder_post, heading):
   wholes = []
   head = matter["head"].replace("$TITLE", write_title(heading))
   header_banner = matter["header_banner"]
   header_page = matter["header_page"].replace(
      "$HEADING",
      write_element_display(heading, None)
   )
   footer = matter["footer"]
   entry = matter["entry"]

   wholes.append("<!DOCTYPE html>")
   wholes.append("<html lang=\"en\">")
   wholes.append(head)
   wholes.append("<body>")
   wholes.append(header_banner)
   wholes.append(header_page)
   for record in records:
      stamp = record.get("stamp")
      name_post = search_path_post(folder_post, stamp)
      display = write_entry(entry, record, name_post)
      wholes.append(display)
   wholes.append(footer)
   wholes.append("</body>")
   wholes.append("</html>")
   whole = '\n\n'.join(wholes)
   return whole

def write_post(matter, plain, record):
   wholes = []
   title = record.get("title")
   head = matter["head"].replace("$TITLE", write_title(title))
   header_banner = matter["header_banner"]
   header_post = write_entry(matter["header_post"], record, None)
   footer = matter["footer"]

   wholes.append("<!DOCTYPE html>")
   wholes.append("<html lang=\"en\">")
   wholes.append(head)
   wholes.append("<body>")
   wholes.append(header_banner)
   wholes.append(header_post)
   wholes.append(plain)
   wholes.append(footer)
   wholes.append("</body>")
   wholes.append("</html>")
   whole = "\n\n".join(wholes)
   return whole

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def write_entry(source, record, name):
      sink = source
      heading = record.get("title")
      stamp = record.get("stamp")
      elision = record.get("genre")
      tags = check_group(record.get("tag"))
      series = record.get("series")
      if heading is not None:
         element = write_element_heading(heading, name)
         sink = sink.replace("$HEADING", element)
      else:
         sink = sink.replace("$HEADING", '')
      if stamp is not None:
         element = write_element_stamp(stamp)
         sink = sink.replace("$STAMP", element)
      else:
         sink = sink.replace("$STAMP", '')
      if elision is not None:
         element = write_element_genre(elision)
         sink = sink.replace("$GENRE", element)
      else:
         sink = sink.replace("$GENRE", '')
      if series is not None:
         element = write_element_series(series)
         sink = sink.replace("$SERIES", element)
      else:
         sink = sink.replace("$SERIES", '')
      if (tags is not None) and (tags is not [None]):
         elements = []
         for tag in tags:
            elements.append(write_element_tag(tag))
         element = '\n'.join(elements)
         sink = sink.replace("$TAG", element)
      else:
         sink = sink.replace("$TAG", '')
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

def search_path_post(folder_post, stamp):
   name_post = ''
   for name in os.listdir(folder_post):
      if name.startswith(stamp):
         name_post = name
         break
   return name_post

'''
# # revised
def search_path_post(folder, stamp):
   name_post = ''
   for name in os.listdir(folder):
      subfolder = os.path.join(folder, name)
      if not os.path.isdir(subfolder):
         continue
      for subname in os.listdir(subfolder):
         if subname.startswith(stamp):
            name_post = subname
            break
   return name_post
'''

def write_element_heading(title, name):
   if not title:
      return None
   sink = ''
   if not name:
      sink = (
         "<span class=\"heading\">"
         + "{}</span>".format(title)
      )
   else:
      sink = (
         "<a class=\"heading\"" + ' '
         + "href=\"/post/{}\">".format(name)
         + "{}</a>".format(title) + ' ' + "</span>"
      )
   return sink

def write_element_display(title, name):
   if not title:
      return None
   sink = ''
   if not name:
      sink = (
         "<span class=\"display\">"
         + "{}</span>".format(title)
      )
   else:
      sink = (
         "<a class=\"display\"" + ' '
         + "href=\"/post/{}\">".format(name)
         + "{}</a>".format(title)
      )
   return sink

def write_element_stamp(stamp):
   if not stamp:
      return None
   date = get_date(stamp)
   sink = (
      "<a class=\"data-stamp\"" + ' '
      + "href=\"/page/{}.html\">{}</a>"
   ).format(unify_name(get_month(stamp)), date)
   return sink

def write_element_genre(elision):
   genre = get_genre(elision)
   if not genre:
      return None
   sink = (
      "<a class=\"data-genre\"" + ' '
      + "href=\"/page/{}.html\">{}</a>"
   ).format(unify_name(elision), genre)
   return sink

def write_element_series(series):
   if not series:
      return None
   sink = (
      "<a class=\"data-series\"" + ' '
      + "href=\"/page/{}.html\">{}</a>"
   ).format(unify_name(series), series)
   return sink

def write_element_tag(tag):
   if not tag:
      return None
   sink = (
      "<a class=\"data-tag\"" + ' '
      + "href=\"/page/{}.html\">{}</a>"
   ).format(unify_name(tag), tag)
   return sink

def write_title(title):
   sink = "<title>{}</title>".format(title)
   return sink

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def get_day(stamp):
   day = stamp[4:6]
   if (day[0] == '0'):
      day = day[1]
   return day

def give_months():
   months = {
      "01": "January", "02": "February", "03": "March",
      "04": "April", "05": "May", "06": "June",
      "07": "July", "08": "August", "09": "September",
      "10": "October", "11": "November", "12": "December",
   }
   return months

def get_month(stamp):
   sink = ''
   months = give_months()
   month = months.get(stamp[2:4])
   year = "20" + stamp[0:2]
   sink = month + ' ' + year
   return sink


def get_date(stamp):
   month = get_month(stamp)
   day = get_day(stamp)
   date = day + ' ' + month
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

def unify_name(source):
   sink = source
   genres = give_genres()
   elisions = {value: key for key, value in genres.items()}
   if sink in elisions:
      sink = elisions.get(sink)
      return sink

   sink = sink.lower()
   sink = sink.strip()
   prefixes = {"The ", "A ", "An "}
   for prefix in prefixes:
      if sink.startswith(prefix):
         sink = sink[len(prefix):]
   infixes = {' the ', ' a ', ', ', ': '}
   for infix in infixes:
      sink = sink.replace(infix, ' ')
   sink = sink.replace(' ', '-')
   return sink

def check_group(member):
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