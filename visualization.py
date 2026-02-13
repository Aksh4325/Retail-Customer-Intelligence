"""
Visualization Module
Simple charts for retail analysis
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


class RetailCharts:
    """Create simple retail analysis charts"""
    
    def __init__(self, output_dir='output'):
        self.output_dir = output_dir
        plt.style.use('seaborn-v0_8-whitegrid')
        sns.set_palette("husl")
    
    def plot_segment_distribution(self, segment_summary):
        """Customer segment pie chart"""
        
        plt.figure(figsize=(10, 8))
        
        colors = sns.color_palette('pastel')
        plt.pie(segment_summary['customer_count'], 
               labels=segment_summary['segment'],
               autopct='%1.1f%%',
               colors=colors,
               startangle=90)
        
        plt.title('Customer Distribution by Segment', 
                 fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        filename = f'{self.output_dir}/segment_distribution.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved: {filename}")
    
    def plot_revenue_by_segment(self, segment_summary):
        """Revenue contribution by segment"""
        
        plt.figure(figsize=(12, 6))
        
        # Sort by revenue
        segment_summary = segment_summary.sort_values('total_revenue', ascending=True)
        
        bars = plt.barh(segment_summary['segment'], 
                       segment_summary['total_revenue'],
                       color='steelblue')
        
        plt.title('Revenue by Customer Segment', 
                 fontsize=14, fontweight='bold')
        plt.xlabel('Revenue (₹)', fontsize=11)
        
        # Add value labels
        for bar in bars:
            width = bar.get_width()
            plt.text(width, bar.get_y() + bar.get_height()/2,
                    f'₹{width:,.0f}',
                    ha='left', va='center', fontsize=9)
        
        plt.tight_layout()
        
        filename = f'{self.output_dir}/revenue_by_segment.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved: {filename}")
    
    def plot_rfm_distribution(self, rfm_data):
        """RFM score distribution"""
        
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
        
        # Recency
        ax1.hist(rfm_data['recency'], bins=20, color='coral', edgecolor='black')
        ax1.set_title('Recency Distribution', fontweight='bold')
        ax1.set_xlabel('Days Since Last Purchase')
        ax1.set_ylabel('Number of Customers')
        
        # Frequency
        ax2.hist(rfm_data['frequency'], bins=20, color='skyblue', edgecolor='black')
        ax2.set_title('Frequency Distribution', fontweight='bold')
        ax2.set_xlabel('Number of Purchases')
        ax2.set_ylabel('Number of Customers')
        
        # Monetary
        ax3.hist(rfm_data['monetary'], bins=20, color='lightgreen', edgecolor='black')
        ax3.set_title('Monetary Distribution', fontweight='bold')
        ax3.set_xlabel('Total Amount Spent (₹)')
        ax3.set_ylabel('Number of Customers')
        
        plt.tight_layout()
        
        filename = f'{self.output_dir}/rfm_distribution.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved: {filename}")
    
    def plot_category_revenue(self, category_data):
        """Revenue by category"""
        
        plt.figure(figsize=(10, 6))
        
        category_data = category_data.sort_values('revenue')
        
        plt.barh(category_data['category'], category_data['revenue'],
                color='teal', alpha=0.7)
        
        plt.title('Revenue by Product Category', 
                 fontsize=14, fontweight='bold')
        plt.xlabel('Revenue (₹)', fontsize=11)
        plt.tight_layout()
        
        filename = f'{self.output_dir}/category_revenue.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved: {filename}")
    
    def plot_monthly_trends(self, monthly_data):
        """Monthly revenue trends"""
        
        plt.figure(figsize=(14, 6))
        
        plt.plot(monthly_data['month'], monthly_data['revenue'],
                marker='o', linewidth=2, markersize=6, color='darkblue')
        
        plt.title('Monthly Revenue Trend', fontsize=14, fontweight='bold')
        plt.xlabel('Month', fontsize=11)
        plt.ylabel('Revenue (₹)', fontsize=11)
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        filename = f'{self.output_dir}/monthly_trends.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved: {filename}")
    
    def plot_top_customers(self, top_customers, top_n=10):
        """Top customers bar chart"""
        
        plt.figure(figsize=(10, 6))
        
        top_n_data = top_customers.head(top_n)
        
        plt.bar(range(len(top_n_data)), top_n_data['monetary'],
               color='gold', edgecolor='black')
        
        plt.title(f'Top {top_n} Customers by Revenue', 
                 fontsize=14, fontweight='bold')
        plt.xlabel('Customer Rank', fontsize=11)
        plt.ylabel('Total Spent (₹)', fontsize=11)
        plt.xticks(range(len(top_n_data)), 
                  [f'#{i+1}' for i in range(len(top_n_data))])
        plt.tight_layout()
        
        filename = f'{self.output_dir}/top_customers.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved: {filename}")
