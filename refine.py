import os
import json
import re
from datetime import datetime
import pandas as pd

# Create the directory to store processed (refined) data
os.makedirs("data/processed", exist_ok=True)

# Load the scraped data from a JSON file
def load_scraped_data(category):
    safe_name = category.replace(" ", "_")
    files = os.listdir("data/refined")
    relevant_files = [file for file in files if file.startswith(safe_name) and file.endswith('.json')]

    all_data = []
    for file in relevant_files:
        with open(f"data/refined/{file}", "r") as f:
            data = json.load(f)
            all_data.extend(data)
    
    return all_data

# Clean and normalize the scraped data
def clean_and_normalize_data(data):
    cleaned_data = []

    for entry in data:
        # Extract the title and description
        title = entry.get('title', '').strip()
        description = entry.get('description', '').strip()
        content = entry.get('content', '').strip()
        images = entry.get('images', [])
        links = entry.get('links', [])

        # Clean the text (e.g., remove unwanted characters, convert to lowercase)
        cleaned_title = re.sub(r'\s+', ' ', title.lower()) if title else ''
        cleaned_description = re.sub(r'\s+', ' ', description.lower()) if description else ''
        cleaned_content = re.sub(r'\s+', ' ', content.lower()) if content else ''

        # Filter out irrelevant or broken links
        cleaned_images = [img for img in images if img.startswith('http')]
        cleaned_links = [link for link in links if link.startswith('http')]

        # Prepare the cleaned entry
        cleaned_entry = {
            "url": entry.get("url"),
            "title": cleaned_title,
            "description": cleaned_description,
            "content": cleaned_content,
            "images": cleaned_images,
            "links": cleaned_links
        }

        cleaned_data.append(cleaned_entry)

    return cleaned_data

# Save the cleaned data to a new JSON or CSV file
def save_cleaned_data(category, data):
    safe_name = category.replace(" ", "_")
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Save as JSON
    json_file_path = f"data/processed/{safe_name}_processed_{timestamp}.json"
    with open(json_file_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"📝 Saved cleaned data to {json_file_path}")
    
    # Optionally, save as CSV for AI model training
    csv_file_path = f"data/processed/{safe_name}_processed_{timestamp}.csv"
    df = pd.DataFrame(data)
    df.to_csv(csv_file_path, index=False)
    print(f"📝 Saved cleaned data to {csv_file_path}")

# Main function to clean and structure data for all categories
def main():
    categories = [
        "best food in ahmedabad",  # Add your other categories here
        "vayu app"
    ]

    for category in categories:
        # Load the scraped data for the category
        scraped_data = load_scraped_data(category)
        
        # Clean and normalize the scraped data
        cleaned_data = clean_and_normalize_data(scraped_data)
        
        # Save the cleaned data to files
        if cleaned_data:
            save_cleaned_data(category, cleaned_data)

if __name__ == "__main__":
    print("🚀 Starting Phase 4: Refining and Structuring Data")
    main()
    print("✅ Phase 4 Complete!")
