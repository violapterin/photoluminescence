import os
import json

import porphyrin.aid as AID

def main(whether_new):
   # Load constants.
   folder_this = os.path.dirname(__file__)
   folder_cipher = os.path.join(folder_this, "post-cipher")
   folder_plain = os.path.join(folder_this, "post-plain")
   folder_matter = os.path.join(folder_this, "matter")
   folder_site = os.path.join(folder_this, "site")
   folder_post = os.path.join(folder_site, "post")
   folder_page = os.path.join(folder_site, "page")
   many_record = load_record(folder_this)
   matter = load_matter(folder_matter)

   # # # # # # # # # # # # # # # #
   # # Convert posts into HTML article.
   if whether_new:
      AID.make_new(folder_cipher, folder_plain)
   else:
      AID.make_all(folder_cipher, folder_plain)

   # # # # # # # # # # # # # # # #
   # # Write posts.
   for record in many_record:
      stamp = record.get("stamp")
      path_plain = search_path_plain(folder_plain, stamp)
      plain = AID.input_file(path_plain)
      base = os.path.basename(path_plain).split('.')[0]
      path_post = os.path.join(folder_post, base + ".html")
      whole = write_post(matter, plain, record)
      AID.output_file(path_post, whole)

   # # # # # # # # # # # # # # # #
   # # Update catalogs.
   many_catalog_stamp = {}
   for record in many_record:
      stamp = record.get("stamp")
      month = get_month(stamp)
      if not month:
         continue
      if month not in many_catalog_stamp:
         many_catalog_stamp[month] = [record]
         continue
      many_catalog_stamp[month].append(record)
   heading = "By date"
   whole = write_catalog(matter, many_catalog_stamp, folder_post, heading)
   path_stamp = os.path.join(folder_site, "stamp.html")
   AID.output_file(path_stamp, whole)

   many_catalog_genre = {}
   for record in many_record:
      elision = record.get("genre")
      genre = get_genre(elision)
      if not genre:
         continue
      if genre not in many_catalog_genre:
         many_catalog_genre[genre] = [record]
         continue
      many_catalog_genre[genre].append(record)
   heading = "By genre"
   whole = write_catalog(matter, many_catalog_genre, folder_post, heading)
   path_genre = os.path.join(folder_site, "genre.html")
   AID.output_file(path_genre, whole)

   many_catalog_tag = {}
   for record in many_record:
      many_tag = check_group(record.get("tag"))
      for tag in many_tag:
         if not tag:
            continue
         if tag not in many_catalog_tag:
            many_catalog_tag[tag] = [record]
            continue
         many_catalog_tag[tag].append(record)
   heading = "By tag"
   whole = write_catalog(matter, many_catalog_tag, folder_post, heading)
   path_tag = os.path.join(folder_site, "tag.html")
   AID.output_file(path_tag, whole)

   many_catalog_series = {}
   for record in many_record:
      series = record.get("series")
      if not series:
         continue
      if series not in many_catalog_series:
         many_catalog_series[series] = [record]
         continue
      many_catalog_series[series].append(record)
   heading = "By series"
   whole = write_catalog(matter, many_catalog_series, folder_post, heading)
   path_series = os.path.join(folder_site, "series.html")
   AID.output_file(path_series, whole)
   
   # # # # # # # # # # # # # # # #
   # # Write pages.
   number_post_max = 12
   number_post_shown = min(number_post_max, len(many_record))
   many_record_index = many_record[:number_post_shown]
   heading = "Latest"
   whole = write_page(matter, many_record_index, folder_post, heading)
   path_index = os.path.join(folder_site, "index.html")
   AID.output_file(path_index, whole)

   for month, catalog in many_catalog_stamp.items():
      heading = month
      name = unify_name(month) + ".html"
      whole = write_page(matter, catalog, folder_post, heading)
      path_stamp = os.path.join(folder_page, name)
      AID.output_file(path_stamp, whole)

   for genre, catalog in many_catalog_genre.items():
      heading = genre
      name = unify_name(genre) + ".html"
      whole = write_page(matter, catalog, folder_post, heading)
      path_genre = os.path.join(folder_page, name)
      AID.output_file(path_genre, whole)

   for tag, catalog in many_catalog_tag.items():
      heading = tag
      name = unify_name(tag) + ".html"
      whole = write_page(matter, catalog, folder_post, heading)
      path_tag = os.path.join(folder_page, name)
      AID.output_file(path_tag, whole)

   for series, catalog in many_catalog_series.items():
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
   path_many_record = os.path.join(folder_this, "record.json")
   many_record = json.loads(AID.input_file(path_many_record))
   many_record = [record for record in many_record if record is not None]
   order = (lambda record: record.get("stamp"))
   many_record.sort(key = order, reverse = True)
   return many_record

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def write_catalog(matter, many_catalog, folder_post, heading):
   many_whole = []
   head = matter["head"].replace("$TITLE", write_title(heading))
   header_banner = matter["header_banner"]
   header_page = matter["header_page"].replace(
      "$HEADING",
      write_element_display(heading, None)
   )
   footer = matter["footer"]
   entry = matter["entry"]

   many_whole.append("<!DOCTYPE html>")
   many_whole.append("<html lang=\"en\">")
   many_whole.append(head)
   many_whole.append("<body>")
   many_whole.append(header_banner)
   many_whole.append(header_page)
   for kind, catalog in many_catalog.items():
      display = write_element_display(kind, unify_name(kind))
      many_whole.append("<p class=\"title-catalog\">")
      many_whole.append(display)
      many_whole.append("</p>")
      '''
      for record in catalog:
         stamp = record.get("stamp")
         name_post = search_path_post(folder_post, stamp)
         display = write_entry(entry, record, name_post)
         many_whole.append(display)
      '''
   many_whole.append(footer)
   many_whole.append("</body>")
   many_whole.append("</html>")
   whole = '\n\n'.join(many_whole)
   return whole

