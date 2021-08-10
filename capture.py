#! /usr/bin/env python3

import os
import io
import numpy as NUMPY
from selenium import webdriver as DRIVER
from PIL import Image as IMAGE
from PIL import ImageEnhance as ENHANCE

def main():
   folder_this = os.path.dirname(__file__)
   folder_cipher = os.path.join(folder_this, "post-cipher")
   folder_book = os.path.join(folder_this, "book")
   folder_shot = os.path.join(folder_book, "shot")
   folder_slice = os.path.join(folder_book, "slice")
   folder_leaf = os.path.join(folder_book, "leaf")
   assert(os.path.isdir(folder_cipher))
   assert(os.path.isdir(folder_book))
   assert(os.path.isdir(folder_shot))
   assert(os.path.isdir(folder_slice))
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
   shred_photograph(folder_slice, folder_shot)

def shred_photograph(folder_slice, folder_shot):
   suffix = ".png"
   tmp = 0
   for name_shot in os.listdir(folder_shot):
      tmp += 1
      if tmp >= 2:
         break

      if not name_shot.endswith(suffix):
         continue
      bare = name_shot[:-len(suffix)]
      path_shot = os.path.join(folder_shot, name_shot)
      if not os.path.isfile(path_shot):
         continue
      print("slicing:", path_shot, "......")
      with IMAGE.open(path_shot) as graph:
         matrix = NUMPY.asarray(graph.convert('L'))
         height = matrix.shape[0]
         width = matrix.shape[1]
         marginal = [sum(row) for row in list(matrix)]
         flip = [255 * width - value for value in marginal]
         print(flip[0:20])
         above = 0
         below = 0
         count_tail = 0
         unit = 24
         bright = int(width / 128)
         for ruler in range(len(flip)):
            gray = flip[ruler]
            if (gray > bright):
               continue
            name_slice = bare + give_tail(count_tail) + suffix
            path_slice = os.path.join(folder_slice, name_slice)
            if (ruler - above >= unit):
               below = ruler
               print("ruler:", ruler)
               part = graph.crop((0, above, height, below + 1))
               part.save(path_slice, quality = 100)
               above = below
               count_tail += 1

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
         graph = enhance_contrast(graph)
         graph = enhance_sharpness(graph)
         graph.save(path_graph, quality = 100)

def enhance_sharpness(graph):
   level = 1.4
   graph = ENHANCE.Sharpness(graph).enhance(level)
   return graph

def enhance_contrast(graph):
   level = 1.2
   graph = ENHANCE.Contrast(graph).enhance(level)
   return graph

def save_screenshot(address):
   tag = "main"
   size = 1536
   os.environ["MOZ_HEADLESS"] = "1"
   print("capturing:", address, "......")
   driver = DRIVER.Firefox()
   driver.set_window_size(size, size)
   driver.get(address)
   element = driver.find_element_by_tag_name(tag)
   graph = element.screenshot_as_png
   driver.quit()
   return graph

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

def give_tail(count):
   base = 26
   start = 97
   small = str(chr(count % base + start))
   big = str(chr(int(count // base) + start))
   tail = str(big) + str(small)
   return big + small

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

main()