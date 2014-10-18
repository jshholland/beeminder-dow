#!/usr/bin/env python3
# -*-: coding: utf-8 -*-
"""Utility to add regular weekly holidays to a Beeminder goal.

The dow_spec argument should be 7 characters long, corresponding to the
7 days of the week starting on Monday. Any character other than '-' means
that the goal should count on that day, so you can enter mnemonic letters
(in your own language if you like) to make it easier to see which day
is which.

For example, a goal which should only run on weekdays would translate to
a dow_spec of the form "mtwtf--", "yyyyy--", "ΔΤΤΠΠ--", or "пвсчп--".
"""

import argparse

import requests


def dow_spec(string):
    """Verify and convert the a dow_spec argument."""
    spec = {}
    days = ['mo', 'tu', 'we', 'th', 'fr', 'sa', 'su']
    if len(string) != 7:
        msg = "{} should be exactly 7 characters long".format(string)
        raise argparse.ArgumentTypeError(msg)
    for day, char in zip(days, string):
        spec[day] = char != '-'
    return spec


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('goal', type=str, help="the goal to work on")
parser.add_argument('dow_spec', type=dow_spec, help="the days to add a holiday")

args = parser.parse_args()

print(args.dow_spec)
