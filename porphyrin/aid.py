import os
from pdb import set_trace

def convert(path_in, path_out):
   from .stem import Document
   source = input_file(path_in)
   document = Document(source = source)
   sink = document.write()
   output_file(path_out, sink)

def make_all(folder_in, folder_out):
   make("ALL", folder_in, folder_out)

def make_new(folder_in, folder_out):
   make("NEW", folder_in, folder_out)

def make(flag, folder_in, folder_out):
   suffix_in = ".ppr"
   suffix_out = ".html"
   things_in = os.scandir(folder_in)
   for thing in things_in:
      name_in = thing.name
      if thing.is_dir():
         make(flag, thing.path, folder_out)
      elif thing.is_file():
         if not thing.path.endswith(suffix_in):
            continue
         name_out = thing.name.replace(suffix_in, suffix_out)
         path_out = os.path.join(folder_out, name_out)
         if not (flag == "ALL"):
            if os.path.isfile(path_out):
               time_in = thing.stat().st_ctime
               time_out = os.path.getmtime(path_out)
               if time_in < time_out:
                  continue
         print(f"Trying to convert {thing.path} to {path_out}:")
         convert(thing.path, path_out) 

def input_file(path):
   if not os.path.exists(path):
      return None
   handle = open(path, mode = 'r')
   source = handle.read()
   handle.close()
   return source

def output_file(path, sink):
   source = input_file(path)
   if (source == sink):
      return
   handle = open(path, mode = 'w')
   handle.write(sink)
   handle.close()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def write_element(cut = '\n', **data):
   assert ("content" in data)
   assert ("tag" in data)
   sink = ''
   sinks_left = ['<' + data["tag"]]
   if ("attributes" in data):
      attributes = data["attributes"]
      values = data["values"]
      assert (len(values) == len(attributes))
      for index in range(len(attributes)):
         sinks_left.append(
            attributes[index] +
            "=\"" + values[index] + '\"'
         )
   sinks_left[-1] += '>'
   sink_left = unite(sinks_left)
   sink_middle = cut + data["content"] + cut
   sink_right = "</" + data["tag"] + '>'
   sink += sink_left
   if sink_middle.strip(" \t\n"):
      sink += sink_middle
   sink += sink_right
   sink = sink.strip(" \t\n")
   return sink

def unite(sources, cut = ' '):
   for index in range(len(sources)):
      sources[index] = (sources[index]).strip()
   sink = (cut.join(sources)).strip(" \t\n")
   return sink

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def get_mark_right(mark_left):
   assert (len(list(set(mark_left))) == 1)
   tip_left = mark_left[0]
   label_left = get_label(mark_left[0])
   if not be_start_asymmetry(label_left):
      mark_right = mark_left
      return mark_left

   mark_right = mark_left
   if (label_left == "DEFINITION_LEFT"):
      tip_right = get_tip("DEFINITION_RIGHT")
   elif (label_left == "COMMENT_LEFT"):
      tip_right = get_tip("COMMENT_RIGHT")
   mark_right = mark_left.replace(tip_left, tip_right)
   return mark_right


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def be_bough(kind):
   kinds = {
      "paragraphs",
      "lines",
      "rows",
   }
   return (kind in kinds)

def be_stem(kind):
   kinds = {
      "paragraph",
      "line",
      "row",
   }
   return (kind in kinds)

def be_frond(kind):
   kinds = {
      "phrase",
      "verse",
      "cell",
   }
   return (kind in kinds)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def give_labels():
   labels = {
      '=': "PARAGRAPHS",
      '/': "LINES",
      '\"': "ROWS",
      '|': "graph",
      '`': "IDENTIFIER",
      '~': "BREAK",
      '<': "COMMENT_LEFT",
      '>': "COMMENT_RIGHT",
      '{': "DEFINITION_LEFT",
      '}': "DEFINITION_RIGHT",
      #
      '@': "SERIF_ROMAN",
      '%': "SERIF_ITALIC",
      '#': "SERIF_BOLD",
      '$': "SANS_ROMAN",
      '&': "SANS_BOLD",
      '+': "MONO",
      '*': "PSEUDO",
      '^': "MATH",
      '\\': "LINK",
      '_': "SPACE",
      '\'': "NEWLINE",
   }
   return labels

def give_tips():
   labels = give_labels()
   tips = {label: tip for tip, label in labels.items()}
   return tips

