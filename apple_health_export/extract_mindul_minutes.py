import xml.etree.ElementTree as ET
import pandas as pd

# List of XML export files that contain activities
files = [
    "apple_health_export/export_cda.xml",
    "apple_health_export/export.xml",
    "apple_health_export-2/export_cda.xml",
    "apple_health_export-2/export.xml"
]

mindful_entries = []

for file in files:
    print(f"Processing file: {file}")
    try:
        tree = ET.parse(file)
        root = tree.getroot()
    except Exception as e:
        print(f"Error parsing file {file}: {e}")
        continue

    # If this is a CDA export, use namespace handling
    if "export_cda.xml" in file:
        # Define namespace mapping (adjust if needed)
        namespaces = {
            'cda': 'urn:hl7-org:v3'
        }
        # Look for all <cda:observation> elements
        for observation in root.findall('.//cda:observation', namespaces):
            code_el = observation.find('cda:code', namespaces)
            if code_el is not None:
                display_name = code_el.get('displayName', '')
                if 'mindful' in display_name.lower() or 'mindfulness' in display_name.lower():
                    entry = {
                        "file": file,
                        "source": "export_cda.xml",
                        "displayName": display_name,
                        "details": ET.tostring(observation, encoding='unicode', method='xml')
                    }
                    mindful_entries.append(entry)
    else:
        # For the plain export.xml, assume records are stored in <Record> elements.
        for record in root.findall('Record'):
            type_attr = record.get('type', '')
            if 'mindful' in type_attr.lower() or 'mindfulness' in type_attr.lower():
                entry = {
                    "file": file,
                    "source": "export.xml",
                    "type": type_attr,
                    "startDate": record.get('startDate'),
                    "endDate": record.get('endDate'),
                    "value": record.get('value'),
                    "unit": record.get('unit'),
                    "details": ET.tostring(record, encoding='unicode', method='xml')
                }
                mindful_entries.append(entry)

if mindful_entries:
    df = pd.DataFrame(mindful_entries)
    print("\nMindful Minutes records found:")
    print(df.head())

    # Save DataFrame to Parquet file with snappy compression
    df.to_parquet('mindful_minutes_data.parquet', compression='snappy')
    print("\nDataFrame saved to mindful_minutes_data.parquet")
else:
    print("No mindful minutes related records found.")