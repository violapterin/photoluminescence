from pdb import set_trace

from .organ import Leaf
from . import aid as AID

class Serif_roman(Leaf):

   KIND = "serif-roman"
   TAG_PLAIN = "span"

   def __init__(self, **data):
      self.fill_basic(**data)
      self.address = ''
      self.bound_wrap = 24

   def write(self):
      content = AID.tune_text(self.source)
      content = AID.chop_word_text(content, self.bound_wrap)
      if content:
         sink = self.write_text(content)
      return sink

class Serif_italic(Leaf):

   KIND = "serif-italic"
   TAG_PLAIN = "em"

   def __init__(self, **data):
      self.fill_basic(**data)
      self.address = ''
      self.bound_wrap = 24

   def write(self):
      content = AID.tune_text(self.source)
      content = AID.chop_word_text(content, self.bound_wrap)
      if content:
         sink = self.write_text(content)
      return sink

class Serif_bold(Leaf):

   KIND = "serif-bold"
   TAG_PLAIN = 'b'

   def __init__(self, **data):
      self.fill_basic(**data)
      self.address = ''
      self.bound_wrap = 24

   def write(self):
      content = AID.tune_text(self.source)
      content = AID.chop_word_text(content, self.bound_wrap)
      if content:
         sink = self.write_text(content)
      return sink

class Sans_roman(Leaf):

   KIND = "sans-roman"
   TAG_PLAIN = "span"

   def __init__(self, **data):
      self.fill_basic(**data)
      self.address = ''
      self.bound_wrap = 24

   def write(self):
      content = AID.tune_text(self.source)
      content = AID.chop_word_text(content, self.bound_wrap)
      if content:
         sink = self.write_text(content)
      return sink

class Sans_bold(Leaf):

   KIND = "sans-bold"
   TAG_PLAIN = 'b'

   def __init__(self, **data):
      self.fill_basic(**data)
      self.address = ''
      self.bound_wrap = 24

   def write(self):
      content = AID.tune_text(self.source)
      content = AID.chop_word_text(content, self.bound_wrap)
      if content:
         sink = self.write_text(content)
      return sink

class Mono(Leaf):

   KIND = "mono"
   TAG_PLAIN = "code"

   def __init__(self, **data):
      self.fill_basic(**data)
      self.address = ''
      self.bound_wrap = 32

   def write(self):
      content = AID.tune_code(self.source)
      content = AID.chop_word_code(content, self.bound_wrap)
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
      many_sink = [
         token_left,
         AID.tune_comment(self.source),
         token_right,
      ]
      sink = AID.unite(many_sink)
      return sink

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Math(Leaf):

   KIND = "math"
   TAG = "span"

   def __init__(self, **data):
      self.fill_basic(**data)

   def write(self):
      many_content = []
      head = self.move_right(0, 0)
      while (head < len(self.source)):
         tissue, head = self.snip_tissue_math(head)
         if tissue:
            tissue.OUTSIDE = True
            many_content.append(tissue.write())
         head = self.move_right(0, head)
      content = AID.unite(many_content, cut = '')
      sink = AID.write_element(
            cut = '',
            content = content,
            tag = self.TAG,
            many_attribute = ["class"],
            many_value = [self.KIND],
      )
      sink.strip()
      return sink

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Pseudo(Leaf):

   KIND = "pseudo"
   TAG = "span"

   def __init__(self, **data):
      self.fill_basic(**data)

   def write(self):
      many_content = []
      head = self.move_right(0, 0)
      while (head < len(self.source)):
         tissue, head = self.snip_tissue_pseudo(head)
         if tissue:
            tissue.OUTSIDE = True
            many_content.append(tissue.write())
         head = self.move_right(0, head)
      content = AID.unite(many_content)
      sink = AID.write_element(
            content = content,
            tag = self.TAG,
            many_attribute = ["class"],
            many_value = [self.KIND],
      )
      return sink
