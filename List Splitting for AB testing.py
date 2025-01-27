import os
import pandas as pd

def process_csv_files(input_folder_path):
    # Iterate through all files in the specified folder
    for filename in os.listdir(input_folder_path):
        if filename.endswith('.csv'):
            # Construct the full file path
            file_path = os.path.join(input_folder_path, filename)
            
            # Read the CSV file into a DataFrame
            df = pd.read_csv(file_path)
            
            # Add a record ID column
            df['Record_ID'] = range(1, len(df) + 1)
            
            # Add a flag column based on the record ID range
            df['Flag'] = (df['Record_ID'] - 1) // 10000 + 1
            
            # Save the updated DataFrame back to the file (or a new file if needed)
            output_file_path = os.path.join(input_folder_path, f"processed_{filename}")
            df.to_csv(output_file_path, index=False)
            
            print(f'Processed {filename} and saved as {output_file_path}')

# Example usage
input_folder_path = r'C:\Path\To\Input_Folder'
process_csv_files(input_folder_path)
