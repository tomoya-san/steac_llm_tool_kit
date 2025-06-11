import os
import json
import sys
import pandas as pd

from openai import OpenAI
from dotenv import load_dotenv

def main():
    # Check if the script is run with the correct number of arguments
    if len(sys.argv) != 2:
        print("Usage: python main.py <output_csv_file_name")
        return
    
    # Check if the input CSV file exists and is valid
    output_csv_path = os.path.join(ROOT_DIR, "out", sys.argv[1])
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
    
    rows = []

    # Process each script file in the raw_scripts directory
    raw_scripts_dir = os.path.join(ROOT_DIR, "input_data/raw_scripts")
    for filename in os.listdir(raw_scripts_dir):
        file_path = os.path.join(raw_scripts_dir, filename)
        if filename.endswith(".txt"):
            # Read the user prompt from the file
            user_prompt = ""
            with open(file_path, "r", encoding="utf-8") as f:
                user_prompt = f.read()
            
            # Skip files with empty content
            if not user_prompt:
                print(f"User prompt is empty. Please check the {filename} file.")
                return
            
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

            response = completion.choices[0].message.content # Response is supposed to be a JSON string
            response = json.loads(response)

            # Iterate through the sections in the response and add them to the rows
            question_count = 0
            for question in response:
                question = {
                    "filename": filename,
                    **question
                }
                rows.append(question)
                question_count += 1
            
            print(f"Processed {question_count} questions from {filename} successfully.")
    
    # Create a DataFrame and save it to CSV
    df = pd.DataFrame(rows)
    df.to_csv(output_csv_path, index=False)

if __name__ == "__main__":
    load_dotenv()
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    main()
