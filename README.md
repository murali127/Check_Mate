# Automated Cheque Processing System

This project is an **Automated Cheque Processing System** that allows users to upload cheque images or PDFs, extract relevant details using OCR, and save the processed data to a MongoDB database. The system also includes a dashboard and analytics for visualizing the processed data.

---

## Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Setup Instructions](#setup-instructions)
   - [Clone the Repository](#clone-the-repository)
   - [Create a Virtual Environment](#create-a-virtual-environment)
   - [Install Dependencies](#install-dependencies)
   - [Set Up Environment Variables](#set-up-environment-variables)
   - [Set Up MongoDB](#set-up-mongodb)
   - [Run the Application](#run-the-application)
4. [Project Structure](#project-structure)
5. [Contributing](#contributing)
6. [License](#license)

---

## Features

- **Cheque Processing**: Upload cheque images or PDFs and extract details like cheque number, account number, amount, payee, and bank.
- **Dashboard**: View all processed cheque data with filtering and search options.
- **Analytics**: Analyze cheque processing performance with interactive charts.
- **Database Integration**: Save extracted data to a MongoDB database.

---

## Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.8 or higher
- MongoDB (local or cloud-based)
- Tesseract OCR (for text extraction)
- Git (for cloning the repository)

---

## Setup Instructions

### Clone the Repository

1. Open a terminal or command prompt.
2. Run the following command to clone the repository:

   ```bash
   git clone https://github.com/your-username/cheque_validation_project.git
   cd cheque_validation_project
   ```

---

### Create a Virtual Environment

1. Create a virtual environment to isolate the project dependencies:

   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

---

### Install Dependencies

1. Install the required Python packages using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

---

### Set Up Environment Variables

1. Create a `.env` file in the root directory of the project and add the following environment variables:

   ```plaintext
   MONGO_URI=<your-mongodb-connection-string>
   GEMINI_API_KEY=<your-gemini-api-key>
   ```

   Replace `<your-mongodb-connection-string>` with your MongoDB connection string and `<your-gemini-api-key>` with your Gemini API key.

2. Create a `secrets.toml` file inside the `.streamlit` directory (create the directory if it doesn't exist) and add the following:

   ```toml
    MONGO_URI="<your-mongodb-connection-string>"
   ```

   Replace `<your-mongodb-connection-string>` with your MongoDB connection string.

---

### Set Up MongoDB

1. Set up a MongoDB database (local or cloud-based).
2. Ensure the database is accessible using the connection string provided in the `.env` and `secrets.toml` files.

---

### Run the Application

1. Start the Streamlit application by running the following command:

   ```bash
   streamlit run main.py
   ```

2. Open your browser and navigate to `http://localhost:8501` to view the application.

---

## Project Structure

```
cheque_validation_project/
├── .gitignore
├── .streamlit/
│   └── secrets.toml
├── .env
├── pages/
│   ├── 1_🏠_Home.py
│   ├── 2_📊_Dashboard.py
│   ├── 3_🧾_Cheque_Processing.py
│   └── 4_📈_Analytics.py
├── utils.py
├── requirements.txt
├── README.md
└── main.py
```

---

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeatureName`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeatureName`).
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [Streamlit](https://streamlit.io/) for the web framework.
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) for text extraction.
- [MongoDB](https://www.mongodb.com/) for database integration.

