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
            page_title="Otto Dörner Data Analysis",
            page_icon="🚛",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Load CSS
        load_css()
        
        # Initialize data processor
        self.data_processor = DataProcessor()
        
    def display_header(self):
        """Display the header with logo and title"""
        display_header()
    
    def display_summary_tab(self, df):
        """Display the summary tab content"""
        st.markdown('<div class="subtitle">Summary Dashboard</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            total_orders = len(df)
            st.metric("Total Orders", f"{total_orders:,}")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            total_containers = df['containers_delivered'].sum()
            st.metric("Total Containers Delivered", f"{total_containers:,}")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col3:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            total_vehicles = df['vehicle_id'].nunique()
            st.metric("Unique Vehicles", f"{total_vehicles:,}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Time series of orders
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Order Trends Over Time</div>', unsafe_allow_html=True)
        
        # Add year filter
        years = sorted(df['delivery_date'].dt.year.unique())
        selected_year = st.selectbox("Select Year", years)
        
        # Filter data by year
        df_filtered = self.data_processor.filter_data()
        
        group_type_to_filter = ['S','W', 'T']
        df_filtered = df_filtered.query("order_type in @group_type_to_filter")
        
        period = st.selectbox("Select Time Period", ["Daily", "Weekly", "Monthly"])
        
        # Add morning/afternoon label
        df_filtered = self.data_processor.add_time_of_day(df_filtered)
        
        # Create separate dataframes for morning and afternoon deliveries
        df_morning, df_afternoon = self.data_processor.get_morning_afternoon_data(df_filtered)
        
        if period == "Daily":
            # Group by day for all orders
            daily_orders = df_filtered.groupby(pd.Grouper(key='delivery_date', freq='D')).size().reset_index(name='count')
            # Group by day for morning orders
            daily_morning = df_morning.groupby(pd.Grouper(key='delivery_date', freq='D')).size().reset_index(name='count')
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=daily_orders['delivery_date'], y=daily_orders['count'], 
                                   name='All Orders', mode='lines'))
            fig.add_trace(go.Scatter(x=daily_morning['delivery_date'], y=daily_morning['count'],
                                   name='Morning Orders', mode='lines'))
            fig.update_layout(title='Daily Order Volume')

        elif period == "Weekly":
            # Group by week for all orders
            weekly_orders = df_filtered.groupby(pd.Grouper(key='delivery_date', freq='W')).size().reset_index(name='count')
            # Group by week for morning orders
            weekly_morning = df_morning.groupby(pd.Grouper(key='delivery_date', freq='W')).size().reset_index(name='count')
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=weekly_orders['delivery_date'], y=weekly_orders['count'],
                                   name='All Orders', mode='lines'))
            fig.add_trace(go.Scatter(x=weekly_morning['delivery_date'], y=weekly_morning['count'],
                                   name='Morning Orders', mode='lines'))
            fig.update_layout(title='Weekly Order Volume')

        else:
            # Group by month for all orders
            monthly_orders = df_filtered.groupby(pd.Grouper(key='delivery_date', freq='ME')).size().reset_index(name='count')
            # Group by month for morning orders
            monthly_morning = df_morning.groupby(pd.Grouper(key='delivery_date', freq='ME')).size().reset_index(name='count')
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=monthly_orders['delivery_date'], y=monthly_orders['count'],
                                   name='All Orders', mode='lines'))
            fig.add_trace(go.Scatter(x=monthly_morning['delivery_date'], y=monthly_morning['count'],
                                   name='Morning Orders', mode='lines'))
            fig.update_layout(title='Monthly Order Volume')
            
        fig = create_branded_chart(fig, f"{period} Order Volume")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Time series forecasting for morning deliveries
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Morning Orders Forecast</div>', unsafe_allow_html=True)
        
        # Get holiday data
        holiday_df = self.data_processor.get_holiday_data()
        
        # Prepare data for forecasting
        train_df, val_df = self.data_processor.prepare_forecast_data(df_morning)        
        # Create and fit Prophet model
        forecaster = Forecaster(holiday_df=holiday_df)
        model = forecaster.create_model(train_df)
        
        # Make forecast
        forecast = forecaster.make_forecast(train_df)
        
        # Create visualization
        fig = create_forecast_chart(train_df, val_df, forecast, "Morning Orders Forecast")
        st.plotly_chart(fig, use_container_width=True)
        
        # Calculate and display forecast metrics
        mape, rmse = forecaster.calculate_metrics(val_df)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("MAPE (Mean Absolute Percentage Error)", f"{mape:.2f}%")
        with col2:
            st.metric("RMSE (Root Mean Square Error)", f"{rmse:.2f}")
            
        st.markdown('</div>', unsafe_allow_html=True)
        

    
    def display_containers_tab(self, df):
        """Display the containers tab content"""
        st.markdown('<div class="subtitle">Container Analysis</div>', unsafe_allow_html=True)
        
        # Container type distribution
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Container Type Distribution</div>', unsafe_allow_html=True)
        container_dist = df['container_type'].value_counts()
        fig = px.bar(x=container_dist.index, y=container_dist.values, title='Container Type Distribution')
        fig = create_branded_chart(fig, "Container Type Distribution")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Container usage by hub
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Container Usage by Hub</div>', unsafe_allow_html=True)
        hub_container = df.groupby(['hub_location', 'container_type']).size().unstack()
        fig = px.bar(hub_container, title='Container Types by Hub', barmode='group')
        fig = create_branded_chart(fig, "Container Types by Hub")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    def display_vehicles_tab(self, df):
        """Display the vehicles tab content"""
        st.markdown('<div class="subtitle">Vehicle Analysis</div>', unsafe_allow_html=True)
        
        # Vehicle group distribution
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Vehicle Group Distribution</div>', unsafe_allow_html=True)
        vehicle_dist = df['vehicle_group'].value_counts()
        fig = px.pie(values=vehicle_dist.values, names=vehicle_dist.index, title='Vehicle Group Distribution')
        fig = create_branded_chart(fig, "Vehicle Group Distribution")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    def display_deliveries_tab(self, df):
        """Display the deliveries tab content"""
        st.markdown('<div class="subtitle">Delivery Analysis</div>', unsafe_allow_html=True)
        
        # Delivery time distribution
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Delivery Time Distribution</div>', unsafe_allow_html=True)
        time_dist = df['time_of_day'].value_counts()
        fig = px.pie(values=time_dist.values, names=time_dist.index, title='Delivery Time Distribution')
        fig = create_branded_chart(fig, "Delivery Time Distribution")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
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
        
        # Create tabs
        tab1, tab2, tab3, tab4 = st.tabs(["Summary", "Containers", "Vehicles", "Deliveries"])
        
        with tab1:
            self.display_summary_tab(df)
            
        with tab2:
            self.display_containers_tab(df)
            
        with tab3:
            self.display_vehicles_tab(df)
                    
        # Display footer        