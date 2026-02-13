"""
Retail Customer Intelligence
Main Application - Simple and Clean
"""

import sys
import os
import pandas as pd

sys.path.append('src')

from data_generator import generate_retail_data, save_data
from database import RetailDB
from rfm_analysis import RFMAnalyzer
from visualization import RetailCharts
from excel_report import ExcelReporter
from dashboard_generator import create_html_dashboard


def print_header(text):
    """Simple header"""
    print("\n" + "="*60)
    print(text.center(60))
    print("="*60 + "\n")


def clear_screen():
    """Clear screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def show_menu():
    """Display menu"""
    print("\n" + "="*60)
    print("RETAIL CUSTOMER INTELLIGENCE".center(60))
    print("="*60)
    print("\n1. Generate Transaction Data")
    print("2. RFM Analysis")
    print("3. Customer Segmentation")
    print("4. Generate Charts")
    print("5. Create Excel Reports")
    print("6. Create HTML Dashboard")
    print("7. Business Recommendations")
    print("8. Run Complete Analysis")
    print("9. Exit")
    print("="*60)


def generate_data():
    """Generate retail data"""
    print_header("DATA GENERATION")
    
    data = generate_retail_data(8000)
    save_data(data)
    
    input("\nPress Enter to continue...")
    return data


def perform_rfm_analysis(data):
    """RFM analysis"""
    print_header("RFM ANALYSIS")
    
    analyzer = RFMAnalyzer(data)
    
    # Calculate RFM
    rfm_data = analyzer.calculate_rfm()
    
    # Assign scores
    rfm_data = analyzer.assign_rfm_scores(rfm_data)
    
    # Segment customers
    rfm_data = analyzer.segment_customers(rfm_data)
    
    # Calculate CLV
    rfm_data = analyzer.calculate_customer_value(rfm_data)
    
    # Show summary
    print("\nRFM Summary:")
    print(rfm_data[['customer_id', 'recency', 'frequency', 'monetary', 
                    'R_score', 'F_score', 'M_score', 'segment']].head(10))
    
    input("\nPress Enter to continue...")
    return rfm_data


def show_segmentation(rfm_data):
    """Show customer segmentation"""
    print_header("CUSTOMER SEGMENTATION")
    
    analyzer = RFMAnalyzer(pd.DataFrame())  # Create instance
    segment_summary = analyzer.get_segment_summary(rfm_data)
    
    print("Customer Segments:\n")
    print(segment_summary.to_string(index=False))
    
    # Top 20% analysis
    print("\n" + "-"*60)
    top_customers, contribution = analyzer.identify_top_customers(rfm_data, 20)
    
    input("\nPress Enter to continue...")
    return segment_summary, top_customers


def generate_charts(rfm_data, segment_summary, top_customers):
    """Generate visualizations"""
    print_header("GENERATING CHARTS")
    
    os.makedirs('output', exist_ok=True)
    
    charts = RetailCharts()
    
    print("Creating charts...")
    charts.plot_segment_distribution(segment_summary)
    charts.plot_revenue_by_segment(segment_summary)
    charts.plot_rfm_distribution(rfm_data)
    charts.plot_top_customers(top_customers)
    
    print("\n✓ All charts saved in 'output/' folder")
    input("\nPress Enter to continue...")


def create_excel_reports(rfm_data, segment_summary, top_customers):
    """Create Excel reports"""
    print_header("CREATING EXCEL REPORTS")
    
    os.makedirs('excel', exist_ok=True)
    
    reporter = ExcelReporter()
    
    reporter.create_customer_rfm_report(rfm_data)
    reporter.create_segment_summary_report(segment_summary)
    reporter.create_top_customers_report(top_customers)
    
    print("\n✓ All Excel reports created in 'excel/' folder")
    input("\nPress Enter to continue...")


def create_dashboard(db, segment_summary, top_customers):
    """Create HTML dashboard"""
    print_header("CREATING HTML DASHBOARD")
    
    overall_stats = db.get_overall_stats()
    
    create_html_dashboard(overall_stats, segment_summary, top_customers)
    
    print("\n✓ Dashboard created: dashboard.html")
    print("  → Open in browser to view")
    input("\nPress Enter to continue...")


def business_recommendations(segment_summary, rfm_data):
    """Show business recommendations"""
    print_header("BUSINESS RECOMMENDATIONS")
    
    print("KEY FINDINGS:\n")
    
    # Total customers and revenue
    total_customers = len(rfm_data)
    total_revenue = rfm_data['monetary'].sum()
    
    print(f"1. Customer Base: {total_customers:,} customers")
    print(f"   Total Revenue: ₹{total_revenue:,.2f}")
    
    # Segment breakdown
    print("\n2. Customer Segments:")
    for _, seg in segment_summary.iterrows():
        print(f"   {seg['segment']}: {seg['customer_count']:,} customers "
              f"({seg['revenue_pct']:.1f}% revenue)")
    
    # Top 20% contribution
    top_20_pct = int(total_customers * 0.2)
    top_20 = rfm_data.nlargest(top_20_pct, 'monetary')
    top_20_revenue = top_20['monetary'].sum()
    contribution = (top_20_revenue / total_revenue) * 100
    
    print(f"\n3. Top 20% Customers: {top_20_pct:,} customers")
    print(f"   Revenue Contribution: {contribution:.1f}%")
    
    # At-risk customers
    at_risk = rfm_data[rfm_data['segment'] == 'At Risk']
    if len(at_risk) > 0:
        print(f"\n4. At-Risk Customers: {len(at_risk):,}")
        print(f"   Potential Lost Revenue: ₹{at_risk['monetary'].sum():,.2f}")
    
    print("\n" + "="*60)
    print("RECOMMENDATIONS:")
    print("="*60)
    
    print("""
