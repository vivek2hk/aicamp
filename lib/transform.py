import csv
import json
import requests
from dotenv import load_dotenv
import os

import json


def validate_and_fix_json(file_path):
    try:
        # Read the JSON file
        with open(file_path, 'r') as file:
            data = file.read()

        # Try to parse the JSON data
        try:
            json_data = json.loads(data)
            print("The JSON file is valid.")
            return json_data
        except json.JSONDecodeError:
            print("The JSON file is invalid. Attempting to fix it...")

            # Try to fix common JSON errors
            # Here, you can add custom logic to handle specific errors.
            # This example only includes basic error handling.
            fixed_data = data.replace("'",
                                      '"')  # Replace single quotes with double quotes
            fixed_data = fixed_data.replace("True", "true").replace("False",
                                                                    "false")  # Replace Python booleans with JSON booleans
            fixed_data = fixed_data.replace("None",
                                            "null")  # Replace Python None with JSON null

            try:
                json_data = json.loads(fixed_data)
                with open(file_path, 'w') as file:
                    json.dump(json_data, file, indent=4)
                print("The JSON file has been fixed and saved.")
                return json_data
            except json.JSONDecodeError:
                print("The JSON file could not be fixed.")
                return None

    except IOError:
        print(f"Error: The file {file_path} does not exist or cannot be read.")
        return None


def csv_to_json(csv_file_path, json_file_path):
    # Read the CSV file and convert it to a list of dictionaries
    data = []
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            json_string = json.dumps(row)
            consolidated_text = json_string.replace("{", "").replace("}", "")
            # summary = generate_summary(row)
            row['consolidated_text'] = str(consolidated_text)
            # row['summary'] = summary
            # print(row)
            data.append(row)

    json_string = json.dumps(data)

    # Write the JSON string to a file
    with open(json_file_path, 'w') as file:
        file.write(json_string)


def generate_summary(input: dict):
    load_dotenv()

    api_key = os.getenv('UPSTAGE_API_KEY')

    from langchain_upstage import ChatUpstage
    from langchain_core.messages import HumanMessage, SystemMessage

    chat = ChatUpstage(upstage_api_key=api_key)
    system_prompt = f"""
    You are a helpful assistant. You are getting an input related to real estate property information as a python dictionary with format
    brokered_by, status, price, bed, bath, acre_lot, street, city, state, zip_code, house_size, prev_sold_date. Generate a summary for the property
    {input}
    """

    messages = [
        SystemMessage(content=system_prompt),
        # HumanMessage(content="Hi, how are you?")
    ]
    response = chat.invoke(messages)
    # print(json.loads(response.json())['content'])

    summary = json.loads(response.json())['content']
    return summary

# Example usage
csv_file_path = '../data/raw/top-1000-realtor-data.csv'
json_file_path = '../data/curated/top-1000-realtor-data.json'
csv_to_json(csv_file_path, json_file_path)