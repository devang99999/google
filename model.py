import json
import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Helper function to check if the file exists
def check_and_create_data_file():
    data_file_path = 'data/raw_data.json'
    
    # Check if the file exists
    if not os.path.exists(data_file_path):
        print(f"❌ File '{data_file_path}' not found, creating a sample file.")
        
        # Example data format (replace this with your actual data)
        sample_data = [
            {"text": "Best food in Ahmedabad", "category": "Food"},
            {"text": "Top tourist places in India", "category": "Travel"},
            {"text": "Best restaurants in New York", "category": "Food"},
            {"text": "Famous landmarks in Paris", "category": "Travel"},
            {"text": "Must-try street foods in Ahmedabad", "category": "Food"},
            {"text": "Explore the Eiffel Tower in Paris", "category": "Travel"}
        ]
        
        # Create the 'data' directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        
        # Write sample data to 'raw_data.json'
        with open(data_file_path, 'w') as f:
            json.dump(sample_data, f, indent=2)
        
        print(f"✅ Sample data saved to '{data_file_path}'")

# Helper function to load data from JSON files
def load_data():
    data_file_path = 'data/raw_data.json'
    
    # Load your data (URLs and their labels) from the JSON files
    with open(data_file_path, 'r') as f:
        data = json.load(f)
    
    # Extract features (text) and labels from the data
    features = [item['text'] for item in data]  # Replace 'text' with the actual key for the textual data
    labels = [item['category'] for item in data]  # Replace 'category' with the actual key for the category/label
    return features, labels

# Model training function
def train_model(features, labels):
    # Initialize TfidfVectorizer
    tfidf_vectorizer = TfidfVectorizer()

    # Fit the TF-IDF vectorizer on the features
    features_tfidf = tfidf_vectorizer.fit_transform(features)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features_tfidf, labels, test_size=0.2, random_state=42)

    # Initialize the model (Multinomial Naive Bayes)
    model = MultinomialNB()

    # Train the model on the training data
    model.fit(X_train, y_train)

    # Evaluate the model
    predictions = model.predict(X_test)
    print("Classification Report:\n", classification_report(y_test, predictions))

    # Return the trained model and the vectorizer
    return model, tfidf_vectorizer

# Function to save the trained model and vectorizer
def save_model(model, tfidf_vectorizer):
    # Save the model and vectorizer to disk using joblib
    os.makedirs('model', exist_ok=True)
    
    # Saving the model using joblib
    joblib.dump(model, 'model/trained_model.joblib')
    
    # Saving the vectorizer using joblib
    joblib.dump(tfidf_vectorizer, 'model/tfidf_vectorizer.joblib')
    
    print("✅ Model and vectorizer saved successfully!")

# Main function to run the training process
def load_model():
    # Check if the raw_data.json file exists, create if not
    check_and_create_data_file()

    # Load your dataset (features and labels)
    features, labels = load_data()

    # Train the model
    model, tfidf_vectorizer = train_model(features, labels)

    # Save the trained model and vectorizer
    save_model(model, tfidf_vectorizer)

    print("Model and vectorizer trained and saved successfully!")

if __name__ == "__main__":
    load_model()