def get_label(tip):
   labels = give_labels()
   label = labels.get(tip)
   return label

def get_tip(label):
   tips = give_tips()
   tip = tips.get(label)
   return tip

def be_start_bough(label):
   labels = {
      "PARAGRAPHS",
      "LINES",
      "ROWS",
      "graph",
      "BREAK",
      "COMMENT_LEFT",
   }
   return (label in labels)

def be_start_leaf(label):
   labels = {
      "SERIF_ROMAN",
      "SERIF_ITALIC",
      "SERIF_BOLD",
      "SANS_ROMAN",
      "SANS_BOLD",
      "MONO",
      "PSEUDO",
      "MATH",
      "LINK",
      "COMMENT_LEFT",
      "DEFINITION_LEFT",
      "IDENTIFIER",
   }
   return (label in labels)

def be_start_asymmetry(label):
   labels = {
      "DEFINITION_LEFT",
      "COMMENT_LEFT",
   }
   return (label in labels)

def be_start_macro(label):
   labels = {
      "IDENTIFIER",
      "DEFINITION_LEFT",
   }
   return (label in labels)

def be_hollow_leaf(label):
   labels = {
      "SPACE",
      "NEWLINE",
   }
   return (label in labels)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def tune_text(source):
   glyphs_space = {' ', '\t', '\n'}
   glyphs_mark = set()
   labels_mark = {
      "SERIF_ROMAN",
      "SERIF_ITALIC",
      "SERIF_BOLD",
      "SANS_ROMAN",
      "SANS_BOLD",
      "COMMENT_LEFT",
      "COMMENT_RIGHT",
      "DEFINITION_LEFT",
      "DEFINITION_RIGHT",
      "IDENTIFIER",
   }
   for label in labels_mark:
      glyphs_mark.add(get_tip(label))
   sink = source
   sink = remove_token(glyphs_mark, sink)
   sink = erase_token(glyphs_space, sink)
   sink = prune_space(sink)
   sink = tune_hypertext(sink)
   return sink

def tune_code(source):
   glyphs_space = set([' ', '\t', '\n'])
   sink = source
   sink = erase_token(glyphs_space, sink)
   sink = tune_hypertext(sink)
   return sink

def tune_comment(source):
   escapes = {
      '----': '-',
      '---': '-',
      '--': '-',
   }
   sink = source
   sink = replace_token(escapes, sink)
   return sink

def tune_hypertext(source):
   escapes = {
      '<': "&lt;",
      '>': "&gt;",
      '&': "&amp;",
      '\"': "&quot;",
      '\'': "&#39;",
   }
   sink = source
   index = 0
   while True:
      if (index >= len(sink)):
         break
      step = 1
      for glyph, escape in escapes.items():
         if (index >= len(sink)):
            break
         if (sink[index] == glyph):
            sink = sink[:index] + escape + sink[index + 1:]
            step = len(escape)
            break
      index += step
   return sink

def tune_address(source):
   escapes = {
      '!': "%21",
      '\"': "%22",
      '#': "%23",
      '$': "%24",
      '%': "%25",
      '&': "%26",
      '\'': "%27",
      '(': "%28",
      ')': "%29",
      '*': "%2A",
      '+': "%2B",
      ',': "%2C",
      '-': "%2D",
      '.': "%2E",
      '/': "%2F",
   }
   sink = source
   index = 0
   while True:
      if (index >= len(sink)):
         break
      for glyph, escape in escapes.items():
         if (index >= len(sink)):
            break
         if (sink[index] == glyph):
            sink = sink[:index] + escape + sink[index + 1:]
            index += len(escape)
            continue
      index += 1
   return sink

def remove_token(tokens, source):
   sink = source
   for token in tokens:
      sink = sink.replace(token, '')
   return sink

def erase_token(tokens, source):
   sink = source
   for token in tokens:
      sink = sink.replace(token, ' ')
   ' '.join(sink.split())
   return sink

def replace_token(tokens_out, source):
   sink = source
   for token_in in tokens_out:
      sink = sink.replace(token_in, tokens_out[token_in])
   return sink

