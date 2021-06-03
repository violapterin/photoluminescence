from pdb import set_trace

from .organ import Stem
from . import aid as AID

class Document(Stem):

   KIND = "document"

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
         contents.append(bough.write())
      result = AID.unite(contents, cut = '\n')
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

class Image(Stem):

   KIND = "image"
   TAG = "img"

   def __init__(self, **data):
      self.fill_basic(**data)
      self.address = ''
      self.sink = None

   def parse(self):
      address = AID.tune_hypertext(self.address)

   def write(self):
      self.parse()
      result = AID.write_element(
         content = '',
         tag = self.TAG,
         attributes = ["class"],
         values = [self.KIND],
      )
      return result

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Break(Stem):

   KIND = "break"
   TAG = "div"

   def __init__(self, **data):
      self.fill_basic(**data)
      self.sinks = []

   def parse(self):
      dingbat = "&#10086;"
      repeat = 3
      self.sinks = dingbat * repeat

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
         contents.append(twig.write())
      content = AID.unite(contents, cut = '\n')
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
         contents.append(twig.write())
      content = AID.unite(contents, cut = '\n')
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
   TAG_PREFIX = "thead"
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
      twig_prefix = self.sinks.pop(0)
      element = AID.write_element(
         content = twig_prefix.write(),
         tag = self.TAG_PREFIX,
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
      content = AID.unite(contents, cut = '\n')
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
         if frond:
            self.sinks.append(frond)
         head = self.move_right(0, head)

   def write(self):
      contents = []
      self.parse()
      for frond in self.sinks:
         contents.append(frond.write())
      content = AID.unite(contents)
      result = AID.write_element(
            content = content,
            tag = self.TAG,
            attributes = ["class"],
            values = [self.KIND],
      )
      return result

class Line(Stem):

   KIND = "line"
   TAG = "div"

   def __init__(self, **data):
      self.fill_basic(**data)
      self.sinks = []

   def parse(self):
      head = self.move_right(0, 0)
      while (head < len(self.source)):
         frond, head = self.shatter_stem("space", Verse, head)
         if frond:
            self.sinks.append(frond)
         head = self.move_right(0, head)

   def write(self):
      contents = []
      self.parse()
      for frond in self.sinks:
         contents.append(frond.write())
      content = AID.unite(contents)
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
         if frond:
            self.sinks.append(frond)
         head = self.move_right(0, head)

   def write(self):
      contents = []
      self.parse()
      for frond in self.sinks:
         contents.append(frond.write())
      content = AID.unite(contents)
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
   TAG = "div"

   def __init__(self, **data):
      self.fill_basic(**data)
      self.sinks = []

   def parse(self):
      head = self.move_right(0, 0)
      while (head < len(self.source)):
         leaf, head = self.snip_leaf(head)
         if leaf:
            self.sinks.append(leaf)
         head = self.move_right(0, head)

   def write(self):
      contents = []
      self.explain()
      self.parse()
      for leaf in self.sinks:
         contents.append(leaf.write())
      content = AID.unite(contents)
      result = AID.write_element(
            cut = ' ',
            content = content,
            tag = self.TAG,
            attributes = ["class"],
            values = [self.KIND],
      )
      return result

class Verse(Stem):

   KIND = "verse"
   TAG = "div"

   def __init__(self, **data):
      self.fill_basic(**data)
      self.sinks = []

   def parse(self):
      head = self.move_right(0, 0)
      while (head < len(self.source)):
         leaf, head = self.snip_leaf(head)
         if leaf:
            self.sinks.append(leaf)
         head = self.move_right(0, head)

   def write(self):
      contents = []
      self.explain()
      self.parse()
      for leaf in self.sinks:
         contents.append(leaf.write())
      content = AID.unite(contents)
      result = AID.write_element(
            cut = ' ',
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
         if leaf:
            self.sinks.append(leaf)
         head = self.move_right(0, head)

   def write(self):
      contents = []
      self.explain()
      self.parse()
      for leaf in self.sinks:
         contents.append(leaf.write())
      content = AID.unite(contents)
      result = AID.write_element(
            cut = ' ',
            content = content,
            tag = self.TAG,
            attributes = ["class"],
            values = [self.KIND],
      )
      return result

