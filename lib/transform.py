import csv
import json


def csv_to_json(csv_file_path, json_file_path):
    # Read the CSV file and convert it to a list of dictionaries
    data = []
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)

    # Write the list of dictionaries to a JSON file
    with open(json_file_path, mode='w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4)


# Example usage
csv_file_path = './data/raw/top-1000-realtor-data.csv'
json_file_path = './data/curated/top-1000-realtor-data.json'
csv_to_json(csv_file_path, json_file_path)
