import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Automated Cheque Processing",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main title
st.title("Automated Cheque Processing System")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "📊 Dashboard", "🧾 Cheque Processing", "📈 Analytics"])

# Redirect to the selected page
if page == "🏠 Home":
    st.switch_page("pages/1_🏠_Home.py")
elif page == "📊 Dashboard":
    st.switch_page("pages/2_📊_Dashboard.py")
elif page == "🧾 Cheque Processing":
    st.switch_page("pages/3_🧾_Cheque_Processing.py")
elif page == "📈 Analytics":
    st.switch_page("pages/4_📈_Analytics.py")