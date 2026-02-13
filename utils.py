"""
Utilities Module
Helper functions for data processing
"""

import pandas as pd
from datetime import datetime


def validate_data(df):
    """
    Validate transaction data
    Check for required columns and data quality
    """
    
    required_columns = ['transaction_id', 'customer_id', 'date', 'amount']
    
    # Check required columns
    missing = [col for col in required_columns if col not in df.columns]
    
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    # Check for nulls
    null_counts = df[required_columns].isnull().sum()
    
    if null_counts.any():
        print("Warning: Found null values:")
        print(null_counts[null_counts > 0])
    
    # Check for negative amounts
    negative = df[df['amount'] < 0]
    if len(negative) > 0:
        print(f"Warning: Found {len(negative)} negative amounts")
    
    return True


def format_currency(amount):
    """Format amount as currency"""
    return f"₹{amount:,.2f}"


def calculate_percentage(part, whole):
    """Calculate percentage"""
    if whole == 0:
        return 0
    return round((part / whole) * 100, 2)


def get_date_range(df, date_column='date'):
    """Get date range from dataframe"""
    
    df[date_column] = pd.to_datetime(df[date_column])
    
    min_date = df[date_column].min()
    max_date = df[date_column].max()
    
    days = (max_date - min_date).days
    
    return {
        'start_date': min_date.strftime('%Y-%m-%d'),
        'end_date': max_date.strftime('%Y-%m-%d'),
        'total_days': days
    }


def create_summary_stats(df, group_by, metric_column):
    """
    Create summary statistics
    Generic function for grouping and aggregation
    """
    
    summary = df.groupby(group_by)[metric_column].agg([
        'count', 'sum', 'mean', 'min', 'max'
    ]).reset_index()
    
    summary.columns = [group_by, 'count', 'total', 'average', 'minimum', 'maximum']
    
    return summary


def filter_date_range(df, start_date=None, end_date=None, date_column='date'):
    """Filter dataframe by date range"""
    
    df[date_column] = pd.to_datetime(df[date_column])
    
    if start_date:
        start_date = pd.to_datetime(start_date)
        df = df[df[date_column] >= start_date]
    
    if end_date:
        end_date = pd.to_datetime(end_date)
        df = df[df[date_column] <= end_date]
    
    return df


def calculate_days_between(date1, date2):
    """Calculate days between two dates"""
    
    d1 = pd.to_datetime(date1)
    d2 = pd.to_datetime(date2)
    
    return (d2 - d1).days


def bin_numeric_column(df, column, bins, labels):
    """
    Bin numeric column into categories
    """
    
    df[f'{column}_category'] = pd.cut(df[column], bins=bins, labels=labels)
    
    return df


def export_to_csv(df, filename, index=False):
    """Export dataframe to CSV"""
    
    df.to_csv(filename, index=index)
    print(f"✓ Exported to {filename}")
