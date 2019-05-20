#!/bin/env python
''' wikitranslator.py
find translations according to wikipedia

usage: wikitranslator.py <word> [<language>]

author: Steffen Brinkmann <brinkmann@mailbox.org>
license: (C) 2017 MIT license (https://mit-license.org/)
'''

import logging
import requests
import sys

logging.basicConfig(level=logging.DEBUG)

if len(sys.argv) == 1 or len(sys.argv) > 4:
    sys.stderr.write("usage: wikitranslator.py <word> [<from_language> [<to_language>]]\n")
    sys.exit(1)

# default values
from_LANG = 'de'
to_LANG = None  # will print all available translations

# set parameters from command line
if len(sys.argv) > 1:
    QUERY = sys.argv[1]
if len(sys.argv) > 2:
    from_LANG =  sys.argv[2]
if len(sys.argv) == 4:
    to_LANG =  sys.argv[3]

logging.debug(f'{from_LANG} {to_LANG}')
# url
url = f'https://{from_LANG}.wikipedia.org/w/api.php'
logging.info(f'requesting from {url}')

# set params
params = {}
params['action'] = 'query'
params['format'] = 'json'
params['prop'] = 'langlinks'
params['titles'] = QUERY
params['redirects'] = ''
params['lllimit'] = 500

# Call API
result = requests.get(url, params=params).json()

if 'error' in result:
    raise Exception(result['error'])
if 'warnings' in result:
    logging.warning(result['warnings'])

logging.debug('type(result["query"]) %s', type(result['query']))

for p in result['query'].values():
    logging.debug('type(p) %s', type(p))
    if isinstance(p, dict):
        for p_id in p.values():
            for lang in p_id['langlinks']:
                if to_LANG is not None:
                    if lang["lang"] == to_LANG:
                        print(f'{lang["lang"]}:\t{lang["*"]}')
                else:
                    print(f'{lang["lang"]}:\t{lang["*"]}')
