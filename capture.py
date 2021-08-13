import os
import io
import copy
import shutil
import numpy as NUMPY
from selenium import webdriver as DRIVER
from PIL import Image as IMAGE
from PIL import ImageEnhance as ENHANCE
from PIL import ImageOps as OPERATION

def main(whether_new):
   folder_this = os.path.dirname(__file__)
   folder_cipher = os.path.join(folder_this, "post-cipher")
   folder_book = os.path.join(folder_this, "book")
   folder_shot = os.path.join(folder_book, "shot")
   folder_strip = os.path.join(folder_book, "strip")
   folder_leaf = os.path.join(folder_book, "leaf")
   if not whether_new:
      if os.path.isdir(folder_shot):
         shutil.rmtree(folder_shot)
      if os.path.isdir(folder_strip):
         shutil.rmtree(folder_strip)
      if os.path.isdir(folder_leaf):
         shutil.rmtree(folder_leaf)
   if not os.path.isdir(folder_shot):
      os.mkdir(folder_shot)
   if not os.path.isdir(folder_strip):
      os.mkdir(folder_strip)
   if not os.path.isdir(folder_leaf):
      os.mkdir(folder_leaf)
   assert(os.path.isdir(folder_cipher))
   assert(os.path.isdir(folder_book))
   assert(os.path.isdir(folder_shot))
   assert(os.path.isdir(folder_strip))
   assert(os.path.isdir(folder_leaf))
   '''
   many_title = [
      "190710-american-village-okinawa",
      "210719-valid-triangle-numbers",
   ]
   '''
   many_title = extract_title(folder_cipher)
   many_title = many_title[0:3] # XXX
   take_photograph(whether_new, folder_shot, many_title)
   shred_photograph(whether_new, folder_strip, folder_shot)
   patch_leaf(whether_new, folder_leaf, folder_strip)

def patch_leaf(whether_new, folder_leaf, folder_strip):
   if whether_new:
      if not compare_folder_with_folder(folder_leaf, folder_strip):
         return
   suffix_in = ".png"
   suffix_out = ".jpg"
   limit_height = constant()["inner_height"]
   total = 0
   number_page = 0
   for name_article in os.listdir(folder_strip):
      folder_article = os.path.join(folder_strip, name_article)
      if not os.path.isdir(folder_article):
         continue
      for name_strip in os.listdir(folder_article):
         if not name_strip.endswith(suffix_in):
            continue
         path_strip = os.path.join(folder_article, name_strip)
         if not os.path.isfile(path_strip):
            continue
         with IMAGE.open(path_strip) as strip:
            height = strip.size[1]
            if (total == 0):
               leaf = copy.copy(strip)
               total += height
            elif (total + height > limit_height):
               name_leaf = str(number_page).zfill(3) + suffix_out
               number_page += 1
               path_leaf = os.path.join(folder_leaf, name_leaf)
               leaf = tune_leaf(leaf)
               print("Saving leaf:", name_leaf, "......")
               leaf.save(path_leaf, quality = 100)
               leaf = copy.copy(strip)
               total = height
            else:
               leaf = concatenate_graph(strip, leaf)
               total += height
   name_leaf = str(number_page).zfill(3) + suffix_out
   path_leaf = os.path.join(folder_leaf, name_leaf)
   leaf = tune_leaf(leaf)
   print("Saving leaf:", name_leaf, "......")
   leaf.save(path_leaf, quality = 100)

def shred_photograph(whether_new, folder_strip, folder_shot):
   suffix_in = ".png"
   suffix_out = ".png"
   for name_shot in os.listdir(folder_shot):
      if not name_shot.endswith(suffix_in):
         continue
      bare_graph = name_shot[:-len(suffix_in)]
      path_graph = os.path.join(folder_shot, name_shot)
      if not os.path.isfile(path_graph):
         continue
      folder_article = os.path.join(folder_strip, bare_graph)
      if not os.path.isdir(folder_article):
         os.mkdir(folder_article)
      if whether_new:
         if not compare_folder_with_file(folder_article, path_graph):
            continue
      limit_bright = 255
      limit_line = constant()["limit_line"]
      with IMAGE.open(path_graph) as graph:
         matrix = NUMPY.asarray(graph.convert('L'))
         height = matrix.shape[0]
         width = matrix.shape[1]
         bright = int(width / 128)
         marginal = [sum(row) for row in list(matrix)]
         flip = [limit_bright * width - value for value in marginal]
         passed = [(value > bright) for value in flip]
         many_boundary = find_boundary(passed)
         limit_boundary = 26 * 26
         if (len(many_boundary) > limit_boundary):
            print(
               "Warning: Image has more than", limit_boundary,
               "strips.", "It is cropped."
            )
         for head in range(0, len(many_boundary) - 1):
            name_strip = bare_graph + give_tail(head) + suffix_out
            path_strip = os.path.join(folder_article, name_strip)
            above = many_boundary[head]
            below = many_boundary[head + 1]
            strip = graph.crop((0, above, width - 1, below))
            if (below - above < limit_line):
               strip = enhance_contrast(strip)
               strip = enhance_sharpness(strip)
            print("Slicing strip:", name_strip, "......")
            strip.save(path_strip, quality = 100)

