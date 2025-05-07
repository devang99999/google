import os
import json
import time
import random
from datetime import datetime
from serpapi import GoogleSearch

# === Setup ===
os.makedirs("logs", exist_ok=True)
os.makedirs("data/urls", exist_ok=True)

# Your SerpAPI API Key (sign up at https://serpapi.com/)
SERP_API_KEY = ''

# Categories for search
CATEGORIES = [
    "best food in ahmedabad",
    "vayu app"
]

def run_search(query):
    print(f"➡️  Searching for: {query}")
    
    search_params = {
        "q": query,
        "api_key": SERP_API_KEY,
        "num": 20  # You can adjust the number of results
    }
    
    # Perform the Google search using SerpAPI
    search = GoogleSearch(search_params)
    results = search.get_dict()
    
    # Check for results and extract URLs
    if 'organic_results' in results:
        urls = [result['link'] for result in results['organic_results']]
    else:
        print(f"❌ No results found for query: {query}")
        return []
    
    # Save raw HTML
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    with open(f"logs/{query.replace(' ', '_')}_{timestamp}.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    
    return urls

def save_urls(query, urls):
    filename = f"data/urls/{query.replace(' ', '_')}.json"
    with open(filename, "w") as f:
        json.dump(urls, f, indent=2)
    print(f"📝 Saved {len(urls)} URLs to {filename}\n")

def main():
    for query in CATEGORIES:
        try:
            urls = run_search(query)
            if urls:
                save_urls(query, urls)
            # Random delay between queries to avoid overloading
            time.sleep(random.randint(10, 25))
        except Exception as e:
            print(f"❌ Error with query '{query}': {e}")

if __name__ == "__main__":
    print("🚀 Starting Google Search with SerpAPI")
    main()
    print("✅ All done!")
