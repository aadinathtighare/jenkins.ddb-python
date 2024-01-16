import boto3
from prettytable import PrettyTable

def fetch_dynamodb_data(table_name, region):
    dynamodb = boto3.resource('dynamodb', region_name=region)
    table = dynamodb.Table(table_name)

    response = table.scan()
    items = response.get('Items', [])

    return items

def print_all_attributes_table(items):
    if not items:
        print("No items found.")
        return

    table = PrettyTable()
    field_names_set = set(['ItemId', 'CIDRBlock'])  # Include CIDRBlock in the field names

    for item in items:
        field_names_set.update(item.keys())

    table.field_names = list(field_names_set)

    for item in items:
        row_values = [item.get('ItemId'), item.get('CIDRBlock')] + [item.get(attribute) for attribute in field_names_set if attribute not in ['ItemId', 'CIDRBlock']]
        table.add_row(row_values)

    print(table)

def get_user_choice(items):
    if not items:
        print("No items found.")
        return None

    item_ids = [item['ItemId'] for item in items]
    prompt = f"Choose ItemId ({', '.join(item_ids)}): "
    
    user_choice = input(prompt)
    while user_choice not in item_ids:
        print("Invalid choice. Please choose a valid ItemId.")
        user_choice = input(prompt)

    return user_choice

if __name__ == "__main__":
    # Replace 'your_table_name' and 'your_region' with your actual DynamoDB table name and region
    table_name = 'blankcidr'
    region = 'ap-south-1'

    try:
        dynamodb_data = fetch_dynamodb_data(table_name, region)
        print_all_attributes_table(dynamodb_data)

        # Get user choice for ItemId
        chosen_item_id = get_user_choice(dynamodb_data)

        # Find the item with the chosen ItemId
        chosen_item = next((item for item in dynamodb_data if item['ItemId'] == chosen_item_id), None)

        if chosen_item:
            print(f"Chosen ItemId: {chosen_item['ItemId']}")
            print(f"CIDRBlock Value: {chosen_item['CIDRBlock']}")
        else:
            print("Invalid ItemId.")

    except Exception as e:
        print(f"Error: {e}")