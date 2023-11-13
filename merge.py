#!/usr/bin/env python3

import argparse
import csv
import dragon_shield
import json
import scryfall
import sys

def load_inventory(file):
    output = json.loads(file.read())
    return output['inventory'], output['not_found']

def merge_inventory(inventory, database):
    merged = []
    not_found = []
    for entry in inventory:
        key = scryfall.gen_key(collector_number=entry['card_number'], set_code=entry['set_code'], lang_code=entry['language_code'])

        if key in database:
            entry['scryfall'] = database[key]
            merged.append(entry)
        else:
            print('Didn\'t find', entry['card_name'], file=sys.stderr)
            not_found.append(entry)

    return merged, not_found

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = 'Merge a CSV Dragon Shield inventory with a Scryfall database'
    )
    parser.add_argument('--csv', type=argparse.FileType('r'))
    parser.add_argument('--database', type=argparse.FileType('r'))
    parser.add_argument('--output', '-o', default=sys.stdout, type=argparse.FileType('w'))
    args = parser.parse_args()

    inventory, skipped = dragon_shield.load_inventory(args.csv)

    database = scryfall.load_scryfall(args.database)

    merged, not_found = merge_inventory(inventory, database)

    print(json.dumps({'inventory': merged, 'not_found': not_found}), file=args.output)
