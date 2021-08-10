#! /usr/bin/env python3

import os
import io
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

   many_title = extract_title(folder_cipher)
   many_title.sort()
   #many_title = many_title[0:4] # XXX
   many_title = [
      "190711-shuri-castle-okinawa",
      "210719-valid-triangle-numbers",
   ]
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
      graph = IMAGE.open(io.BytesIO(binary))
      graph = enhance_contrast(graph)
      graph = enhance_sharpness(graph)
      graph.save(path_graph, quality = 92)

def enhance_sharpness(graph):
   level = 1.3
   graph = ENHANCE.Sharpness(graph).enhance(level)
   return graph

def enhance_contrast(graph):
   level = 1.1
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

def extract_title(folder):
   many_title = []
   suffix = ".txt"
   for name in os.listdir(folder):
      path = os.path.join(folder, name)
      if os.path.isfile(path):
         if not name.endswith(suffix):
            continue
         bare = name[:-len(suffix)]
         many_title.append(bare)
      elif os.path.isdir(path):
         many_title.extend(extract_title(path))
   return many_title

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

main()