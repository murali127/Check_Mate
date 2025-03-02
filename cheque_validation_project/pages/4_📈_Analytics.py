# pages/4_📈_Analytics.py
import streamlit as st
from pymongo import MongoClient
import pandas as pd
import altair as alt

# Page title
st.title("📈 Analytics")

# Connect to MongoDB
def get_db_connection():
    client = MongoClient(st.secrets["MONGO_URI"])
    db = client["cheque_processing_db"]
    return db["cheque_details"]

# Fetch data from MongoDB
def fetch_cheque_data():
    collection = get_db_connection()
    data = list(collection.find({}, {"_id": 0}))  # Exclude the _id field
    return pd.DataFrame(data)

# Display analytics
st.header("Cheque Processing Statistics")
data = fetch_cheque_data()

# Debug: Print columns to verify field names

if not data.empty:
    # Check if 'amount in numbers' exists in the data
    if "amount in numbers" in data.columns:
        total_cheques = len(data)
        successful_cheques = len(data[data["amount in numbers"].notnull()])
        unsuccessful_cheques = total_cheques - successful_cheques

        # Calculate success rate
        success_rate = (successful_cheques / total_cheques) * 100 if total_cheques > 0 else 0

        # Display metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Cheques Processed", total_cheques)
        col2.metric("Successful Cheques", successful_cheques)
        col3.metric("Unsuccessful Cheques", unsuccessful_cheques)

        # Display success rate
        st.subheader("Cheque Processing Success Rate")
        st.metric("Success Rate", f"{success_rate:.2f}%")

        # Visualization: Success Rate Over Time
        st.subheader("Success Rate Over Time")
        if "timestamp" in data.columns and "amount in numbers" in data.columns:
            # Convert timestamp to datetime
            data["timestamp"] = pd.to_datetime(data["timestamp"])

            # Calculate success rate over time
            data["success"] = data["amount in numbers"].notnull().astype(int)
            success_over_time = data.groupby(data["timestamp"].dt.date)["success"].mean() * 100

            # Create a DataFrame for the chart
            success_df = pd.DataFrame({
                "Date": success_over_time.index,
                "Success Rate": success_over_time.values
            })

            # Create Altair chart
            chart = alt.Chart(success_df).mark_line().encode(
                x="Date:T",
                y="Success Rate:Q",
                tooltip=["Date", "Success Rate"]
            ).properties(
                width=700,
                height=400,
                title="Success Rate Over Time"
            )
            st.altair_chart(chart)
        else:
            st.warning("No timestamp or amount data available for visualization.")

        # Visualization: Cheque Distribution by Bank
        st.subheader("Cheque Distribution by Bank")
        if "bank" in data.columns:
            bank_distribution = data["bank"].value_counts().reset_index()
            bank_distribution.columns = ["Bank", "Count"]

            # Create Altair chart
            bank_chart = alt.Chart(bank_distribution).mark_bar().encode(
                x="Bank:N",
                y="Count:Q",
                tooltip=["Bank", "Count"]
            ).properties(
                width=700,
                height=400,
                title="Cheque Distribution by Bank"
            )
            st.altair_chart(bank_chart)
        else:
            st.warning("No bank data available for visualization.")
    else:
        st.warning("The 'amount in numbers' field is missing in the data.")
else:
    st.warning("No cheque data found in the database.")