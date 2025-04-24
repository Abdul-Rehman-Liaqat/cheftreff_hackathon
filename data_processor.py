import pandas as pd
import numpy as np
from datetime import datetime
import holidays

class DataProcessor:
    def __init__(self, data_path='data/combined.csv'):
        self.data_path = data_path
        self.df = None
        
    def load_data(self):
        """Load data from CSV file"""
        try:
            # Read the CSV with low_memory=False to avoid mixed type warnings
            self.df = pd.read_csv(self.data_path, low_memory=False)
            # Rename columns to more readable format
            column_mapping = {
                'LiefZeitV': 'earliest_delivery_time',
                'LiefZeitB': 'latest_delivery_time',
                'LiefKWJ': 'delivery_year',
                'Monat': 'delivery_month',
                'LiefDatum': 'delivery_date',
                'CVgId': 'order_id',
                'Typ': 'customer_type',
                'LoAdrId': 'customer_site_id',
                'LoPlz': 'customer_zipcode',
                'LoOrt': 'customer_city',
                'DspGrpKz': 'vehicle_group',
                'DspZenKz': 'hub_location',
                'AArtKz': 'order_type',
                'ConTyp': 'container_type',
                'CSAnz': 'containers_delivered',
                'CHAnz': 'containers_picked_up',
                'FzgNr': 'vehicle_id',
                'Bez': 'waste_type',
                'Plz': 'disposal_site_zipcode',
                'Ort': 'disposal_site_city',
                'AddDatum': 'order_datetime',
                'EntPlz': 'destination_zipcode',
                'EntOrt': 'destination_city'
            }
            self.df = self.df.rename(columns=column_mapping)
            # Convert delivery_date column to datetime
            self.df['delivery_date'] = pd.to_datetime(self.df['delivery_date'])
            return self.df
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return None
    
    def filter_data(self, year=None, order_types=None):
        """Filter data by year and order types"""
        df_filtered = self.df.copy()
        
        if year:
            df_filtered = df_filtered[df_filtered['delivery_date'].dt.year == year]
            
        if order_types:
            df_filtered = df_filtered[df_filtered['order_type'].isin(order_types)]
            
        return df_filtered
    
    def add_time_of_day(self, df=None):
        """Add time of day label (Morning/Afternoon) to the dataframe"""
        if df is None:
            df = self.df
            
        df['time_of_day'] = df['latest_delivery_time'].fillna('14:00').apply(
            lambda x: 'Morning' if int(str(x).split(':')[0]) < 12 else 'Afternoon'
        )
        return df
    
    def get_morning_afternoon_data(self, df=None):
        """Split data into morning and afternoon deliveries"""
        if df is None:
            df = self.df
            
        df = self.add_time_of_day(df)
        df_morning = df[df['time_of_day'] == 'Morning']
        df_afternoon = df[df['time_of_day'] == 'Afternoon']
        
        return df_morning, df_afternoon
    
    def get_holiday_data(self, years=None):
        """Get holiday data for forecasting"""
        if years is None:
            years = list(range(2020, 2026))
            
        de_holidays = holidays.Germany(years=years)
        
        # Convert to Prophet holiday format
        holiday_df = pd.DataFrame([
            {'ds': date, 'holiday': name, 'lower_window': 0, 'upper_window': 0}
            for date, name in de_holidays.items()
        ])
        
        # Add holiday effects
        holiday_df['prior_scale'] = 10.0  # Stronger holiday effects
        
        return holiday_df
    
    def prepare_forecast_data(self, df_morning, forecast_period=45):
        """Prepare data for Prophet forecasting"""
        # Create a date range from Jan 4 to Mar 31
        date_range = pd.date_range(start='2021-01-04', end='2025-03-31', freq='D')
        
        # Group by delivery date and get counts
        daily_counts = df_morning.groupby('delivery_date').count()[['delivery_year']].reset_index()
        
        # Create a DataFrame with all dates and merge with counts
        prophet_df = pd.DataFrame({'ds': date_range})
        prophet_df = prophet_df.merge(daily_counts[['delivery_date', 'delivery_year']], 
                                    left_on='ds', 
                                    right_on='delivery_date', 
                                    how='left')
        
        # Fill missing values with 0 and clean up columns
        prophet_df['y'] = prophet_df['delivery_year'].fillna(0)
        prophet_df = prophet_df[['ds', 'y']]  # Keep only required Prophet columns
        
        # Split data into training and validation sets (last 30 days for validation)
        cutoff_date = prophet_df['ds'].max() - pd.Timedelta(days=30)
        
        # Remove weekends from both training and validation sets
        train_df = prophet_df[(prophet_df['ds'] <= cutoff_date) & 
                            (prophet_df['ds'].dt.dayofweek < 5)]  # 0-4 are Monday-Friday
        val_df = prophet_df[(prophet_df['ds'] > cutoff_date) & 
                          (prophet_df['ds'].dt.dayofweek < 5)]
        
        # Set floor and carrying capacity
        train_df['cap'] = train_df['y'].max() * 1.5  # Upper bound
        train_df['floor'] = 0  # Lower bound to prevent negative values
        return train_df, val_df 