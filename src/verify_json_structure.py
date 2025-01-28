import json

# Load the preprocessed data
with open("../data/preprocessed/preprocessed_blog_data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Validation checks
valid_entries = []
invalid_entries = []

for entry in data:
    if entry["text"].strip() and isinstance(entry["age"], int) and entry["gender"] in ["male", "female"]:
        valid_entries.append(entry)
    else:
        invalid_entries.append(entry)

# Print validation results
print(f"Total entries: {len(data)}")
print(f"Valid entries: {len(valid_entries)}")
print(f"Invalid entries: {len(invalid_entries)}")
