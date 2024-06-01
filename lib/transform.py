import csv
import json
import requests
from dotenv import load_dotenv
import os


def csv_to_json(csv_file_path, json_file_path):
    # Read the CSV file and convert it to a list of dictionaries
    data = []
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            consolidated_text = json.dumps(row)
            summary = generate_summary(row)
            row['consolidated_text'] = consolidated_text
            row['summary'] = summary
            print(row)
            data.append(row)

    # Write the list of dictionaries to a JSON file
    with open(json_file_path, mode='w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4)


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
# csv_file_path = './data/raw/top-1000-realtor-data.csv'
# json_file_path = './data/curated/top-1000-realtor-data.json'
# csv_to_json(csv_file_path, json_file_path)