1. LOYALTY PROGRAM FOR CHAMPIONS
   → Target: Top 10-15% customers (Champions segment)
   → Offer: Exclusive discounts, early access, VIP benefits
   → Expected Impact: 15-20% increase in repeat purchases
   → Implementation: Launch tiered rewards program

2. RE-ENGAGEMENT CAMPAIGN FOR AT-RISK
   → Target: At-Risk segment (haven't purchased recently)
   → Strategy: Personalized email with special offer
   → Timing: Immediate - before they become "Lost"
   → Expected Recovery: 20-30% of at-risk customers

3. NURTURE POTENTIAL LOYALISTS
   → Target: Recent customers (Potential Loyalists)
   → Action: Welcome series, product recommendations
   → Goal: Convert to Champions within 6 months
   → Expected Conversion: 25-35%

4. CATEGORY-SPECIFIC CAMPAIGNS
   → Analyze purchase patterns by category
   → Send targeted product recommendations
   → Cross-sell and upsell opportunities
   → Expected Increase: 10-15% in AOV

5. WIN-BACK LOST CUSTOMERS
   → Target: Lost segment
   → Offer: Strong incentive (20% discount)
   → Low priority (only 5% revenue contribution)
   → ROI may be limited - focus on other segments first
""")
    
    input("\nPress Enter to continue...")


def run_complete_analysis():
    """Run full pipeline"""
    print_header("COMPLETE ANALYSIS PIPELINE")
    
    print("This will:\n")
    print("1. Generate 8,000 transactions")
    print("2. Perform RFM analysis")
    print("3. Segment customers")
    print("4. Calculate CLV")
    print("5. Generate charts")
    print("6. Create Excel reports")
    print("7. Create HTML dashboard\n")
    
    confirm = input("Continue? (y/n): ")
    if confirm.lower() != 'y':
        return
    
    # Generate data
    print("\n[1/7] Generating data...")
    data = generate_retail_data(8000)
    save_data(data)
    
    # Database
    print("\n[2/7] Loading to database...")
    db = RetailDB()
    db.connect()
    db.load_data('data/transactions.csv')
    
    # RFM Analysis
    print("\n[3/7] Performing RFM analysis...")
    analyzer = RFMAnalyzer(data)
    rfm_data = analyzer.calculate_rfm()
    rfm_data = analyzer.assign_rfm_scores(rfm_data)
    rfm_data = analyzer.segment_customers(rfm_data)
    rfm_data = analyzer.calculate_customer_value(rfm_data)
    
    # Segmentation
    print("\n[4/7] Customer segmentation...")
    segment_summary = analyzer.get_segment_summary(rfm_data)
    top_customers, contribution = analyzer.identify_top_customers(rfm_data, 20)
    
    # Charts
    print("\n[5/7] Creating charts...")
    os.makedirs('output', exist_ok=True)
    charts = RetailCharts()
    charts.plot_segment_distribution(segment_summary)
    charts.plot_revenue_by_segment(segment_summary)
    charts.plot_rfm_distribution(rfm_data)
    charts.plot_top_customers(top_customers)
    
    # Excel reports
    print("\n[6/7] Creating Excel reports...")
    os.makedirs('excel', exist_ok=True)
    reporter = ExcelReporter()
    reporter.create_customer_rfm_report(rfm_data)
    reporter.create_segment_summary_report(segment_summary)
    reporter.create_top_customers_report(top_customers)
    
    # Dashboard
    print("\n[7/7] Creating dashboard...")
    overall_stats = db.get_overall_stats()
    create_html_dashboard(overall_stats, segment_summary, top_customers)
    
    # Summary
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE!")
    print("="*60)
    print(f"\nTransactions: {len(data):,}")
    print(f"Customers: {rfm_data['customer_id'].nunique():,}")
    print(f"Total Revenue: ₹{data['amount'].sum():,.2f}")
    print(f"Top 20% Contribution: {contribution:.1f}%")
    
    print("\nGenerated Files:")
    print("  • data/transactions.csv")
    print("  • excel/customer_rfm.xlsx")
    print("  • excel/segment_summary.xlsx")
    print("  • excel/top_customers.xlsx")
    print("  • output/*.png (4 charts)")
    print("  • dashboard.html")
    
    db.close()
    
    input("\nPress Enter to continue...")


def main():
    """Main application"""
    
    db = None
    data = None
    rfm_data = None
    segment_summary = None
    top_customers = None
    
    while True:
        clear_screen()
        show_menu()
        
        try:
            choice = int(input("\nEnter choice: "))
        except ValueError:
            print("Invalid input!")
            input("Press Enter...")
            continue
        
        if choice == 1:
            data = generate_data()
        
        elif choice == 2:
            if data is None:
                data = pd.read_csv('data/transactions.csv')
            rfm_data = perform_rfm_analysis(data)
        
        elif choice == 3:
            if rfm_data is None:
                print("Please run RFM analysis first (Option 2)")
                input("Press Enter...")
                continue
            segment_summary, top_customers = show_segmentation(rfm_data)
        
        elif choice == 4:
            if rfm_data is None or segment_summary is None:
                print("Please complete RFM analysis and segmentation first")
                input("Press Enter...")
                continue
            generate_charts(rfm_data, segment_summary, top_customers)
        
        elif choice == 5:
            if rfm_data is None or segment_summary is None:
                print("Please complete RFM analysis and segmentation first")
                input("Press Enter...")
                continue
            create_excel_reports(rfm_data, segment_summary, top_customers)
        
        elif choice == 6:
            if segment_summary is None:
                print("Please complete segmentation first")
                input("Press Enter...")
                continue
            if db is None:
                db = RetailDB()
                db.connect()
                db.load_data('data/transactions.csv')
            create_dashboard(db, segment_summary, top_customers)
        
        elif choice == 7:
            if rfm_data is None or segment_summary is None:
                print("Please complete analysis first")
                input("Press Enter...")
                continue
            business_recommendations(segment_summary, rfm_data)
        
        elif choice == 8:
            run_complete_analysis()
        
        elif choice == 9:
            if db:
                db.close()
            print("\n" + "="*60)
            print("Thank you!")
            print("\nDeveloper: Akshay Tiwari")
            print("Email: akshay.tiwari@example.com")
            print("\n© 2026 Retail Analytics Project")
            print("="*60 + "\n")
            break
        
        else:
            print("Invalid choice!")
            input("Press Enter...")


if __name__ == "__main__":
    main()
