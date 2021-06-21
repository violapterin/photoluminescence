from pdb import set_trace

from .organ import Leaf
from . import aid as AID

# #  &  &a  &A  &b  &B
# #  *                  *0  *1
# #     .a  .A  .b  .B  .0  .1  ..  .&  .*
class Math_letter(Leaf):

   KIND = "math-letter"
   TAG = "span"
   OUTSIDE = False
   LATERAL = True

   def __init__(self, **data):
      self.fill_basic(**data)
      self.accent = ''

   def write(self):
      letter_accent = ''
      letter = ''
      tip = self.source[0]
      tail = self.source[1]
      label_tip = AID.get_label_math(tip)
      label_tail = AID.get_label_math(tail)

      if (len(self.source) >= 4):
         tip_one = self.source[2]
         tip_two = self.source[3]
         label_one = get_label_math(tip_one)
         label_two = get_label_math(tip_two)
         if (label_one == "ACCENT_ONE"):
            if (label_two == "ACCENT_ONE"):
               self.accent = "\\bar"
            elif (label_two == "ACCENT_TWO"):
               self.accent = "\\hat"
         elif (label_one == "ACCENT_TWO"):
            if (label_two == "ACCENT_ONE"):
               self.accent = "\\breve"
            elif (label_two == "ACCENT_TWO"):
               self.accent = "\\tilde"

      elif (label == "BOLD"):
         if (tail.islower() or tail.isupper()):
            letter = tail
      elif (label == "BLACK"):
         if (tail.islower()):
            letter = AID.write_latex("\\mathbb", tail)
         elif (tail.isupper()):
            letter = AID.write_latex("\\fraktur", tail)
      elif (label == "CURSIVE"):
         if (tail.islower()):
            letter = AID.write_latex("\\mathcal", tail)
         elif (tail.isupper()):
            letter = AID.write_latex("\\mathscr", tail)
      elif (label == "GREEK"):
         uppers = (
            "\\@", "\\infty", "\\Xi",
            "\\Delta", "\\&",
            "\\Phi", "\\Gamma", "\\hslash",
            "\\bot", "\\top", "\\S",
            "\\Lambda", "\\mho", "\\nabla",
            "\\%", "\\Pi", "\\Theta",
            "\\surd", "\\Sigma", "\\eth",
            "\\Upsilon", "\\$", "\\Omega",
            "\\#", "\\Psi", "\\partial",
         )
         lowers = (
            "\\alpha", "\\beta", "\\xi",
            "\\delta", "\\varepsilon",
            "\\varphi", "\\gamma", "\\eta",
            "\\iota", "\\imath","\\kappa",
            "\\lambda", "\\mu", "\\nu",
            "\\varnothing", "\\pi", "\\vartheta",
            "\\rho", "\\sigma", "\\tau",
            "\\upsilon", "\\digamma", "\\omega",
            "\\chi", "\\psi", "\\zeta",
         )
         table_upper = get_table_upper(uppers)
         table_lower = get_table_lower(lowers)
         if (tail.isupper()):
            letter = table_upper.get(tail)
         elif (tail.islower()):
            letter = table_lower.get(tail)

      if not letter:
         data = self.give_data(0, len(self.source))
         from .caution import Token_invalid_as_symbol as creator
         creator(**data).panic()
      if self.accent:
         letter_accent = AID.write_latex(self.accent, letter)
      else:
         letter_accent = letter
      sink = self.write_math_outside(letter_accent)
      return sink

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

