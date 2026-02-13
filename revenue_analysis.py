"""
Revenue Analysis Module
Detailed revenue breakdowns and trends
"""

import pandas as pd


class RevenueAnalyzer:
    """Analyze revenue patterns"""
    
    def __init__(self, transactions):
        self.df = transactions.copy()
        self.df['date'] = pd.to_datetime(self.df['date'])
    
    def get_daily_revenue(self):
        """Calculate daily revenue"""
        
        daily = self.df.groupby('date')['amount'].sum().reset_index()
        daily.columns = ['date', 'revenue']
        
        return daily.sort_values('date')
    
    def get_monthly_revenue(self):
        """Calculate monthly revenue"""
        
        self.df['month'] = self.df['date'].dt.to_period('M')
        
        monthly = self.df.groupby('month').agg({
            'amount': 'sum',
            'transaction_id': 'count',
            'customer_id': 'nunique'
        }).reset_index()
        
        monthly.columns = ['month', 'revenue', 'transactions', 'customers']
        monthly['month'] = monthly['month'].astype(str)
        
        # Calculate average per transaction
        monthly['avg_per_transaction'] = monthly['revenue'] / monthly['transactions']
        
        return monthly
    
    def calculate_revenue_growth(self):
        """Month-over-month revenue growth"""
        
        monthly = self.get_monthly_revenue()
        
        # Calculate growth
        monthly['prev_revenue'] = monthly['revenue'].shift(1)
        monthly['growth_pct'] = ((monthly['revenue'] - monthly['prev_revenue']) / 
                                 monthly['prev_revenue'] * 100).round(2)
        
        return monthly
    
    def get_revenue_by_customer_segment(self, rfm_data):
        """
        Revenue breakdown by RFM segment
        Requires RFM data
        """
        
        # Merge with transactions
        merged = self.df.merge(
            rfm_data[['customer_id', 'segment']], 
            on='customer_id', 
            how='left'
        )
        
        segment_revenue = merged.groupby('segment')['amount'].agg(['sum', 'mean', 'count']).reset_index()
        segment_revenue.columns = ['segment', 'total_revenue', 'avg_transaction', 'transactions']
        
        # Calculate percentage
        total_revenue = segment_revenue['total_revenue'].sum()
        segment_revenue['revenue_pct'] = (segment_revenue['total_revenue'] / total_revenue * 100).round(2)
        
        return segment_revenue.sort_values('total_revenue', ascending=False)
    
    def identify_revenue_peaks(self):
        """Find highest revenue days"""
        
        daily = self.get_daily_revenue()
        
        # Get top 10 days
        top_days = daily.nlargest(10, 'revenue')
        
        return top_days
    
    def calculate_revenue_concentration(self):
        """
        Calculate how concentrated revenue is
        Gini coefficient (simplified)
        """
        
        customer_revenue = self.df.groupby('customer_id')['amount'].sum().sort_values()
        
        n = len(customer_revenue)
        cumsum = customer_revenue.cumsum()
        
        # Simplified Gini calculation
        gini = (2 * sum((i + 1) * val for i, val in enumerate(customer_revenue.values))) / (n * cumsum.iloc[-1])
        gini = gini - (n + 1) / n
        
        return round(gini, 3)
    
    def get_revenue_forecast_simple(self, periods=3):
        """
        Simple revenue forecast
        Using moving average
        """
        
        monthly = self.get_monthly_revenue()
        
        # Calculate 3-month moving average
        monthly['ma_3'] = monthly['revenue'].rolling(window=3).mean()
        
        # Last MA value as forecast
        last_ma = monthly['ma_3'].iloc[-1]
        
        # Simple forecast: repeat last MA
        forecast = pd.DataFrame({
            'month': [f'Forecast_{i+1}' for i in range(periods)],
            'forecasted_revenue': [last_ma] * periods
        })
        
        return forecast
