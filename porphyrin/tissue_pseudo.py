from pdb import set_trace

from .organ import Leaf
from . import aid as AID

# #  &  &a  &A  &b  &B
# #  *                  *0  *1
# #     .a  .A  .b  .B  .0  .1  ..  &.  *.
class Pseudo_letter(Leaf):

   KIND = "pseudo-letter"
   TAG = "span"

   def __init__(self, **data):
      self.fill_basic(**data)

   def write(self):
      assert (len(self.source) == 2)
      content = ''
      letter = ''
      many_letter = ()
      tip = self.source[0]
      tail = self.source[1]
      label_tip = AID.get_label_math(tip)
      label_tail = AID.get_label_math(tail)
      many_alphabet_latin = (
         *(AID.give_many_alphabet_upper()),
         *(AID.give_many_alphabet_lower()),
      )
      many_alphabet_greek = (
         'Д', 'Б', 'Γ', 'Δ', 'Э', 'Ж',
         #A    B    G    D    E    Z
         'Ђ', 'Θ', 'Я', 'Ч', 'Λ', 'Ш',
         #H    Q    I    K    L    M
         'И', 'Ξ', 'Ю', 'Π', 'Л', 'Σ',
         #N    C    O    P    R    S
         'Ц', 'Ѫ', 'Φ', 'Щ', 'Ψ', 'Ω',
         #T    U    F    X    Y    W
         '£', '€',
         #V    J

         'α', 'β', 'γ', 'δ', 'ε', 'ζ',
         #A    B    G    D    E    Z
         'η', 'θ', 'ι', 'κ', 'λ', 'μ',
         #H    Q    I    K    L    M
         'ν', 'ξ', 'ø', 'π', 'ρ', 'σ',
         #N    C    O    P    R    S
         'τ', 'υ', 'φ', 'χ', 'ψ', 'ω',
         #T    U    F    X    Y    W
         '$', '¢',
         #V    J
      )
      many_kanji_first = (
         '零', '壹', '貳', '參', '肆',
         '伍', '陸', '柒', '捌', '玖',
         '甲', '乙', '丙', '丁', '戊',
         '己', '庚', '辛', '壬', '癸', 
         '子', '丑', '寅', '卯', '辰', '巳',
         '午', '未', '申', '酉', '戌', '亥', 
         '乾', '兌', '離', '震',
         '巽', '坎', '艮', '坤', 
         '鼠', '牛', '虎', '兔', '龍', '蛇',
         '馬', '羊', '猴', '雞', '狗', '豬', 
      )
      many_kanji_second = (
         '幫', '滂', '並', '明',
         '非', '敷', '奉', '微', 
         '端', '透', '定', '泥',
         '知', '澈', '澄', '娘', 
         '精', '清', '從', '心', '邪',
         '照', '穿', '床', '審', '禪', 
         '見', '溪', '群', '疑',
         '影', '曉', '匣', '喻', '來', '日', 
         '通', '江', '止', '遇',
         '蟹', '臻', '山', '效', 
         '果', '假', '宕', '梗',
         '曾', '流', '深', '咸', 
      )

      suffix_kind = "italic"
      if (label_tip == "BOLD"):
         many_letter = many_alphabet_latin
         suffix_kind = "bold"
      elif (label_tip == "SERIF_BLACK"):
         many_letter = many_alphabet_latin
         suffix_kind = "serif-black"
      elif (label_tip == "SANS_BLACK"):
         many_letter = many_alphabet_latin
         suffix_kind = "sans-black"
      elif (label_tip == "GREEK"):
         many_letter = many_alphabet_greek
         suffix_kind = "italic"
      elif (label_tip == "GREEK_BOLD"):
         many_letter = many_alphabet_greek
         suffix_kind = "bold"
      elif (label_tip == "KANJI_FIRST"):
         many_letter = many_kanji_first
         suffix_kind = "serif-black"
      elif (label_tip == "KANJI_SECOND"):
         many_letter = many_kanji_second
         suffix_kind = "sans-black"

      assert (len(self.source) == 2)
      tip = self.source[0]
      tail = self.source[1]
      content = many_letter.get(tail)
      if not content:
         data = self.give_data()
         from .caution import Token_invalid_as_symbol as creator
         creator(**data).panic()
      if many_letter:
         table_letter = AID.get_table_sign(many_sign)
         letter = table_letter.get(tail)
      sink = write_element(
            cut = '',
            content = content,
            tag = self.TAG,
            many_attribute = ["class"],
            many_value = [self.KIND + '-' + suffix_kind],
      )
      return sink

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

