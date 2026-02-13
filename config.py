"""
Configuration Module
Project settings and constants
"""

# File paths
DATA_DIR = 'data'
OUTPUT_DIR = 'output'
EXCEL_DIR = 'excel'
DATABASE_DIR = 'database'

# File names
TRANSACTIONS_FILE = 'transactions.csv'
DATABASE_FILE = 'retail.db'

# RFM Configuration
RFM_BINS = 5  # Number of bins for RFM scoring
RECENCY_BINS = [0, 30, 90, 180, 365, float('inf')]
RECENCY_LABELS = [5, 4, 3, 2, 1]

# Customer Segments
SEGMENTS = {
    'Champions': {'R': (4, 5), 'F': (4, 5), 'M': (4, 5)},
    'Loyal Customers': {'R': (3, 5), 'F': (3, 5)},
    'Potential Loyalists': {'R': (4, 5), 'F': (1, 2)},
    'At Risk': {'R': (1, 2), 'F': (3, 5)},
    'Lost': {'R': (1, 2), 'F': (1, 2)}
}

# Business Metrics
TOP_CUSTOMER_PERCENTILE = 20  # Top 20% customers
CHURN_DAYS_THRESHOLD = 180    # 180 days = churned
RETENTION_PERIOD_DAYS = 30    # Retention within 30 days
LOYAL_CUSTOMER_MIN_PURCHASES = 5

# Product Categories
PRODUCT_CATEGORIES = [
    'Electronics',
    'Clothing',
    'Home & Kitchen',
    'Books',
    'Sports',
    'Beauty'
]

# Data Generation Settings
DEFAULT_NUM_TRANSACTIONS = 8000
DEFAULT_NUM_CUSTOMERS_RATIO = 0.4  # 40% of transactions = unique customers
LOYAL_CUSTOMER_RATIO = 0.15        # 15% are loyal (5-15 purchases)

# Chart Settings
CHART_STYLE = 'seaborn-v0_8-whitegrid'
CHART_DPI = 300
CHART_FIGURE_SIZE = (12, 6)

# Excel Settings
EXCEL_HEADER_COLOR = '4472C4'
EXCEL_HEADER_FONT_COLOR = 'FFFFFF'

# Dashboard Settings
DASHBOARD_TITLE = 'Retail Customer Intelligence Dashboard'
DASHBOARD_KPI_CARDS = ['Total Revenue', 'Total Customers', 'Avg Transaction Value']

# Report Settings
REPORT_TOP_CUSTOMERS = 50
REPORT_TOP_CATEGORIES = 10

# Color Schemes
SEGMENT_COLORS = {
    'Champions': '#2ecc71',
    'Loyal Customers': '#3498db',
    'Potential Loyalists': '#f39c12',
    'At Risk': '#e67e22',
    'Lost': '#e74c3c',
    'Others': '#95a5a6'
}

# Revenue Categories
REVENUE_CATEGORIES = {
    'low': (0, 5000),
    'medium': (5000, 20000),
    'high': (20000, float('inf'))
}

# Display Settings
DECIMAL_PLACES = 2
CURRENCY_SYMBOL = '₹'
DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

# Analysis Settings
MIN_TRANSACTIONS_FOR_ANALYSIS = 100
MIN_CUSTOMERS_FOR_SEGMENTATION = 50

# Validation Settings
MAX_TRANSACTION_AMOUNT = 100000  # Flag transactions above this
MIN_TRANSACTION_AMOUNT = 100      # Flag transactions below this

def get_config():
    """Return all configuration as dictionary"""
    
    return {
        'paths': {
            'data': DATA_DIR,
            'output': OUTPUT_DIR,
            'excel': EXCEL_DIR,
            'database': DATABASE_DIR
        },
        'rfm': {
            'bins': RFM_BINS,
            'top_percentile': TOP_CUSTOMER_PERCENTILE
        },
        'business': {
            'churn_days': CHURN_DAYS_THRESHOLD,
            'retention_days': RETENTION_PERIOD_DAYS,
            'loyal_min_purchases': LOYAL_CUSTOMER_MIN_PURCHASES
        }
    }
