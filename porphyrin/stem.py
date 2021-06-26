from pdb import set_trace

from .organ import Stem
from . import aid as AID

class Document(Stem):

   KIND = "document"
   TAG = "main"

   def __init__(self, **data):
      self.fill_basic(**data)
      self.sinks = []
      self.address = ''
      self.definitions = []
      self.instructions = []
      self.expanded = False

   def parse(self):
      head = self.move_right(0, 0)
      while (head < len(self.source)):
         bough, head = self.snip_bough(head)
         if bough:
            self.sinks.append(bough)
         head = self.move_right(0, head)

   def write(self):
      contents = []
      self.parse()
      for bough in self.sinks:
         if bough:
            contents.append(bough.write())
      content = AID.unite(contents, cut = '\n')
      result = AID.write_element(
            content = content,
            tag = self.TAG,
            attributes = ["class"],
            values = [self.KIND],
      )
      return result

   def expand(self, head_left):
      assert (len(self.definitions) == len(self.instructions))
      sink = self.source[head_left:]
      for count in range(len(self.definitions)):
         definition = self.definitions[count]
         instruction = self.instructions[count]
         sink = sink.replace(definition, instruction)
      self.source = sink

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Graph(Stem):

   KIND = "graph"
   TAG = "img"

   def __init__(self, **data):
      self.fill_basic(**data)
      self.address = ''
      self.sink = None

   def parse(self):
      leaf, _ = self.snip_leaf(0)
      if not (leaf.KIND == "link"):
         from .caution import Invalid_link_for_image as creator
         creator(**data).panic()
      self.sink = leaf.write()

   def write(self):
      self.parse()
      contents = ["<img"]
      contents.append("src=\"" + self.sink + '\"')
      contents.append("class=\"" + self.KIND + '\"')
      caption = self.sink.split('/')[-1]
      contents.append("alt=\"" + AID.extract_caption(self.sink) + '\"')
      contents.append('>')
      result = AID.unite(contents)
      return result

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Break(Stem):

   KIND = "break"
   TAG = "div"

   def __init__(self, **data):
      self.fill_basic(**data)
      self.sinks = []

   def parse(self):
      space = "<span class=\"phrase\">&emsp;</span>"
      dingbat = "<span class=\"phrase\">&#10086;</span>"
      repeat = 3
      for _ in range(repeat):
         self.sinks.append(space)
         self.sinks.append(dingbat)

   def write(self):
      contents = []
      self.parse()
      for sink in self.sinks:
         contents.append(sink)
      content = AID.unite(contents)
      result = AID.write_element(
         content = content,
         tag = self.TAG,
         attributes = ["class"],
         values = [self.KIND],
      )
      return result

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Paragraphs(Stem):

   KIND = "paragraphs"
   TAG = "div"

   def __init__(self, **data):
      self.fill_basic(**data)
      self.sinks = []

   def parse(self):
      head = self.move_right(0, 0)
      while (head < len(self.source)):
         twig, head = self.shatter_stem("newline", Paragraph, head)
         if twig:
            self.sinks.append(twig)
         head = self.move_right(0, head)

   def write(self):
      contents = []
      self.explain()
      self.parse()
      for twig in self.sinks:
         if twig:
            contents.append(twig.write())
      content = AID.unite(contents, cut = '\n')
      if not content:
         return ''
      result = AID.write_element(
            content = content,
            tag = self.TAG,
            attributes = ["class"],
            values = [self.KIND],
      )
      return result

class Lines(Stem):

   KIND = "lines"
   TAG = "div"

   def __init__(self, **data):
      self.fill_basic(**data)
      self.sinks = []

   def parse(self):
      head = self.move_right(0, 0)
      while (head < len(self.source)):
         twig, head = self.shatter_stem("newline", Line, head)
         if twig:
            self.sinks.append(twig)
         head = self.move_right(0, head)

   def write(self):
      contents = []
      self.parse()
      for twig in self.sinks:
         if twig:
            contents.append(twig.write())
      content = AID.unite(contents, cut = '\n')
      if not content:
         return ''
      result = AID.write_element(
            content = content,
            tag = self.TAG,
            attributes = ["class"],
            values = [self.KIND],
      )
      return result

