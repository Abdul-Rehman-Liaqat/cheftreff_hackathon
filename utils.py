# This file is kept for backward compatibility
# All functions have been moved to their respective modules:
# - UI functions -> functions/ui.py
# - Chart functions -> functions/charts.py
# - Theme and styles -> styles/theme.py

from functions.ui import load_logo, load_css, display_header, display_footer
from functions.charts import create_branded_chart, create_forecast_chart
from styles.theme import OTTO_DORNER_BLUE, OTTO_DORNER_ORANGE, STYLES

__all__ = [
    'load_logo',
    'load_css',
    'display_header',
    'display_footer',
    'create_branded_chart',
    'create_forecast_chart',
    'OTTO_DORNER_BLUE',
    'OTTO_DORNER_ORANGE',
    'STYLES'
] 