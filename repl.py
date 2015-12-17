#!/usr/bin/env python
# -*- coding: utf-8 -*-

from evaluator import Environment, evaluate_string, lispify


if __name__ == '__main__':
    env = Environment.default()
    evaluate_string("(import lib/stdlib)", env)
    evaluate_string("(import lib/merge-sort)", env)

    # while True:
    #     user_input = raw_input('> ')
    #     if len(user_input.strip()) == 0:
    #         continue
    #     retval = evaluate_string(user_input, env)
    #     # and print a result if any
    #     if retval is not None:
    #         print(lispify(retval))
    print(lispify(evaluate_string("(sqrt 9)", env)))
    print(lispify(evaluate_string("(count 1 '(1 0 9 1 8 71 8.1))", env)))

    print(lispify(evaluate_string("(define array '(1 -8 5 19 7 3 4 9))", env)))
    print(lispify(evaluate_string("(merge-sort array)", env)))
