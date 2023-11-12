#!/usr/bin/env python3

import argparse
import json
import requests
import sys

valid_bulk_types = [
    'oracle_cards',
    'unique_artwork',
    'default_cards',
    'all_cards',
    'rulings'
]

def get_database(bulk_type, output):
    with requests.get('https://api.scryfall.com/bulk-data') as response:
        for data in response.json()['data']:
            if data['type'] == bulk_type:
                download_uri = data['download_uri']
    with requests.get(download_uri) as response:
        output.write(response.text)

def gen_key(collector_number, set_code, lang_code):
    return '%s.%s.%s' % (collector_number.lower(), set_code.lower(), lang_code.lower())

def load_scryfall(file):
    database = {}
    card_array = json.loads(file.read())
    for card in card_array:
        key = gen_key(collector_number=card['collector_number'], set_code=card['set'], lang_code=card['lang'])
        database[key] = card
    return database

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = 'Download Scryfall database'
    )
    parser.add_argument('--bulk-type', default='all_cards', choices=valid_bulk_types)
    parser.add_argument('--output', default=sys.stdout, type=argparse.FileType('w'))
    args = parser.parse_args()

    get_database(args.bulk_type, args.output)
