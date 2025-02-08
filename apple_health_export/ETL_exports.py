import pandas as pd
import xml.etree.ElementTree as ET

# Parse the XML file
tree = ET.parse('apple_health_export/export_cda.xml')
print("Parsed XML file")
root = tree.getroot()

# Define namespace mapping for easier xpath queries
namespaces = {
    'cda': 'urn:hl7-org:v3',
    'sdtc': 'urn:l7-org:sdtc',
    'fhir': 'http://hl7.org/fhir/v3'
}

# Extract vital signs data
vital_signs = []
for observation in root.findall('.//cda:observation', namespaces):
    # print(observation)
    # Get the measurement type
    code = observation.find('cda:code', namespaces)
    if code is not None:
        measurement_type = code.get('displayName')
        
        # Get the text data
        text = observation.find('cda:text', namespaces)
        if text is not None:
            data = {}
            for child in text:
                data[child.tag] = child.text
            
            data['measurement_type'] = measurement_type
            vital_signs.append(data)

# Convert to DataFrame
df = pd.DataFrame(vital_signs)

# Clean column names by removing namespace prefixes
df.columns = df.columns.str.replace('{urn:hl7-org:v3}', '')

# Convert value column to numeric
df['value'] = pd.to_numeric(df['value'], errors='coerce')

print(df.head())

# Print value counts of measurement types
print("\nMeasurement Type Frequencies:")
print(df['measurement_type'].value_counts())


# Save DataFrame to Parquet file for efficient storage
df.to_parquet('vital_signs_data.parquet', compression='snappy')
print("\nDataFrame saved to vital_signs_data.parquet")

