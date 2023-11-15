import os
import json
import uuid
from random import uniform


# Function to read a JSON file and return the data
def read_json_file(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, 1):
            try:
                json_obj = json.loads(line)
                data.append(json_obj)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON on line {line_number}: {e}")
    return data


# Function to generate a random transaction amount
def generate_amount(min_amount, max_amount):
    return round(uniform(min_amount, max_amount), 2)


# Function to generate transactions
def generate_transactions(businesses, reviews, output_file_path):
    transactions = []
    for review in reviews[:]:
        transaction = {
            "transaction_id": str(uuid.uuid4()),
            "business_id": review["business_id"],
            "user_id": review["user_id"],
            "time": review["date"],
            "amount": generate_amount(10, 500)  # Random amount between $10 and $500
        }
        transactions.append(transaction)

    # Write the transactions to the output file

    with open(output_file_path, 'a') as outfile:
        # pretty print
        # json.dump(transactions, outfile, indent=4)
        for i, transaction in enumerate(transactions):
            json.dump(transaction, outfile)
            outfile.write('\n')
            if i % 1000 == 0:
                print(f"{i} transactions written to file...")

    print(f"Transaction dataset created with {len(transactions)} transactions.")


# Paths to the input JSON files
business_file_path = './yelp/yelp_academic_dataset_user.json'
review_file_path = './yelp/yelp_academic_dataset_review.json'

print("Reading the data from JSON files...")
# Read the data from JSON files
business_data = read_json_file(business_file_path)
review_data = read_json_file(review_file_path)

print("Generating the transactions...")
# Generate the transactions and write to a file
generate_transactions(business_data, review_data, 'transactions.json')
