"""
Product Analysis Module
Analyze product category performance
"""

import pandas as pd


class ProductAnalyzer:
    """Analyze product categories and trends"""
    
    def __init__(self, transactions):
        self.df = transactions.copy()
        self.df['date'] = pd.to_datetime(self.df['date'])
    
    def get_category_performance(self):
        """Analyze each product category"""
        
        category_stats = self.df.groupby('category').agg({
            'transaction_id': 'count',
            'amount': ['sum', 'mean', 'min', 'max'],
            'quantity': 'sum',
            'customer_id': 'nunique'
        }).round(2)
        
        category_stats.columns = ['transactions', 'total_revenue', 'avg_amount', 
                                   'min_amount', 'max_amount', 'total_quantity', 
                                   'unique_customers']
        
        # Calculate revenue percentage
        total_revenue = category_stats['total_revenue'].sum()
        category_stats['revenue_pct'] = (category_stats['total_revenue'] / total_revenue * 100).round(2)
        
        return category_stats.sort_values('total_revenue', ascending=False)
    
    def get_bestselling_categories(self):
        """Top categories by transactions"""
        
        category_counts = self.df['category'].value_counts()
        
        return category_counts
    
    def get_category_trends(self):
        """Category sales trends over time"""
        
        # Group by month and category
        self.df['month'] = self.df['date'].dt.to_period('M')
        
        trends = self.df.groupby(['month', 'category'])['amount'].sum().reset_index()
        trends['month'] = trends['month'].astype(str)
        
        return trends
    
    def get_cross_sell_opportunities(self):
        """
        Find categories often bought together
        Simple co-occurrence analysis
        """
        
        # Get customers and their categories
        customer_categories = self.df.groupby('customer_id')['category'].apply(list)
        
        # Count category combinations
        combinations = {}
        
        for categories in customer_categories:
            unique_cats = list(set(categories))
            
            # If customer bought from multiple categories
            if len(unique_cats) > 1:
                for i, cat1 in enumerate(unique_cats):
                    for cat2 in unique_cats[i+1:]:
                        pair = tuple(sorted([cat1, cat2]))
                        combinations[pair] = combinations.get(pair, 0) + 1
        
        # Convert to dataframe
        if combinations:
            cross_sell = pd.DataFrame([
                {'category_1': pair[0], 'category_2': pair[1], 'count': count}
                for pair, count in combinations.items()
            ])
            
            return cross_sell.sort_values('count', ascending=False)
        
        return None
    
    def calculate_category_growth(self):
        """Calculate growth rate by category"""
        
        # Get first and last month for each category
        self.df['month'] = self.df['date'].dt.to_period('M')
        
        monthly_category = self.df.groupby(['month', 'category'])['amount'].sum().reset_index()
        
        growth_rates = {}
        
        for category in monthly_category['category'].unique():
            cat_data = monthly_category[monthly_category['category'] == category].sort_values('month')
            
            if len(cat_data) >= 2:
                first_month_revenue = cat_data.iloc[0]['amount']
                last_month_revenue = cat_data.iloc[-1]['amount']
                
                if first_month_revenue > 0:
                    growth = ((last_month_revenue - first_month_revenue) / first_month_revenue) * 100
                    growth_rates[category] = round(growth, 2)
        
        return growth_rates
