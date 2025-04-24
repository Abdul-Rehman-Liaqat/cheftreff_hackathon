# Otto Dörner Data Analysis Dashboard

A Streamlit-based dashboard for analyzing waste management and resource planning data for Otto Dörner.

## Project Structure

The project has been refactored into a modular structure:

- `app.py`: Main entry point that initializes and runs the dashboard
- `data_processor.py`: Handles data loading and preprocessing
- `forecaster.py`: Contains time series forecasting functionality
- `dashboard.py`: Implements the Streamlit dashboard UI
- `utils.py`: Contains utility functions for styling and visualization

## Features

- **Summary Dashboard**: Overview of key metrics and order trends
- **Container Analysis**: Distribution of container types and usage by hub
- **Vehicle Analysis**: Vehicle group distribution and utilization over time
- **Delivery Analysis**: Order type distribution and delivery time analysis
- **Forecasting**: Time series forecasting for morning orders

## Installation

1. Clone the repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the dashboard:
   ```
   streamlit run app.py
   ```

## Data

The dashboard uses data from the `data/combined.csv` file, which contains waste management and delivery information.

## Dependencies

- streamlit
- pandas
- plotly
- numpy
- prophet
- holidays
- cairosvg
- Pillow
- requests 