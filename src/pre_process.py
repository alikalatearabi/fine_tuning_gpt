import os
import re
import json
import glob

# Define dataset paths
DATASET_PATH = "../data/data/blogs"  # Path to the unzipped "blogs" folder
OUTPUT_PATH = "../data/preprocessed"  # Path to save the preprocessed data
os.makedirs(OUTPUT_PATH, exist_ok=True)

# Define output file for preprocessed data
OUTPUT_FILE = os.path.join(OUTPUT_PATH, "preprocessed_blog_data.json")

# Function to clean the text
def clean_text(text):
    """
    Cleans blog text by removing unwanted characters and normalizing whitespace.
    """
    text = re.sub(r"http\S+", "", text)  # Remove URLs
    text = re.sub(r"[^\w\s.,!?]", "", text)  # Remove special characters
    text = re.sub(r"\s+", " ", text).strip()  # Normalize whitespace
    return text

# Function to parse the date from <date> tags
def parse_date(line):
    """
    Extracts the date from a line containing <date> tags.
    """
    return line.strip().split("<date>")[-1].split("</date>")[0]

# Preprocess the dataset
def preprocess_blog_dataset():
    """
    Preprocesses the Blog Authorship Corpus dataset by extracting, cleaning, and organizing the data.
    """
    chunk_size = 500  # Tokens per chunk (adjust as needed)
    processed_data = []
    key = 0  # Unique ID for each chunk

    # Get all blog files
    blog_files = glob.glob(os.path.join(DATASET_PATH, "*.xml"))
    total_files = len(blog_files)

    print(f"Found {total_files} blog files. Starting preprocessing...")

    # Iterate over all blog files with a tracker
    for i, file_path in enumerate(blog_files):
        file_name = os.path.basename(file_path)
        blogger_id, gender, age, job, horoscope = tuple(file_name.split(".")[:-1])

        with open(file_path, encoding="latin_1") as file:
            date = ""
            content = ""

            # Process each line in the file
            for line in file:
                line = line.strip()

                # Extract the date
                if "<date>" in line:
                    date = parse_date(line)

                # Extract and clean blog post text
                elif line != "" and not line.startswith("<"):
                    content += f" {clean_text(line)}"

                # Chunk the content if it gets too large or a new post starts
                if len(content.split()) >= chunk_size or line == "":
                    if content.strip():  # Ensure non-empty content
                        processed_data.append({
                            "id": key,
                            "text": content.strip(),
                            "date": date,
                            "gender": gender,
                            "age": int(age),
                            "job": job,
                            "horoscope": horoscope,
                        })
                        key += 1
                        content = ""  # Reset content for the next chunk

        # Update progress tracker
        print(f"Processed file {i + 1}/{total_files}: {file_name}")

    # Save the preprocessed data to a JSON file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as output_file:
        json.dump(processed_data, output_file, indent=2, ensure_ascii=False)

    print(f"✅ Preprocessed data saved to {OUTPUT_FILE}")

# Run the preprocessing function
if __name__ == "__main__":
    preprocess_blog_dataset()
