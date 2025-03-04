import streamlit as st

# Custom CSS for modern UI and Font Awesome icons
st.markdown(
    """
    <style>
    /* General styling */
    body {
        font-family: 'Arial', sans-serif;
        background-color: #ecf0f1;
    }

    /* Title styling */
    .title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #fffff;
        margin-bottom: 1rem;
    }

    /* Welcome message styling */
    .welcome {
        font-size: 1.2rem;
        color: #34495e;
        margin-bottom: 2rem;
    }

    /* Divider styling */
    .divider {
        border-top: 2px solid #3498db;
        margin: 2rem 0;
    }

    /* Feature card styling */
    .feature-card {
        background: rgba(255, 255, 255, 0.8); /* Semi-transparent background */
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }

    .feature-card h3 {
        font-size: 1.5rem;
        color: #2980b9;
        margin-bottom: 1rem;
    }

    .feature-card p {
        font-size: 1rem;
        color: #34495e;
    }

    /* Icon styling */
    .icon {
        font-size: 2rem;
        color: #3498db;
        margin-bottom: 1rem;
    }

    /* Button styling */
    .stButton button {
        background-color: #3498db;
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: bold;
        transition: background-color 0.3s ease;
    }

    .stButton button:hover {
        background-color: #2980b9;
    }
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    """,
    unsafe_allow_html=True,
)

# Page title
st.markdown('<div class="title">🏠 Home</div>', unsafe_allow_html=True)

# Welcome message
st.markdown(
    """
    <div class="welcome">
        <h2>Welcome to the Automated Cheque Processing System!</h2>
        <p>
            This system allows you to:
            <ul>
                <li><strong>Upload and process cheques</strong> for automated extraction of details.</li>
                <li><strong>View processed cheque data</strong> in the Dashboard.</li>
                <li><strong>Analyze cheque processing performance</strong> in the Analytics section.</li>
            </ul>
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Add a stylish divider
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Features section
st.markdown('<div class="title">✨ Features</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="feature-card">
            <div class="icon"><i class="fas fa-file-invoice"></i></div>
            <h3>Cheque Processing</h3>
            <p>
                - Upload cheque PDFs.<br>
                - Automatically detect and extract cheque details.<br>
                - Save extracted data to the database.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="feature-card">
            <div class="icon"><i class="fas fa-tachometer-alt"></i></div>
            <h3>Dashboard</h3>
            <p>
                - View all processed cheque data.<br>
                - Filter and search through extracted details.<br>
                - Export data for further analysis.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="feature-card">
            <div class="icon"><i class="fas fa-chart-line"></i></div>
            <h3>Analytics</h3>
            <p>
                - Track processing success rates.<br>
                - Analyze trends in cheque processing.<br>
                - Visualize data with interactive charts.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Add a call-to-action button
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="title">Ready to get started?</div>', unsafe_allow_html=True)

if st.button("Go to Cheque Processing"):
    st.switch_page("pages/3_🧾_Cheque_Processing.py")