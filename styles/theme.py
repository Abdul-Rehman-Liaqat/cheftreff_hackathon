# Otto Dörner brand colors
OTTO_DORNER_BLUE = "#003366"  # Dark blue from Otto Dörner website
OTTO_DORNER_ORANGE = "#FF9900"  # Orange accent color

# CSS styles
STYLES = """
    <style>
        .stApp {
            background-color: var(--background-color);
        }
        
        /* Make text more readable on dark background */
        .stMarkdown, p, h1, h2, h3 {
            color: white !important;
        }
        
        /* Style buttons and other interactive elements */
        .stButton>button {
            background-color: var(--secondary-color);
            color: white;
        }
        
        /* Style sidebar */
        .css-1d391kg {
            background-color: rgba(255, 255, 255, 0.1);
        }
        
        /* Otto Dörner brand colors */
        :root {
            --primary-color: #003366; /* Dark blue from Otto Dörner */
            --secondary-color: #FF9900; /* Orange accent color */
            --background-color: #003366; /* Changed to Otto Dörner blue */
            --text-color: #FFFFFF; /* Changed to white for better contrast */
        }
        
        /* Main title styling */
        .main-title {
            color: var(--text-color);
            font-family: 'Arial', sans-serif;
            font-weight: bold;
            font-size: 32px;
            margin-bottom: 20px;
        }
        
        /* Subtitle styling */
        .subtitle {
            color: var(--text-color);
            font-family: 'Arial', sans-serif;
            font-weight: bold;
            font-size: 24px;
            margin-bottom: 15px;
        }
        
        /* Metric styling */
        .metric-container {
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            border-left: 5px solid var(--secondary-color);
            color: var(--text-color);
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 4px 4px 0px 0px;
            gap: 1px;
            padding: 10px 20px;
            color: var(--text-color);
        }
        
        .stTabs [aria-selected="true"] {
            background-color: var(--secondary-color);
            color: var(--background-color);
        }
        
        /* Chart container styling */
        .chart-container {
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            margin-bottom: 20px;
            color: var(--text-color);
        }
        
        /* Footer styling */
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
        
        /* Fix for text colors */
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
            color: var(--text-color) !important;
        }
        
        /* Make all text white by default */
        .stMarkdown, p, span, div {
            color: var(--text-color) !important;
        }
        
        /* Style metric values */
        .stMetric {
            color: var(--text-color) !important;
        }
        
        /* Style metric labels */
        .stMetricLabel {
            color: var(--text-color) !important;
        }
    </style>
""" 