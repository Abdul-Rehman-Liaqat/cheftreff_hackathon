import pandas as pd
import numpy as np
from prophet import Prophet

class Forecaster:
    def __init__(self, holiday_df=None):
        self.holiday_df = holiday_df
        self.model = None
        self.forecast = None
        
    def create_model(self, train_df):
        """Create and fit Prophet model"""
        self.model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=True,
            seasonality_mode='multiplicative',
            changepoint_prior_scale=0.01,  # Reduce flexibility to prevent overfitting
            seasonality_prior_scale=10.0,  # Increase impact of seasonality
            holidays=self.holiday_df,
            growth='logistic'
        )
        
        # Set floor and carrying capacity
        train_df['cap'] = train_df['y'].max() * 1.5  # Upper bound
        train_df['floor'] = 0  # Lower bound to prevent negative values
        
        # Fit the model
        self.model.fit(train_df)
        
        return self.model
    
    def make_forecast(self, train_df, forecast_period=45):
        """Make future predictions"""
        # Make future predictions including validation period
        future_dates = self.model.make_future_dataframe(periods=forecast_period)
        future_dates['cap'] = train_df['y'].max() * 1.5  # Set capacity for future dates
        future_dates['floor'] = 0  # Set floor for future dates
        
        self.forecast = self.model.predict(future_dates)
        
        return self.forecast
    
    def calculate_metrics(self, val_df):
        """Calculate forecast metrics"""
        if self.forecast is None or val_df is None:
            return None, None
            
        val_forecast = self.forecast[self.forecast['ds'].isin(val_df['ds'])]
        
        # Calculate MAPE (Mean Absolute Percentage Error)
        mape = np.mean(np.abs((val_df['y'].values - val_forecast['yhat'].values) / val_df['y'].values)) * 100
        
        # Calculate RMSE (Root Mean Square Error)
        rmse = np.sqrt(np.mean((val_df['y'].values - val_forecast['yhat'].values)**2))
        
        return mape, rmse 