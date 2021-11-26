#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.string_to_token import State


class RecipeParser:
  def __init__(self, recipe: str):
    self.recipe = recipe
  def __call__(self):
    s = State(test)
    s.disassemble()

    recipe_count = None
    recipe_name = None
    recipe_delimiter = 'of'

    for token in s.tokens:
      if (token.name == recipe_delimiter):
        state = token.prev_token
        while True:
          if (state.is_symbol):
            state = state.prev_token
            continue
          recipe_count = state.name
          break
        state = token.next_token
        while True:
          if (state.is_symbol):
            state = state.next_token
            continue
          recipe_name = state.name
          break
    print(recipe_count, recipe_delimiter, recipe_name)


if __name__ == '__main__':
  test = 'Ton of shit'
  RecipeParser(test)()
