# Python Script for Automated Data Download and Report Generation

This Python script of logging into a specific web application, downloading data, and generating reports by interacting with an API. It leverages Selenium for web automation, Requests for HTTP requests, and handles timezone conversions for accurate reporting times. Additionally, it utilizes environment variables for secure credential management.

## Video Preview

[![Video Preview](https://github.com/DevRex-0201/Project-Images/blob/main/video%20preview/Py-ReportGenerator-AutoDownload.png)](https://brand-car.s3.eu-north-1.amazonaws.com/Four+Seasons/Py-ReportGenerator-AutoDownload.mp4)

## Features

- **Web Automation**: Logs into `https://app.textel.net/login` using credentials stored in environment variables and navigates through the site to initiate a data download.
- **API Interaction**: Authenticates with an API to obtain an access token and uses it to request the creation of a detailed report based on a specific time range.
- **Timezone Handling**: Converts local times to UTC to align with API requirements for report generation.
- **Secure Credential Management**: Utilizes dotenv for environment variable management, enhancing security by avoiding hard-coded credentials.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your system.
- Pip for installing Python packages.

## Dependencies

The script requires the following Python libraries:

- `requests`: For making HTTP requests.
- `selenium`: For automating web browser interaction.
- `webdriver_manager`: For managing the web driver instance.
- `python-dotenv`: For loading environment variables from a `.env` file.
- `pytz`: For timezone conversions.
- `json`: For JSON parsing.
- `time`: For handling sleep/wait times.

## Setup Instructions

1. **Clone the Repository**
   Clone this repository to your local machine using `git clone`, followed by the repository URL.

2. **Install Dependencies**
   Install the necessary Python packages by running the following command in your terminal:
   ```
   pip install requests selenium webdriver_manager python-dotenv pytz
   ```

3. **Environment Variables**
   Create a `.env` file in the root directory of the project. Add the following environment variables:
   ```
   USER_NAME=your_username
   USER_PASS=your_password
   ```
   Replace `your_username` and `your_password` with your actual login credentials for the web application.

4. **WebDriver**
   The script uses ChromeDriver for Selenium. Ensure Chrome is installed on your system. The `webdriver_manager` takes care of the driver setup.

## Usage

To run the script, navigate to the project directory in your terminal and execute:

```
python script_name.py
```

Replace `script_name.py` with the actual name of the Python script.

## Important Considerations

- The script currently targets specific element IDs and classes for the `https://app.textel.net` domain. These identifiers may change, requiring updates to the script.
- The script uses hardcoded email and password in the `authenticate_and_get_token` function for demonstration purposes. Consider using environment variables for these credentials as well.
- Make sure your system's firewall or antivirus does not block the script or the WebDriver from running.
- The script does not handle all possible exceptions and errors. Implement additional error handling as needed for robustness.
