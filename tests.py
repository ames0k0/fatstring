#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from string_to_token import State


def test_alphabet_token():
    target = 'j'

    s = State(target)
    s.disassemble()

    tokens = len(s.tokens)
    token_name = s.tokens[0].name

    assert tokens == 1, f"Excepted single token, but got: {tokens}"
    assert token_name == target, f"Target alphabet is not in token {token_name}"



def test_is_alphabet_digit():
    target = '5'

    s = State(target)
    s.disassemble()

    tokens = len(s.tokens)
    token_name = s.tokens[0].name

    assert tokens == 1, f"Excepted single token, but got: {tokens}"
    assert token_name == target, f"Target alphabet is not in token {token_name}"



def test_is_alphabet_symbol():
    target = '.'

    s = State(target)
    s.disassemble()

    tokens = len(s.tokens)
    token_name = s.tokens[0].name

    assert tokens == 1, f"Excepted single token, but got: {tokens}"
    assert token_name == target, f"Target alphabet is not in token {token_name}"



def test_set_alphabets_has_multiple_type():
    target = '5.'

    s = State(target)
    s.disassemble()

    tokens = len(s.tokens)
    first_token, second_token = s.tokens

    assert tokens == 2, f"Excepted two token, but got: {tokens}"
    assert first_token.is_multiple == True, f"Doesn't changet to multiple: {target}"
    assert second_token.is_multiple == True, f"Doesn't changet to multiple: {target}"



def test_remove_alphabets_multiple_type():
    target = '5.0'

    s = State(target)
    s.disassemble()
    s._recreate_token_state(1)

    first_token, removed_token, second_token = s.tokens

    assert first_token.is_multiple == False, f"Doesn't removed multiple sign: {target} : {first_token}"
    assert second_token.is_multiple == False, f"Doesn't removed multiple sign: {target} : {second_token}"


def test_only_one_alphabets_with_multiple_type():
    target = '5.0j'

    s = State(target)
    s.disassemble()
    s._recreate_token_state(1)

    first_token, removed_token, second_token, third_token = s.tokens

    assert first_token.is_multiple == False, \
        f"Removed multiple sign from wrong element: {target} :: {first_token}"

    assert second_token.is_multiple == True, \
        f"Removed multiple sign from wrong element: {target} :: {second_token}"

    assert third_token.is_multiple == True, \
        f"Doesn't removed multiple sign: {target} :: {third_token}"


def test_turning_token_to_zombie_type():
    target = '5.0j'

    s = State(target)
    s.disassemble()
    s._recreate_token_state(1)

    first_token, removed_token, second_token, third_token = s.tokens

    assert len(s.tokens) == 4, f"Just changed token type, not removed but: {removed_token}"
    assert removed_token.real_type == 'zombie', \
        f"Token doesn't turned into 'zombie' after removing: {removed_token}"
