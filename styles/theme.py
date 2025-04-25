# Otto Dörner brand colors
OTTO_DORNER_BLUE = "#003366"  # Dark blue from Otto Dörner website
OTTO_DORNER_ORANGE = "#FF9900"  # Orange accent color

# CSS styles
STYLES = """
    <style>
        .stApp {
            background-color: var(--background-color);
        }

        /* Otto Dörner brand colors */
        :root {
            --primary-color: #003366;
            --secondary-color: #FF9900;
            --background-color: #003366;
            --text-color: #FFFFFF;
        }

        /* General text color settings */
        .stMarkdown, p, h1, h2, h3, h4, h5, h6 {
            color: var(--text-color) !important;
        }

        /* Make all text white by default, EXCEPT inside dropdown menu */
        .stMarkdown, p, span, div:not([data-baseweb="menu"]) {
            color: var(--text-color) !important;
        }

        /* Style metric values and labels */
        .stMetric, .stMetricLabel {
            color: var(--text-color) !important;
        }

        /* Button styling */
        .stButton>button {
            background-color: var(--secondary-color);
            color: white;
        }

        /* Sidebar background */
        .css-1d391kg {
            background-color: rgba(255, 255, 255, 0.1);
        }

        /* Main title */
        .main-title {
            color: var(--text-color);
            font-family: 'Arial', sans-serif;
            font-weight: bold;
            font-size: 32px;
            margin-bottom: 20px;
        }

        /* Subtitle */
        .subtitle {
            color: var(--text-color);
            font-family: 'Arial', sans-serif;
            font-weight: bold;
            font-size: 24px;
            margin-bottom: 15px;
        }

        /* Metric container */
        .metric-container {
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            border-left: 5px solid var(--secondary-color);
            color: var(--text-color);
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2px;
        }

        .stTabs [data-baseweb="tab"] {
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 4px 4px 0px 0px;
            padding: 10px 20px;
            color: var(--text-color);
        }

        .stTabs [aria-selected="true"] {
            background-color: var(--secondary-color);
            color: var(--background-color);
        }

        /* Chart container */
        .chart-container {
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            margin-bottom: 20px;
            color: var(--text-color);
        }

        /* Footer */
        .footer {
            text-align: center;
            padding: 20px;
            color: var(--text-color);
            font-size: 14px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            margin-top: 30px;
        }

        /* Logo container */
        .logo-container {
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
        }

        /* ===== Selectbox (dropdown) styling ===== */

        /* Target the entire selectbox component */
        .stSelectbox {
            color: white !important;
        }

        /* Dark background for the selectbox with better contrast */
        div[data-baseweb="select"] {
            background-color: #1a1a1a !important;
            border-radius: 5px;
            padding: 5px !important;
            border: 1px solid #444 !important;
        }

        /* Fix for the selected option container */
        div[data-baseweb="select"] div[data-testid="stSelectbox"] {
            background-color: #1a1a1a !important;
        }

        /* Selected text inside selectbox with good contrast */
        div[data-baseweb="select"] span {
            color: white !important;
            font-weight: 500 !important;
        }

        /* Style the input part of the selectbox */
        div[data-baseweb="select"] div[data-baseweb="input"] {
            background-color: #1a1a1a !important;
        }

        /* Inner container of the selectbox */
        div[data-baseweb="select"] div {
            background-color: #1a1a1a !important;
            color: white !important;
        }

        /* Target specific Streamlit selectbox elements */
        .css-1qg05tj, .css-m1tyzr, .css-1s2u09g, .e1q3nk1v2 {
            background-color: #1a1a1a !important;
            color: white !important;
        }

        /* Target any input elements inside selectbox */
        div[data-baseweb="select"] input {
            background-color: #1a1a1a !important;
            color: white !important;
        }

        /* Dropdown menu background */
        div[data-baseweb="menu"] {
            background-color: #1a1a1a !important;
        }

        /* Ensure the menu has a solid background */
        div[data-baseweb="menu"],
        div[data-baseweb="popover"],
        div[data-baseweb="popover"] div,
        div[data-baseweb="popover"] ul,
        div[data-baseweb="menu"] div,
        div[data-baseweb="menu"] ul {
            background-color: #1a1a1a !important;
            border: 1px solid #444 !important;
        }

        /* Text color for dropdown options with good contrast */
        div[data-baseweb="menu"] div[role="option"] {
            color: white !important;
            font-weight: 400 !important;
        }

        /* Make active/selected option more visible */
        div[data-baseweb="menu"] div[aria-selected="true"] {
            background-color: #333 !important;
            color: var(--secondary-color) !important;
            font-weight: 500 !important;
        }

        /* Hover effect for dropdown options with better visibility */
        div[data-baseweb="menu"] div[role="option"]:hover {
            background-color: #333 !important;
            color: var(--secondary-color) !important;
        }

        /* Make select arrow more visible */
        div[data-baseweb="select"] svg {
            color: var(--secondary-color) !important;
        }

        /* Fix for any popover elements */
        [data-baseweb="popover"] {
            background-color: #1a1a1a !important;
            border: 1px solid #444 !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5) !important;
        }

        /* Force solid background on any nested elements */
        [data-baseweb="popover"] * {
            background-color: #1a1a1a !important;
        }

        /* Ensure all option text is visible */
        [role="option"] {
            color: white !important;
            background-color: #1a1a1a !important;
        }
    </style>
"""
