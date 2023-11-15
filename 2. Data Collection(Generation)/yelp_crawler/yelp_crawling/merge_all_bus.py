import json
import os


def merge_json_files(folder_path, output_file):
    unique_ids = set()

    # Open the output file
    with open(output_file, 'w') as outfile:
        # List all JSON files in the folder
        for file_name in os.listdir(folder_path):
            print(f"Merging file {file_name}")
            if file_name.endswith('.json'):
                file_path = os.path.join(folder_path, file_name)

                # Read each JSON file line by line
                with open(file_path, 'r') as file:
                    for line in file:
                        try:
                            entry = json.loads(line)
                            business_id = entry.get("business_id")
                            # if business_id and business_id not in unique_ids:
                            if business_id:
                                unique_ids.add(business_id)
                                # Write each valid entry to the output file as a separate line
                                json.dump(entry, outfile)
                                outfile.write('\n')
                        except json.JSONDecodeError as e:
                            print(f"Error decoding JSON in file {file_name}: {e}")


# Usage
folder_path = './sg_data/'  # replace with your folder path
output_file = 'all_sg_data.json'  # name of the output file
merge_json_files(folder_path, output_file)
