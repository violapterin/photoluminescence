import os
import io
import copy
import shutil
import numpy as NUMPY
from selenium import webdriver as DRIVER
from PIL import Image as IMAGE

def main(whether_new):
   folder_this = os.path.dirname(__file__)
   folder_cipher = os.path.join(folder_this, "post-cipher")
   folder_book = os.path.join(folder_this, "book")
   folder_shot = os.path.join(folder_book, "shot")
   folder_strip = os.path.join(folder_book, "strip")
   folder_leaf = os.path.join(folder_book, "leaf")
   assert(os.path.isdir(folder_cipher))
   assert(os.path.isdir(folder_book))
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
   many_title = extract_title(folder_cipher)

   take_photograph(whether_new, folder_shot, many_title)
   shred_photograph(whether_new, folder_strip, folder_shot)
   patch_leaf(whether_new, folder_leaf, folder_strip)

def patch_leaf(whether_new, folder_leaf, folder_strip):
   if whether_new:
      if not compare_folder_with_folder(folder_leaf, folder_strip):
         return
   suffix_in = ".png"
   suffix_out = ".png"
   height_inner = constant()["height_inner"]
   limit_switch = constant()["limit_switch"]
   total = 0
   number_page = 0
   stamp_last = ''
   stamp_next = ''
   leaf = None
   for name_article in os.listdir(folder_strip):
      folder_article = os.path.join(folder_strip, name_article)
      if not os.path.isdir(folder_article):
         continue
      for name_strip in os.listdir(folder_article):
         stamp_next = name_strip[0:6]
         if not name_strip.endswith(suffix_in):
            continue
         path_strip = os.path.join(folder_article, name_strip)
         if not os.path.isfile(path_strip):
            continue
         with IMAGE.open(path_strip) as strip:
            height = strip.size[1]
            height_skip = constant()["height_skip"]
            whether_clear = False
            whether_switch = False
            if stamp_last and (stamp_last != stamp_next):
               whether_switch = True
            stamp_last = stamp_next
            if whether_switch:
               if (total + height_skip > limit_switch):
                  whether_clear = True
            else:
               if (total + height > height_inner):
                  whether_clear = True
            if whether_switch:
               leaf = append_skip(leaf)
               total += height_skip
            if whether_clear:
               total = 0
               name_leaf = str(number_page).zfill(3) + suffix_out
               number_page += 1
               leaf = tune_leaf(leaf)
               print("Saving leaf:", name_leaf, "......")
               path_leaf = os.path.join(folder_leaf, name_leaf)
               leaf.save(path_leaf, quality = 100)
               leaf = None
            if leaf:
               leaf = concatenate_graph(strip, leaf)
            else:
               leaf = copy.copy(strip)
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
      with IMAGE.open(path_graph) as graph:
         matrix = NUMPY.asarray(graph.convert('L'))
         height = matrix.shape[0]
         width = matrix.shape[1]
         least_bright = int(width * constant()["least_bright"])
         marginal = [sum(row) for row in list(matrix)]
         flip = [limit_bright * width - value for value in marginal]
         passed = [(value > least_bright) for value in flip]
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
            print("Slicing:", name_strip, "......")
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
   #id_heading = "header-post"
   kind = "essay"
   size = constant()["width_window"]
   os.environ["MOZ_HEADLESS"] = "1"
   driver = DRIVER.Firefox()
   driver.set_window_size(size, size)
   print("Capturing address:", address, "......")
   driver.get(address)
   element = driver.find_element_by_class_name(kind)
   binary = element.screenshot_as_png
   graph = IMAGE.open(io.BytesIO(binary))
   driver.quit()
   graph = graph.convert("RGB")
   return graph

def concatenate_graph(down, top):
   height_top = top.size[1]
   height_down = down.size[1]
   width = max(top.size[0], down.size[0])
   height = height_top + height_down
   dimension = (width, height)
   combined = IMAGE.new("RGBA", dimension, "WHITE")
   ratio_top = constant()["ratio_top"]
   more_width_top = int(ratio_top * (width - top.size[0]))
   more_width_down = int((1 / 2) * (width - down.size[0]))
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
   width_outer = constant()["width_outer"]
   height_inner = constant()["height_inner"]
   height_outer = constant()["height_outer"]
   margin_height = int((height_outer - height_inner) / 2)
   more_width = int((width_outer - leaf.size[0]) / 2)
   more_height = height_outer - leaf.size[1]
   more_height = int(more_height * constant()["height_outer"])
   more_height = max(0, min(margin_height, more_height))
   dimension = (width_outer, height_outer)
   combined = IMAGE.new("RGBA", dimension, "WHITE")
   more = (more_width, more_height)
   combined.paste(leaf, more, mask = leaf_alpha)
   combined = combined.convert("RGB")
   return combined

def append_skip(leaf):
   width_skip = constant()["width_skip"]
   height_skip = constant()["height_skip"]
   height_stripe = constant()["height_stripe"]
   dimension_skip = (width_skip, height_skip)
   dimension_stripe = (width_skip, height_stripe)
   skip = IMAGE.new("RGBA", dimension_skip, "WHITE")
   stripe = IMAGE.new("RGBA", dimension_stripe, "GRAY")
   stripe_alpha = stripe.convert("RGBA")
   offset = (0, int(height_skip / 2))
   skip.paste(stripe, offset, mask = stripe_alpha)
   if not leaf:
      skip = skip.convert("RGB")
      return skip
   else:
      leaf = concatenate_graph(skip, leaf)
   leaf = leaf.convert("RGB")
   return leaf

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
      return True
   if not os.path.isdir(that_folder):
      return False
   time_this = get_time_folder(this_folder)
   time_that = get_time_folder(that_folder)
   return (time_this < time_that)

def compare_folder_with_file(folder, path):
   if not os.path.isdir(folder):
      return True
   if not os.path.isfile(path):
      return False
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
      "width_window": 1600,
      "width_inner": 1080,
      "height_inner": 1440,
      "width_outer": 1200,
      "height_outer": 1700,
      "limit_switch": 960,
      "width_skip": 720,
      "height_skip": 96,
      "height_blank": 48,
      "height_stripe": 3,
      "least_bright": 1/192,
      "ratio_top": 2/3,
   }
   return table

