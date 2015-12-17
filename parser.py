#!/usr/bin/env python
# -*- coding: utf-8 -*-

import lexer

class ParseException(Exception):
    pass

def parse(tokens):
    """ Builds a parse tree from given tokens """
    if len(tokens) == 0:
        raise ParseException("Unexpected EOF")
    cursor = tokens.pop(0)
    # Got an opening bracket, parse the function call recursively
    if cursor == lexer.OpenBracket:
        internal = []
        while tokens[0] is not lexer.CloseBracket:
            internal.append(parse(tokens))
        del tokens[0] # eat a closing bracket
        return internal
    elif cursor == lexer.CloseBracket:
        raise ParseException("Unexpected close bracket found")
    elif cursor == lexer.SingleQuote:
        return ["quote", parse(tokens)]
    else:
        return parse_atom(cursor)

def parse_atom(token):
    """ Numbers become numbers, everything else becomes a symbol """
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return lexer.Symbol(token)
