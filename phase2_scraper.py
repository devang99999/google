import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

# Create necessary directories for storing refined (scraped) data
os.makedirs("data/urls", exist_ok=True)  # For crawled URLs (metadata)
os.makedirs("data/refined", exist_ok=True)  # For detailed scraped data

# Load URLs from Phase 1 (Crawling phase)
def load_urls_from_file(category):
    """
    Load the list of URLs that were crawled in Phase 1 for a specific category.
    """
    safe_name = category.replace(" ", "_")
    file_path = f"data/urls/{safe_name}.json"
    
    # Ensure the file exists before attempting to load
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            urls = json.load(f)
        return urls
    else:
        print(f"❌ File {file_path} not found!")
        return []

# Function to extract detailed data from a webpage (scraping)
def scrape_detailed_data_from_page(url):
    """
    Scrapes detailed data from the given webpage (title, description, content, images, and links).
    """
    try:
        print(f"➡️  Scraping: {url}")
        # Send request to the webpage
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extracting title, description, and other data
        title = soup.title.string if soup.title else "No Title"
        description = soup.find('meta', attrs={'name': 'description'})
        description = description['content'] if description else "No Description"
        
        # Extracting main content (paragraphs, links, etc.)
        content = ''
        for paragraph in soup.find_all('p'):
            content += paragraph.get_text()

        # Extracting all images
        images = [img['src'] for img in soup.find_all('img', src=True)]
        
        # Extracting all links
        links = [a['href'] for a in soup.find_all('a', href=True)]

        # Store all scraped data in a structured way
        data = {
            "url": url,
            "title": title,
            "description": description,
            "content": content.strip(),
            "images": images,
            "links": links
        }

        return data
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to scrape {url}: {e}")
        return None
    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")
        return None

# Save crawled data (basic metadata) to a JSON file
def save_crawled_data(category, data):
    """
    Save metadata of the crawled data (e.g., titles, URLs) to a JSON file.
    """
    safe_name = category.replace(" ", "_")
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_path = f"data/urls/{safe_name}_crawled_{timestamp}.json"

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"📝 Saved crawled data to {file_path}")

# Save detailed scraped data to a JSON file
def save_scraped_data(category, data):
    """
    Save the detailed scraped data to a JSON file.
    """
    safe_name = category.replace(" ", "_")
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_path = f"data/refined/{safe_name}_scraped_{timestamp}.json"

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"📝 Saved scraped data to {file_path}")

# Main function to scrape detailed data for all categories
def run_scraping():
    """
    Main function to scrape detailed data for multiple categories.
    """
    categories = [
        "best food in ahmedabad",  # Example category 1
        "vayu app"  # Example category 2
    ]
    
    for category in categories:
        # Load URLs for the category (from Phase 1 Crawling)
        urls = load_urls_from_file(category)
        
        if not urls:
            print(f"❌ No URLs found for category: {category}")
            continue
        
        # List to hold detailed scraped data
        scraped_data = []

        # Crawl and save metadata (title, description, URL) for each URL
        crawled_data = []
        for url in urls:
            # Scrape detailed data from each URL
            page_data = scrape_detailed_data_from_page(url)
            if page_data:
                scraped_data.append(page_data)

                # Store crawled data (metadata) - we are storing titles and URLs here
                crawled_entry = {
                    "url": page_data["url"],
                    "title": page_data["title"],
                    "description": page_data["description"]
                }
                crawled_data.append(crawled_entry)
        
        # Save both crawled and scraped data in separate files
        if crawled_data:
            save_crawled_data(category, crawled_data)  # Save crawled metadata
        
        if scraped_data:
            save_scraped_data(category, scraped_data)  # Save scraped detailed content
        
        # Sleep to avoid being blocked (be polite)
        print(f"⏳ Sleeping for a few seconds...\n")
        time.sleep(5)

if __name__ == "__main__":
    print("🚀 Starting Phase 3: Scraping Detailed Data")
    run_scraping()
    print("✅ Phase 3 Complete!")
