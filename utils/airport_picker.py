import csv
import random
import os

AIRPORTS_CSV = os.path.join(os.path.dirname(__file__), '..', 'airports.csv')

def load_airports():
    airports = []
    with open(AIRPORTS_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Filter for medium or large airports only
            if row['type'] in ('large_airport', 'medium_airport'):
                airports.append(row)
    return airports

def get_random_destination(airports):
    return random.choice(airports)
