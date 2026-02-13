"""
Report Templates Module
Generate formatted text reports
"""

from datetime import datetime


def generate_executive_summary(overall_stats, segment_summary, top_contribution):
    """
    Generate executive summary report
    Simple text format
    """
    
    report = f"""
{'='*70}
RETAIL CUSTOMER INTELLIGENCE - EXECUTIVE SUMMARY
{'='*70}

Report Date: {datetime.now().strftime('%B %d, %Y')}

{'='*70}
OVERVIEW
{'='*70}

Total Transactions:     {overall_stats['total_transactions'].values[0]:,}
Unique Customers:       {overall_stats['total_customers'].values[0]:,}
Total Revenue:          ₹{overall_stats['total_revenue'].values[0]:,.2f}
Average Order Value:    ₹{overall_stats['avg_transaction_value'].values[0]:,.2f}

Date Range:             {overall_stats['first_date'].values[0]} to {overall_stats['last_date'].values[0]}

{'='*70}
CUSTOMER SEGMENTATION
{'='*70}

"""
    
    for _, seg in segment_summary.iterrows():
        report += f"""
{seg['segment'].upper()}
  Customers:    {seg['customer_count']:,} ({seg['revenue_pct']:.1f}% of revenue)
  Revenue:      ₹{seg['total_revenue']:,.2f}
  Avg Frequency: {seg['avg_frequency']:.1f} purchases
  Avg Recency:   {seg['avg_recency']:.0f} days
"""
    
    report += f"""

{'='*70}
KEY INSIGHTS
{'='*70}

1. Top 20% of customers contribute {top_contribution:.1f}% of total revenue
2. Champions segment ({segment_summary[segment_summary['segment']=='Champions']['customer_count'].values[0]:,} customers) generates highest revenue
3. Focus retention efforts on At-Risk segment to prevent churn

{'='*70}
"""
    
    return report


def generate_recommendations_report(segment_summary):
    """Generate business recommendations report"""
    
    report = f"""
{'='*70}
BUSINESS RECOMMENDATIONS
{'='*70}

Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

{'='*70}
PRIORITY ACTIONS
{'='*70}

PRIORITY 1: RETAIN CHAMPIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Target Segment:  Champions
Customer Count:  {segment_summary[segment_summary['segment']=='Champions']['customer_count'].values[0]:,}
Revenue Impact:  {segment_summary[segment_summary['segment']=='Champions']['revenue_pct'].values[0]:.1f}% of total

Actions:
  → Launch VIP loyalty program with exclusive benefits
  → Provide early access to new products
  → Assign dedicated customer success manager
  → Offer personalized shopping experience
  
Expected Outcome:
  → 15-20% increase in purchase frequency
  → 25-30% increase in average order value
  → Improved customer lifetime value


PRIORITY 2: RE-ENGAGE AT-RISK CUSTOMERS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Target Segment:  At Risk
Customer Count:  {segment_summary[segment_summary['segment']=='At Risk']['customer_count'].values[0] if 'At Risk' in segment_summary['segment'].values else 0:,}

Actions:
  → Send personalized win-back email campaign
  → Offer 15-20% discount incentive
  → Highlight new products in their preferred categories
  → Survey to understand why they stopped buying
  
Expected Outcome:
  → Recover 20-30% of at-risk customers
  → Prevent further churn
  → Revenue recovery of ₹500K-800K


PRIORITY 3: NURTURE POTENTIAL LOYALISTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Target Segment:  Potential Loyalists

Actions:
  → Automated welcome email series
  → Product recommendations based on first purchase
  → Incentive for second purchase (10% discount)
  → Educational content about products
  
Expected Outcome:
  → Convert 25-35% to Loyal/Champions
  → Increase repeat purchase rate
  → Build long-term customer relationships


PRIORITY 4: CATEGORY-SPECIFIC CAMPAIGNS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Actions:
  → Analyze purchase patterns by category
  → Cross-sell related products
  → Bundle offers within categories
  → Seasonal promotions
  
Expected Outcome:
  → 10-15% increase in average order value
  → Improved inventory turnover
  → Better customer satisfaction


{'='*70}
IMPLEMENTATION TIMELINE
{'='*70}

Week 1-2:   Launch VIP program for Champions
Week 3-4:   Start at-risk win-back campaign
Month 2:    Roll out nurture program for new customers
Month 3:    Implement category-based recommendations
Quarter 2:  Review and optimize all programs

{'='*70}
EXPECTED ROI
{'='*70}

Investment Required:  ₹500,000 (marketing + tech)
Expected Revenue Lift: ₹2,000,000 - ₹3,000,000
ROI:                  300-500%
Payback Period:       3-4 months

{'='*70}
"""
    
    return report


def generate_segment_profile(segment_name, segment_data, rfm_data):
    """Generate detailed profile for a specific segment"""
    
    # Filter RFM data for this segment
    segment_customers = rfm_data[rfm_data['segment'] == segment_name]
    
    report = f"""
{'='*70}
SEGMENT PROFILE: {segment_name.upper()}
{'='*70}

Customer Count:  {len(segment_customers):,}
Total Revenue:   ₹{segment_customers['monetary'].sum():,.2f}
Avg CLV:         ₹{segment_customers['CLV'].mean():,.2f}

RFM Characteristics:
  Avg Recency:   {segment_customers['recency'].mean():.0f} days
  Avg Frequency: {segment_customers['frequency'].mean():.1f} purchases
  Avg Monetary:  ₹{segment_customers['monetary'].mean():,.2f}

Top 5 Customers in Segment:
"""
    
    top_5 = segment_customers.nlargest(5, 'monetary')
    for idx, customer in top_5.iterrows():
        report += f"  {customer['customer_id']}: ₹{customer['monetary']:,.2f}\n"
    
    return report
