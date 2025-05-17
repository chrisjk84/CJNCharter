import csv

def load_airports(filepath):("data/airports.csv")  
    airports = []
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convert latitude and longitude to floats for calculations
            row['latitude_deg'] = float(row['latitude_deg'])
            row['longitude_deg'] = float(row['longitude_deg'])
            airports.append(row)
    return airports