class Rows(Stem):

   KIND = "rows"
   TAG_ALL = "table"
   TAG_HEAD = "thead"
   TAG_BODY = "tbody"

   def __init__(self, **data):
      self.fill_basic(**data)
      self.sinks = []

   def parse(self):
      head = self.move_right(0, 0)
      while (head < len(self.source)):
         twig, head = self.shatter_stem("newline", Row, head)
         if twig:
            self.sinks.append(twig)
         head = self.move_right(0, head)

   def write(self):
      contents = []
      self.parse()
      twig_head = self.sinks.pop(0)
      element = AID.write_element(
         content = twig_head.write(),
         tag = self.TAG_HEAD,
         attributes = ["class"],
         values = [self.KIND],
      )
      contents.append(element)
      for twig_body in self.sinks:
         element = AID.write_element(
            content = twig_body.write(),
            tag = self.TAG_BODY,
         )
         contents.append(element)

      setups = ["<colgroup>"]
      count_row = len(self.sinks[0].sinks)
      highest_count_row = 12
      if (count_row > highest_count_row):
         row = self.sinks[0]
         data = row.give_data(0, len(row.source))
         from .caution import Too_many_column as creator
         creator(**data).panic()
      weights = [0] * count_row
      for row in self.sinks:
         if not (len(row.sinks) == count_row):
            data = row.give_data(0, len(row.source))
            from .caution import Column_not_agreeing as creator
            creator(**data).panic()
         for index in range(count_row):
            weights[index] += len(row.sinks[index].source)
      percentages = AID.normalize_percentage(weights)
      for percentage in percentages:
         setups.append("<col style=\"width: {}%;\">".format(percentage))
      setups.append("</colgroup>")
      setup = AID.unite(setups, cut = '\n')
      contents.insert(0, setup)

      content = AID.unite(contents, cut = '\n')
      if not content:
         return ''
      result = AID.write_element(
         content = content,
         tag = self.TAG_ALL,
         attributes = ["class"],
         values = [self.KIND],
      )
      return result

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Paragraph(Stem):

   KIND = "paragraph"
   TAG = "p"

   def __init__(self, **data):
      self.fill_basic(**data)
      self.sinks = []

   def parse(self):
      head = self.move_right(0, 0)
      while (head < len(self.source)):
         frond, head = self.shatter_stem("space", Phrase, head)
         if not frond:
            continue
         self.sinks.append(frond)
         head = self.move_right(0, head)

   def write(self):
      contents = []
      self.parse()
      for frond in self.sinks:
         contents.append(frond.write())
      content = AID.unite(contents)
      if not content:
         return ''
      result = AID.write_element(
            content = content,
            tag = self.TAG,
            attributes = ["class"],
            values = [self.KIND],
      )
      return result

class Line(Stem):

   KIND = "line"
   TAG = "p"

   def __init__(self, **data):
      self.fill_basic(**data)
      self.sinks = []

   def parse(self):
      head = self.move_right(0, 0)
      while (head < len(self.source)):
         frond, head = self.shatter_stem("space", Verse, head)
         if not frond:
            continue
         self.sinks.append(frond)
         head = self.move_right(0, head)

   def write(self):
      contents = []
      self.parse()
      for frond in self.sinks:
         contents.append(frond.write())
      content = AID.unite(contents)
      if not content:
         return ''
      result = AID.write_element(
            content = content,
            tag = self.TAG,
            attributes = ["class"],
            values = [self.KIND],
      )
      return result