def write_page(matter, many_record, folder_post, heading):
   many_whole = []
   head = matter["head"].replace("$TITLE", write_title(heading))
   header_banner = matter["header_banner"]
   header_page = matter["header_page"].replace(
      "$HEADING",
      write_element_display(heading, None)
   )
   footer = matter["footer"]
   entry = matter["entry"]

   many_whole.append("<!DOCTYPE html>")
   many_whole.append("<html lang=\"en\">")
   many_whole.append(head)
   many_whole.append("<body>")
   many_whole.append(header_banner)
   many_whole.append(header_page)
   for record in many_record:
      stamp = record.get("stamp")
      name_post = search_path_post(folder_post, stamp)
      display = write_entry(entry, record, name_post)
      many_whole.append(display)
   many_whole.append(footer)
   many_whole.append("</body>")
   many_whole.append("</html>")
   whole = '\n\n'.join(many_whole)
   return whole

def write_post(matter, plain, record):
   many_whole = []
   title = record.get("title")
   head = matter["head"].replace("$TITLE", write_title(title))
   header_banner = matter["header_banner"]
   header_post = write_entry(matter["header_post"], record, None)
   footer = matter["footer"]

   many_whole.append("<!DOCTYPE html>")
   many_whole.append("<html lang=\"en\">")
   many_whole.append(head)
   many_whole.append("<body>")
   many_whole.append(header_banner)
   many_whole.append(header_post)
   many_whole.append(plain)
   many_whole.append(footer)
   many_whole.append("</body>")
   many_whole.append("</html>")
   whole = "\n\n".join(many_whole)
   return whole

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def write_entry(source, record, name):
      sink = source
      heading = record.get("title")
      stamp = record.get("stamp")
      elision = record.get("genre")
      many_tag = check_group(record.get("tag"))
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
      if (many_tag is not None) and (many_tag is not [None]):
         many_element = []
         for tag in many_tag:
            many_element.append(write_element_tag(tag))
         element = '\n'.join(many_element)
         sink = sink.replace("$TAG", element)
      else:
         sink = sink.replace("$TAG", '')
      return sink

def search_path_plain(folder, stamp):
   path_plain = ''
   for name in os.listdir(folder):
      if name.startswith(stamp):
         if not name.split('.')[0]:
            continue
         path_plain = os.path.join(folder, name)
         break
   return path_plain

def search_path_post(folder, stamp):
   name_post = ''
   for name in os.listdir(folder):
      path = os.path.join(folder, name)
      if os.path.isfile(path):
         if name.startswith(stamp):
            name_post = name
      elif os.path.isdir(path):
         for name_deep in os.listdir(path):
            if name_deep.startswith(stamp):
               name_post = name_deep
               break
      if name_post:
         break
   return name_post

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
         + "href=\"/page/{}.html\">".format(name)
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
   prefixes = {
      "vocabulary": "voluminous",
      "data": "detailed",
      "notes": "negligible",
      "comments": "contentious",
      "expositions": "exotic",
      "quests": "quaint",
      "inventions": "incongruous",
      "readings": "reflective",
      "satires": "sincere",
      "aphorisms": "anomalous",
      "memories": "misleading",
      "fictions": "fantastic",
   }
   genres = {}
   for key, prefix in prefixes.items():
      prefix = prefix.capitalize()
      genres[key] = prefix + ' ' + key
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
   infixes = {
      ' the ', ' a ',
      ',', ':', ';', '.',
      '“', '”', '‘', '’',
      '«', '»', '‹', '›',
      '  ', '   ', '    ',
   }
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
