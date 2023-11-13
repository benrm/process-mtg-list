#!/usr/bin/env python3

import argparse
import json
import merge
import sys

parser = argparse.ArgumentParser(
    description = 'Print price totals from JSON inventory'
)
parser.add_argument('--input', '-i', default=sys.stdin, type=argparse.FileType('r'))
args = parser.parse_args()

inventory, _ = merge.load_inventory(args.input)

scryfall_price = 0
low_price = 0
mid_price = 0
market_price = 0
for entry in inventory:
    try:
        quantity = int(entry['quantity'])
        prices = entry['scryfall']['prices']
        match entry['printing'].lower():
            case 'normal':
                scryfall_price += quantity * float(prices['usd'])
            case 'foil':
                scryfall_price += quantity * float(prices['usd_foil'])
            case 'etched foil':
                scryfall_price += quantity * float(prices['usd_etched'])
            case _:
                raise Exception('unknown printing')

        low_price += quantity * entry['low_price']
        mid_price += quantity * entry['mid_price']
        market_price += quantity * entry['market_price']

    except Exception as e:
        print(entry['card_name'], 'has no price:', str(e), file=sys.stderr)

print('Scryfall Price:', round(scryfall_price, 2))
print('Low Price:', round(low_price, 2))
print('Mid Price:', round(mid_price, 2))
print('Market Price:', round(market_price, 2))
