#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from typing import Tuple


class Token:
    """Token of string <setting real names to optimize searching logic>

    Methods
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

        NotImplemented:
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

    def __init__(self, character_index, character):
        self.index = character_index
        self.name = character

    def __str__(self):
        return f"""
            {self.__class__.__name__}
            name={self.name}
            type={self.real_type}
            index={self.index}
            endidx={self.index + len(self.name)}
            is_symbol={self.is_symbol}
            is_multiple={self.is_multiple}
        """



class Character:

    __slots__ = ('token')


    def character_type(self, character: str) -> Tuple[str, bool]:
        """Setting name to some characters (converting character to *name)
        """

        utype = None

        others = {
            'digit': ('digit', False),
            'alpha': ('alpha', False),
            'space': ('space', True),
            '.':     ('dot',   True),
            ',':     ('comma', True),
            ';':     ('semi_colon', True),
            # '\'': 'single_quote',
            # '"': 'double_quote',
        }

        rec_types = others['digit'] \
            if character.isdigit() else others['alpha'] \
            if character.isalpha() else others['space'] \
            if character.isspace() else None

        if rec_types is not None:
            return rec_types

        has_name = others.get(character)

        if has_name is None:
            raise NotImplementedError(f"<{character}>: not found")

        return has_name


    def is_space(self, value):
        if value == 'space':
            return True


    def _token_types(self, tokens):
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


    def check_for_multiple_types(self):
        # tokens -> [..., -1]

        multiple_types, tokens_between_spaces = self._token_types(reversed(self.tokens))

        if not tokens_between_spaces:
            return None

        if multiple_types:

            for multi_token in tokens_between_spaces:
                multi_token.is_multiple = True


    def disassemble(self):
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
            del self.tokens[token_index]
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

        del self.tokens[token_index]



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
    # s._recreate_token_state(1)


    for token in s.tokens:
        print(token)