class Math_sign(Leaf):

   KIND = "math-sign"
   TAG = "span"
   OUTSIDE = False
   LATERAL = True

   def __init__(self, **data):
      self.fill_basic(**data)

   def write(self):
      assert (len(self.source) == 2)
      content = ''
      sign = ''
      signs = ()
      tip = self.source[0]
      tail = self.source[1]
      label_tip = AID.get_label_math(tip)
      label_tail = AID.get_label_math(tail)

      if (label_tip == "ABSTRACTION"):
         signs = (
            "\\sum", "\\prod", "\\int", "\\oint",
            "\\bigoplus", "\\bigodot", "\\bigotimes",
            "\\bigcup", "\\bigcap", "\\bigsqcup",
         )
      elif (label_tip == "OPERATION_ONE"):
         signs = (
            "\\pm", "\\oplus", "\\cup",
            "\\sqcup", "\\vee", "\\curlyvee",
            "\\spadesuit", "\\heartsuit",
            "\\diamondsuit", "\\clubsuit", 
         )
      elif (label_tip == "OPERATION_TWO"):
         signs = (
            "\\mp", "\\ominus", "\\cap",
            "\\sqcap", "\\wedge", "\\curlywedge",
            "\\neg", "\\angle",
            "\\square", "\\blacksquare",
         )
      elif (label_tip == "OPERATION_THREE"):
         signs = (
            "\\times", "\\odot", "\\otimes",
            "\\bullet", "\\circ", "\\star",
            "\\ltimes", "\\rtimes", "\\div", "\\oslash", 
         )
      elif (label_tip == "LINE"):
         signs = (
            "\\mid", "\\nmid", "\\backslash",
            "\\parallel", "\\nparallel", "\\between",
            "\\dotsc", "\\dotsb", "\\vdots", "\\ddots",
         )
      elif (label_tip == "ARROW_LEFT"):
         self.LATERAL = False
         signs = (
            "\\Leftarrow", "\\Lleftarrow",
            "\\nwarrow", "\\swarrow",
            "\\leftarrowtail", "\\twoheadleftarrow", 
            "\\hookleftarrow", "\\curvearrowleft",
            "\\triangleleft", "\\blacktriangleleft", 
         )
      elif (label_tip == "ARROW_RIGHT"):
         self.LATERAL = False
         signs = (
            "\\Rightarrow", "\\Rrightarrow",
            "\\nearrow", "\\searrow",
            "\\rightarrowtail", "\\twoheadrightarrow", 
            "\\hookrightarrow", "\\curvearrowright",
            "\\triangleright", "\\blacktriangleright", 
         )
      elif (label_tip == "ARROW_MIDDLE"):
         self.LATERAL = False
         signs = (
            "\\downarrow", "\\Uparrow", "\\Downarrow",
            "\\updownarrow", "\\Updownarrow",
            "\\blacktriangle", "\\blacktriangledown",
            "\\dagger", "\\ddagger", "\\wr",
         )
      elif (label_tip == "EQUIVALENCE_ONE"):
         self.LATERAL = False
         signs = (
            "\\neq", "\\equiv", "\\not\\equiv", "\\doteq",
            "\\leftrightarrow", "\\not\\leftrightarrow",
            "\\Leftrightarrow", "\\not\\Leftrightarrow",
            "\\leftrightsquigarrow", "\\not\\leftrightsquigarrow",
         )
      elif (label_tip == "EQUIVALENCE_TWO"):
         self.LATERAL = False
         signs = (
            "\\approx", "\\simeq", "\\approxeq", "\\cong",
            "\\propto", "\\asymp", "\\gtreqless", "\\lesseqgtr"
            "\\leftrightarrows", "\\rightleftarrows",
         )
      elif (label_tip == "ORDER_LEFT"):
         self.LATERAL = False
         signs = (
            "\\leq", "<", "\\ll", "\\lesssim",
            "\\subseteq", "\\subsetneq", "\\in",
            "\\preceq", "\\precneqq", "\\dashv",
         )
      elif (label_tip == "ORDER_RIGHT"):
         self.LATERAL = False
         signs = (
            "\\geq", ">", "\\gtrsim", "\\gg",
            "\\supseteq", "\\supsetneq", "\\notin",
            "\\succeq", "\\succneqq", "\\vdash",
         )

      if signs:
         table_sign = AID.get_table_sign(signs)
      if tail.isdigit():
         sign = table_sign.get(tail)
      if not sign:
         data = self.give_data(0, len(self.source))
         from .caution import Token_invalid_as_symbol as creator
         creator(**data).panic()
      sink = self.write_math_outside(sign)
      return sink

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

