import streamlit as st
import requests
from io import BytesIO
from PIL import Image
from styles.theme import STYLES

def load_logo():
    """Load Otto Dörner logo"""
    # URL of the Otto Dörner logo
    logo_url = "https://www.doerner.de/wp-content/uploads/2021/03/otto-doerner-logo.svg"
    try:
        response = requests.get(logo_url)
        if response.status_code == 200:
            # Convert SVG to PNG using PIL
            from cairosvg import svg2png
            png_data = svg2png(bytestring=response.content)
            return Image.open(BytesIO(png_data))
        else:
            # Fallback to a text logo if image can't be loaded
            return None
    except Exception as e:
        st.warning(f"Could not load logo: {str(e)}")
        return None

def load_css():
    """Load custom CSS for Otto Dörner branding"""
    st.markdown(STYLES, unsafe_allow_html=True)

def display_header():
    """Display the header with logo and title"""
    # Display Otto Dörner logo
    logo = load_logo()
    if logo:
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        st.image(logo, width=300)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Fallback to text logo if image can't be loaded
        # st.markdown('<div class="main-title">Otto Dörner Data Analysis</div>', unsafe_allow_html=True)
        pass    
    # st.markdown('<div class="subtitle">Waste Management & Resource Planning</div>', unsafe_allow_html=True)

def display_footer():
    """Display the footer"""
    st.markdown(
        '<div class="footer">© 2024 Otto Dörner Data Analysis Dashboard</div>',
        unsafe_allow_html=True
    ) 