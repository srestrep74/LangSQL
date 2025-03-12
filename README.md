# LangSQL

## Overview

LangSQL is a project that integrates various technologies to provide a comprehensive solution for SQL-related tasks. The project is structured into two main components:

- **Frontend**: Developed using Vue.js, the frontend offers an interactive user interface for users to interact with the application.

- **Backend**: Built with Python, the backend handles the core logic and data processing tasks.

## Features

- **Interactive SQL Editor**: Allows users to write and execute SQL queries in real-time.

- **Data Visualization**: Provides graphical representations of query results for better data analysis.

- **User Authentication**: Ensures secure access to the application with user login and registration functionalities.

## Installation

To set up the LangSQL project locally, follow these steps:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/srestrep74/LangSQL.git
    ```

2. **Navigate to the Project Directory**:
   ```bash
   cd LangSQL
   ```

3. **Navigate to the backend directory**:

     ```bash
     cd backend
     ```

4. **Create a virtual environment**:

     ```bash
     python -m venv env
     ```

5. **Activate the virtual environment**:

     - On Windows:

       ```bash
       .\env\Scripts\activate
       ```

     - On macOS/Linux:

       ```bash
       source env/bin/activate
       ```

6. **Install the required dependencies**:
     ```bash
     pip install -r requirements.txt
     ```

7. **Run the backend server**:
     ```bash
     python app.py
     ```

## Usage
Once the application is set up and running:

- Write SQL Queries: Use the interactive editor to compose your SQL queries.

- Execute Queries: Run your queries and view the results instantly.

- Visualize Data: Utilize the data visualization tools to gain insights from your query results.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.