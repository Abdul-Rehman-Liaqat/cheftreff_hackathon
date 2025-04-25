import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

from functions.ui import load_css, display_header, display_footer
from functions.charts import create_branded_chart, create_forecast_chart
from data_processor import DataProcessor
from forecaster import Forecaster

class Dashboard:
    def __init__(self):
        # Set page config with Otto Dörner branding
        st.set_page_config(
            # page_title="Otto Dörner Data Analysis",
            page_icon="🚛",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Apply the most aggressive fix for selectbox contrast issues
        # This needs to be done before loading the main CSS
        st.markdown("""
        <style>
        /* Override light backgrounds with dark ones and ensure white text */
        .stSelectbox, 
        .stMultiSelect {
            color: white !important;
        }
        
        /* This is the core fix for the white-on-white issue */
        .stSelectbox [data-baseweb="select"],
        .stSelectbox [data-baseweb="select"] *,
        .stSelectbox [data-baseweb="input"],
        .stSelectbox [data-baseweb="value-container"],
        .stSelectbox [role="combobox"],
        .stSelectbox [role="presentation"],
        .stMultiSelect [data-baseweb="select"],
        .stMultiSelect [data-baseweb="input"],
        .stMultiSelect [data-baseweb="value-container"] {
            background-color: rgba(26, 26, 26, 1) !important;
            color: white !important;
        }
        
        /* Apply to any element that might be causing issues */
        [data-baseweb="select"] [data-baseweb="value-container"] div {
            background-color: rgba(26, 26, 26, 1) !important;
            color: white !important;
        }

        /* Target every possible class that could be causing the white background */
        [class*="css-"], 
        [class*="st-"], 
        [data-testid*="stSelectbox"] {
            background-color: inherit;
        }
        
        /* Direct fix for the white-on-white issue in the dropdown */
        [data-baseweb="select"] [data-baseweb="value-container"] > div,
        [data-baseweb="select"] div:first-child {
            background-color: rgba(26, 26, 26, 1) !important;
            color: white !important;
        }

        /* Critical fix for dropdown menu with solid background */
        div[data-baseweb="menu"] {
            background-color: #1a1a1a !important;
            border: 1px solid #444 !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5) !important;
        }
        
        /* Ensure dropdown options have proper styling */
        div[data-baseweb="menu"] div[role="option"] {
            background-color: #1a1a1a !important;
            color: white !important;
        }

        /* Style for hover state on dropdown options */
        div[data-baseweb="menu"] div[role="option"]:hover {
            background-color: #333 !important;
            color: #FF9900 !important;
        }

        /* Style for selected option */
        div[data-baseweb="menu"] div[aria-selected="true"] {
            background-color: #333 !important;
            color: #FF9900 !important;
        }

        /* Apply to the actual dropdown list container */
        ul[role="listbox"] {
            background-color: #1a1a1a !important;
        }

        /* Every possible menu item */
        [data-baseweb="menu"] *, 
        [role="listbox"] *, 
        [role="option"] {
            background-color: #1a1a1a !important;
            color: white !important;
        }
        
        /* Hover state */
        [role="option"]:hover {
            background-color: #333 !important;
            color: #FF9900 !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Load main CSS
        load_css()
        
        # Initialize data processor
        self.data_processor = DataProcessor()
        
    def display_header(self):
        """Display the header with logo and title"""
        display_header()
    
    def display_dashboard(self, df):
        """Display the main dashboard content"""
        # Filter data 
        df_filtered = self.data_processor.filter_data()
        
        group_type_to_filter = ['S','W', 'T']
        df_filtered = df_filtered.query("order_type in @group_type_to_filter")
        
        # Add morning/afternoon label
        df_filtered = self.data_processor.add_time_of_day(df_filtered)
        
        # Create separate dataframes for morning and afternoon deliveries
        df_morning, df_afternoon = self.data_processor.get_morning_afternoon_data(df_filtered)
        
        # Get holiday data
        holiday_df = self.data_processor.get_holiday_data()
        
        # Get unique values for dropdowns
        container_types = df_morning['container_type'].unique().tolist()
        hub_locations = df_morning['hub_location'].unique().tolist()
        
        # Add "All" option to the beginning of the lists
        container_types = ["All"] + container_types
        hub_locations = ["All"] + hub_locations

        # Create dropdowns with custom CSS for black text
        col1, col2 = st.columns(2)
        with col1:
            selected_container = st.selectbox("Select Container Type", container_types)
            
        with col2:
            selected_hub = st.selectbox("Select Hub Location", hub_locations)

        # Filter data based on selections
        filtered_df = df_morning.copy()
        
        # Apply container type filter if not "All"
        if selected_container != "All":
            filtered_df = filtered_df[filtered_df['container_type'] == selected_container]
            
        # Apply hub location filter if not "All"
        if selected_hub != "All":
            filtered_df = filtered_df[filtered_df['hub_location'] == selected_hub]

        # Prepare filtered data for forecasting
        train_df, val_df = self.data_processor.prepare_forecast_data(filtered_df)

        # Create and fit Prophet model
        forecaster = Forecaster(holiday_df=holiday_df)
        model = forecaster.create_model(train_df)

        # Make forecast
        forecast = forecaster.make_forecast(train_df)
        
        # Display metrics above the chart
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Get the first forecast date after validation data
            if not val_df.empty:
                last_validation_date = val_df['ds'].max()
                future_forecast = forecast[forecast['ds'] > last_validation_date]
                
                if not future_forecast.empty:
                    # Get first forecasted data point after validation
                    first_forecast_date = future_forecast['ds'].min()
                    containers_forecast = round(future_forecast[future_forecast['ds'] == first_forecast_date]['yhat'].values[0])
                    forecast_date_str = first_forecast_date.strftime('%Y-%m-%d')
                    st.metric("Containers Needed Next Day", f"{containers_forecast}")
                    # st.markdown(f'<div style="font-size: 0.8rem; color: #888;">Forecast for {forecast_date_str}</div>', unsafe_allow_html=True)
                else:
                    containers_forecast = "N/A"
                    st.metric("Containers Needed Next Day", "No forecast available")
            else:
                containers_forecast = "N/A"
                st.metric("Containers Needed Next Day", "No validation data")
            
        with col2:
            # Calculate trucks needed based on containers (assuming average of 3 containers per truck)
            if containers_forecast != "N/A":
                # Assuming an average of 3 containers per truck
                trucks_needed = int(np.ceil(containers_forecast / 4))
                st.metric("Trucks Needed Next Day", f"{trucks_needed}")
            else:
                st.metric("Trucks Needed Next Day", "N/A")
            
        with col3:
            # Empty column for balance
            pass

        # Get model components for explanation
        model_details = {
            "changepoint_prior_scale": forecaster.model.changepoint_prior_scale,
            "seasonality_prior_scale": forecaster.model.seasonality_prior_scale,
            "seasonality_mode": forecaster.model.seasonality_mode
        }
        
        # Get forecast components if available
        forecast_components = None
        if not val_df.empty and 'ds' in forecast.columns:
            if not future_forecast.empty:
                forecast_date = first_forecast_date
                forecast_components = forecast[forecast['ds'] == forecast_date]
                
                # Request component-wise forecast to see all seasonality effects
                if hasattr(forecaster.model, 'component_modes'):
                    # Prophet version 1.0 and above
                    forecast_with_components = forecaster.model.predict(pd.DataFrame({'ds': [forecast_date]}))
                else:
                    # Legacy Prophet
                    forecast_with_components = forecast_components.copy()
        
        # Add explanation about the forecast with actual numbers
        # st.markdown(f"""
        # ### Forecast Analysis
        
        # This forecast is based on historical delivery patterns for {"all container types" if selected_container == "All" else f"'{selected_container}' containers"} 
        # at {"all hub locations" if selected_hub == "All" else f"the '{selected_hub}' hub"}.
        # """)
        
        if forecast_components is not None and len(forecast_components) > 0:
            # Explicitly list all possible components
            components_to_check = ['trend', 'weekly', 'yearly', 'holidays', 'multiplicative_terms', 
                                  'additive_terms', 'daily', 'weekly_MONDAY', 'weekly_TUESDAY', 
                                  'weekly_WEDNESDAY', 'weekly_THURSDAY', 'weekly_FRIDAY']
            
            # Extract basic components
            trend = forecast_components['trend'].values[0]
            yhat = forecast_components['yhat'].values[0]
            
            # Check for weekly components in various formats
            weekly = 0
            # Direct weekly component
            if 'weekly' in forecast_components:
                weekly = forecast_components['weekly'].values[0]
            # Day-of-week components
            elif any(day in forecast_components for day in ['weekly_MONDAY', 'weekly_TUESDAY', 'weekly_WEDNESDAY', 'weekly_THURSDAY', 'weekly_FRIDAY']):
                # Find which day of the week this forecast is for
                dow = forecast_date.day_name().upper()
                if f'weekly_{dow}' in forecast_components:
                    weekly = forecast_components[f'weekly_{dow}'].values[0]
            
            # Get yearly seasonality
            yearly = forecast_components['yearly'].values[0] if 'yearly' in forecast_components else 0
            
            # Get holiday effect
            holidays_effect = forecast_components['holidays'].values[0] if 'holidays' in forecast_components else 0
            
            # Infer weekly effect if we have the total forecast and other components
            if weekly == 0:
                # Estimate weekly by subtracting other known components
                remaining = yhat - trend - yearly - holidays_effect
                weekly = remaining  # Attribute remaining effect to weekly pattern
            
            # Normalize small values to zero to avoid confusion
            if abs(weekly) < 0.01: weekly = 0
            if abs(yearly) < 0.01: yearly = 0
            if abs(holidays_effect) < 0.01: holidays_effect = 0
            
            # Ensure weekly seasonality has some value (at least 1% effect)
            if abs(weekly) < 0.01 * trend:
                weekly = 0.01 * trend if trend > 0 else 1
            
            # Calculate day of week effect
            day_of_week = forecast_date.day_name()
            yhat_rounded = round(yhat)
            holidays_effect_rounded = round(holidays_effect)
            weekly_rounded = round(weekly)
            yearly_rounded = round(yearly)
            trend_correction = yhat_rounded - (holidays_effect_rounded + weekly_rounded + yearly_rounded)
            markdown_text = f"""
            For **{forecast_date.strftime('%Y-%m-%d')}** ({day_of_week}), we expect **{containers_forecast} containers** based on:
            
            - **Regular demand**: {round(trend_correction)} containers
            - **{day_of_week} effect**: {'+' if weekly_rounded >= 0 else ''}{round(weekly_rounded)} containers 
            - **Seasonal demand**: {'+' if yearly_rounded >= 0 else ''}{round(yearly_rounded)} containers
            - **Holiday impact**: {'+' if holidays_effect_rounded >= 0 else ''}{round(holidays_effect_rounded)} containers
            
            This means you'll need **{trucks_needed} trucks**. 
            """
            if weekly_rounded > 0:
                markdown_text += f"The {day_of_week} effect shows that deliveries are typically {'higher' if weekly_rounded > 0 else 'lower'} on this day of the week."
            st.markdown(markdown_text)
            
        else:
            st.markdown("""
            The forecast considers:
            - Which day of the week it is (some days have more deliveries)
            - Time of year (seasonal patterns in container usage)
            - Holidays (which can reduce or increase demand)
            
            Each truck can carry up to 4 containers, and we always round up to ensure you have enough trucks.
            """)

        # Create visualization title based on selections
        if selected_container == "All" and selected_hub == "All":
            title = "Forecast for All Container Types and Hubs"
        elif selected_container == "All":
            title = f"Forecast for All Container Types at {selected_hub}"
        elif selected_hub == "All":
            title = f"Forecast for {selected_container} at All Hubs"
        else:
            title = f"Forecast for {selected_container} at {selected_hub}"
            
        # Create visualization
        fig = create_forecast_chart(train_df, val_df, forecast, title)
        st.plotly_chart(fig, use_container_width=True)
    
    def display_footer(self):
        """Display the footer"""
        display_footer()
    
    def run(self):
        """Run the dashboard"""
        # Load data
        df = self.data_processor.load_data()
        if df is None:
            st.error("Error loading data. Please check the data file.")
            return
        
        # Display header
        self.display_header()
        
        # Display dashboard content
        self.display_dashboard(df)
        
        # Display footer
        self.display_footer()        