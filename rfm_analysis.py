"""
RFM Analysis
Simple customer segmentation using RFM methodology
"""

import pandas as pd
from datetime import datetime


class RFMAnalyzer:
    """Calculate RFM scores for customers"""
    
    def __init__(self, transactions):
        self.df = transactions.copy()
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.analysis_date = datetime.now()
    
    def calculate_rfm(self):
        """
        Calculate RFM metrics for each customer
        Simple and straightforward
        """
        
        print("\nCalculating RFM scores...")
        
        # Group by customer
        customer_data = self.df.groupby('customer_id').agg({
            'date': lambda x: (self.analysis_date - x.max()).days,  # Recency
            'transaction_id': 'count',  # Frequency
            'amount': 'sum'  # Monetary
        }).reset_index()
        
        customer_data.columns = ['customer_id', 'recency', 'frequency', 'monetary']
        
        print(f"  Analyzed {len(customer_data)} customers")
        
        return customer_data
    
    def assign_rfm_scores(self, rfm_data):
        """
        Assign scores (1-5) to RFM metrics
        Simple bin-based approach
        """
        
        print("Assigning RFM scores...")
        
        # Recency score (lower is better)
        # 5 = bought very recently, 1 = bought long ago
        rfm_data['R_score'] = pd.cut(rfm_data['recency'], 
                                     bins=5, 
                                     labels=[5, 4, 3, 2, 1])
        
        # Frequency score (higher is better)
        # 5 = bought many times, 1 = bought once
        rfm_data['F_score'] = pd.cut(rfm_data['frequency'], 
                                     bins=5, 
                                     labels=[1, 2, 3, 4, 5])
        
        # Monetary score (higher is better)
        # 5 = high spender, 1 = low spender
        rfm_data['M_score'] = pd.cut(rfm_data['monetary'], 
                                     bins=5, 
                                     labels=[1, 2, 3, 4, 5])
        
        # Convert to int
        rfm_data['R_score'] = rfm_data['R_score'].astype(int)
        rfm_data['F_score'] = rfm_data['F_score'].astype(int)
        rfm_data['M_score'] = rfm_data['M_score'].astype(int)
        
        # Combined RFM score
        rfm_data['RFM_score'] = (rfm_data['R_score'].astype(str) + 
                                rfm_data['F_score'].astype(str) + 
                                rfm_data['M_score'].astype(str))
        
        print("  ✓ RFM scores assigned")
        
        return rfm_data
    
    def segment_customers(self, rfm_data):
        """
        Segment customers based on RFM scores
        Simple rule-based segmentation
        """
        
        print("Segmenting customers...")
        
        def get_segment(row):
            """Simple segmentation logic"""
            
            r = row['R_score']
            f = row['F_score']
            m = row['M_score']
            
            # Champions: Best customers
            if r >= 4 and f >= 4 and m >= 4:
                return 'Champions'
            
            # Loyal: Regular customers
            elif r >= 3 and f >= 3:
                return 'Loyal Customers'
            
            # Potential Loyalists: Recent customers
            elif r >= 4 and f <= 2:
                return 'Potential Loyalists'
            
            # At Risk: Used to buy often but haven't recently
            elif r <= 2 and f >= 3:
                return 'At Risk'
            
            # Lost: Haven't bought in long time
            elif r <= 2 and f <= 2:
                return 'Lost'
            
            else:
                return 'Others'
        
        rfm_data['segment'] = rfm_data.apply(get_segment, axis=1)
        
        print("  ✓ Customers segmented")
        
        return rfm_data
    
    def calculate_customer_value(self, rfm_data):
        """
        Calculate Customer Lifetime Value (CLV)
        Simple calculation
        """
        
        # Simple CLV = Average purchase value × Purchase frequency
        # This is a simplified version
        
        avg_purchase = rfm_data['monetary'] / rfm_data['frequency']
        
        # Estimated future purchases (simple: based on frequency)
        # If they buy often, they'll probably buy more in future
        estimated_future = rfm_data['frequency'] * 0.5  # Conservative estimate
        
        # CLV = Average purchase × Expected future purchases
        rfm_data['CLV'] = avg_purchase * estimated_future
        
        return rfm_data
    
    def get_segment_summary(self, rfm_data):
        """Get summary statistics by segment"""
        
        summary = rfm_data.groupby('segment').agg({
            'customer_id': 'count',
            'monetary': 'sum',
            'frequency': 'mean',
            'recency': 'mean',
            'CLV': 'sum'
        }).reset_index()
        
        summary.columns = ['segment', 'customer_count', 'total_revenue', 
                          'avg_frequency', 'avg_recency', 'total_clv']
        
        # Calculate revenue percentage
        total_revenue = summary['total_revenue'].sum()
        summary['revenue_pct'] = (summary['total_revenue'] / total_revenue * 100).round(2)
        
        # Sort by revenue
        summary = summary.sort_values('total_revenue', ascending=False)
        
        return summary
    
    def identify_top_customers(self, rfm_data, percentile=20):
        """
        Identify top X% customers by revenue
        """
        
        # Sort by monetary value
        sorted_customers = rfm_data.sort_values('monetary', ascending=False)
        
        # Get top percentile
        top_n = int(len(sorted_customers) * (percentile / 100))
        top_customers = sorted_customers.head(top_n)
        
        # Calculate their revenue contribution
        top_revenue = top_customers['monetary'].sum()
        total_revenue = rfm_data['monetary'].sum()
        contribution_pct = (top_revenue / total_revenue * 100)
        
        print(f"\nTop {percentile}% customers:")
        print(f"  Customers: {len(top_customers):,}")
        print(f"  Revenue: ₹{top_revenue:,.2f}")
        print(f"  Contribution: {contribution_pct:.1f}% of total revenue")
        
        return top_customers, contribution_pct
