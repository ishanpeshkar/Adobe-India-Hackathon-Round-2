import pandas as pd

def guess_label(row):
    """
    Applies a set of simple rules (heuristics) to guess the label for a row of features.
    This creates a "best guess" to speed up manual labeling.
    """
    # Rule 1: Very long lines are almost always body text.
    if row['word_count'] > 25 or row['line_length'] > 200:
        return 'Body'

    # Rule 2: Text that is smaller than or same size as body text is likely body.
    if row['size_vs_body'] <= 0 and not row['is_bold']:
        return 'Body'
    
    # Rule 3: Text ending with a period is usually body text.
    if row['text'].strip().endswith('.') and not row['is_all_caps']:
        return 'Body'

    # --- Heading Guessing Logic ---
    # Score the line based on how "heading-like" it is.
    score = 0
    if row['size_vs_body'] > 0:
        score += row['size_vs_body'] * 2  # Larger size = higher score
    if row['is_bold']:
        score += 5  # Boldness is a strong signal
    if row['is_all_caps']:
        score += 3
    if row['starts_with_number']:
        score += 2
    if row['ends_with_colon']:
        score += 2
    
    # Classify based on score
    if score > 15:
        return 'H1'
    elif score > 9:
        return 'H2'
    elif score > 3:
        return 'H3'
    elif score > 0:
        return 'H4'
    else:
        # If it doesn't meet any heading criteria, default to Body.
        return 'Body'

def main():
    """
    Loads the feature CSV, applies the heuristic guesser, and saves a new
    pre-labeled CSV ready for manual correction.
    """
    try:
        df = pd.read_csv("features.csv")
    except FileNotFoundError:
        print("Error: 'features.csv' not found. Please run 'create_training_data.py' first.")
        return

    print("Applying heuristic rules to pre-label the data...")
    
    # Apply the guessing function to every row to create the new 'label' column
    df['label'] = df.apply(guess_label, axis=1)
    
    output_path = 'prelabeled_data.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\nPre-labeling complete! Saved to '{output_path}'")
    print("Next Step: Open this file, correct any mistakes in the 'label' column, and save it as 'labeled_data.csv'.")

if __name__ == "__main__":
    main()