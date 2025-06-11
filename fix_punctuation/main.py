import os
import sys
import pandas as pd

from openai import OpenAI
from dotenv import load_dotenv


def main():
    # Check if the script is run with the correct number of arguments
    if len(sys.argv) != 3:
        print("Usage: python main.py <input_csv_file_name> <output_csv_file_name>")
        return
    
    # Check if the input CSV file exists and is valid
    input_csv_path = os.path.join(ROOT_DIR, f"input_data/{sys.argv[1]}")
    if not os.path.exists(input_csv_path):
        print(f"The file {input_csv_path} does not exist.")
        return
    
    # Check if the output CSV file has a .csv extension
    output_csv_path = os.path.join(ROOT_DIR, f"out/{sys.argv[2]}")
    if not output_csv_path.lower().endswith('.csv'):
        print("The output file path must end with .csv")
        return
    
    # Initialize OpenAI client
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ.get("OPENROUTER_API_KEY")
    )

    # Load the system prompt from file
    system_prompt = ""
    with open(os.path.join(ROOT_DIR, "input_data/system_prompt.txt"), "r", encoding="utf-8") as f:
        system_prompt = f.read()

    # Check if the system prompt is empty
    if not system_prompt:
        print("System prompt is empty. Please check the system_prompt.txt file.")
        return
    
    # Load the CSV file to a dataframe
    df = pd.read_csv(input_csv_path)

    # Check if the required column exists
    if "raw_asr_text" not in df.columns:
        print("The CSV file must contain a 'raw_asr_text' column.")
        return

    # Ensure the 'gpt_fixed_text' column exists, if not create it
    if 'gpt_fixed_text' not in df.columns:
        df['gpt_fixed_text'] = ""

    # Set up prompts for each row
    for idx, row in df.iterrows():
        user_prompt = row['raw_asr_text']
        # Skip rows with empty 'raw_asr_text'
        if pd.isna(user_prompt) or user_prompt.strip() == "":
            print(f"Skipping row {idx} due to empty 'raw_asr_text'.")
            continue

        # Create the completion request
        completion = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )

        response = completion.choices[0].message.content

        # Write the response back to the dataframe
        df.at[idx, 'gpt_fixed_text'] = response
        print(f"Processed row {idx}: {response[:10]}...")

    # Save the updated CSV
    df.to_csv(output_csv_path, index=False)

if __name__ == "__main__":
    load_dotenv()
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    main()
