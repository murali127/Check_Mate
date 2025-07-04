import streamlit as st
from pymongo import MongoClient
import pandas as pd
import json

# Page title
st.title("📊 Dashboard")

# Connect to MongoDB
def get_db_connection():
    client = MongoClient(st.secrets["MONGO_URI"])  # Access MongoDB URI from secrets.toml
    db = client["cheque_processing_db"]
    return db["cheque_details"]

# Fetch data from MongoDB
def fetch_cheque_data():
    collection = get_db_connection()
    data = list(collection.find({}, {"_id": 0}))  # Exclude the _id field
    return pd.DataFrame(data)

# Display data
st.header("Processed Cheque Data")
data = fetch_cheque_data()

if not data.empty:
    # Add filters and search in the sidebar
    st.sidebar.header("Filters")

    # Filter by Bank
    bank_filter = st.sidebar.selectbox("Filter by Bank", ["All"] + list(data["bank"].unique()))

    # Search by Cheque Number, Account Number, or Payee
    search_query = st.sidebar.text_input("Search by Cheque Number, Account Number, or Payee")

    # Apply filters
    if bank_filter != "All":
        data = data[data["bank"] == bank_filter]

    if search_query:
        # Filter data based on search query
        data = data[
            data["chequeNumber"].astype(str).str.contains(search_query, case=False) |
            data["accountNumber"].astype(str).str.contains(search_query, case=False) |
            data["payee"].astype(str).str.contains(search_query, case=False)
        ]

    # Reset index to start from 1 instead of 0
    data.reset_index(drop=True, inplace=True)
    data.index = data.index + 1

    # Display filtered data
    st.write(f"Showing {len(data)} records:")

    # Make the table extendible in all directions
    st.dataframe(
        data,
        height=400,  # Set a fixed height for vertical scrolling
        width=1000,  # Set a fixed width for horizontal scrolling
        use_container_width=True,  # Make the table responsive to the container width
    )

    # Add download buttons for filtered data
    col1, col2 = st.columns(2)

    # Download as CSV
    csv = data.to_csv(index=False).encode("utf-8")
    col1.download_button(
        label="Download Filtered Data as CSV",
        data=csv,
        file_name="filtered_cheque_data.csv",
        mime="text/csv",
    )

    # Download as JSON
    json_data = data.to_json(orient="records", indent=4)
    col2.download_button(
        label="Download Filtered Data as JSON",
        data=json_data,
        file_name="filtered_cheque_data.json",
        mime="application/json",
    )
else:
    st.warning("No cheque data found in the database.")