def give_wide_space():
   return "<span class=\"phrase\">&ensp;</span>"

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def prune_space(source):
   sink = source
   spot = 0
   while (True):
      if (spot >= len(sink) - 2):
         break
      if (
         be_ideograph(sink[spot])
         and (sink[spot + 1] == ' ') 
         and be_ideograph(sink[spot + 2])
      ):
         sink = sink[:spot + 1] + sink[spot + 2:]
         continue
      spot += 1
   spot = 0
   while (True):
      if (spot >= len(sink) - 1):
         break
      if (
         (be_ideograph(sink[spot]) and be_latin(sink[spot + 1]))
         or (be_latin(sink[spot]) and be_ideograph(sink[spot + 1]))
      ):
         sink = sink[:spot + 1] + ' ' + sink[spot + 1:]
         spot += 2
         continue
      spot += 1
   return sink

def be_ideograph(glyph):
   if (u'\u4e00' <= glyph <= u'\u9fff'):
      return True # CJK Unified Ideographs
   if (u'\u3400' <= glyph <= u'\u4dbf'):
      return True # CJK Unified Ideographs Extension A
   if (u'\u00020000' <= glyph <= u'\u0002a6df'):
      return True # CJK Unified Ideographs Extension B
   if (u'\u0002a700' <= glyph <= u'\u0002b73f'):
      return True # CJK Unified Ideographs Extension C
   if (u'\u0002b740' <= glyph <= u'\u0002b81f'):
      return True # CJK Unified Ideographs Extension D
   if (glyph in "。，、；：「」『』（）？！─…‥《》〈〉．"):
      return True # Fullwidth forms
   return False

def be_latin(glyph):
   if (glyph in {' ', '\t', '\n'}):
      return False
   if (u'\u0000' <= glyph <= u'\u007F'):
      return True # Basic Latin
   if (u'\u0080' <= glyph <= u'\u00FF'):
      return True # Latin-1 Supplement
   if (u'\u0100' <= glyph <= u'\u017F'):
      return True # Latin Extended-A
   if (u'\u0180' <= glyph <= u'\u024F'):
      return True # Latin Extended-B
   if (u'\u0250' <= glyph <= u'\u02AF'):
      return True # IPA Extensions
   return False

def normalize_percentage(weights):
   percentages = []
   grosses = weights
   partition = 100
   lowest = 5
   while (True):
      if not grosses:
         break
      gross = min(grosses)
      percentage = round(partition * gross / sum(grosses))
      grosses.pop(grosses.index(gross))
      percentage = max(lowest, percentage)
      partition -= percentage
      percentages.append(percentage)
   return percentages

def extract_caption(address):
   caption = address.split('/')[-1]
   for index in range(len(caption)):
      glyph = caption[index]
      if not glyph.isalnum():
         caption = caption.replace(glyph, ' ')
   caption = ' '.join(caption.split())
   return caption

def be_literary(kind):
   kinds = {
      "serif-roman",
      "serif-italic",
      "serif-bold",
      "sans-roman",
      "sans-bold",
   }
   return (kind in kinds)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def get_tip_right_math(tip_left):
   assert (len(tip_left) == 1)
   tip_right = ''
   label_left = get_label_math(tip_left)
   if not be_start_asymmetry_math(label_left):
      tip_right = tip_left
      return tip_right
   if (label_left == "START_PAIR"):
      tip_right = get_tip_math("STOP_PAIR")
   elif (label_left == "START_TRIPLET"):
      tip_right = get_tip_math("STOP_TRIPLET")
   elif (label_left == "START_TUPLE"):
      tip_right = get_tip_math("STOP_TUPLE")
   elif (label_left == "ARROW_LEFT"):
      tip_right = get_tip_math("ARROW_RIGHT")
   elif (label_left == "ORDER_LEFT"):
      tip_right = get_tip_math("ORDER_RIGHT")
   return tip_right

def get_tip_middle_math(tip_left):
   assert (len(tip_left) == 1)
   tip_middle = ''
   label_left = get_label_math(tip_left)
   if (label_left == "START_PAIR"):
      tip_middle = get_tip_math("CUT_PAIR")
   if (label_left == "START_TRIPLET"):
      tip_middle = get_tip_math("CUT_TRIPLET")
   if (label_left == "START_TUPLE"):
      tip_middle = get_tip_math("CUT_TUPLE")
   return tip_middle

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def write_latex(command, *items):
   sink = ''
   sinks = []
   sinks.append(command)
   for item in items:
      sinks.append('{' + item + '}')
   sink = unite(sinks)
   return sink

def give_alphabets_upper():
   alphabets = (
      'A', 'B', 'C',
      'D', 'E', 
      'F', 'G', 'H', 
      'I', 'J', 'K', 
      'L', 'M', 'N', 
      'O', 'P', 'Q', 
      'R', 'S', 'T',
      'U', 'V', 'W',
      'X', 'Y', 'Z',
   )
   return alphabets

