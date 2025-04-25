import streamlit as st
import requests
from io import BytesIO
from PIL import Image
from styles.theme import STYLES

def load_logo():
    """Load Otto Dörner logo from local file"""
    try:
        # Load logo from local file
        return Image.open("data/otto_dorner_logo.webp")
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
        col1, col2, col3 = st.columns([1, 1 , 1])
        with col2:
            st.image(logo, width=250)  # Centered in middle column
    else:
        # Fallback to text logo if image can't be loaded
        st.markdown('<div class="main-title">Otto Dörner Data Analysis</div>', unsafe_allow_html=True)
            
    # Add a divider after the logo
    st.markdown('<hr style="height:3px;border:none;color:#FF9900;background-color:#FF9900;margin-bottom:30px;" />', unsafe_allow_html=True)

def display_footer():
    """Display the footer"""
    st.markdown(
        '<div class="footer">© 2025 Otto Dörner</div>',
        unsafe_allow_html=True
    ) 