def take_photograph(whether_new, folder_shot, many_title):
   prefix = "https://www.violapterin.com/post/"
   many_path_graph = []
   suffix_in = ".html"
   suffix_out = ".png"
   for title in many_title:
      stamp = title.split('-')[0]
      address = prefix + title + suffix_in
      path_graph = os.path.join(folder_shot, stamp) + suffix_out
      if os.path.isfile(path_graph):
         continue
      many_path_graph.append(path_graph)
      graph = save_screenshot(address)
      graph.save(path_graph, quality = 100)

def save_screenshot(address):
   id_heading = "header-post"
   class_content = "document"
   size = constant()["outer_width"]
   os.environ["MOZ_HEADLESS"] = "1"
   driver = DRIVER.Firefox()
   driver.set_window_size(size, size)
   print("Capturing address:", address, "......")
   driver.get(address)
   element_heading = driver.find_element_by_id(id_heading)
   binary_heading = element_heading.screenshot_as_png
   graph_heading = IMAGE.open(io.BytesIO(binary_heading))
   element_content = driver.find_element_by_class_name(class_content)
   binary_content = element_content.screenshot_as_png
   graph_content = IMAGE.open(io.BytesIO(binary_content))
   driver.quit()
   graph = concatenate_graph(graph_content, graph_heading)
   return graph

def concatenate_graph(down, top):
   height_top = top.size[1]
   height_down = down.size[1]
   width = max(top.size[0], down.size[0])
   height = height_top + height_down
   dimension = (width, height)
   combined = IMAGE.new("RGBA", dimension, (255, 255, 255))
   more_width_top = (width - top.size[0]) // 2
   more_width_down = (width - down.size[0]) // 2
   offset_top = (more_width_top, 0)
   offset_down = (more_width_down, top.size[1])
   top_alpha = top.convert("RGBA")
   down_alpha = down.convert("RGBA")
   combined.paste(top, offset_top, mask = top_alpha)
   combined.paste(down, offset_down, mask = down_alpha)
   combined = combined.convert("RGB")
   return combined


def tune_leaf(leaf):
   leaf_alpha = leaf.convert("RGBA")
   width_outer = constant()["outer_width"]
   height_inner = constant()["inner_height"]
   height_outer = constant()["outer_height"]
   more_width = (width_outer - leaf.size[0]) // 2
   more_height = (height_outer - leaf.size[1]) // 2
   margin_height = (height_outer - height_inner) // 2
   more_height = max(0, min(margin_height, more_height))
   dimension = (width_outer, height_outer)
   combined = IMAGE.new("RGBA", dimension, (255, 255, 255))
   combined.paste(leaf, (more_width, more_height), mask = leaf_alpha)
   combined = combined.convert("RGB")
   return combined

def enhance_sharpness(strip):
   level = 2.0
   strip = ENHANCE.Sharpness(strip).enhance(level)
   return strip

def enhance_contrast(strip):
   level = 1.1
   strip = ENHANCE.Contrast(strip).enhance(level)
   return strip

def extract_title(folder_cipher):
   many_title = []
   suffix = ".txt"
   for name in os.listdir(folder_cipher):
      path = os.path.join(folder_cipher, name)
      if os.path.isfile(path):
         if not name.endswith(suffix):
            continue
         bare = name[:-len(suffix)]
         many_title.append(bare)
      elif os.path.isdir(path):
         many_title.extend(extract_title(path))
   many_title.sort()
   return many_title

def find_boundary(record):
   unit = 24
   filled = 8
   many_point = [0]
   head = 0
   cumulative = 0
   while(head + 1 < len(record)):
      head += 1
      last = many_point[-1]
      if record[head]:
         cumulative += 1
      else:
         if (head - last < unit):
            continue
         if (cumulative < filled):
            continue
         many_point.append(head)
         cumulative = 0
   return many_point

def compare_folder_with_folder(this_folder, that_folder):
   if not os.path.isdir(this_folder):
      return true
   if not os.path.isdir(that_folder):
      return false
   time_this = get_time_folder(this_folder)
   time_that = get_time_folder(that_folder)
   return (time_this < time_that)

def compare_folder_with_file(folder, path):
   if not os.path.isdir(folder):
      return true
   if not os.path.isfile(path):
      return false
   time_folder = get_time_folder(folder)
   time_path = get_time_path(folder)
   return (time_folder < time_path)

def get_time_folder(folder):
   time_folder = 0
   many_thing = os.scandir(folder)
   for thing in many_thing:
      time = 0
      if thing.is_file():
         time = thing.stat().st_mtime
      elif thing.is_dir():
         time = get_time_folder(thing.path)
      if time_folder < time:
         time_folder = time
   return time_folder

def get_time_path(path):
   time_path = os.stat(path).st_mtime # last modified time
   return time_path

def give_tail(count):
   base = 26 # number of Latin alphabets
   start = 97 # ASCII code of 'a'
   small = chr(count % base + start)
   big = chr(count // base + start)
   tail = str(big) + str(small)
   return tail

def constant():
   table = {
      "inner_width": 840,
      "inner_height": 1080,
      "outer_width": 960,
      "outer_height": 1360,
      "limit_line": 300,
   }
   return table

