from pdb import set_trace

from . import aid as AID

# # Stem: Document
# # Stem (bough): Paragraphs, Lines, Rows, Graph, Break,
# # Stem (twig): Paragraph, Line, Row, Newline
# # Stem (frond): Phrase, Verse, Cell, Space
# # Leaf: Math, Pseudo,
# # Leaf: Serif_roman, Serif_italic, Serif_bold,
# # Leaf: Sans_roman, Sans_bold, Mono,

class Organ(object):

   def __init__(self, **data):
      self.fill_basic(**data)
   
   def fill_basic(self, **data):
      self.source = data.pop("source", '')
      self.leftmost = data.pop("leftmost", '')
      self.rightmost = data.pop("rightmost", '')
      self.count_line = data.pop("count_line", 0)
      self.count_glyph = data.pop("count_glyph", 0)

   def give_data(self, head_left, head_right):
      data = {
         "source" : (self.source[head_left: head_right]).rstrip(" \t\n"),
         "leftmost" : self.get_leftmost_new(head_left),
         "rightmost" : self.get_rightmost_new(head_right),
         "count_line" : self.get_count_line_new(head_left),
         "count_glyph" : self.get_count_glyph_new(head_left),
      }
      return data

   def get_leftmost_new(self, head):
      left = self.source[: head]
      sink = left.split('\n')[-1]
      return sink

   def get_rightmost_new(self, head):
      right = self.source[head :]
      sink = right.split('\n')[0]
      return sink

   def get_count_glyph_new(self, head):
      count_glyph = self.count_glyph
      left = self.source[: head]
      fragments = left.split('\n')
      if (len(fragments) == 1):
         count_glyph += len(fragments[0])
         return count_glyph
      count_glyph = len(fragments[-1])
      return count_glyph

   def get_count_line_new(self, head):
      count = self.count_line
      left = self.source[: head]
      fragments = left.split('\n')
      count += len(fragments) - 1
      return count

   def explain(self):
      print(f"Writing {self.KIND} with source:", flush = True)
      fragments = self.source.split('\n')
      counts = []
      for count in range(len(fragments)):
         if (abs(count) < 3) or (abs(count - len(fragments)) < 3):
            counts.append(count)
      color_default = "\033[0m"
      color_yellow = "\033[93m"
      for count in counts:
         print(">>", color_yellow, fragments[count], color_default)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

   def move_left(self, step, head):
      probe = head
      whitespaces = {' ', '\t', '\n'}
      size = len(self.source)
      interval = range(size)
      probe = self.confine_head(probe)
      if (probe == 0):
         return 0

      while (probe in interval):
         if (self.source[probe] not in whitespaces):
            break
         else:
            probe -= 1
      if (probe == 0):
         return probe
      for _ in range(step):
         probe -= 1
         while (probe in interval):
            if (self.source[probe] not in whitespaces):
               break
            else:
               probe -= 1
      probe = self.confine_head(probe)
      return probe

   def move_right(self, step, head):
      probe = head
      whitespaces = {' ', '\t', '\n'}
      size = len(self.source)
      interval = range(size)
      probe = self.confine_head(probe)
      if (probe == size):
         return size

      while (probe in interval):
         if (self.source[probe] not in whitespaces):
            break
         else:
            probe += 1
      if (probe == size):
         return probe
      for _ in range(step):
         probe += 1
         while (probe in interval):
            if (self.source[probe] not in whitespaces):
               break
            else:
               probe += 1
      probe = self.confine_head(probe)
      return probe

   def confine_head(self, head):
      probe = head
      size = len(self.source)
      if (probe > size):
         probe = size
      if (probe < 0):
         probe = 0
      return probe

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

   def find_greedy(self, mark_left, mark_right, head_left):
      fragment = self.source[head_left:]
      fragment = fragment.split(mark_left, 1)[1]
      content = fragment.split(mark_right, 1)[0]
      head_right = head_left
      head_right += len(mark_left) + len(content) + len(mark_right)
      return head_right

   def find_balanced(self, mark_left, mark_right, head_left):
      probe_right = head_left
      count = 0
      interval = range(len(self.source) - len(mark_right) + 1)
      while (probe_right in interval):
         head_right = probe_right + len(mark_right)
         mark_probe = self.source[probe_right: head_right]
         if (mark_probe == mark_left):
            count += 1
         elif (mark_probe == mark_right):
            count -= 1
         if (count == 0):
            break
         probe_right += 1
      return head_right

   def probe_mark(self, head_left):
      mark = ''
      tip = self.source[head_left]
      head_right = head_left
      interval = range(len(self.source))
      while (head_right in interval):
         if not (self.source[head_right] == tip):
            break
         head_right += 1
      mark_left = self.source[head_left: head_right]
      return mark_left

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Stem(Organ):

   # # for empty organs:
   # `head_left`, `mark_left`, `head_right`
   # # for inhabited organs:
   # `head_left`, `mark_left`,
   # `probe_left`, `content`, `probe_right`,
   # `mark_right`, `head_right`
   def snip_bough(self, head_left):
      from . import stem as STEM
      bough = None
      probe_left = 0
      probe_right = 0
      head_right = self.move_right(0, head_left)
      if (head_right >= len(self.source)):
         return leaf, head_right
      mark_left = self.probe_mark(head_left).rstrip(" \n\t")
      mark_right = AID.get_mark_right(mark_left)
      label = AID.get_label(mark_left[0])

      if (label == "BREAK"):
         head_right = self.move_right(len(mark_left), head_left)
         data = self.give_data(head_left, head_left)
         from .stem import Break as creator
         bough = creator(**data)
         return bough, head_right

      head_right = self.find_greedy(mark_left, mark_right, head_left)
      probe_left = self.move_right(0, head_left + len(mark_left))
      probe_right = self.move_left(0, head_right - len(mark_right))
      content = self.source[probe_left: probe_right]

      data = self.give_data(head_left, probe_left)
      if not AID.be_start_bough(label):
         from .caution import Allowing_only_bough as creator
         creator(**data).panic()
      elif (probe_right > len(self.source)):
         from .caution import Not_matching_mark_bough as creator
         creator(**data).panic()
      elif (AID.be_start_macro(label) and self.expanded):
         from .caution import Macro_not_gathered as creator
         creator(**data).panic()

      if (label == "INSTRUCTION"):
         self.instructions.append(content)
         return None, head_right
      elif (label == "DEFINITION_LEFT"):
         self.definitions.append(content)
         return None, head_right
      elif not self.expanded:
         self.expand(head_left)
         self.expanded = True
         return None, 0

      data = self.give_data(probe_left, probe_right)
      if not data["source"]:
         return None, head_right
      if (label == "PARAGRAPHS"):
         bough = STEM.Paragraphs(**data)
      if (label == "LINES"):
         bough = STEM.Lines(**data)
      if (label == "ROWS"):
         bough = STEM.Rows(**data)
      if (label == "graph"):
         bough = STEM.Graph(**data)
      if (label == "BREAK"):
         bough = STEM.Break(**data)
      if (label == "COMMENT_LEFT"):
         bough = None
      return bough, head_right

   # # for empty organs:
   # `head_left`, `mark_left`, `head_right`
   # # for inhabited organs:
   # `head_left`, `mark_left`,
   # `probe_left`, `content`, `probe_right`,
   # `mark_right`, `head_right`
   def snip_leaf(self, head_left):
      from . import leaf as LEAF
      leaf = None
      probe_left = 0
      probe_right = 0
      mark_left = self.probe_mark(head_left).rstrip(" \n\t")
      mark_right = AID.get_mark_right(mark_left)
      label = AID.get_label(mark_left[0])

      if AID.be_hollow_leaf(label):
         head_right = self.move_right(len(mark_left), head_left)
         data = self.give_data(head_left, head_right)
         if (label == "SPACE"):
            leaf = LEAF.Space(**data)
            return leaf, head_right
         if (label == "NEWLINE"):
            leaf = LEAF.Newline(**data)
            return leaf, head_right

      head_right = self.find_greedy(mark_left, mark_right, head_left)
      probe_left = self.move_right(0, head_left + len(mark_left))
      probe_right = self.move_left(0, head_right - len(mark_right))
      content = self.source[probe_left: probe_right]

      data = self.give_data(head_left, probe_left)
      if (probe_right > len(self.source)):
         from .caution import Not_matching_mark_leaf as creator
         creator(**data).panic()
      if not AID.be_start_leaf(label):
         from .caution import Allowing_only_leaf as creator
         creator(**data).panic()

      data = self.give_data(probe_left, probe_right)
      if not data["source"]:
         return None, head_right
      if (label == "SERIF_ROMAN"):
         leaf = LEAF.Serif_roman(**data)
      if (label == "SERIF_ITALIC"):
         leaf = LEAF.Serif_italic(**data)
      if (label == "SERIF_BOLD"):
         leaf = LEAF.Serif_bold(**data)
      if (label == "SANS_ROMAN"):
         leaf = LEAF.Sans_roman(**data)
      if (label == "SANS_BOLD"):
         leaf = LEAF.Sans_bold(**data)
      if (label == "MONO"):
         leaf = LEAF.Mono(**data)
      if (label == "PSEUDO"):
         leaf = LEAF.Pseudo(**data)
      if (label == "MATH"):
         leaf = LEAF.Math(**data)
      if (label == "LINK"):
         leaf = LEAF.Link(**data)
      if (label == "COMMENT_LEFT"):
         leaf = None
      return leaf, head_right

   def shatter_stem(self, kind_stop, creator, head_left):
      branch = None
      head_middle = self.move_right(0, head_left)
      head_right = head_middle
      while (head_right < len(self.source)):
         leaf, probe = self.snip_leaf(head_right)
         head_middle = probe
         head_right = self.move_right(0, probe)
         if leaf and (leaf.KIND == kind_stop):
            break
      data = self.give_data(head_left, head_middle)
      if not data["source"]:
         return None, head_right
      branch = creator(**data)
      return branch, head_right

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Leaf(Organ):

   def write_text(self, content):
      sink = AID.write_element(
         cut = '',
         content = content,
         tag = self.give_tag_text(),
         attributes = self.give_attributes_text(),
         values = self.give_values_text(),
      )
      return sink

   def give_tag_text(self):
      assert (hasattr(self, "address"))
      assert (hasattr(self, "TAG_PLAIN"))
      tag = self.TAG_PLAIN
      if self.address:
         tag = 'a'
      return tag

   def give_attributes_text(self):
      assert (hasattr(self, "address"))
      attributes = ["class"]
      if self.address:
         attributes.append("href")
      return attributes

   def give_values_text(self):
      assert (hasattr(self, "address"))
      values = [self.KIND]
      if self.address:
         values.append(self.address)
      return values

   def write_math_bracket(self, mark_left, mark_right):
      contents = [mark_left]
      head = self.move_right(0, 0)
      while (head < len(self.source)):
         tissue, head = self.snip_tissue_math(head)
         if tissue:
            contents.append(tissue.write())
         head = self.move_right(0, head)
      contents.append(mark_right)
      content = AID.unite(contents)
      sink = self.write_math_outside(content)
      return sink

   def write_math_outside(self, source):
      assert (hasattr(self, "OUTSIDE"))
      sink = ''
      tag = "span"
      mark_left = "\\("
      mark_right = "\\)"
      if (self.OUTSIDE):
         content = mark_left + source + mark_right
         sink = AID.write_element(
            cut = '',
            content = content,
            tag = tag,
            attributes = ["class"],
            values = [self.KIND],
         )
      else:
         sink = source
      sink = sink.strip()
      return sink

   def write_pseudo_outside(self, source):
      tag = "span"
      sink = AID.write_element(
         cut = ' ',
         content = source,
         tag = tag,
         attributes = ["class"],
         values = [self.KIND],
      )
      return sink

   def capitalize(self):
      if not AID.be_literary(self.KIND):
         return
      for index in range(len(self.source)):
         glyph = self.source[index]
         if not glyph.isalpha():
            continue
         self.source = (
            self.source[:index]
            + glyph.upper()
            + self.source[index + 1:]
         )
         break

   # # # # # # # # # # # # # # # #

   # head_left, head_after, probe_middle, probe_right, head_right,
   def snip_tissue_math(self, head_left):
      from . import tissue_math as TISSUE
      tissue = TISSUE.Math_void()
      tip_left = self.source[head_left]
      label_left = AID.get_label_math(tip_left)
      head_after = self.move_right(1, head_left)
      if not AID.be_start_math(label_left):
         data = self.give_data(head_left, head_after)
         from .caution import Token_invalid_as_symbol as creator
         creator(**data).panic()

      if (AID.be_cut_math(label_left)):
         head_right = head_after
         data = self.give_data(head_left, head_right)
         if not data["source"]:
            tissue = TISSUE.Math_void()
            return tissue, head_right
         if (label_left == "CUT_PAIR"):
            tissue = TISSUE.Math_cut_pair(**data)
         elif (label_left == "CUT_TRIPLET"):
            tissue = TISSUE.Math_cut_triplet(**data)
         elif (label_left == "CUT_TUPLE"):
            tissue = TISSUE.Math_cut_tuple(**data)
         return tissue, head_right

      if (head_after >= len(self.source)):
         return tissue, len(self.source)

      tip_after = self.source[head_after]
      label_after = AID.get_label_math(tip_after)
      if AID.be_stop_asymmetry_math(label_left):
         data = self.give_data(head_left, head_after)
         from .caution import Bracket_mismatched as creator
         creator(**data).panic()

      if (AID.be_start_symbol_math(label_left)):
         head_right = self.move_right(1, head_after)
         if (head_right < len(self.source)):
            tip_middle = self.source[head_right]
            label_middle = AID.get_label_math(tip_middle)
            if (AID.be_start_accent_math(label_middle)):
               head_right = self.move_right(2, head_right)
         if (head_right - head_left < 2):
            data = self.give_data(head_left, head_right)
            from .caution import Token_invalid_as_symbol as creator
            creator(**data).panic()
         data = self.give_data(head_left, head_right)
         if not data["source"]:
            tissue = TISSUE.Math_void()
            return tissue, head_right
         if (AID.be_start_letter_math(label_left)):
            tissue = TISSUE.Math_letter(**data)
         elif (AID.be_start_sign_math(label_left)):
            tissue = TISSUE.Math_sign(**data)
         return tissue, head_right

      if (AID.be_start_box_math(label_left)):
         tip_right = AID.get_tip_right_math(tip_left)
         head_right = self.find_balanced(tip_left, tip_right, head_left)
         probe_right = head_right - 1
         data = self.give_data(head_after, probe_right)
         if not data["source"]:
            tissue = TISSUE.Math_void()
            return tissue, head_right
         if (label_left == "START_PAIR"):
            tissue = TISSUE.Math_pair(**data)
         if (label_left == "START_TRIPLET"):
            tissue = TISSUE.Math_triplet(**data)
         if (label_left == "START_TUPLE"):
            tissue = TISSUE.Math_tuple(**data)
         if (label_left == "SERIF"):
            tissue = TISSUE.Math_serif(**data)
         if (label_left == "SANS"):
            tissue = TISSUE.Math_sans(**data)
         if (label_left == "MONO"):
            tissue = TISSUE.Math_mono(**data)
         if (label_left == "CHECK"):
            tissue = TISSUE.Math_void()
         return tissue, head_right

      if (label_left == "PLAIN"):
         if not AID.be_start_asymmetry_math(label_after):
            head_right = self.move_right(1, head_after)
            data = self.give_data(head_left, head_right)
            if not data["source"]:
               tissue = TISSUE.Math_void()
               return tissue, head_right
            tissue = TISSUE.Math_plain(**data)
         else:
            tip_right = AID.get_tip_right_math(tip_after)
            head_right = self.find_balanced(tip_after, tip_right, head_after)
            probe_middle = self.move_right(1, head_after)
            probe_right = head_right - 2
            data = self.give_data(probe_middle, probe_right)
            if not data["source"]:
               tissue = TISSUE.Math_void()
               return tissue, head_right

            if (label_after == "START_PAIR"):
               tissue = TISSUE.Math_bracket_round(**data)
            if (label_after == "START_TRIPLET"):
               tissue = TISSUE.Math_bracket_square(**data)
            if (label_after == "START_TUPLE"):
               tissue = TISSUE.Math_bracket_curly(**data)
            if (label_after == "ORDER_LEFT"):
               tissue = TISSUE.Math_bracket_angle(**data)
            if (label_after == "ARROW_LEFT"):
               tissue = TISSUE.Math_bracket_line(**data)
      return tissue, head_right

   # # # # # # # # # # # # # # # #

   # head_left, probe_left, probe_right, head_right,
   def snip_tissue_pseudo(self, head_left):
      from . import tissue_pseudo as TISSUE
      tissue = TISSUE.Pseudo_void()
      tip_left = self.source[head_left]
      label_left = AID.get_label_pseudo(tip_left)
      head_right = self.move_right(1, head_left)
      if (head_after >= len(self.source)):
         tissue = TISSUE.Pseudo_void()
         return tissue, len(self.source)
      if not AID.be_start_pseudo(label_left):
         data = self.give_data(head_left, head_right)
         from .caution import Token_invalid_as_symbol as creator
         creator(**data).panic()
      if AID.be_stop_asymmetry_pseudo(label_left):
         data = self.give_data(head_left, head_after)
         from .caution import Bracket_mismatched as creator
         creator(**data).panic()

      if (AID.be_start_symbol_pseudo(label_left)):
         head_right = self.move_right(2, head_left)
         if (head_right - head_left < 2):
            data = self.give_data(head_left, head_right)
            from .caution import Token_invalid_as_symbol as creator
            creator(**data).panic()
         data = self.give_data(head_left, head_right)
         if not data["source"]:
            tissue = TISSUE.Pseudo_void()
            return tissue, head_right
         if (AID.be_letter_pseudo(label_left)):
            tissue = TISSUE.Pseudo_letter(**data)
         elif (AID.be_sign_pseudo(label_left)):
            tissue = TISSUE.Pseudo_sign(**data)
         return tissue, head_right

      elif (label_left == "PLAIN"):
         head_right = self.move_right(2, head_left)
         data = self.give_data(head_left, head_right)
         if not data["source"]:
            tissue = TISSUE.Pseudo_void()
            return tissue, head_right
         tissue = TISSUE.Pseudo_plain(**data)
         return tissue, head_right

      if (AID.be_start_bracket_pseudo(label_left)):
         tip_left = self.source[head_left]
         tip_right = AID.get_tip_right_pseudo(tip_left)
         head_right = self.find_balanced(tip_left, tip_right, head_left)
         probe_left = self.move_right(1, head_left)
         probe_right = self.move_left(1, head_right)
         data = give_data(probe_left, probe_right)
         if not data["source"]:
            tissue = TISSUE.Pseudo_void()
            return tissue, head_right
         if (label_left == "START_ROUND"):
            tissue = TISSUE.Pseudo_bracket_round(**data)
         if (label_left == "START_SQUARE"):
            tissue = TISSUE.Pseudo_bracket_square(**data)
         if (label_left == "START_CURLY"):
            tissue = TISSUE.Pseudo_bracket_curly(**data)
         if (label_left == "START_REMARK"):
            tissue = TISSUE.Pseudo_remark(**data)
         if (label_left == "SERIF"):
            tissue = TISSUE.Pseudo_serif(**data)
         if (label_left == "SANS"):
            tissue = TISSUE.Pseudo_sans(**data)
         if (label_left == "MONO"):
            tissue = TISSUE.Pseudo_mono(**data)
         if (label_left == "CHECK"):
            tissue = TISSUE.Pseudo_void()
      return tissue, head_right

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Caution(Organ):

   def __init__(self, **data):
      self.fill_basic(**data)
      message_left = ''
      message_right = ''

   def panic(self):
      self.warn()
      # Use the line below to show the stack:
      assert(1 == 0) # XXX
      raise SystemExit()

   def warn(self):
      color_default = "\033[0m"
      color_yellow = "\033[93m"
      color_red = "\033[91m"
      print(
         f"At line {self.count_line},",
         f"character {self.count_glyph}:"
      )
      print(
         ">> \t", color_yellow, self.leftmost,
         color_red, self.source,
         color_yellow, self.rightmost,
         color_default,
         sep = '',
      )
      print(
         color_yellow, self.message_left,
         color_red, self.source,
         color_yellow, self.message_right,
         color_default,
      )
