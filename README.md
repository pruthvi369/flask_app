
# Flask CSV API

## Overview

This Flask application provides a RESTful API for handling CSV file uploads, processing data, and retrieving statistics. It includes endpoints for uploading CSV files, calculating summary statistics, and querying the data. Basic authentication using an API key is implemented to secure the endpoints.

## Features

- **Upload CSV**: Allows users to upload CSV files and store their contents in an in-memory SQLite database.
- **Retrieve Statistics**: Provides summary statistics (e.g., mean, median) for numerical columns in the uploaded data.
- **Query Data**: Enables users to filter the data based on specific column values.
- **Basic Authentication**: Secures the endpoints using an API key.

## Getting Started

### Prerequisites

Ensure you have Python and pip installed. You will also need to install the following Python packages:

- Flask
- Pandas

### Installation

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Dependencies**

   ```bash
   pip install flask pandas
   ```

3. **Set Up Environment Variables**

   You can set the API key as an environment variable or directly in the code.

   - **Set API Key via Environment Variable**:
     - **Linux/Mac**:
       ```bash
       export API_KEY="your_custom_api_key"
       ```
     - **Windows**:
       ```bash
       set API_KEY=your_custom_api_key
       ```
     Replace `"your_custom_api_key"` with your desired API key.

   - **Set API Key in Code**:
     Open `app.py` and modify the line:
     ```python
     API_KEY = "your_custom_api_key"
     ```

### Running the Application

Run the Flask application using:

```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000`.

## API Endpoints

### 1. Upload CSV

- **URL**: `/upload`
- **Method**: `POST`
- **Headers**:
  - `API-Key`: Your API key
- **Body**: Form-data
  - Key: `file` (type: File)
- **Description**: Uploads a CSV file and stores its contents in an in-memory SQLite database.
- **Responses**:
  - `200 OK`: File uploaded successfully.
  - `400 Bad Request`: No file part or invalid file format.
  - `401 Unauthorized`: Invalid API key.
  - `500 Internal Server Error`: Failed to process file.

### 2. Retrieve Statistics

- **URL**: `/statistics`
- **Method**: `GET`
- **Headers**:
  - `API-Key`: Your API key
- **Description**: Retrieves summary statistics (e.g., mean, median) for numerical columns in the uploaded data.
- **Responses**:
  - `200 OK`: Summary statistics returned.
  - `401 Unauthorized`: Invalid API key.
  - `500 Internal Server Error`: Failed to retrieve statistics.

### 3. Query Data

- **URL**: `/query`
- **Method**: `GET`
- **Parameters**:
  - `column`: The name of the column to filter by.
  - `value`: The value to filter on.
- **Headers**:
  - `API-Key`: Your API key
- **Description**: Queries the data based on a specific column value and returns the filtered results.
- **Responses**:
  - `200 OK`: Filtered data returned.
  - `400 Bad Request`: Missing column or value parameters.
  - `401 Unauthorized`: Invalid API key.
  - `500 Internal Server Error`: Failed to query data.

## Example Requests

### Upload CSV

- **cURL**:
  ```bash
  curl -X POST http://127.0.0.1:5000/upload   -H "API-Key: your_custom_api_key"   -F "file=@path/to/your/file.csv"
  ```

### Retrieve Statistics

- **cURL**:
  ```bash
  curl -X GET http://127.0.0.1:5000/statistics   -H "API-Key: your_custom_api_key"
  ```

### Query Data

- **cURL**:
  ```bash
  curl -X GET "http://127.0.0.1:5000/query?column=<column_name>&value=<value>"   -H "API-Key: your_custom_api_key"
  ```

## Troubleshooting

- **Ensure API Key is Set**: Verify that the `API_KEY` environment variable is correctly set or that the key is hardcoded in the `app.py` file.
- **Check File Format**: Only CSV files are accepted. Ensure the file is correctly formatted.
- **Database Errors**: The application uses an in-memory SQLite database; ensure there are no issues with the database setup.


