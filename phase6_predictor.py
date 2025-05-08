import joblib
import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Function to load the trained model and vectorizer
def load_model_and_vectorizer():
    # Load the model and vectorizer using joblib
    model = joblib.load('model/trained_model.joblib')
    tfidf_vectorizer = joblib.load('model/tfidf_vectorizer.joblib')
    return model, tfidf_vectorizer

# Function to make predictions on new data
def predict_new_data(model, tfidf_vectorizer, new_data):
    # Transform the new data using the vectorizer
    new_data_tfidf = tfidf_vectorizer.transform(new_data)
    
    # Make predictions
    predictions = model.predict(new_data_tfidf)
    
    # Return predictions
    return predictions

# Function to save predictions to a JSON file
def save_predictions(predictions, output_file='predictions.json'):
    # Save predictions to a JSON file
    with open(output_file, 'w') as f:
        json.dump(predictions.tolist(), f, indent=2)
    print(f"✅ Predictions saved to {output_file}")

# Main function to run the predictions
def main():
    # Load the trained model and vectorizer
    model, tfidf_vectorizer = load_model_and_vectorizer()
    
    # Example new data (replace with actual data you want to predict)
    new_data = [
        "Best restaurants to visit in Ahmedabad",
        "Top tourist destinations in Paris",
        "Delicious food delivery apps in Mumbai"
    ]
    
    # Make predictions on new data
    predictions = predict_new_data(model, tfidf_vectorizer, new_data)
    
    # Print out the predictions
    for text, prediction in zip(new_data, predictions):
        print(f"Text: '{text}' -> Predicted Category: {prediction}")
    
    # Save predictions to a JSON file
    save_predictions(predictions)

if __name__ == "__main__":
    main()
