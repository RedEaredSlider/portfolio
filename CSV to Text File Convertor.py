import os

def csv_to_txt(folder_path, csv_filename, txt_filename):
    # Construct the full file paths
    csv_filepath = os.path.join(folder_path, csv_filename)
    txt_filepath = os.path.join(folder_path, txt_filename)
    
    # Rename the file
    os.rename(csv_filepath, txt_filepath)
    print(f"Renamed {csv_filepath} to {txt_filepath}")

# Specify the folder location and filenames
folder_path = r'C:\Path\To\Your\Folder'  # Update with your folder path
csv_filename = 'sample.csv'
txt_filename = 'sample.txt'

csv_to_txt(folder_path, csv_filename, txt_filename)
