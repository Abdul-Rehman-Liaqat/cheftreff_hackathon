import plotly.express as px
import plotly.graph_objects as go
from styles.theme import OTTO_DORNER_BLUE
import pandas as pd
from datetime import datetime, timedelta

def create_branded_chart(fig, title):
    """Apply Otto Dörner branding to a chart"""
    fig.update_layout(
        title=title,
        title_font=dict(size=20, color=OTTO_DORNER_BLUE),
        font=dict(family="Arial", size=12),
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(gridcolor="#E6E6E6", zerolinecolor="#CCCCCC"),
        yaxis=dict(gridcolor="#E6E6E6", zerolinecolor="#CCCCCC"),
        legend=dict(
            font=dict(size=12),
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="#CCCCCC",
            borderwidth=1
        ),
        margin=dict(l=50, r=50, t=80, b=50)
    )
    return fig

def create_forecast_chart(train_df, val_df, forecast, title="Forecast"):
    """Create a forecast visualization chart"""
    fig = go.Figure()

    # Filter forecast to only show data for 2025
    forecast_2025 = forecast[forecast['ds'].dt.year == 2025]
    
    # Determine the last month in the available data
    last_date_in_data = max(train_df['ds'].max(), val_df['ds'].max())
    forecast_start_date = last_date_in_data - timedelta(days=30)  # Last month of data
    forecast_end_date = last_date_in_data + timedelta(days=60)    # Next 2 months
    
    # Keep only actual data before the forecast
    forecast_data = forecast_2025[
        (forecast_2025['ds'] >= forecast_start_date) & 
        (forecast_2025['ds'] <= forecast_end_date)
    ]
    
    # Plot training data for 2025 (visible)
    train_2025 = train_df[train_df['ds'].dt.year == 2025]
    if not train_2025.empty:
        fig.add_trace(go.Scatter(
            x=train_2025['ds'],
            y=train_2025['y'],
            name='Historical Data',
            mode='markers+lines',
            line=dict(color=OTTO_DORNER_BLUE)
        ))
    
    # Plot validation data for 2025 (visible)
    val_2025 = val_df[val_df['ds'].dt.year == 2025]
    if not val_2025.empty:
        fig.add_trace(go.Scatter(
            x=val_2025['ds'],
            y=val_2025['y'],
            name='Validation Data',
            mode='markers+lines',
            line=dict(color='#FF9900')
        ))

    # Plot only the forecast period
    fig.add_trace(go.Scatter(
        x=forecast_data['ds'],
        y=forecast_data['yhat'].clip(lower=0),
        name='Forecast',
        mode='lines',
        line=dict(color='#00CC96', dash='dash')
    ))

    # Add confidence intervals for the forecast period only
    fig.add_trace(go.Scatter(
        x=forecast_data['ds'].tolist() + forecast_data['ds'].tolist()[::-1],
        y=forecast_data['yhat_upper'].tolist() + forecast_data['yhat_lower'].tolist()[::-1],
        fill='toself',
        fillcolor='rgba(0, 204, 150, 0.2)',
        line=dict(color='rgba(255, 255, 255, 0)'),
        name='Confidence Interval'
    ))

    # Find the actual date range to display (only months with data)
    # Combine all the data that will be displayed in the chart
    all_displayed_dates = []
    if not train_2025.empty:
        all_displayed_dates.extend(train_2025['ds'].tolist())
    if not val_2025.empty:
        all_displayed_dates.extend(val_2025['ds'].tolist())
    all_displayed_dates.extend(forecast_data['ds'].tolist())
    
    if all_displayed_dates:
        min_date = min(all_displayed_dates)
        max_date = max(all_displayed_dates)
        
        # Set to beginning of the month for min date
        display_start = pd.Timestamp(year=min_date.year, month=min_date.month, day=1)
        
        # Set to end of the month for max date
        if max_date.month == 12:
            display_end = pd.Timestamp(year=max_date.year+1, month=1, day=1) - pd.Timedelta(days=1)
        else:
            display_end = pd.Timestamp(year=max_date.year, month=max_date.month+1, day=1) - pd.Timedelta(days=1)
    else:
        # Fallback if no data
        display_start = pd.Timestamp('2025-01-01')
        display_end = pd.Timestamp('2025-01-31')

    # Update title to reflect the period being shown
    title = f"{title} ({display_start.strftime('%b')} - {display_end.strftime('%b')} 2025)"
    fig = create_branded_chart(fig, title)
    
    # Set x-axis range to only the months being used
    fig.update_layout(
        xaxis=dict(
            range=[
                display_start,
                display_end
            ]
        )
    )
    
    return fig 