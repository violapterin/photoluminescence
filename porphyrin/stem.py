from .organ import Stem
from . import aid as AID

class Document(Stem):

   KIND = "document"
   TAG = "main"

   def __init__(self, **data):
      self.fill_basic(**data)
      self.many_sink = []
      self.address = ''
      self.definitions = []
      self.instructions = []
      self.expanded = False

   def parse(self):
      head = self.move_right(0, 0)
      while (head < len(self.source)):
         bough, head = self.snip_bough(head)
         head = self.move_right(0, head)
         if not bough:
            continue
         self.many_sink.append(bough)

   def write(self):
      many_content = []
      self.parse()
      for bough in self.many_sink:
         if bough:
            many_content.append(bough.write())
      content = AID.unite(many_content, cut = '\n')
      result = AID.write_element(
            content = content,
            tag = self.TAG,
            many_attribute = ["class"],
            many_value = [self.KIND],
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
      many_content = ["<img"]
      many_content.append("src=\"" + self.sink + '\"')
      many_content.append("class=\"" + self.KIND + '\"')
      caption = self.sink.split('/')[-1]
      many_content.append("alt=\"" + AID.extract_caption(self.sink) + '\"')
      many_content.append('>')
      result = AID.unite(many_content)
      return result

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Break(Stem):

   KIND = "break"
   TAG = "div"

   def __init__(self, **data):
      self.fill_basic(**data)
      self.many_sink = []

   def parse(self):
      dingbat = "<span class=\"phrase\">❦</span>"
      space = "<span class=\"phrase\">&emsp;</span>"
      repeat = 3
      for _ in range(repeat):
         self.many_sink.append(space)
         self.many_sink.append(dingbat)

   def write(self):
      many_content = []
      self.parse()
      for sink in self.many_sink:
         many_content.append(sink)
      content = AID.unite(many_content)
      result = AID.write_element(
         content = content,
         tag = self.TAG,
         many_attribute = ["class"],
         many_value = [self.KIND],
      )
      return result

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Section(Stem):

   KIND = "section"
   TAG = "div"

   def __init__(self, **data):
      self.fill_basic(**data)
      self.many_sink = []

   def parse(self):
      head = self.move_right(0, 0)
      while (head < len(self.source)):
         twig, head = self.shatter_stem("newline", Paragraph, head)
         head = self.move_right(0, head)
         if not twig:
            continue
         self.many_sink.append(twig)

   def write(self):
      many_content = []
      self.explain()
      self.parse()
      for twig in self.many_sink:
         if twig:
            many_content.append(twig.write())
      content = AID.unite(many_content, cut = '\n')
      if not content:
         return ''
      result = AID.write_element(
            content = content,
            tag = self.TAG,
            many_attribute = ["class"],
            many_value = [self.KIND],
      )
      return result

class Stanza(Stem):

   KIND = "stanza"
   TAG = "div"

   def __init__(self, **data):
      self.fill_basic(**data)
      self.many_sink = []

   def parse(self):
      head = self.move_right(0, 0)
      while (head < len(self.source)):
         twig, head = self.shatter_stem("newline", Line, head)
         head = self.move_right(0, head)
         if not twig:
            continue
         self.many_sink.append(twig)

   def write(self):
      many_content = []
      self.parse()
      for twig in self.many_sink:
         if twig:
            many_content.append(twig.write())
      content = AID.unite(many_content, cut = '\n')
      if not content:
         return ''
      result = AID.write_element(
            content = content,
            tag = self.TAG,
            many_attribute = ["class"],
            many_value = [self.KIND],
      )
      return result

class Array(Stem):

   KIND = "array"
   TAG_ALL = "table"
   TAG_HEAD = "thead"
   TAG_BODY = "tbody"

   def __init__(self, **data):
      self.fill_basic(**data)
      self.many_sink = []

   def parse(self):
      head = self.move_right(0, 0)
      while (head < len(self.source)):
         twig, head = self.shatter_stem("newline", Row, head)
         head = self.move_right(0, head)
         if not twig:
            continue
         self.many_sink.append(twig)

   def write(self):
      many_content = []
      self.parse()
      twig_head = self.many_sink.pop(0)
      element = AID.write_element(
         content = twig_head.write(),
         tag = self.TAG_HEAD,
      )
      many_content.append(element)
      for twig_body in self.many_sink:
         element = AID.write_element(
            content = twig_body.write(),
            tag = self.TAG_BODY,
         )
         many_content.append(element)

      many_setup = ["<colgroup>"]
      count_twig = len(self.many_sink[0].many_sink)
      limit_count_twig = 12
      if (count_twig > limit_count_twig):
         twig = self.many_sink[0]
         data = twig.give_data(0, len(twig.source))
         from .caution import Too_many_column as creator
         creator(**data).panic()
      many_weight = [0] * count_twig
      for twig in self.many_sink:
         if not (len(twig.many_sink) == count_twig):
            data = twig.give_data(0, len(twig.source))
            from .caution import Column_not_agreeing as creator
            creator(**data).panic()
         for row in range(count_twig):
            many_weight[row] += len(twig.many_sink[row].source)
      many_percentage = AID.normalize_percentage(many_weight)
      for column in range(len(many_percentage)):
         percentage = many_percentage[column]
         many_setup.append(f"<col style=\"width: {percentage}%;\">")
      many_setup.append("</colgroup>")
      setup = AID.unite(many_setup, cut = '\n')
      many_content.insert(0, setup)
      content = AID.unite(many_content, cut = '\n')
      if not content:
         return ''
      result = AID.write_element(
         content = content,
         tag = self.TAG_ALL,
         many_attribute = ["class"],
         many_value = [self.KIND],
      )
      return result

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Paragraph(Stem):

   KIND = "paragraph"
   TAG = "p"

   def __init__(self, **data):
      self.fill_basic(**data)
      self.many_sink = []

   def parse(self):
      head = self.move_right(0, 0)
      while (head < len(self.source)):
         frond, head = self.shatter_stem("space", Phrase, head)
         head = self.move_right(0, head)
         if not frond:
            continue
         self.many_sink.append(frond)

   def write(self):
      many_content = []
      self.parse()
      for frond in self.many_sink:
         many_content.append(frond.write())
      content = AID.unite(many_content)
      if not content:
         return ''
      result = AID.write_element(
            content = content,
            tag = self.TAG,
            many_attribute = ["class"],
            many_value = [self.KIND],
      )
      return result

class Line(Stem):

   KIND = "line"
   TAG = "p"

   def __init__(self, **data):
      self.fill_basic(**data)
      self.many_sink = []

   def parse(self):
      head = self.move_right(0, 0)
      while (head < len(self.source)):
         frond, head = self.shatter_stem("space", Verse, head)
         head = self.move_right(0, head)
         if not frond:
            continue
         self.many_sink.append(frond)

   def write(self):
      many_content = []
      self.parse()
      for frond in self.many_sink:
         many_content.append(frond.write())
      content = AID.unite(many_content)
      if not content:
         return ''
      result = AID.write_element(
            content = content,
            tag = self.TAG,
            many_attribute = ["class"],
            many_value = [self.KIND],
      )
      return result

class Row(Stem):

   KIND = "row"
   TAG = "tr"

   def __init__(self, **data):
      self.fill_basic(**data)
      self.many_sink = []

   def parse(self):
      head = self.move_right(0, 0)
      while (head < len(self.source)):
         frond, head = self.shatter_stem("space", Cell, head)
         head = self.move_right(0, head)
         if not frond:
            continue
         self.many_sink.append(frond)
      size = len(self.many_sink)
      ratio = 3 / size - 3 / (size * size) + 1 / (size * size * size)
      for twig in self.many_sink:
         twig.bound_wrap = int(ratio * twig.bound_wrap)

   def write(self):
      many_content = []
      self.parse()
      for frond in self.many_sink:
         many_content.append(frond.write())
      content = AID.unite(many_content)
      result = AID.write_element(
            content = content,
            tag = self.TAG,
            many_attribute = ["class"],
            many_value = [self.KIND],
      )
      return result

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Phrase(Stem):

   KIND = "phrase"
   TAG = "span"

   def __init__(self, **data):
      self.fill_basic(**data)
      self.many_sink = []

   def parse(self):
      head = self.move_right(0, 0)
      while (head < len(self.source)):
         head = self.move_right(0, head)
         leaf, head = self.snip_leaf(head)
         if (not leaf) or (not leaf.source.strip(" \t\n")):
            continue
         if (leaf.KIND == "link"):
            if not self.many_sink:
               from .caution import Disallowing_link as creator
               creator(**data).panic()
            address = leaf.write()
            self.many_sink[-1].address = address
         else:
            self.many_sink.append(leaf)

   def write(self):
      many_content = []
      self.explain()
      self.parse()
      for leaf in self.many_sink:
         if AID.be_literary(leaf.KIND):
            leaf.capitalize()
            break
      kind_last = ''
      for leaf in self.many_sink:
         whether_glue = False
         if AID.be_literary(leaf.KIND):
            many_stop = {',', ':', ';', '.', '?', '!'}
            if leaf.source[0] in many_stop:
               whether_glue = True
         if whether_glue:
            last = many_content.pop()
            many_content.append(last + leaf.write())
         else:
            many_content.append(leaf.write())
         kind_last = leaf.KIND
      content = AID.unite(many_content)
      if not content:
         return AID.give_wide_space(self.KIND)
      result = AID.write_element(
            cut = '',
            content = content,
            tag = self.TAG,
            many_attribute = ["class"],
            many_value = [self.KIND],
      )
      return result

class Verse(Stem):

   KIND = "verse"
   TAG = "span"

   def __init__(self, **data):
      self.fill_basic(**data)
      self.many_sink = []

   def parse(self):
      head = self.move_right(0, 0)
      while (head < len(self.source)):
         leaf, head = self.snip_leaf(head)
         head = self.move_right(0, head)
         if (not leaf) or (not leaf.source.strip(" \t\n")):
            continue
         if (leaf.KIND == "link"):
            if not self.many_sink:
               from .caution import Disallowing_link as creator
               creator(**data).panic()
            address = leaf.write()
            self.many_sink[-1].address = address
         else:
            self.many_sink.append(leaf)

   def write(self):
      many_content = []
      self.explain()
      self.parse()
      for leaf in self.many_sink:
         many_content.append(leaf.write())
      content = AID.unite(many_content)
      if not content:
         return AID.give_wide_space(self.KIND)
      result = AID.write_element(
            cut = '',
            content = content,
            tag = self.TAG,
            many_attribute = ["class"],
            many_value = [self.KIND],
      )
      return result

class Cell(Stem):

   KIND = "cell"
   TAG = "td"

   def __init__(self, **data):
      self.fill_basic(**data)
      self.many_sink = []
      self.bound_wrap = 24

   def parse(self):
      head = self.move_right(0, 0)
      while (head < len(self.source)):
         leaf, head = self.snip_leaf(head)
         head = self.move_right(0, head)
         if (not leaf) or (not leaf.source.strip(" \t\n")):
            continue
         if (leaf.KIND == "link"):
            if not self.many_sink:
               from .caution import Disallowing_link as creator
               creator(**data).panic()
            address = leaf.write()
            self.many_sink[-1].address = address
         else:
            self.many_sink.append(leaf)
      for leaf in self.many_sink:
         leaf.bound_wrap = self.bound_wrap

   def write(self):
      many_content = []
      self.explain()
      self.parse()
      for leaf in self.many_sink:
         many_content.append(leaf.write())
      content = AID.unite(many_content)
      if not content:
         return AID.give_wide_space(self.KIND)
      result = AID.write_element(
            cut = '',
            content = content,
            tag = self.TAG,
            many_attribute = ["class"],
            many_value = [self.KIND],
      )
      return result
