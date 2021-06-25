from pdb import set_trace

from .organ import Leaf
from . import aid as AID

class Serif_roman(Leaf):

   KIND = "serif-roman"
   TAG_PLAIN = "span"

   def __init__(self, **data):
      self.fill_basic(**data)
      self.address = ''

   def write(self):
      content = AID.tune_text(self.source)
      if content:
         sink = self.write_text(content)
      return sink

class Serif_italic(Leaf):

   KIND = "serif-italic"
   TAG_PLAIN = "em"

   def __init__(self, **data):
      self.fill_basic(**data)
      self.address = ''

   def write(self):
      content = AID.tune_text(self.source)
      if content:
         sink = self.write_text(content)
      return sink

class Serif_bold(Leaf):

   KIND = "serif-bold"
   TAG_PLAIN = 'b'

   def __init__(self, **data):
      self.fill_basic(**data)
      self.address = ''

   def write(self):
      content = AID.tune_text(self.source)
      if content:
         sink = self.write_text(content)
      return sink

class Sans_roman(Leaf):

   KIND = "sans-roman"
   TAG_PLAIN = "span"

   def __init__(self, **data):
      self.fill_basic(**data)
      self.address = ''

   def write(self):
      content = AID.tune_text(self.source)
      if content:
         sink = self.write_text(content)
      return sink

class Sans_bold(Leaf):

   KIND = "sans-bold"
   TAG_PLAIN = 'b'

   def __init__(self, **data):
      self.fill_basic(**data)
      self.address = ''

   def write(self):
      content = AID.tune_text(self.source)
      if content:
         sink = self.write_text(content)
      return sink

class Mono(Leaf):

   KIND = "mono"
   TAG_PLAIN = "code"

   def __init__(self, **data):
      self.fill_basic(**data)
      self.address = ''

   def write(self):
      content = AID.tune_code(self.source)
      if content:
         sink = self.write_text(content)
      return sink

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Link(Leaf):

   KIND = "link"

   def __init__(self, **data):
      self.fill_basic(**data)

   def write(self):
      return AID.tune_hypertext(self.source)

class Newline(Leaf):

   KIND = "newline"

   def __init__(self, **data):
      self.fill_basic(**data)

   def write(self):
      return ''

class Space(Leaf):

   KIND = "space"

   def __init__(self, **data):
      self.fill_basic(**data)

   def write(self):
      return ''

class Comment(Leaf):

   KIND = "comment"

   def __init__(self, **data):
      self.fill_basic(**data)

   def write(self):
      token_left = "<!--"
      token_right = "-->"
      sinks = [
         token_left,
         AID.tune_comment(self.source),
         token_right,
      ]
      sink = AID.unite(sinks)
      return sink

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Math(Leaf):

   KIND = "math"
   TAG = "span"

   def __init__(self, **data):
      self.fill_basic(**data)

   def write(self):
      contents = []
      head = self.move_right(0, 0)
      while (head < len(self.source)):
         tissue, head = self.snip_tissue_math(head)
         if tissue:
            # # XXX comment out this line when debugging:
            tissue.OUTSIDE = True
            contents.append(tissue.write())
         head = self.move_right(0, head)
      content = AID.unite(contents)
      sink = AID.write_element(
            cut = ' ',
            content = content,
            tag = self.TAG,
            attributes = ["class"],
            values = [self.KIND],
      )
      return sink

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Pseudo(Leaf):

   KIND = "pseudo"
   TAG = "span"

   def __init__(self, **data):
      self.fill_basic(**data)

   def write(self):
      contents = []
      head = self.move_right(0, 0)
      while (head < len(self.source)):
         tissue, head = self.snip_tissue_pseudo(head)
         if tissue:
            tissue.OUTSIDE = True
            contents.append(tissue.write())
         head = self.move_right(0, head)
      content = AID.unite(contents)
      sink = AID.write_element(
            content = content,
            tag = self.TAG,
            attributes = ["class"],
            values = [self.KIND],
      )
      return sink