def give_alphabets_lower():
   alphabets_upper = give_alphabets_upper()
   alphabets_lower = []
   for alphabet in alphabets_upper:
      alphabets_lower.append(alphabet.lower())
   alphabets_lower = tuple(alphabets_lower)
   return alphabets_lower

def give_digits():
   digits = (
      '0', '1', '2', '3', '4',
      '5', '6', '7', '8', '9',
   )
   return digits

def get_table_sign(targets):
   digits = give_digits()
   table = dict(zip(digits, targets))
   return table

def get_table_upper(targets):
   table = dict(zip(give_alphabets_upper(), targets))
   return table

def get_table_lower(targets):
   table = dict(zip(give_alphabets_lower(), targets))
   return table

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def give_labels_math():
   labels = {
      '.': "PLAIN",
      '#': "BOLD",
      '&': "BLACK",
      '@': "CURSIVE",
      '$': "GREEK",
      '!': "ACCENT_ONE",
      '?': "ACCENT_TWO",
      #
      '/': "LINE",
      '+': "OPERATION_ONE",
      '-': "OPERATION_TWO",
      '*': "OPERATION_THREE",
      '=': "EQUIVALENCE_ONE",
      '~': "EQUIVALENCE_TWO",
      '\\': "ARROW_LEFT",
      '|': "ARROW_RIGHT",
      '^': "ARROW_MIDDLE",
      '<': "ORDER_LEFT",
      '>': "ORDER_RIGHT",
      '%': "ABSTRACTION",
      #
      '(': "START_PAIR",
      ',': "CUT_PAIR",
      ')': "STOP_PAIR",
      '[': "START_TRIPLET",
      ':': "CUT_TRIPLET",
      ']': "STOP_TRIPLET",
      '{': "START_TUPLE",
      ';': "CUT_TUPLE",
      '}': "STOP_TUPLE",
      '\'': "SERIF" ,
      '\"': "SANS",
      '`': "MONO",
      '_': "CHECK",
   }
   return labels

def give_tips_math():
   labels = give_labels_math()
   tips = {label: tip for tip, label in labels.items()}
   return tips

def get_label_math(tip):
   labels = give_labels_math()
   label = labels.get(tip)
   return label

def get_tip_math(label):
   tips = give_tips_math()
   tip = tips.get(label)
   return tip

def be_start_letter_math(label):
   labels = {
      "BOLD",
      "BLACK",
      "CURSIVE",
      "GREEK",
   }
   return (label in labels)

def be_start_sign_math(label):
   labels = {
      "LINE",
      "OPERATION_ONE",
      "OPERATION_TWO",
      "OPERATION_THREE",
      "EQUIVALENCE_ONE",
      "EQUIVALENCE_TWO",
      "ARROW_LEFT",
      "ARROW_RIGHT",
      "ARROW_MIDDLE",
      "ORDER_LEFT",
      "ORDER_RIGHT",
      "ABSTRACTION",
   }
   return (label in labels)

def be_start_accent_math(label):
   labels = {
      "ACCENT_ONE",
      "ACCENT_TWO",
   }
   return (label in labels)

def be_start_asymmetry_math(label):
   labels = {
      "START_PAIR",
      "START_TRIPLET",
      "START_TUPLE",
      "ARROW_LEFT",
      "ORDER_LEFT",
   }
   return (label in labels)

def be_stop_asymmetry_math(label):
   labels = {
      "STOP_PAIR",
      "STOP_TRIPLET",
      "STOP_TUPLE",
      "ARROW_LEFT",
      "ORDER_LEFT",
   }
   return (label in labels)

def be_start_box_math(label):
   labels = {
      "START_PAIR",
      "START_TRIPLET",
      "START_TUPLE",
      "SERIF",
      "SANS",
      "MONO",
      "CHECK",
   }
   return (label in labels)

def be_cut_math(label):
   labels = {
      "CUT_PAIR",
      "CUT_TRIPLET",
      "CUT_TUPLE",
   }
   return (label in labels)

def be_not_lateral_math(label):
   labels = {
      "BOLD",
      "BLACK",
      "CURSIVE",
      "GREEK",
      "EQUIVALENCE_ONE",
      "EQUIVALENCE_TWO",
   }
   return (label in labels)

