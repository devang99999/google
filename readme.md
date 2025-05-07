# Google Search Data Scraper & Classifier

This project is a comprehensive solution for scraping Google search results, extracting detailed information from webpages, and classifying the content using machine learning. The system is divided into multiple phases, where data is first crawled, then scraped for detailed information, and finally classified for insights.

## Project Phases

### Phase 1: Google Search Crawling
- **Purpose:** Collect Google search result URLs based on predefined categories or search terms.
- **Steps:**
  - Perform Google searches for categories such as "best food in Ahmedabad."
  - Save the URLs from the search results to a JSON file.
  
### Phase 2: Crawling & Scraping Web Data
- **Purpose:** Extract metadata (title, description) and content (text, images, links) from the URLs obtained in Phase 1.
- **Steps:**
  - Scrape each URL for basic metadata and detailed content.
  - Store the crawled data and detailed scraped data separately.

### Phase 3: Content Classification Model
- **Purpose:** Use machine learning to classify the scraped data into relevant categories.
- **Steps:**
  - Preprocess scraped text data.
  - Train a classifier to predict categories based on scraped content.
  - Save the trained model and the vectorizer for future predictions.

### Phase 4: Automation of the Entire Process
- **Purpose:** Automate the scraping, crawling, and classification tasks, making the process easier to run periodically or on-demand.
- **Steps:**
  - Combine all previous phases into an automated script that runs the whole pipeline.

### Phase 5: Model Prediction & Evaluation
- **Purpose:** Test the trained model using a separate dataset and evaluate its performance using metrics like accuracy, precision, recall, and F1 score.
- **Steps:**
  - Load the saved model and vectorizer.
  - Predict the categories of new data using the model.
  - Evaluate the model performance and display metrics.

---

## Installation

### Requirements

Before running the project, make sure to install the required dependencies:

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <project_directory>
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - Mac/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies from requirements.txt:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Phase 1: Google Search Crawling
Run the crawler to get URLs for predefined categories:
```bash
python phase1_crawler.py
```
This will search Google for categories like "best food in Ahmedabad" and save the results to JSON files in the `data/urls` directory.

### Phase 2: Web Scraping
Run the scraper to extract metadata and content from the URLs:
```bash
python phase2_scraper.py
```
This will crawl through the URLs obtained from Phase 1 and extract the following details:
- Title of the webpage
- Description
- Main content (paragraphs, links, images)

The scraped data will be stored in the `data/refined` directory, and metadata (title and description) will be stored in the `data/urls` directory.

### Phase 3: Content Classification Model
Train the classification model using the scraped data:
```bash
python phase3_model.py
```
This will:
- Load the scraped data.
- Preprocess the data and create a TF-IDF feature vector.
- Train a classification model using the scikit-learn library (e.g., RandomForestClassifier or SVM).
- Save the trained model and vectorizer for future use.

### Phase 4: Automation
Automate the process by running all steps in one go:
```bash
python phase4_automation.py
```
This will run the entire pipeline: crawl, scrape, classify, and save results, all automatically.

### Phase 5: Prediction and Evaluation
Test and evaluate the model using new data or test sets:
```bash
python phase5_predictor.py
```
This will load the saved model and vectorizer, predict the category for new data, and evaluate the performance using various metrics like accuracy, precision, and recall.

## Project Structure
```
.
├── phase1_crawler.py      # Script for crawling Google search results
├── phase2_scraper.py      # Contains scraping logic for extracting data
├── phase3_model.py        # Script for training the classification model
├── phase4_automation.py   # Automation script for the entire process
├── phase5_predictor.py    # Script for prediction and evaluation
├── data                   # Data directory for storing raw and refined data
│   ├── raw                # Contains raw data (URLs from Google)
│   ├── refined            # Contains scraped data (titles, descriptions, content)
│   └── urls               # Contains crawled metadata
├── logs                   # Contains logs of scraping and crawling processes
├── models                 # Directory for storing trained models
├── requirements.txt       # List of dependencies for the project
└── README.md              # This README file
```

## Model Evaluation
- **Precision:** Measures how many selected items are relevant.
- **Recall:** Measures how many relevant items are selected.
- **F1-Score:** The harmonic mean of precision and recall.
- **Accuracy:** The proportion of correctly predicted instances.

The model will be evaluated with a classification report showing these metrics.

## Production Deployment Guide

To run this project in production, follow these steps:

1. **Set up a server environment**:
   - Use a cloud provider like AWS, GCP, or Azure
   - Configure a VM with sufficient CPU and memory resources
   - Install Python 3.8+ and required dependencies

2. **Set up a production database**:
   - Use MongoDB or PostgreSQL instead of file-based storage
   - Configure proper authentication and backup procedures

3. **Implement rate limiting and proxy rotation**:
   - Add proxy support to avoid IP bans
   - Implement random delays between requests
   - Use a proxy rotation service if needed

4. **Set up scheduled jobs**:
   - Use cron jobs or a task scheduler like Celery
   - Schedule regular crawling and model retraining

5. **Add monitoring and logging**:
   - Set up logging to a central service (e.g., ELK stack)
   - Configure alerts for failures or anomalies

6. **Use containerization**:
   - Create a Docker image of your application
   - Define services using Docker Compose or Kubernetes

7. **Set up CI/CD pipeline**:
   - Automate testing and deployment
   - Use GitHub Actions or Jenkins

8. **Scale horizontally**:
   - Deploy multiple instances for parallel processing
   - Use a load balancer to distribute requests

9. **Add a user interface**:
   - Create a web dashboard using Flask or Django
   - Implement API endpoints for programmatic access

10. **Ensure legal compliance**:
    - Review and comply with robots.txt files
    - Respect website terms of service
    - Consider adding proper user-agent identification

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements
- BeautifulSoup for web scraping
- Requests for HTTP requests
- scikit-learn for machine learning algorithms
- Playwright for browser automation
- TwoCaptcha for captcha-solving (if applicable)