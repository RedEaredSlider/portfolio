import csv
import requests

def find_zip_code(street_address, city, state):
    address_query = f"{street_address}, {city}, {state}"
    response = requests.get(
        "https://nominatim.openstreetmap.org/search",
        params={"q": address_query, "format": "json", "limit": 1}
    )

    if response.status_code == 200:
        data = response.json()
        if data and isinstance(data, list) and "address" in data[0]:
            return data[0]["address"].get("postcode")
    else:
        print(f"Failed to retrieve zip code for {address_query}: {response.status_code}")
    
    return None

def process_csv(input_path, output_path):
    with open(input_path, mode='r', newline='') as input_file:
        reader = csv.DictReader(input_file)
        fieldnames = reader.fieldnames + ['ZipCode']
        
        with open(output_path, mode='w', newline='') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()

            total_rows = sum(1 for row in reader)
            input_file.seek(0)  # Reset file pointer
            next(reader)  # Skip header row
            
            for idx, row in enumerate(reader, 1):
                street_address = row['StreetAddress']
                city = row['City']
                state = row['State']
                
                zip_code = find_zip_code(street_address, city, state)
                
                row['ZipCode'] = zip_code if zip_code else 'Not Found'
                writer.writerow(row)

                # Calculate and display progress
                progress = idx / total_rows * 100
                print(f"Progress: {progress:.2f}%", end='\r')

    print("\nCSV file processed successfully.")

def main():
    input_file_path = r'C:\xxxxxx'
    output_file_path = r'C:\xxxxxxxx'
    process_csv(input_file_path, output_file_path)

if __name__ == "__main__":
    main()


    
