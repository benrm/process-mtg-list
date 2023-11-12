#!/usr/bin/env python3

import argparse
import csv
import json
import sys

language_codes = {
    'English': 'en',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Italian': 'it',
    'Portuguese': 'pt',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Russian': 'ru',
    'Simplified Chinese': 'zhs',
    'Traditional Chinese': 'zht',
    'Hebrew': 'he',
    'Latin': 'la',
    'Ancient Greek': 'grc',
    'Arabic': 'ar',
    'Sanskrit': 'sa',
    'Phyrexian': 'ph'
}

def load_inventory(csvinfile, skipped_output, separator=True, header=True):
    inventory = []
    if separator:
        csvinfile.readline()
    if header:
        csvinfile.readline()
    rows = csv.reader(csvinfile)
    skipped_output_csv = csv.writer(skipped_output)
    for row in rows:
        try:
            entry = {
                'folder': row[0],
                'quantity': int(row[1]),
                'trade_quantity': int(row[2]),
                'card_name': row[3],
                'set_code': row[4],
                'set_name': row[5],
                'card_number': row[6],
                'condition': row[7],
                'printing': row[8],
                'language': row[9],
                'language_code': language_codes[row[9]],
                'price_bought': float(row[10]),
                'date_bought': row[11],
                'low_price': float(row[12]),
                'mid_price': float(row[13]),
                'market_price': float(row[14])
            }
            inventory.append(entry)
        except Exception as e:
            row.append(str(e))
            skipped_output_csv.writerow(row)
    return inventory

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = 'Process a Dragon Shield CSV file'
    )
    parser.add_argument('--input', '-i', type=argparse.FileType('r'))
    parser.add_argument('--skipped-output', default=sys.stderr, type=argparse.FileType('w'))
    parser.add_argument('--output', '-o', default=sys.stdout, type=argparse.FileType('w'))
    parser.add_argument('--no-header', default=False, action='store_true')
    parser.add_argument('--no-separator-line', default=False, action='store_true')
    args = parser.parse_args()

    inventory = load_inventory(args.input, args.skipped_output, not args.no_header, not args.no_separator_line)

    print(json.dumps(inventory), file=args.output)
