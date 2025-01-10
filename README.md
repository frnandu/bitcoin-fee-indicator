# Bitcoin Fee Indicator

## Overview
The Bitcoin Fee Indicator is a system tray application that fetches and displays the current Bitcoin transaction fee rates. It provides real-time updates on various fee rates, allowing users to make informed decisions when sending Bitcoin transactions.

## Features
- Displays the fastest, half-hour, hourly, economy, and minimum Bitcoin transaction fees.
- Updates the fee rates every 5 minutes.
- Provides a refresh option to manually update the fee rates.
- Allows the user to quit the application from the system tray.

## Supported Platforms
This application is designed to run on:
- Linux (with GTK 3 and AppIndicator support)

## Prerequisites
Before running the application, ensure you have the following installed:
- Python 3
- Required Python packages:
  - `requests`
  - `PyGObject`
  - `cairosvg`

You can install the required packages using pip:

```bash
pip install requests PyGObject cairosvg
```

## Environment Variables
You can set the `FEE_API_BASE_URL` environment variable to specify a custom API base URL for fetching fee rates. If not set, it defaults to `https://mempool.space`.

## Running the Application
1. Clone the repository or download the `indicator.py` file.
2. Open a terminal and navigate to the directory containing `indicator.py`.
3. Run the application using the following command:
   ```bash
   python3 indicator.py
   ```

4. The application will appear in your system tray, displaying the current Bitcoin fee rates.

## License
This project is licensed under the MIT License.