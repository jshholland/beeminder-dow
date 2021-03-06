#!/usr/bin/env python3
# coding: utf-8
#
# Copyright © 2014 Josh Holland <josh@inv.alid.pw>
#
# This file is released under the BSD licence; see the COPYING file for
# details.
#
# More information is available from the project homepage at
# https://github.com/jshholland/beeminder-dow
#
"""Utility to add regular weekly holidays to a Beeminder goal.

The dow_spec argument should be 7 characters long, corresponding to the
7 days of the week starting on Monday. Any character other than '-' means
that the goal should count on that day, so you can enter mnemonic letters
(in your own language if you like) to make it easier to see which day
is which.

For example, a goal which should only run on weekdays would translate to
a dow_spec of the form "mtwtf--", "yyyyy--", "ΔΤΤΠΠ--", or "пвсчп--".

The API key specified by the -k/--api-key option can be obtained by
visiting https://www.beeminder.com/api/v1/auth_token.json.
"""

import argparse
import datetime
import itertools
import os.path
import sys

import requests


# General functions


def run_length_encode(seq):
    for _, g in itertools.groupby(seq):
        yield len(list(g))


def next_monday(date):
    """Return the datetime.date of the next Monday after date."""
    weekday = date.weekday()
    # monday is 0
    diff = 7 - weekday
    return date + datetime.timedelta(days=diff)


# Specific functions for this script


def dow_spec(string):
    """Verify and convert the a dow_spec argument.

    The format returned is a list of bools such that for any datetime.date
    object, spec[date.weekday()] is True iff the goal should run on that day.
    """
    spec = [True] * 7
    if len(string) != 7:
        msg = "{} should be exactly 7 characters long".format(string)
        raise argparse.ArgumentTypeError(msg)
    for i, char in enumerate(string):
        spec[i] = char != '-'
    return spec


def get_response(base_url, goal, token):
    """Get a response from base_url using token."""
    params = {'auth_token': token}

    response = requests.get(base_url + '/users/me.json', params=params)
    username = response.json()['username']

    r = requests.get(base_url + '/users/{}/goals/{}.json'.format(username, goal), params=params)

    if r.status_code == 404:
        print("Goal not found")
        sys.exit(1)

    return r.json()


def main(args):
    """Run the program with command line args args."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('goal', type=str, help="the goal to work on")
    parser.add_argument('dow_spec', type=dow_spec, help="days to add a holiday")
    parser.add_argument('--api-key-file', '-k', type=argparse.FileType('r'),
                        help="file containing API key (default: %(default)s)",
                        default=os.path.expanduser('~/.beem_api_key'))
    parser.add_argument('--base-url', help="base url to make requests against",
                        default='https://www.beeminder.com/api/v1')

    ns = parser.parse_args(args)

    r = get_response(ns.base_url, ns.goal, ns.api_key_file.read().strip())

    today = datetime.date.today()
    horizon = today + datetime.timedelta(weeks=1)
    cur_date = next_monday(horizon)
    end_date = datetime.date.fromtimestamp(r['goaldate'])
    rate = r['rate']
    roadall = r['roadall']

    should_apply = itertools.cycle(ns.dow_spec)

    rle = run_length_encode(should_apply)

    print(list(itertools.islice(rle, 30)))

    increase = ns.dow_spec[0]

if __name__ == '__main__':
    main(sys.argv[1:])
