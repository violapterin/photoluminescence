#! /usr/bin/env python3

import os
import io
import numpy as NUMPY
from selenium import webdriver as DRIVER
from PIL import Image as IMAGE
from PIL import ImageEnhance as ENHANCE
from PIL import ImageOps as OPERATION

def main():
   folder_this = os.path.dirname(__file__)
   folder_cipher = os.path.join(folder_this, "post-cipher")
   folder_book = os.path.join(folder_this, "book")
   folder_shot = os.path.join(folder_book, "shot")
   folder_strip = os.path.join(folder_book, "strip")
   folder_leaf = os.path.join(folder_book, "leaf")
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
   many_title = many_title[0:1] # XXX
   take_photograph(folder_shot, many_title)
   #shred_photograph(folder_strip, folder_shot)
   #patch_leaf(folder_strip, folder_leaf)

def patch_leaf(folder_strip, folder_leaf):
   limit_height = 1080
   total = 0
   for name_strip in os.listdir(folder_strip):
      path_strip = os.path.join(folder_strip, name_strip)
      if not os.path.isfile(path_strip):
         continue
      leaf = None
      with IMAGE.open(path_strip) as strip:
         if (total == 0):
            leaf = copy(strip)
         height = graph.size[1]
         if (total + height > limit_height):
            patch(strip, leaf)
         total += height

def shred_photograph(folder_strip, folder_shot):
   suffix = ".png"
   tmp = 0 # XXX
   for name_shot in os.listdir(folder_shot):
      tmp += 1 # XXX
      if tmp >= 2: break # XXX
      if not name_shot.endswith(suffix):
         continue
      bare_graph = name_shot[:-len(suffix)]
      path_graph = os.path.join(folder_shot, name_shot)
      if not os.path.isfile(path_graph):
         continue
      folder_graph = os.path.join(folder_strip, bare_graph)
      if not os.path.isdir(folder_graph):
         os.system("mkdir" + ' ' + folder_graph)
      if not compare_folder_with_file(folder_graph, path_graph):
         continue
      print("Slicing:", path_graph, "......")
      limit_bright = 255
      height_line = 288
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
            name_strip = bare_graph + give_tail(head) + suffix
            path_strip = os.path.join(folder_graph, name_strip)
            above = many_boundary[head]
            below = many_boundary[head + 1]
            part = graph.crop((0, above, width - 1, below))
            if (below - above < height_line):
               part = enhance_contrast(part)
               part = enhance_sharpness(part)
            part.save(path_strip, quality = 100)

def take_photograph(folder_shot, many_title):
   prefix = "https://www.violapterin.com/post/"
   many_path_graph = []
   for title in many_title:
      stamp = title.split('-')[0]
      address = prefix + title + ".html"
      path_graph = os.path.join(folder_shot, stamp) + ".png"
      if os.path.isfile(path_graph):
         continue
      many_path_graph.append(path_graph)
      binary = save_screenshot(address)
      with IMAGE.open(io.BytesIO(binary)) as graph:
         graph.save(path_graph, quality = 100)

def pad_leaf(leaf):
   width = 1200
   height = 1700
   more_width = width - leaf.size[0]
   more_height = height - leaf.size[1]
   left_width = more_width // 2
   left_height = more_height // 2
   right_width = more_width - left_width
   right_height = more_height - left_height
   coordinate = (
      left_width,
      left_height,
      right_width,
      right_height,
   )
   expanded = OPERATION.expand(leaf, coordinate)
   return expanded

def save_screenshot(address):
   id_heading = "header-post"
   class_content = "document"
   size = 1536
   os.environ["MOZ_HEADLESS"] = "1"
   print("Capturing:", address, "......")
   driver = DRIVER.Firefox()
   driver.set_window_size(size, size)
   driver.get(address)
   element_heading = driver.find_element_by_id(id_heading)
   graph_heading = element_heading.screenshot_as_png
   element_content = driver.find_element_by_class(class_content)
   graph_content = element_content.screenshot_as_png
   driver.quit()
   graph = concatenate_graph(graph_content, graph_heading)
   return graph

def enhance_sharpness(strip):
   level = 2.5
   strip = ENHANCE.Sharpness(strip).enhance(level)
   return strip

def enhance_contrast(strip):
   level = 1.0
   strip = ENHANCE.Contrast(strip).enhance(level)
   return strip

def concatenate_graph(down, top):
   height_top = top.size[1]
   height_down = down.size[1]
   width = max(top.size[0], down.size[0])
   dimension = (width, height_top + height_down)
   combined = IMAGE.new("RGB", dimension)
   combined.paste(top, (0, 0))
   combined.paste(down, (0, height_top))
   return combined

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

def compare_folder_with_file(folder, path):
   time_folder = 0
   time_path = os.stat(path).st_mtime
   many_thing = os.scandir(folder)
   for thing in many_thing:
      if not thing.is_file():
         continue
      time = thing.stat().st_mtime
      if time_folder < time:
         time_folder = time
   return (time_folder < time_path)

def give_tail(count):
   base = 26
   start = 97
   small = str(chr(count % base + start))
   big = str(chr(count // base + start))
   tail = str(big) + str(small)
   return big + small

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

main()