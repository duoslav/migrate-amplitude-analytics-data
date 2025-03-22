# Migrate Amplitude Analytics Data

## Overview

`migrate.py` is a Python script designed to help you migrate your analytics data from one Amplitude organization to another.

## Features

1. Log in to your Amplitude account.
2. Navigate to the "Settings" page.
3. Under "Projects", select the project you want to export data from.
4. Find the "Export Data" section to export your data.
5. Find the "API Key" section and copy your API key.

## Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/duoslav/migrate-amplitude-analytics-data.git
cd migrate-amplitude-analytics-data
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

To run the script, use the following command:

```bash
python migrate.py --api-key YOUR_AMPLITUDE_API_KEY --zip-file PATH_TO_EXPORT.ZIP
```

### Example

```bash
python migrate.py --api-key abc123 --zip-file /path/to/export.zip
```

### CLI Arguments

- `--api-key`: Your Amplitude API key.
- `--zip-file`: The path to the export.zip file.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

If you have any questions or need further assistance, feel free to open an issue on GitHub.

