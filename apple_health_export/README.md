# Apple Health Mindful Minutes Extractor

This repository contains a Python script that processes Apple Health export files in XML format to extract mindful minutes records. The tool handles both the CDA namespaced XML and the plain XML formats, consolidating the mindful or mindfulness records into a single Parquet file for further analysis.

## Repository Structure

- **apple_health_export/**
  - `export_cda.xml` – Apple Health export in CDA format.
  - `export.xml` – Plain XML Apple Health export.
  - Additional files (e.g., workout routes in GPX format).
- **apple_health_export-2/**
  - `export_cda.xml` – Apple Health export in CDA format.
  - `export.xml` – Plain XML Apple Health export.
  - Additional files.
- `apple_health_export/extract_mindul_minutes.py` – The Python script that extracts mindful minutes from the XML files.
- `.gitignore` – Git ignore rules (e.g., to ignore Parquet output files).

## Prerequisites

- Python 3.6 or later
- The following Python libraries:
  - **pandas**
  - **pyarrow** (for saving Parquet files)
  
You can install the dependencies using pip:
```bash
pip install pandas pyarrow
```

## How to Run

Execute the extraction script by running:

```bash
python apple_health_export/extract_mindul_minutes.py
```

When you run the script, it will:

1. Iterate through multiple Apple Health XML export files.
2. Parse either the CDA namespaced elements or the plain XML `<Record>` elements.
3. Identify and extract records whose descriptions or types include "mindful" or "mindfulness."
4. Consolidate the extracted records into a pandas DataFrame.
5. Save the data into a compressed Parquet file named `mindful_minutes_data.parquet`.

## Output

After successful execution, you will see a preview of the DataFrame in the terminal and a new file:
- **mindful_minutes_data.parquet** – Contains the extracted mindful minutes records.

## Contributing

Contributions to improve the extraction logic or add more features are welcome. Please open an issue or submit a pull request with your suggestions or improvements.

## License

This project is released under the MIT License. See the [LICENSE](LICENSE) file for details.
