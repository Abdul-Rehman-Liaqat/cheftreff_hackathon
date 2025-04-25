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
            changepoint_prior_scale=0.05,  # Increased from 0.01 to allow more flexibility
            seasonality_prior_scale=1.0,   # Reduced from 10.0 to prevent overfitting
            holidays=self.holiday_df,
            growth='linear'                # Changed from logistic to linear for less constraint
        )
        
        # Fit the model without floor and cap constraints
        self.model.fit(train_df)
        
        return self.model
    
    def make_forecast(self, train_df, forecast_period=45):
        """Make future predictions"""
        # Make future predictions including validation period
        future_dates = self.model.make_future_dataframe(periods=forecast_period)
        
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