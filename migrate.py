import os
import json
import zipfile
import gzip
import requests
import argparse

# Configuration
parser = argparse.ArgumentParser(description="Migrate Amplitude Analytics Data")
parser.add_argument("--api-key", required=True, help="Amplitude API Key")
parser.add_argument("--zip-file", required=True, help="Path to the export.zip file")
args = parser.parse_args()

API_KEY = args.api_key
ZIP_FILE_PATH = args.zip_file
PRIMARY_ENDPOINT = os.getenv("AMPLITUDE_ENDPOINT", "https://api2.amplitude.com/2/httpapi")
SECONDARY_ENDPOINT = "https://api.eu.amplitude.com/2/httpapi"
EXTRACTED_FOLDER = os.getenv("EXTRACTED_FOLDER", "extracted_events")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 100))  # Amplitude recommends sending 10-1000 events per request

# Step 1: Extract the ZIP file
def extract_zip(zip_path, extract_to):
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Extracted files to {extract_to}")

# Step 2: Read and format JSON & JSON.GZ files line by line
def load_events_from_folder(folder):
    events = []
    for root, _, files in os.walk(folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if file_name.endswith(".json") or file_name.endswith(".json.gz"):
                open_func = gzip.open if file_name.endswith(".json.gz") else open
                mode = "rt" if file_name.endswith(".json.gz") else "r"

                with open_func(file_path, mode, encoding="utf-8") as file:
                    for line in file:
                        line = line.strip("\ufeff")  # Remove BOM marker if present
                        try:
                            data = json.loads(line)
                            events.append(data)
                        except json.JSONDecodeError as e:
                            print(f"Skipping invalid JSON line in {file_name}: {e}")
    return events

# Step 3: Send data to Amplitude
def send_events(events):
    payload = {"api_key": API_KEY, "events": events}
    response = requests.post(PRIMARY_ENDPOINT, json=payload)
    if response.status_code == 200:
        print(f"Successfully sent {len(events)} events to primary endpoint.")
    else:
        print(f"Failed to send events to primary endpoint. Response: {response.text}")
        print(f"Trying secondary endpoint.")
        response = requests.post(SECONDARY_ENDPOINT, json=payload)
        if response.status_code == 200:
            print(f"Successfully sent {len(events)} events to secondary endpoint.")
        else:
            print(f"Failed to send events to secondary endpoint. Response: {response.text}")

# Main execution
if __name__ == "__main__":
    extract_zip(ZIP_FILE_PATH, EXTRACTED_FOLDER)
    all_events = load_events_from_folder(EXTRACTED_FOLDER)

    print(f"Total events loaded: {len(all_events)}")

    # Send events in batches
    for i in range(0, len(all_events), BATCH_SIZE):
        send_events(all_events[i:i + BATCH_SIZE])

    print("Data import completed!")
