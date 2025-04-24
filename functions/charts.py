import plotly.express as px
import plotly.graph_objects as go
from styles.theme import OTTO_DORNER_BLUE

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

    # Plot training data
    fig.add_trace(go.Scatter(
        x=train_df['ds'],
        y=train_df['y'],
        name='Training Data',
        mode='markers+lines',
        line=dict(color=OTTO_DORNER_BLUE)
    ))
    
    # Plot validation data
    fig.add_trace(go.Scatter(
        x=val_df['ds'],
        y=val_df['y'],
        name='Validation Data',
        mode='markers+lines',
        line=dict(color='#FF9900')
    ))

    # Plot forecast
    fig.add_trace(go.Scatter(
        x=forecast['ds'],
        y=forecast['yhat'].clip(lower=0),
        name='Forecast',
        mode='lines',
        line=dict(color='#00CC96', dash='dash')
    ))

    # Add confidence intervals
    fig.add_trace(go.Scatter(
        x=forecast['ds'].tolist() + forecast['ds'].tolist()[::-1],
        y=forecast['yhat_upper'].tolist() + forecast['yhat_lower'].tolist()[::-1],
        fill='toself',
        fillcolor='rgba(0, 204, 150, 0.2)',
        line=dict(color='rgba(255, 255, 255, 0)'),
        name='Confidence Interval'
    ))

    fig = create_branded_chart(fig, title)
    return fig 