class Row(Stem):

   KIND = "row"
   TAG = "tr"

   def __init__(self, **data):
      self.fill_basic(**data)
      self.sinks = []

   def parse(self):
      head = self.move_right(0, 0)
      while (head < len(self.source)):
         frond, head = self.shatter_stem("space", Cell, head)
         if not frond:
            continue
         self.sinks.append(frond)
         head = self.move_right(0, head)

   def write(self):
      contents = []
      self.parse()
      for frond in self.sinks:
         contents.append(frond.write())
      content = AID.unite(contents)
      if not content.strip(" \t\n"):
         return "&nbsp;&nbsp;"
      result = AID.write_element(
            content = content,
            tag = self.TAG,
            attributes = ["class"],
            values = [self.KIND],
      )
      return result

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Phrase(Stem):

   KIND = "phrase"
   TAG = "span"

   def __init__(self, **data):
      self.fill_basic(**data)
      self.sinks = []

   def parse(self):
      head = self.move_right(0, 0)
      while (head < len(self.source)):
         leaf, head = self.snip_leaf(head)
         if (not leaf) or (not leaf.source.strip(" \t\n")):
            continue
         if (leaf.KIND == "link"):
            if not self.sinks:
               from .caution import Disallowing_link as creator
               creator(**data).panic()
            address = leaf.write()
            self.sinks[-1].address = address
         else:
            self.sinks.append(leaf)
         head = self.move_right(0, head)

   def write(self):
      contents = []
      self.explain()
      self.parse()
      for leaf in self.sinks:
         if not AID.be_literary(leaf.KIND):
            continue
         leaf.capitalize()
         break
      for leaf in self.sinks:
         if AID.be_literary(leaf.KIND):
            punctuations = {',', ':', ';', '.', '?', '!'}
            if leaf.source[0] in punctuations:
               last = contents.pop()
               contents.append(last + leaf.write())
               continue
         contents.append(leaf.write())
      content = AID.unite(contents)
      if not content:
         return AID.give_wide_space()
      result = AID.write_element(
            cut = '',
            content = content,
            tag = self.TAG,
            attributes = ["class"],
            values = [self.KIND],
      )
      return result

class Verse(Stem):

   KIND = "verse"
   TAG = "span"

   def __init__(self, **data):
      self.fill_basic(**data)
      self.sinks = []

   def parse(self):
      head = self.move_right(0, 0)
      while (head < len(self.source)):
         leaf, head = self.snip_leaf(head)
         if (not leaf) or (not leaf.source.strip(" \t\n")):
            continue
         if (leaf.KIND == "link"):
            if not self.sinks:
               from .caution import Disallowing_link as creator
               creator(**data).panic()
            address = leaf.write()
            self.sinks[-1].address = address
         else:
            self.sinks.append(leaf)
         head = self.move_right(0, head)

   def write(self):
      contents = []
      self.explain()
      self.parse()
      for leaf in self.sinks:
         contents.append(leaf.write())
      content = AID.unite(contents)
      if not content:
         return AID.give_wide_space()
      result = AID.write_element(
            cut = '',
            content = content,
            tag = self.TAG,
            attributes = ["class"],
            values = [self.KIND],
      )
      return result

class Cell(Stem):

   KIND = "cell"
   TAG = "td"

   def __init__(self, **data):
      self.fill_basic(**data)
      self.sinks = []

   def parse(self):
      head = self.move_right(0, 0)
      while (head < len(self.source)):
         leaf, head = self.snip_leaf(head)
         if (not leaf) or (not leaf.source.strip(" \t\n")):
            continue
         if (leaf.KIND == "link"):
            if not self.sinks:
               from .caution import Disallowing_link as creator
               creator(**data).panic()
            address = leaf.write()
            self.sinks[-1].address = address
         else:
            self.sinks.append(leaf)
         head = self.move_right(0, head)

   def write(self):
      contents = []
      self.explain()
      self.parse()
      for leaf in self.sinks:
         contents.append(leaf.write())
      content = AID.unite(contents)
      if not content:
         return AID.give_wide_space()
      result = AID.write_element(
            cut = '',
            content = content,
            tag = self.TAG,
            attributes = ["class"],
            values = [self.KIND],
      )
      return result
