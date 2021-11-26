#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO:
# - Better attribute names
# - Make types like namedtuples, so ('digit' -> t.digit)

from typing import Tuple, Any, NoReturn, Optional


class Token:
  """Token of string <setting real names to optimize searching logic>

  Attributes
  -------
    name : str
      full token
    index : int
      about where this token starts. Index from target string
    real_type:
      type that differ from anothers
      [alpha, digit, ..., others that may help me to make meaningfull logic writing]
    is_multiple : bool
      does this token was seperated with some delimiter Tokens
    next : Token
      next Token
    prev : Token
      prev Token
  """

  name: str = ''
  index: int = 0
  real_type: str = ''
  index_end: int = 0
  is_symbol: bool = False
  is_multiple: bool = False
  prev_token: Any = None
  next_token: Any = None

  def __init__(self, character_index, character):
    self.index = character_index
    self.name = character

  def beautify(self) -> str:
    return f"""
        {self.__class__.__name__}
        name={self.name}
        type={self.real_type}
        index={self.index}
        endidx={self.index + len(self.name)}
        is_symbol={self.is_symbol}
        is_multiple={self.is_multiple}
        prev_token={self.prev_token}
        next_tokne={self.next_token}
    """

class Character:
  __slots__ = ('token', 'char_types')

  def __init__(self):
    self.char_types = {
      'digit':  ('digit', False),
      'alpha':  ('alpha', False),
      'space':  ('space', True),
      '.':      ('dot',   True),
      ',':      ('comma', True),
      ';':      ('semi_colon', True),
      '/':      ('forward_slash', True),
      # '\'': 'single_quote',
      # '"': 'double_quote',
    }

  def register_new_type(self, character: str, real_type: str, is_symbol: bool):
    self.char_types[character] = (real_type, is_symbol)

  def character_type(self, character: str) -> Tuple[str, bool]:
    """Setting name to some characters (converting character to *name)
    """
    rec_types = self.char_types['digit'] \
      if character.isdigit() else self.char_types['alpha'] \
      if character.isalpha() else self.char_types['space'] \
      if character.isspace() else None

    if rec_types is not None:
      return rec_types

    has_name = self.char_types.get(character)

    if has_name is None:
      raise NotImplementedError(f"<{character}>: not found")

    return has_name

  def is_space(self, value: str) -> Optional[bool]:
    if value == 'space':
      return True

  def _token_types(self, tokens: Any) -> Tuple[bool, list]:
    token_type = None
    multiple_types = False
    tokens_between_spaces = []

    for token in tokens:
      if self.is_space(token.real_type):
        break

      tokens_between_spaces.append(token)

      if token_type is None:
        token_type = token.real_type
      elif token_type and token_type != token.real_type:
        multiple_types = True

    return multiple_types, tokens_between_spaces

  def check_for_multiple_types(self) -> None:
    # tokens -> [..., -1]

    multiple_types, tokens_between_spaces = self._token_types(reversed(self.tokens))

    if not tokens_between_spaces:
      return None

    if multiple_types:
      for multi_token in tokens_between_spaces:
        multi_token.is_multiple = True

  def linking_tokens(self) -> NoReturn:
    """Just saving next and prev token to current token
    """
    # [None, prev_next, None]
    for tidx, token in enumerate(self.tokens):
      if tidx:
        self.tokens[tidx-1].next_token = token
        self.tokens[tidx].prev_token = self.tokens[tidx-1]

  def token_to_zombie(self, token_index: int) -> NoReturn:
    """Token not just removing from tokens, but changing type to 'zombie'
    """
    token = self.tokens[token_index]
    token.name = ''
    token.real_type = 'zombie'
    token.is_symbol = False
    token.is_multiple = False

  def disassemble(self) -> NoReturn:
    """Generating data to minimize searching
    """
    current_char_type = None
    token_group = None

    for char_index, char in enumerate(self.target):
      token = Token(char_index, char)
      char_type, is_symbol = self.character_type(char)

      if current_char_type is None:
        token_group = token
        current_char_type = char_type
        token_group.is_symbol = is_symbol

      elif char_type == current_char_type:
        token_group.name += char
      else:
        token_group.real_type = current_char_type
        # token_group.index_end = char_index

        self.tokens.append(token_group)

        # check appended tokens
        # looking back til space | start of tokens

        if self.is_space(char_type):
          self.check_for_multiple_types()

        # new type
        token_group = token
        current_char_type = char_type
        token_group.is_symbol = is_symbol

    token_group.real_type = current_char_type
    self.tokens.append(token_group)
    self.check_for_multiple_types()
    self.linking_tokens()


class State(Character):
  """Using only holding product state <parsed (recognized) data from product>
  """

  def __init__(self, target: str):
    self.target = target
    self.tokens = []
    super().__init__()

  def _recreate_token_state(self, token_index):
    # 13x5  -> -x [13, 5]   ; 13  -> not multiple
    # 1.3x5 -> -x [1.3, 5]  ; 1.3 -> is multiple (no need to remove multi sign)

    if not self.tokens[token_index].is_multiple:
      self.token_to_zombie(token_index)
      return None

    # backward
    multiple_types, tokens_between_spaces = self._token_types(reversed(self.tokens[:token_index]))

    # only deleting token if it is multiple
    if not multiple_types:
      # even it's a space
      self.tokens[token_index-1].is_multiple = False

    # forward
    multiple_types, tokens_between_spaces = self._token_types(self.tokens[token_index+1:])

    if not multiple_types:
      self.tokens[token_index+1].is_multiple = False

    self.token_to_zombie(token_index)


class SIgt(State):
  """Test client side
  """

  def __init__(self, target):
    super().__init__(target)

  def s(self):
    print('>>>>', self.tokens)


if __name__ == '__main__':
  target = '5.0j'

  print('\t    TARGET: 5.0j')

  s = SIgt(target)
  s.disassemble()
  s._recreate_token_state(1)
  s._recreate_token_state(2)
  s.register_new_type(character='*', real_type='star', is_symbol=True)

  for token in s.tokens:
    print(token.beautify())
