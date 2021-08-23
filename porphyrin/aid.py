import os

def make_all(folder_in, folder_out):
   whether_all = True
   make(whether_all, folder_in, folder_out)

def make_new(folder_in, folder_out):
   whether_all = False
   make(whether_all, folder_in, folder_out)

def make(whether_all, folder_in, folder_out):
   suffix_in = ".txt"
   suffix_out = ".html"
   many_thing_in = os.scandir(folder_in)
   for thing in many_thing_in:
      name_in = thing.name
      name_out = name_in.replace(suffix_in, suffix_out)
      path_in = thing.path
      path_out = os.path.join(folder_out, name_out)
      if thing.is_dir():
         make(whether_all, path_in, folder_out)
      elif thing.is_file():
         if not path_in.endswith(suffix_in):
            continue
         if not whether_all:
            if os.path.exists(path_out):
               time_in = thing.stat().st_mtime
               time_out = os.path.getmtime(path_out)
               if time_in < time_out:
                  continue
         print(f"Converting {path_in} to {path_out}:")
         if os.path.exists(path_out):
            os.remove(path_out)
         convert(path_in, path_out) 

def convert(path_in, path_out):
   from .stem import Document
   source = input_file(path_in)
   document = Document(source = source)
   sink = document.write()
   output_file(path_out, sink)

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
   many_sink_left = ['<' + data["tag"]]
   if ("many_attribute" in data):
      many_attribute = data["many_attribute"]
      many_value = data["many_value"]
      assert (len(many_value) == len(many_attribute))
      for index in range(len(many_attribute)):
         many_sink_left.append(
            many_attribute[index] +
            "=\"" + many_value[index] + '\"'
         )
   many_sink_left[-1] += '>'
   sink_left = unite(many_sink_left)
   sink_middle = cut + data["content"] + cut
   sink_right = "</" + data["tag"] + '>'
   sink += sink_left
   if sink_middle.strip(" \t\n"):
      sink += sink_middle
   sink += sink_right
   sink = sink.strip(" \t\n")
   return sink

def get_mark_right(mark_left):
   assert (len(tuple(set(mark_left))) == 1)
   tip_left = mark_left[0]
   label_left = get_label(tip_left)
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

def unite(many_source, cut = ' '):
   if not many_source:
      return ''
   for index in range(len(many_source)):
      many_source[index] = (many_source[index]).strip()
   sink = (cut.join(many_source)).strip(" \t\n")
   return sink

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def be_bough(kind):
   many_kind = {
      "section",
      "stanza",
      "array",
   }
   return (kind in many_kind)

def be_stem(kind):
   many_kind = {
      "paragraph",
      "line",
      "row",
   }
   return (kind in many_kind)

def be_frond(kind):
   many_kind = {
      "phrase",
      "verse",
      "cell",
   }
   return (kind in many_kind)