def be_start_symbol_math(label):
   being = (
      be_start_letter_math(label)
      or be_start_sign_math(label)
   )
   return being

def be_start_math(label):
   miscellaneous = {
      "PLAIN",
      "CUT_PAIR",
      "CUT_TRIPLET",
      "CUT_TUPLE",
   }
   being = (
      be_start_symbol_math(label)
      or be_start_box_math(label)
      or (label in miscellaneous)
   )
   return being

def kind_be_cut_math(kind):
   kinds = {
      "math-cut-pair",
      "math-cut-triplet",
      "math-cut-tuple",
   }
   return (kind in kinds)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def get_tip_right_pseudo(tip_left):
   assert (len(tip_left) == 1)
   label_left = get_label_pseudo(tip_left)
   tip_right = ''
   if not be_start_asymmetry_pseudo(label_left):
      tip_right = tip_left
      return tip_right
   if (label_left == "START_ROUND"):
      tip_right = get_tip_pseudo("STOP_ROUND")
   elif (label_left == "START_SQUARE"):
      tip_right = get_tip_pseudo("STOP_SQUARE")
   elif (label_left == "START_CURLY"):
      tip_right = get_tip_pseudo("STOP_CURLY")
   elif (label_left == "START_ANGLE"):
      tip_right = get_tip_pseudo("STOP_ANGLE")
   elif (label_left == "QUOTE_SINGLE"):
      tip_right = tip_left
   elif (label_left == "QUOTE_DOUBLE"):
      tip_right = tip_left
   return tip_right

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def give_labels_pseudo():
   labels = {
      "PLAIN": '.',
      "BOLD": ',',
      "SERIF_BLACK": ';',
      "SANS_BLACK": ':',
      "GREEK": '-',
      "GREEK_BOLD": '=',
      "KANJI_FIRST": '!',
      "KANJI_SECOND": '?',
      #
      "KANA_FIRST": '~',
      "KANA_SECOND": '@',
      "KANA_THIRD": '#',
      "KANA_FOURTH": '$',
      "KANA_FIFTH": '%',
      "KANA_SIXTH": '^',
      "KANA_SEVENTH": '&',
      "KANA_EIGHTH": '*',
      "KANA_NINTH": '+',
      #
      "START_ROUND": '(',
      "STOP_ROUND": ')',
      "CUT_ROUND": '/',
      "START_SQUARE": '[',
      "CUT_SQUARE": '\\',
      "STOP_SQUARE": ']',
      "START_CURLY": '{',
      "CUT_CURLY": '|',
      "STOP_CURLY": '}',
      "START_REMARK": '<',
      "STOP_REMARK": '>',
      #
      "SERIF": '\"',
      "SANS": '\'',
      "MONO": '`',
      "CHECK": '_',
   }
   return labels

def give_tips_pseudo():
   labels = give_labels_pseudo()
   tips = {label: tip for tip, label in labels.items()}
   return tips

def get_label_pseudo(tip):
   labels = give_labels_pseudo()
   label = labels.get(tip)
   return label

def get_tip_pseudo(label):
   tips = give_tips_pseudo()
   tip = tips.get(label)
   return tip

def be_start_letter_pseudo(label):
   labels = {
      "BOLD",
      "SERIF_BLACK",
      "SANS_BLACK",
      "GREEK",
      "GREEK_BOLD",
      "KANJI_FIRST",
      "KANJI_SECOND",
   }
   return (label in labels)

def be_start_sign_pseudo(label):
   labels = {
      "KANA_FIRST",
      "KANA_SECOND",
      "KANA_THIRD",
      "KANA_FOURTH",
      "KANA_FIFTH",
      "KANA_SIXTH",
      "KANA_SEVENTH",
      "KANA_EIGHTH",
      "KANA_NINTH",
   }
   return (label in labels)

def be_start_bracket_pseudo(label):
   labels = {
      "START_ROUND",
      "START_SQUARE",
      "START_CURLY",
      "START_REMARK",
      "SERIF",
      "SANS",
      "MONO",
      "CHECK",
   }
   return (label in labels)

def be_start_symbol_pseudo(label):
   being = (
      be_start_letter_pseudo(label)
      or be_start_sign_pseudo(label)
   )
   return being

def be_start_pseudo(label):
   being = (
      be_start_symbol_pseudo(label)
      or be_start_box_pseudo(label)
      or (label == "PLAIN")
   )
   return being
