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
      letters = ()
      tip = self.source[0]
      tail = self.source[1]
      label_tip = AID.get_label_math(tip)
      label_tail = AID.get_label_math(tail)
      alphabets_latin = (
         *(AID.give_alphabets_upper()),
         *(AID.give_alphabets_lower()),
      )
      alphabets_greek = ( # XXX
      )
      kanji_first = (
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
      kanji_second = (
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
         letters = alphabets_latin
         suffix_kind = "bold"
      elif (label_tip == "SERIF_BLACK"):
         letters = alphabets_latin
         suffix_kind = "serif-black"
      elif (label_tip == "SANS_BLACK"):
         letters = alphabets_latin
         suffix_kind = "sans-black"
      elif (label_tip == "GREEK"):
         letters = alphabets_greek
         suffix_kind = "italic"
      elif (label_tip == "GREEK_BOLD"):
         letters = alphabets_greek
         suffix_kind = "bold"
      elif (label_tip == "KANJI_FIRST"):
         letters = kanji_first
         suffix_kind = "serif-black"
      elif (label_tip == "KANJI_SECOND"):
         letters = kanji_second
         suffix_kind = "sans-black"

      assert (len(self.source) == 2)
      tip = self.source[0]
      tail = self.source[1]
      content = letters.get(tail)
      if not content:
         data = self.give_data()
         from .caution import Token_invalid_as_symbol as creator
         creator(**data).panic()
      if letters:
         table_letter = AID.get_table_sign(signs)
         letter = table_letter.get(tail)
      sink = write_element(
            cut = '',
            content = content,
            tag = self.TAG,
            attributes = ["class"],
            values = [self.KIND + '-' + suffix_kind],
      )
      return sink

      # # ... ...
      # # '零', '壹', '貳', '參', '肆', '伍', '陸', '柒', '捌', '玖',
      # # '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸', 
      # # '子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', 
      # # '乾', '兌', '離', '震', '巽', '坎', '艮', '坤', 
      # # '鼠', '牛', '虎', '兔', '龍', '蛇', '馬', '羊', '猴', '雞', '狗', '豬', 
      # # 
      # # '幫', '滂', '並', '明', '非', '敷', '奉', '微', 
      # # '端', '透', '定', '泥', '知', '澈', '澄', '娘', 
      # # '精', '清', '從', '心', '邪', '照', '穿', '床', '審', '禪', 
      # # '見', '溪', '群', '疑', '影', '曉', '匣', '喻', '來', '日', 
      # # '通', '江', '止', '遇', '蟹', '臻', '山', '效', 
      # # '果', '假', '宕', '梗', '曾', '流', '深', '咸', 

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
      signs = ()
      tip = self.source[0]
      tail = self.source[1]
      label_tip = AID.get_label_math(tip)
      label_tail = AID.get_label_math(tail)

      if (label_tip == "KANA_FIRST"):
         signs = ('い', 'ろ', 'は', 'に', 'ほ',
               'イ', 'ロ', 'ハ', 'ニ', 'ホ')
      elif (label_tip == "KANA_SECOND"):
         signs = ('へ', 'と', 'ち', 'り', 'ぬ',
               'ヘ', 'ト', 'チ', 'リ', 'ヌ')
      elif (label_tip == "KANA_THIRD"):
         signs = ('る', 'を', 'わ', 'か', 'よ',
               'ル', 'ヲ', 'ワ', 'カ', 'ヨ')
      elif (label_tip == "KANA_FOURTH"):
         signs = ('た', 'れ', 'そ', 'つ', 'ね',
               'タ', 'レ', 'ソ', 'ツ', 'ネ')
      elif (label_tip == "KANA_FIFTH"):
         signs = ('な', 'ら', 'む', 'う', 'の',
               'ナ', 'ラ', 'ム', 'ウ', 'ノ')
      elif (label_tip == "KANA_SIXTH"):
         signs = ('お', 'く', 'や', 'ま', 'け',
               'オ', 'ク', 'ヤ', 'マ', 'ケ')
      elif (label_tip == "KANA_SEVENTH"):
         signs = ('ふ', 'こ', 'え', 'て', 'あ',
               'フ', 'コ', 'エ', 'テ', 'ア')
      elif (label_tip == "KANA_EIGHTH"):
         signs = ('さ', 'き', 'ゆ', 'め', 'み',
               'サ', 'キ', 'ユ', 'メ', 'ミ')
      elif (label_tip == "KANA_NINTH"):
         signs = ('し', 'ひ', 'も', 'せ', 'す',
               'シ', 'ヒ', 'モ', 'セ', 'ス')
      suffix_kind = ''
      if (tail in {'0', '1', '2', '3', '4'}):
         suffix_kind = "serif-bold"
      elif (tail in {'5', '6', '7', '8', '9'}):
         suffix_kind = "sans-bold"

      assert (len(self.source) == 2)
      tip = self.source[0]
      tail = self.source[1]
      if signs:
         table_sign = AID.get_table_sign(signs)
         sign = table_sign.get(tail)
      if not content:
         data = self.give_data()
         from .caution import Token_invalid_as_symbol as creator
         creator(**data).panic()
      sink = write_element(
            cut = '',
            content = content,
            tag = self.TAG,
            attributes = ["class"],
            values = [self.KIND + '-' + suffix_kind],
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
            attributes = ["class"],
            values = [self.KIND + suffix_kind],
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