class Math_plain(Leaf):

   KIND = "math-plain"
   TAG = "span"
   OUTSIDE = False
   LATERAL = True

   def __init__(self, **data):
      self.fill_basic(**data)

   def write(self):
      assert (len(self.source) == 2)
      content = ''
      symbol = ''
      tip = self.source[0]
      tail = self.source[1]
      label_tip = AID.get_label_math(tip)
      label_tail = AID.get_label_math(tail)

      if (tail.isalnum()):
         symbol = tail
      else:
         table_symbol = {
            "PLAIN": '.',
            "BOLD": "\\aleph",
            "BLACK": "\\forall",
            "CURSIVE": "\\leftthreetimes",
            "GREEK": "\\exists",
            #
            "ABSTRACTION": "\\wp",
            "LINE": '/',
            "OPERATION_ONE": '+',
            "OPERATION_TWO": '-',
            "OPERATION_THREE": "\\cdot",
            "EQUIVALENCE_ONE": '=',
            "EQUIVALENCE_TWO": "\\sim",
            "ARROW_MIDDLE": "\\uparrow",
            "ARROW_LEFT": "\\leftarrow",
            "ARROW_RIGHT": "\\rightarrow",
            #
            "SERIF": "\\prime",
            "SANS": "\\prime\\prime",
            "MONO": "\\prime\\prime\\prime",
            "CUT_PAIR": ',',
            "CUT_TRIPLET": ':',
            "CUT_TUPLE": ';',
            "CHECK": "\\quad",
            "ACCENT_ONE": '!',
            "ACCENT_TWO": '?',
         }
         symbol = table_symbol.get(label_tail)

      if not symbol:
         data = self.give_data(0, len(self.source))
         from .caution import Token_invalid_as_symbol as creator
         creator(**data).panic()
      sink = self.write_math_outside(symbol)
      if AID.be_not_lateral_math(label_tail):
         self.LATERAL = False
      return sink

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

class Math_bracket_round(Leaf):

   KIND = "math-bracket-round"
   OUTSIDE = False
   LATERAL = True

   def __init__(self, **data):
      self.fill_basic(**data)

   def write(self):
      mark_left = "\\left("
      mark_right = "\\right)"
      sink = self.write_math_bracket(mark_left, mark_right)
      return sink

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

class Math_bracket_square(Leaf):

   KIND = "math-bracket-square"
   OUTSIDE = False
   LATERAL = True

   def __init__(self, **data):
      self.fill_basic(**data)

   def write(self):
      mark_left = "\\left["
      mark_right = "\\right]"
      sink = self.write_math_bracket(mark_left, mark_right)
      return sink

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

class Math_bracket_curly(Leaf):

   KIND = "math-bracket-curly"
   OUTSIDE = False
   LATERAL = True

   def __init__(self, **data):
      self.fill_basic(**data)

   def write(self):
      mark_left = "\\left\\{"
      mark_right = "\\right\\}"
      sink = self.write_math_bracket(mark_left, mark_right)
      return sink

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

class Math_bracket_angle(Leaf):

   KIND = "math-bracket-angle"
   OUTSIDE = False
   LATERAL = True

   def __init__(self, **data):
      self.fill_basic(**data)

   def write(self):
      mark_left = "\\left\\langle"
      mark_right = "\\right\\rangle"
      sink = self.write_math_bracket(mark_left, mark_right)
      return sink

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

class Math_bracket_line(Leaf):

   KIND = "math-bracket-line"
   OUTSIDE = False
   LATERAL = True

   def __init__(self, **data):
      self.fill_basic(**data)

   def write(self):
      mark_left = "\\left|"
      mark_right = "\\right|"
      sink = self.write_math_bracket(mark_left, mark_right)
      return sink

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# # boxes: pair, triplet, tuple

class Math_pair(Leaf):

   KIND = "math-pair"
   TAG = "span"
   OUTSIDE = False
   LATERAL = True

   def __init__(self, **data):
      self.fill_basic(**data)

   def write(self):
      label_cut = "CUT_PAIR"
      head_left = self.move_right(0, 0)
      head_right = head_left
      boxes = [[]]
      while (head_right < len(self.source)):
         tissue, head_right = self.snip_tissue_math(head_left)
         if not tissue:
            continue
         head_left = head_right
         head_right = self.move_right(0, head_right)
         if tissue:
            label = AID.get_label_math(tissue.source[0])
            if (label == label_cut):
               boxes.append([])
            else:
               boxes[-1].append(tissue)
      if not (len(boxes) == 2):
         data = self.give_data(0, len(self.source))
         from .caution import Containing_wrong_number_boxes as creator
         creator(**data).panic()

      box_top, box_bottom = boxes
      top = AID.unite([tissue.write() for tissue in box_top])
      bottom = AID.unite([tissue.write() for tissue in box_bottom])
      command = "\\frac"
      content = AID.write_latex(command, top, bottom)
      sink = self.write_math_outside(content)
      return sink

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

