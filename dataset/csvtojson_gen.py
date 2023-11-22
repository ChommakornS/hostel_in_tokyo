import csv
import json

# Replace 'hostel.csv' with CSV file name and 'hosteldataset.json' with the desired JSON output file name
csv_file = 'hostel.csv'
json_file = 'hosteldataset.json'

data = []

# Specify the encoding when opening the CSV file
with open(csv_file, 'r', encoding='utf-8') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        # Create a custom JSON structure
        json_data = {
            "hostel.name": row["hostel.name"],
            "City": row["City"],
            "price.from": row["price.from"],
            "Distance": row["Distance"],
            "summary.score": row["summary.score"],
            "rating.band": row["rating.band"],
            "atmosphere": row["atmosphere"],
            "cleanliness": row["cleanliness"],
            "facilities": row["facilities"],
            "location.y": row["location.y"],
            "security": row["security"],
            "staff": row["staff"],
            "valueformoney": row["valueformoney"],
            "lon": row["lon"],
            "lat": row["lat"],
            "hotel description": row["hotel description"],
            "Link discord": row["Link discord"]
        }
        data.append(json_data)

with open(json_file, 'w', encoding='utf-8') as jsonfile:
    for item in data:
        json.dump(item, jsonfile, ensure_ascii=False, separators=(',', ':'))
        jsonfile.write("\n")  


