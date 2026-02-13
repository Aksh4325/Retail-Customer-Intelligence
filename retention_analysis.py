"""
Retention Analysis Module
Analyze customer retention patterns
"""

import pandas as pd
import numpy as np


class RetentionAnalyzer:
    """Customer retention analysis"""
    
    def __init__(self, transactions):
        self.df = transactions.copy()
        self.df['date'] = pd.to_datetime(self.df['date'])
    
    def calculate_cohort_retention(self):
        """
        Simple cohort retention analysis
        Track customers by their first purchase month
        """
        
        # Get first purchase date for each customer
        customer_cohort = self.df.groupby('customer_id')['date'].min().reset_index()
        customer_cohort.columns = ['customer_id', 'cohort_date']
        customer_cohort['cohort_month'] = customer_cohort['cohort_date'].dt.to_period('M')
        
        # Merge with transactions
        df_cohort = self.df.merge(customer_cohort[['customer_id', 'cohort_month']], on='customer_id')
        df_cohort['transaction_month'] = df_cohort['date'].dt.to_period('M')
        
        # Calculate month number (0, 1, 2, etc.)
        df_cohort['month_number'] = (
            (df_cohort['transaction_month'] - df_cohort['cohort_month']).apply(lambda x: x.n)
        )
        
        # Count unique customers per cohort per month
        cohort_data = df_cohort.groupby(['cohort_month', 'month_number'])['customer_id'].nunique().reset_index()
        
        # Pivot to create retention table
        retention_table = cohort_data.pivot(index='cohort_month', 
                                            columns='month_number', 
                                            values='customer_id')
        
        # Calculate retention percentages
        retention_pct = retention_table.divide(retention_table[0], axis=0) * 100
        
        return retention_pct.round(2)
    
    def get_retention_rate(self, period_days=30):
        """
        Simple retention rate
        % of customers who return within X days
        """
        
        retention_data = []
        
        for customer in self.df['customer_id'].unique():
            customer_purchases = self.df[self.df['customer_id'] == customer].sort_values('date')
            
            if len(customer_purchases) > 1:
                # Check if second purchase was within period
                first_purchase = customer_purchases.iloc[0]['date']
                second_purchase = customer_purchases.iloc[1]['date']
                
                days_between = (second_purchase - first_purchase).days
                
                if days_between <= period_days:
                    retention_data.append(1)
                else:
                    retention_data.append(0)
            else:
                retention_data.append(0)  # Didn't return
        
        retention_rate = (sum(retention_data) / len(retention_data)) * 100
        
        return {
            'retention_rate': round(retention_rate, 2),
            'retained_customers': sum(retention_data),
            'total_customers': len(retention_data),
            'period_days': period_days
        }
    
    def identify_loyal_customers(self, min_purchases=5):
        """Find loyal customers (repeated purchases)"""
        
        customer_counts = self.df.groupby('customer_id').size()
        
        loyal = customer_counts[customer_counts >= min_purchases]
        
        loyal_df = self.df[self.df['customer_id'].isin(loyal.index)]
        
        loyal_stats = loyal_df.groupby('customer_id').agg({
            'transaction_id': 'count',
            'amount': 'sum',
            'date': ['min', 'max']
        }).reset_index()
        
        loyal_stats.columns = ['customer_id', 'purchases', 'total_spent', 
                               'first_purchase', 'last_purchase']
        
        # Calculate customer tenure
        loyal_stats['tenure_days'] = (
            pd.to_datetime(loyal_stats['last_purchase']) - 
            pd.to_datetime(loyal_stats['first_purchase'])
        ).dt.days
        
        return loyal_stats.sort_values('total_spent', ascending=False)
    
    def calculate_customer_stickiness(self):
        """
        Stickiness = Active days / Total days since first purchase
        """
        
        stickiness_data = []
        
        for customer in self.df['customer_id'].unique():
            customer_data = self.df[self.df['customer_id'] == customer]
            
            first_purchase = customer_data['date'].min()
            last_purchase = customer_data['date'].max()
            
            total_days = (last_purchase - first_purchase).days + 1
            active_days = len(customer_data['date'].unique())
            
            if total_days > 0:
                stickiness = (active_days / total_days) * 100
                stickiness_data.append(stickiness)
        
        avg_stickiness = np.mean(stickiness_data) if stickiness_data else 0
        
        return round(avg_stickiness, 2)
