#!/usr/bin/env python3

import argparse
import json
import merge
import operator
import sys

parser = argparse.ArgumentParser(
    description = 'Print inventory in reverse price order'
)
parser.add_argument('--input', '-i', default=sys.stdin, type=argparse.FileType('r'))
args = parser.parse_args()

inventory, _ = merge.load_inventory(args.input)

s = sorted(inventory, key=operator.itemgetter('low_price'), reverse=True)

for row in s:
    print('Card: %s, Price: %s' % (row['card_name'], row['low_price']))
