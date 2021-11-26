#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List

from src.string_to_token import State, Token


def print_t(s: State) -> None:
  for token in s.tokens:
    print(token.beautify())


def digits_without_multiple(target: str) -> None:
  s = State(target)
  s.disassemble()

  for token in s.tokens:
    if (token.real_type == 'digit') and (not token.is_multiple):
      # TODO: name -> content
      print(token.name)


def digits_with_multiple(target: str) -> None:
  s = State(target)
  s.disassemble()

  for token in s.tokens:
    if (token.real_type == 'digit') and (token.is_multiple):
      print(token.name)


def digits_and_multiple_content(target: str) -> None:
  s = State(target)
  s.disassemble()

  def with_content(stack: List[Token]) -> None:
    # 80/181/EEC -> content ?
    print(''.join([s.name for s in stack]))
  def only_digit_content(stack: List[Token]) -> None:
    # 80/181 -> content ?
    if (not stack[0].name.isdigit()):
      stack.pop(0)
    while True:
      if (stack[-1].name.isdigit()):
        break
      del stack[-1]
    with_content(stack)

  skip_tokens = 0
  for token in s.tokens:
    if (skip_tokens):
      skip_tokens -= 1
      continue
    if (token.real_type == 'digit'):
      if (token.is_multiple):
        stack = []
        state = token
        while True:
          stack.insert(0, state)
          state = state.prev_token
          if (not state.is_multiple):
            break
        state = token.next_token
        while True:
          if (not state.is_multiple):
            break
          stack.append(state)
          skip_tokens += 1
          state = state.next_token
        # XXX:
        # does the front token matter if not digit ?
        # what about the token in the back of the digit ?
        # with_content(stack)
        only_digit_content(stack)
      else:
        print(token.name)


if __name__ == '__main__':
  test = 'With the implementation of the EU Directive 80/181/EEC on 1 January 2010'
  digits_without_multiple(test)
  print('-'*50)
  digits_with_multiple(test)
  print('-'*50)
  digits_and_multiple_content(test)
