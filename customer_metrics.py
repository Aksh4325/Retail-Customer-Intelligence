"""
Customer Metrics Module
Calculate various customer behavior metrics
"""

import pandas as pd
from datetime import datetime


class CustomerMetrics:
    """Calculate customer-level metrics"""
    
    def __init__(self, transactions):
        self.df = transactions.copy()
        self.df['date'] = pd.to_datetime(self.df['date'])
    
    def calculate_repeat_purchase_rate(self):
        """
        Calculate repeat purchase rate
        Simple: % of customers who bought more than once
        """
        
        customer_counts = self.df.groupby('customer_id').size()
        
        total_customers = len(customer_counts)
        repeat_customers = len(customer_counts[customer_counts > 1])
        
        repeat_rate = (repeat_customers / total_customers) * 100
        
        return {
            'total_customers': total_customers,
            'repeat_customers': repeat_customers,
            'one_time_customers': total_customers - repeat_customers,
            'repeat_rate': round(repeat_rate, 2)
        }
    
    def calculate_average_order_value(self):
        """Calculate AOV"""
        
        aov = self.df['amount'].mean()
        
        # By segment if available
        if 'category' in self.df.columns:
            category_aov = self.df.groupby('category')['amount'].mean()
            return {
                'overall_aov': round(aov, 2),
                'category_aov': category_aov.to_dict()
            }
        
        return {'overall_aov': round(aov, 2)}
    
    def calculate_purchase_frequency(self):
        """
        How often do customers buy?
        Average days between purchases
        """
        
        frequency_data = []
        
        for customer in self.df['customer_id'].unique():
            customer_data = self.df[self.df['customer_id'] == customer].sort_values('date')
            
            if len(customer_data) > 1:
                # Calculate days between purchases
                dates = customer_data['date'].tolist()
                gaps = [(dates[i] - dates[i-1]).days for i in range(1, len(dates))]
                avg_gap = sum(gaps) / len(gaps)
                frequency_data.append(avg_gap)
        
        if frequency_data:
            avg_purchase_frequency = sum(frequency_data) / len(frequency_data)
            return round(avg_purchase_frequency, 1)
        
        return None
    
    def calculate_churn_rate(self, days_threshold=180):
        """
        Calculate churn rate
        Customers who haven't bought in X days
        """
        
        current_date = datetime.now()
        
        last_purchases = self.df.groupby('customer_id')['date'].max()
        
        # Days since last purchase
        days_since = (current_date - last_purchases).dt.days
        
        churned = len(days_since[days_since > days_threshold])
        total = len(days_since)
        
        churn_rate = (churned / total) * 100
        
        return {
            'churned_customers': churned,
            'active_customers': total - churned,
            'churn_rate': round(churn_rate, 2)
        }
    
    def calculate_customer_value_distribution(self):
        """
        Categorize customers by total spending
        """
        
        customer_totals = self.df.groupby('customer_id')['amount'].sum()
        
        # Define categories
        low_value = len(customer_totals[customer_totals < 5000])
        medium_value = len(customer_totals[(customer_totals >= 5000) & (customer_totals < 20000)])
        high_value = len(customer_totals[customer_totals >= 20000])
        
        return {
            'low_value': low_value,
            'medium_value': medium_value,
            'high_value': high_value,
            'total': len(customer_totals)
        }
    
    def get_customer_journey_stats(self):
        """
        Analyze customer journey
        From first to last purchase
        """
        
        journey_stats = self.df.groupby('customer_id').agg({
            'date': ['min', 'max', 'count'],
            'amount': 'sum'
        })
        
        journey_stats.columns = ['first_purchase', 'last_purchase', 'total_purchases', 'total_spent']
        
        # Calculate customer lifespan
        journey_stats['lifespan_days'] = (
            pd.to_datetime(journey_stats['last_purchase']) - 
            pd.to_datetime(journey_stats['first_purchase'])
        ).dt.days
        
        return journey_stats