def be_literary(kind):
   many_kind = {
      "serif-roman",
      "serif-italic",
      "serif-bold",
      "sans-roman",
      "sans-bold",
   }
   return (kind in many_kind)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def give_many_label():
   many_label = {
      '=': "SECTION",
      '/': "STANZA",
      '\"': "ARRAY",
      '|': "GRAPH",
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
   return many_label

def give_many_tip():
   many_label = give_many_label()
   many_tip = {label: tip for tip, label in many_label.items()}
   return many_tip

def get_label(tip):
   many_label = give_many_label()
   label = many_label.get(tip)
   return label

def get_tip(label):
   many_tip = give_many_tip()
   tip = many_tip.get(label)
   return tip

def be_start_bough(label):
   many_label = {
      "SECTION",
      "STANZA",
      "ARRAY",
      "GRAPH",
      "BREAK",
      "COMMENT_LEFT",
   }
   return (label in many_label)

def be_start_leaf(label):
   many_label = {
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
   return (label in many_label)

def be_start_asymmetry(label):
   many_label = {
      "DEFINITION_LEFT",
      "COMMENT_LEFT",
   }
   return (label in many_label)

def be_start_macro(label):
   many_label = {
      "IDENTIFIER",
      "DEFINITION_LEFT",
   }
   return (label in many_label)

def be_hollow_leaf(label):
   many_label = {
      "SPACE",
      "NEWLINE",
   }
   return (label in many_label)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def tune_text(source):
   many_glyph_space = {' ', '\t', '\n'}
   many_glyph_mark = set()
   many_label_mark = {
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
   for label in many_label_mark:
      many_glyph_mark.add(get_tip(label))
   sink = source
   sink = remove_token(many_glyph_mark, sink)
   sink = erase_token(many_glyph_space, sink)
   sink = prune_space(sink)
   sink = tune_hypertext(sink)
   return sink

def tune_code(source):
   many_glyph_space = set([' ', '\t', '\n'])
   sink = source
   sink = erase_token(many_glyph_space, sink)
   sink = tune_hypertext(sink)
   return sink

def tune_comment(source):
   many_escape = {
      '------': '-',
      '-----': '-',
      '----': '-',
      '---': '-',
      '--': '-',
   }
   sink = source
   sink = replace_token(many_escape, sink)
   return sink

def tune_hypertext(source):
   many_escape = give_escape_hypertext()
   sink = source
   index = 0
   while True:
      if (index >= len(sink)):
         break
      step = 1
      for glyph, escape in many_escape.items():
         if (index >= len(sink)):
            break
         if (sink[index] == glyph):
            sink = sink[:index] + escape + sink[index + 1:]
            step = len(escape)
            break
      index += step
   return sink

def remove_token(many_token, source):
   sink = source
   for token in many_token:
      sink = sink.replace(token, '')
   return sink

def erase_token(many_token, source):
   sink = source
   for token in many_token:
      sink = sink.replace(token, ' ')
   ' '.join(sink.split())
   return sink

def replace_token(many_token_out, source):
   sink = source
   for token_in in many_token_out:
      sink = sink.replace(token_in, many_token_out[token_in])
   return sink

def give_escape_hypertext():
   many_escape = {
      '<': "&lt;",
      '>': "&gt;",
      '&': "&amp;",
      '\"': "&quot;",
      '\'': "&#39;",
   }
   return many_escape

def shall_agree_escape_hypertext(source, head_left):
   many_escape = give_escape_hypertext()
   for glyph, escape in many_escape.items():
      head_right = head_left + len(escape)
      piece = source[head_left: head_right]
      if (piece == escape):
         return True
   return False

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def chop_word_text(source, bound):
   many_cut = give_punctuation_halfwidth() + tuple("aeiou")
   sink = chop_word(many_cut, bound, source)
   return sink

def chop_word_code(source, bound):
   many_cut = give_punctuation_halfwidth()
   sink = chop_word(many_cut, bound, source)
   return sink

def chop_word(many_cut, bound, source):
   head_left = 0
   head_right = 0
   head = 0
   whether_run_last = False
   whether_run_next = False
   many_wound = []
   while (True):
      if (head < len(source)):
         glyph = source[head]
         whether_deal = False
         whether_run_next = be_halfwidth(glyph)
         if (not whether_run_last) and whether_run_next:
            head_left = head
         if whether_run_last and (not whether_run_next):
            whether_deal = True
         whether_run_last = whether_run_next
         head_right = head
      else:
         whether_deal = True
      if whether_deal and (head_right - head_left >= bound):
         piece = source[head_left: head_right]
         wound = head_left + find_wound(many_cut, piece)
         many_wound.append(wound)
      if (head >= len(source)):
         break
      head += 1
   sink = insert_chop("<wbr>", many_wound, source)
   return sink

def find_wound(many_cut, source):
   margin = 6
   half = int(len(source) / 2)
   for cut in many_cut:
      many_found = []
      for index, glyph in enumerate(source):
         if (glyph == cut):
            many_found.append(index)
      found = take_value_from_offset(half, many_found)
      if shall_agree_escape_hypertext(source, found):
         continue
      if (found < margin) or (len(source) - found - 1 < margin):
         continue
      return found
   return half

def take_value_from_offset(offset, queue):
   if not queue:
      return -1
   queue_offset = [index - offset for index in queue]
   queue_offset.sort(key = abs)
   queue_native = [index + offset for index in queue_offset]
   return queue_native[0]

def insert_chop(chop, many_wound, source):
   if not many_wound:
      return source
   sink = source
   many_wound.sort(reverse = True)
   for wound in many_wound:
      sink = sink[:wound + 1] + chop + sink[wound + 1:]
   return sink

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def prune_space(source):
   sink = source
   spot = 0
   while (True):
      if (spot >= len(sink) - 2):
         break
      if (
         be_ideograph(sink[spot])
         and be_space(sink[spot + 1])
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

   spot = 0
   many_line = {'-', '–', '—'}
   while (True):
      if (spot >= len(sink) - 2):
         break
      if (sink[spot] in many_line and be_space(sink[spot + 1])):
         sink = sink[:spot + 1] + sink[spot + 2:]
         spot += 1
         continue
      spot += 1
   return sink

def be_halfwidth(glyph):
   if be_latin(glyph):
      return True
   elif be_punctuation_halfwidth(glyph):
      return True
   return False

def be_fullwidth(glyph):
   if be_ideograph(glyph):
      return True
   elif be_punctuation_fullwidth(glyph):
      return True
   return False

def be_ideograph(glyph):
   if be_space(glyph):
      return False
   elif be_punctuation(glyph):
      return False
   elif (u'\u4e00' <= glyph <= u'\u9fff'):
      return True # CJK Unified Ideographs
   elif (u'\u3040' <= glyph <= u'\u309f'):
      return True # hiragana
   elif (u'\u30a0' <= glyph <= u'\u30ff'):
      return True # katakana
   elif (u'\u3400' <= glyph <= u'\u4dbf'):
      return True # CJK Unified Ideographs Extension A
   elif (u'\u00020000' <= glyph <= u'\u0002a6df'):
      return True # CJK Unified Ideographs Extension B
   elif (u'\u0002a700' <= glyph <= u'\u0002b73f'):
      return True # CJK Unified Ideographs Extension C
   elif (u'\u0002b740' <= glyph <= u'\u0002b81f'):
      return True # CJK Unified Ideographs Extension D
   return False

def be_latin(glyph):
   if be_space(glyph):
      return False
   elif be_punctuation(glyph):
      return False
   elif (u'\u0000' <= glyph <= u'\u007F'):
      return True # Basic Latin
   elif (u'\u0080' <= glyph <= u'\u00FF'):
      return True # Latin-1 Supplement
   elif (u'\u0100' <= glyph <= u'\u017F'):
      return True # Latin Extended-A
   elif (u'\u0180' <= glyph <= u'\u024F'):
      return True # Latin Extended-B
   elif (u'\u0250' <= glyph <= u'\u02AF'):
      return True # IPA Extensions
   return False

def be_punctuation(glyph):
   if be_space(glyph):
      return False
   elif be_punctuation_fullwidth(glyph):
      return True
   elif be_punctuation_halfwidth(glyph):
      return True
   return False

def be_punctuation_halfwidth(glyph):
   many_punctuation = give_punctuation_halfwidth()
   if glyph in many_punctuation:
      return True
   return False

def be_punctuation_fullwidth(glyph):
   many_punctuation = give_punctuation_fullwidth()
   if glyph in many_punctuation:
      return True
   return False

def be_space(glyph):
   many_space = tuple(" \t\n")
   if glyph in many_space:
      return True
   return False

def give_punctuation_halfwidth():
   # sorted in increasing priority
   many_punctuation = tuple(
      "()“”[]‘’—"
      + ".?!;:,"
      + "«»‹›\'\"`{}"
      + "-–_/|\\"
      + "=<>+*^~"
      + "@#$%&"
   )
   return many_punctuation

def give_punctuation_fullwidth():
   # sorted in increasing priority
   many_punctuation = tuple(
      "（）「」『』─…‥"
      + "。？！；：，、"
      + "《》〈〉．"
   )
   return many_punctuation

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def normalize_percentage(many_weight):
   many_percentage = [None] * len(many_weight)
   many_gross = many_weight.copy()
   hundred = 100
   lowest = 5
   while (True):
      if not many_gross:
         break
      gross = min(many_gross)
      percentage = round(hundred * gross / sum(many_gross))
      spot = many_gross.index(gross)
      many_gross.pop(spot)
      percentage = max(lowest, percentage)
      hundred -= percentage
      many_percentage[spot] = percentage
   return many_percentage

def extract_caption(address):
   base = address.split('/')[-1]
   hold = base.split('.')
   hold.pop()
   caption = ''.join(hold)
   for index in range(len(caption)):
      glyph = caption[index]
      if not glyph.isalnum():
         caption = caption.replace(glyph, ' ')
   caption = ' '.join(caption.split())
   return caption

def give_wide_space(kind):
   sink = f"<span class=\"{kind}\">&ensp;</span>"
   return sink

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

def get_accent(accent):
   command = ''
   tip_one = accent[0]
   tip_two = accent[1]
   label_accent_one = get_label_math(tip_one)
   label_accent_two = get_label_math(tip_two)
   if (label_accent_one == "ACCENT_ONE"):
      if (label_accent_two == "ACCENT_ONE"):
         command = "\\bar"
      elif (label_accent_two == "ACCENT_TWO"):
         command = "\\hat"
   elif (label_accent_one == "ACCENT_TWO"):
      if (label_accent_two == "ACCENT_ONE"):
         command = "\\breve"
      elif (label_accent_two == "ACCENT_TWO"):
         command = "\\tilde"
   return command

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def write_latex(command, *many_option):
   sink = ''
   many_sink = []
   many_sink.append(command)
   for option in many_option:
      if option:
         many_sink.append('{' + option + '}')
   sink = unite(many_sink, cut = '')
   return sink

def insert_space_narrow_latex(content):
   space = "\\,"
   sink = space + content + space
   return sink

def insert_space_wide_latex(content):
   space = "\\;"
   sink = space + content + space
   return sink

def winnow_space_latex(source):
   sink = source
   many_single = ("\\,", "\\:", "\\;")
   many_double = {
      "\\,\\,": "\\,",
      "\\:\\,": "\\:",
      "\\;\\,": "\\;",
      "\\,\\:": "\\:",
      "\\:\\:": "\\:",
      "\\;\\:": "\\;",
      "\\,\\;": "\\;",
      "\\:\\;": "\\;",
      "\\;\\;": "\\;",
   }
   for single in many_single:
      if sink.startswith(single):
         sink = sink[len(single):]
   for single in many_single:
      if sink.endswith(single):
         sink = sink[:-len(single)]
   for double, single in many_double.items():
      sink = sink.replace(double, single)
   return sink

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def get_table_sign(targets):
   digits = give_digits()
   table = dict(zip(digits, targets))
   return table

def get_table_upper(targets):
   table = dict(zip(give_many_alphabet_upper(), targets))
   return table

def get_table_lower(targets):
   table = dict(zip(give_many_alphabet_lower(), targets))
   return table

def give_many_alphabet_upper():
   many_alphabet = tuple(
      "ABCDEFGH"
      + "IJKLMNO"
      + "PQRST"
      + "UVWXYZ"
   )
   return many_alphabet

def give_many_alphabet_lower():
   many_alphabet_upper = give_many_alphabet_upper()
   many_alphabet_lower = []
   for alphabet in many_alphabet_upper:
      many_alphabet_lower.append(alphabet.lower())
   many_alphabet_lower = tuple(many_alphabet_lower)
   return many_alphabet_lower

def give_digits():
   digits = tuple("0123456789")
   return digits

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def give_many_label_math():
   many_label = {
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
   return many_label

def give_many_tip_math():
   many_label = give_many_label_math()
   many_tip = {label: tip for tip, label in many_label.items()}
   return many_tip

def get_label_math(tip):
   many_label = give_many_label_math()
   label = many_label.get(tip)
   return label

def get_tip_math(label):
   many_tip = give_many_tip_math()
   tip = many_tip.get(label)
   return tip

def be_start_math(label):
   many_other = {
      "PLAIN",
      "CUT_PAIR",
      "CUT_TRIPLET",
      "CUT_TUPLE",
   }
   being = (
      be_start_symbol_math(label)
      or be_start_box_math(label)
      or (label in many_other)
   )
   return being

def be_start_symbol_math(label):
   being = (
      be_start_letter_math(label)
      or be_start_sign_math(label)
   )
   return being

def be_start_letter_math(label):
   many_label = {
      "BOLD",
      "BLACK",
      "CURSIVE",
      "GREEK",
   }
   return (label in many_label)

def be_start_sign_math(label):
   many_label = {
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
   return (label in many_label)

def be_start_accent_math(label):
   many_label = {
      "ACCENT_ONE",
      "ACCENT_TWO",
   }
   return (label in many_label)

def be_start_asymmetry_math(label):
   many_label = {
      "START_PAIR",
      "START_TRIPLET",
      "START_TUPLE",
      "ARROW_LEFT",
      "ORDER_LEFT",
   }
   return (label in many_label)

def be_stop_asymmetry_math(label):
   many_label = {
      "STOP_PAIR",
      "STOP_TRIPLET",
      "STOP_TUPLE",
      "ARROW_RIGHT",
      "ORDER_RIGHT",
   }
   return (label in many_label)

def be_start_box_math(label):
   many_label = {
      "START_PAIR",
      "START_TRIPLET",
      "START_TUPLE",
      "SERIF",
      "SANS",
      "MONO",
      "CHECK",
   }
   return (label in many_label)

def be_cut_math(label):
   many_label = {
      "CUT_PAIR",
      "CUT_TRIPLET",
      "CUT_TUPLE",
   }
   return (label in many_label)

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

def give_many_label_pseudo():
   many_label = {
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
   return many_label

def give_many_tip_pseudo():
   many_label = give_many_label_pseudo()
   many_tip = {label: tip for tip, label in many_label.items()}
   return many_tip

def get_label_pseudo(tip):
   many_label = give_many_label_pseudo()
   label = many_label.get(tip)
   return label

def get_tip_pseudo(label):
   many_tip = give_many_tip_pseudo()
   tip = many_tip.get(label)
   return tip

def be_start_pseudo(label):
   being = (
      be_start_symbol_pseudo(label)
      or be_start_bracket_pseudo(label)
      or (label == "PLAIN")
   )
   return being

def be_start_symbol_pseudo(label):
   being = (
      be_start_letter_pseudo(label)
      or be_start_sign_pseudo(label)
   )
   return being

def be_start_letter_pseudo(label):
   many_label = {
      "BOLD",
      "SERIF_BLACK",
      "SANS_BLACK",
      "GREEK",
      "GREEK_BOLD",
      "KANJI_FIRST",
      "KANJI_SECOND",
   }
   return (label in many_label)

def be_start_sign_pseudo(label):
   many_label = {
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
   return (label in many_label)

def be_start_bracket_pseudo(label):
   many_label = {
      "START_ROUND",
      "START_SQUARE",
      "START_CURLY",
      "START_REMARK",
      "SERIF",
      "SANS",
      "MONO",
      "CHECK",
   }
   return (label in many_label)
