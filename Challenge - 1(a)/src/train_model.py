import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

def train():
    """Trains a classifier on the labeled data and saves the model."""
    print("Loading labeled data...")
    try:
        data = pd.read_csv("labeled_data.csv")
    except FileNotFoundError:
        print("Error: 'labeled_data.csv' not found. Please complete the labeling step first.")
        return

    print(f"Training on {len(data)} labeled examples.")

    # Define the features the model will use to learn
    features = [
        'font_size', 'size_vs_body', 'is_bold', 'y_pos', 
        'line_length', 'word_count', 'is_all_caps', 
        'starts_with_number', 'ends_with_colon'
    ]
    
    X = data[features]
    y = data['label']

    # Split data to test the model's performance
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

    print("Training the RandomForest model...")
    model = RandomForestClassifier(n_estimators=150, random_state=42, class_weight='balanced')
    model.fit(X_train, y_train)

    # --- Evaluate the Model ---
    print("\n--- Model Performance Report ---")
    predictions = model.predict(X_test)
    print(classification_report(y_test, predictions))
    print("--------------------------------\n")
    
    # --- Save the Final Model ---
    model_filename = 'document_outline_model.pkl'
    joblib.dump(model, model_filename)
    print(f"Model successfully trained and saved to '{model_filename}'!")
    print("Next Step: Copy this .pkl file and the new 'process_pdfs.py' to your final Docker project folder.")

if __name__ == "__main__":
    train()