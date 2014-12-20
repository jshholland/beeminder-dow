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


def next_monday(date):
    """Return the datetime.date of the next Monday after date."""
    weekday = date.weekday()
    # monday is 0
    diff = 7 - weekday
    return date + datetime.timedelta(days=diff)


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('goal', type=str, help="the goal to work on")
parser.add_argument('dow_spec', type=dow_spec, help="days to add a holiday")
parser.add_argument('--api-key-file', '-k', type=argparse.FileType('r'),
                    help="file containing API key (default: %(default)s)",
                    default=os.path.expanduser('~/.beem_api_key'))
parser.add_argument('--base-url', help="base url to make requests against",
                    default='https://www.beeminder.com/api/v1')

args = parser.parse_args()

base = args.base_url
token = args.api_key_file.read().strip()

params = {'auth_token': token}

response = requests.get(base + '/users/me.json', params=params)
username = response.json()['username']

r = requests.get(base + '/users/{}/goals/{}.json'.format(username, args.goal),
                 params=params)

if r.status_code == 404:
    print("Goal not found")
    sys.exit(1)

r = r.json()

today = datetime.date.today()
horizon = today + datetime.timedelta(weeks=1)
cur_date = next_monday(horizon)
end_date = datetime.date.fromtimestamp(r['goaldate'])
rate = r['rate']
roadall = r['roadall']

should_apply = itertools.cycle(args.dow_spec)

rle = (len(list(g)) for k, g in itertools.groupby(should_apply))

print(list(itertools.islice(rle, 30)))

increase = args.dow_spec[0]

