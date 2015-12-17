#!/usr/bin/env python
# -*- coding: utf-8 -*-

Symbol = str
List   = list
Number = (int, float)
OpenBracket  = '('
CloseBracket = ')'
SingleQuote  = '\''

SPECIALS = [OpenBracket, CloseBracket, SingleQuote]

def tokenize(source_string):
    """ Converts a string input a list of whitespace-separated Lisp tokens """
    prepared = source_string
    # Since these are separate tokens we need to devide them
    # from other symbols. Thus we add extra whitespaces before
    # and after each symbol
    for symbol in SPECIALS:
        prepared = prepared.replace(symbol, " " + symbol + " ")
    # Remove comments (everything starting with ';')
    prepared = strip_comments(prepared)
    return prepared.split()


def strip_comments(source_string):
    """ # Excludes Lisp comments from a source string """
    result = source_string
    # Remove commented-out lines
    result = [x for x in result.splitlines() if not x.lstrip().startswith(";")]
    # Exclude comments from other strings
    result = "\n".join([x[:x.find(";")] if (";" in x) else x for x in result])
    return result
