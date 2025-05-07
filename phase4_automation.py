import os
import time
import json
import schedule
from datetime import datetime
from phase2_scraper import run_scraping  # Assume this is your scraping function
from phase3_model import train_model, save_model, load_model  # From your previous code

# Function to run the scraping and model retraining process
def run_automation():
    print(f"Running automation at {datetime.now()}")
    
    # Step 1: Run Scraping Process (Phase 1)
    print("Starting web scraping...")
    run_scraping()  # Scrape new data and store it
    
    # Step 2: Load new data for retraining
    print("Loading new data...")
    new_data = load_new_data('data/raw_data.json')  # Load scraped data
    
    # Step 3: Retrain Model (Phase 5)
    print("Retraining model...")
    features, labels = preprocess_data(new_data)  # Preprocess the new data
    model, vectorizer = train_model(features, labels)  # Retrain model
    
    # Step 4: Save the retrained model
    print("Saving the retrained model...")
    save_model(model, vectorizer)  # Save model to disk
    
    print(f"Automation process completed at {datetime.now()}")

# Set up automatic scheduling (e.g., every week)
schedule.every(7).days.do(run_automation)

# Run the automation process
while True:
    schedule.run_pending()  # Run scheduled tasks
    time.sleep(1)  # Sleep for 1 second to prevent CPU overuse