class Pseudo_sign(Leaf):

   KIND = "pseudo-sign"
   TAG = "span"

   def __init__(self, **data):
      self.fill_basic(**data)

   def write(self):
      assert (len(self.source) == 2)
      content = ''
      sign = ''
      many_sign = ()
      tip = self.source[0]
      tail = self.source[1]
      label_tip = AID.get_label_math(tip)
      label_tail = AID.get_label_math(tail)

      if (label_tip == "KANA_FIRST"):
         many_sign = ('い', 'ろ', 'は', 'に', 'ほ',
               'イ', 'ロ', 'ハ', 'ニ', 'ホ')
      elif (label_tip == "KANA_SECOND"):
         many_sign = ('へ', 'と', 'ち', 'り', 'ぬ',
               'ヘ', 'ト', 'チ', 'リ', 'ヌ')
      elif (label_tip == "KANA_THIRD"):
         many_sign = ('る', 'を', 'わ', 'か', 'よ',
               'ル', 'ヲ', 'ワ', 'カ', 'ヨ')
      elif (label_tip == "KANA_FOURTH"):
         many_sign = ('た', 'れ', 'そ', 'つ', 'ね',
               'タ', 'レ', 'ソ', 'ツ', 'ネ')
      elif (label_tip == "KANA_FIFTH"):
         many_sign = ('な', 'ら', 'む', 'う', 'の',
               'ナ', 'ラ', 'ム', 'ウ', 'ノ')
      elif (label_tip == "KANA_SIXTH"):
         many_sign = ('お', 'く', 'や', 'ま', 'け',
               'オ', 'ク', 'ヤ', 'マ', 'ケ')
      elif (label_tip == "KANA_SEVENTH"):
         many_sign = ('ふ', 'こ', 'え', 'て', 'あ',
               'フ', 'コ', 'エ', 'テ', 'ア')
      elif (label_tip == "KANA_EIGHTH"):
         many_sign = ('さ', 'き', 'ゆ', 'め', 'み',
               'サ', 'キ', 'ユ', 'メ', 'ミ')
      elif (label_tip == "KANA_NINTH"):
         many_sign = ('し', 'ひ', 'も', 'せ', 'す',
               'シ', 'ヒ', 'モ', 'セ', 'ス')
      suffix_kind = ''
      if (tail in {'0', '1', '2', '3', '4'}):
         suffix_kind = "serif-bold"
      elif (tail in {'5', '6', '7', '8', '9'}):
         suffix_kind = "sans-bold"

      assert (len(self.source) == 2)
      tip = self.source[0]
      tail = self.source[1]
      if many_sign:
         table_sign = AID.get_table_sign(many_sign)
         sign = table_sign.get(tail)
      if not content:
         data = self.give_data()
         from .caution import Token_invalid_as_symbol as creator
         creator(**data).panic()
      sink = write_element(
            cut = '',
            content = content,
            tag = self.TAG,
            many_attribute = ["class"],
            many_value = [self.KIND + '-' + suffix_kind],
      )
      return sink

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

class Pseudo_plain(Leaf):

   KIND = "pseudo-plain"
   TAG = "span"

   def __init__(self, **data):
      self.fill_basic(**data)

   def write(self):
      tip = self.source[0]
      tail = self.source[1]
      invalid = False
      if (len(self.source) == 2):
         invalid = True
      if (tip == AID.get_tip_pseudo("PLAIN")):
         invalid = True
      if not isascii(tail):
         invalid = True
      if invalid:
         data = self.give_data(0, len(self.source))
         from .caution import Token_invalid_as_symbol as creator
         creator(**data).panic()
      kind = "pseudo-mono"
      if (isalpha(tail)):
         kind = "pseudo-italic"
      sink = write_element(
            cut = '',
            content = sink,
            tag = self.TAG,
            many_attribute = ["class"],
            many_value = [self.KIND + suffix_kind],
      )
      return sink

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Pseudo_round(Leaf):

   KIND = "pseudo-round"

   def __init__(self, **data):
      self.fill_basic(**data)
      self.level = 0

   def write(self):
      sink += '('
      sink += write_element(
         cut = '',
         content = self.level,
         tag = "sub",
      )

      sink += ')'
      sink += write_element(
         cut = '',
         content = self.level,
         tag = "sub",
      )
      result += ' '
      return result

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Pseudo_square(Leaf):
   pass

class Pseudo_curly(Leaf):
   pass

class Pseudo_serif(Leaf):
   pass

class Pseudo_sans(Leaf):
   pass

class Pseudo_mono(Leaf):
   pass

class Pseudo_tiny(Leaf):
   pass

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

class Pseudo_void(Leaf):

   KIND = "pseudo-void"

   def __init__(self):
      pass

   def write(self):
      return ''
