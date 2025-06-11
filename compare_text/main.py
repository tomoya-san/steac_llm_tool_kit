import sys
import os
import pandas as pd

from difflib import SequenceMatcher

def compare_texts(original_text, fixed_text):
    # Compare two texts and return a list of words
    original_text_words = original_text.split()
    fixed_text_words = fixed_text.split()

    # Use SequenceMatcher to find differences
    matcher = SequenceMatcher(None, original_text_words, fixed_text_words)
    changes = []

    # Iterate through the opcodes to identify changes
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():

        if tag == "equal":
            for word in original_text_words[i1:i2]:
                changes.append(("equal", word, word))
        elif tag == "replace":
            for w1, w2 in zip(original_text_words[i1:i2], fixed_text_words[j1:j2]):
                changes.append(("replace", w1, w2))
            # Handle unequal lengths (e.g. 3→2 or 2→3 replacements)
            len1 = i2 - i1
            len2 = j2 - j1
            if len1 > len2:
                for w1 in original_text_words[i1 + len2:i2]:
                    changes.append(("delete", w1, ""))
            elif len2 > len1:
                for w2 in fixed_text_words[j1 + len1:j2]:
                    changes.append(("insert", "", w2))
        elif tag == "delete":
            for w1 in original_text_words[i1:i2]:
                changes.append(("delete", w1, ""))
        elif tag == "insert":
            for w2 in fixed_text_words[j1:j2]:
                changes.append(("insert", "", w2))

    return changes


def generate_summary(changes):
    summary = ""
    change_count = 0

    for change in changes:
        action, original_word, fixed_word = change
        if action == "replace":
            summary += f"'{original_word}' -> '{fixed_word}'\n"
            change_count += 1
        elif action == "delete":
            summary += f"'{original_word}' -> ''\n"
            change_count += 1
        elif action == "insert":
            summary += f"'' -> '{fixed_word}'\n"
            change_count += 1

    if not summary:
        summary = "IDENTICAL"

    return summary, change_count

def main():
    # Check if the script is run with the correct number of arguments
    if len(sys.argv) != 3:
        print("Usage: python main.py <original_text> <fixed_text>")
        return

    # Check if the input CSV file exists and is valid
    input_csv_path = os.path.join(ROOT_DIR, "input_data", sys.argv[1])
    if not os.path.exists(input_csv_path):
        print(f"The file {input_csv_path} does not exist.")
        return
    
    # Check if the output CSV file has a .csv extension
    output_csv_path = os.path.join(ROOT_DIR, "out", sys.argv[2])
    if not output_csv_path.lower().endswith('.csv'):
        print("The output file path must end with .csv")
        return
    
    # Load the CSV file to a dataframe
    df = pd.read_csv(input_csv_path)

    # Check if the required columns exist
    if "original_text" not in df.columns or "fixed_text" not in df.columns:
        print("The CSV file must contain 'original_text' and 'fixed_text' columns.")
        return
    
    # Ensure the 'changes' column exists, if not create it
    if "changes" not in df.columns:
        df["changes"] = ""

    # Process each row to compare original and fixed texts
    for idx, row in df.iterrows():
        original_text = row["original_text"]
        fixed_text = row["fixed_text"]
        changes = compare_texts(original_text, fixed_text)
        changes_summary, change_count = generate_summary(changes)
        df.at[idx, "changes"] = changes_summary
        print(f"Row {idx}: {change_count} changes found.")

    # Save the updated dataframe to the output CSV file
    df.to_csv(output_csv_path, index=False)

if __name__ == "__main__":
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    main()