class Math_triplet(Leaf):

   KIND = "math-triplet"
   OUTSIDE = False
   LATERAL = True
   
   def __init__(self, **data):
      self.fill_basic(**data)

   def write(self):
      label_cut = "CUT_TRIPLET"
      head_left = self.move_right(0, 0)
      head_right = head_left
      boxes = [[]]
      while (head_right < len(self.source)):
         tissue, head_right = self.snip_tissue_math(head_left)
         if not tissue:
            continue
         head_left = head_right
         head_right = self.move_right(0, head_right)
         label = AID.get_label_math(tissue.source[0])
         if (label == label_cut):
            boxes.append([])
         else:
            boxes[-1].append(tissue)
      if not (len(boxes) == 3):
         data = self.give_data(0, len(self.source))
         from .caution import Containing_wrong_number_boxes as creator
         creator(**data).panic()

      box_top, box_main, box_bottom = boxes
      be_lateral = ((len(box_main) == 1) and box_main[0].LATERAL)
      top = AID.unite([tissue.write() for tissue in box_top])
      main = AID.unite([tissue.write() for tissue in box_main])
      bottom = AID.unite([tissue.write() for tissue in box_bottom])
      content = ''
      if (be_lateral):
         contents = []
         contents.append(AID.write_latex('', main))
         contents.append(AID.write_latex('^', top))
         contents.append(AID.write_latex('_', bottom))
         content = AID.unite(contents)
      else:
         underset = AID.write_latex("\\underset", bottom, main)
         content = AID.write_latex("\\overset", top, underset)
      sink = self.write_math_outside(content)
      return sink

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

class Math_tuple(Leaf):

   KIND = "math-tuple"
   OUTSIDE = False
   LATERAL = True

   def __init__(self, **data):
      self.fill_basic(**data)

   def write(self):
      label_cut = "CUT_TUPLE"
      head_left = self.move_right(0, 0)
      head_right = head_left
      boxes = [[]]
      while (head_right < len(self.source)):
         tissue, head_right = self.snip_tissue_math(head_left)
         if not tissue:
            continue
         head_left = head_right
         head_right = self.move_right(0, head_right)
         label = AID.get_label_math(tissue.source[0])
         if tissue and (label == label_cut):
            boxes.append([])
         else:
            boxes[-1].append(tissue)

      contents = []
      contents.append(AID.write_latex("\\begin", "matrix"))
      for box in boxes:
         sink_tissue = AID.unite([tissue.write() for tissue in box])
         contents.append(sink_tissue + "\\\\")
      contents.append(AID.write_latex("\\end", "matrix"))
      content = AID.unite(contents, cut = '\n')
      sink = self.write_math_outside()
      return sink

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

class Math_cut(Leaf):

   KIND = "math-cut"

   def __init__(self, **data):
      self.fill_basic(**data)

   def write(self):
      pass

class Math_check(Leaf):

   KIND = "math-check"

   def __init__(self, **data):
      self.fill_basic(**data)

   def write(self):
      pass

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# # texts: serif, sans, mono

class Math_serif(Leaf):

   KIND = "math"
   LATERAL = True

   def __init__(self, **data):
      self.fill_basic(**data)

   def write(self):
      command = "\\mathrm"
      if not isalnum(self.source):
         data = self.give_data()
         from .caution import Allowing_only_alphabets as creator
         creator(**data).panic()
      sink = AID.write_latex(command, self.source)
      return sink

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

class Math_sans(Leaf):

   KIND = "math"
   LATERAL = True

   def __init__(self, **data):
      self.fill_basic(**data)

   def write(self):
      command = "\\mathsf"
      if not isalnum(self.source):
         data = self.give_data()
         from .caution import Allowing_only_alphabets as creator
         creator(**data).panic()
      sink = AID.write_latex(command, self.source)
      return sink

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

class Math_mono(Leaf):

   KIND = "math"
   LATERAL = True

   def __init__(self, **data):
      self.fill_basic(**data)

   def write(self):
      command = "\\mathtt"
      if not isalnum(self.source):
         data = self.give_data()
         from .caution import Allowing_only_alphabets as creator
         creator(**data).panic()
      sink = AID.write_latex(command, self.source)
      return sink
