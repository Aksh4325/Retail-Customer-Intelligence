"""
HTML Dashboard Generator
Create simple Power BI style dashboard
"""


def create_html_dashboard(overall_stats, segment_summary, top_customers):
    """
    Generate simple HTML dashboard
    Power BI style - clean and simple
    """
    
    print("Creating HTML Dashboard...")
    
    # Calculate some key metrics
    total_revenue = overall_stats['total_revenue'].values[0]
    total_customers = overall_stats['total_customers'].values[0]
    avg_value = overall_stats['avg_transaction_value'].values[0]
    
    # Prepare segment data for chart
    segment_data = segment_summary.to_dict('records')
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Retail Customer Intelligence Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }}
        
        .dashboard {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 30px;
        }}
        
        h1 {{
            color: #2c3e50;
            margin-bottom: 30px;
            font-size: 28px;
        }}
        
        .kpi-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .kpi-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .kpi-card.green {{
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        }}
        
        .kpi-card.orange {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }}
        
        .kpi-label {{
            font-size: 14px;
            opacity: 0.9;
            margin-bottom: 8px;
        }}
        
        .kpi-value {{
            font-size: 32px;
            font-weight: bold;
        }}
        
        .segment-section {{
            margin-top: 40px;
        }}
        
        h2 {{
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 22px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        
        th {{
            background: #3498db;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 500;
        }}
        
        td {{
            padding: 12px;
            border-bottom: 1px solid #ddd;
        }}
        
        tr:hover {{
            background: #f8f9fa;
        }}
        
        .revenue-bar {{
            display: inline-block;
            height: 20px;
            background: #3498db;
            border-radius: 3px;
        }}
        
        .top-customers {{
            margin-top: 40px;
        }}
        
        .footer {{
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #7f8c8d;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="dashboard">
        <h1>🛍️ Retail Customer Intelligence Dashboard</h1>
        
        <!-- KPI Cards -->
        <div class="kpi-cards">
            <div class="kpi-card">
                <div class="kpi-label">Total Revenue</div>
                <div class="kpi-value">₹{total_revenue:,.0f}</div>
            </div>
            
            <div class="kpi-card green">
                <div class="kpi-label">Total Customers</div>
                <div class="kpi-value">{total_customers:,}</div>
            </div>
            
            <div class="kpi-card orange">
                <div class="kpi-label">Avg Transaction Value</div>
                <div class="kpi-value">₹{avg_value:,.0f}</div>
            </div>
        </div>
        
        <!-- Customer Segments -->
        <div class="segment-section">
            <h2>📊 Customer Segments Analysis</h2>
            
            <table>
                <thead>
                    <tr>
                        <th>Segment</th>
                        <th>Customers</th>
                        <th>Revenue</th>
                        <th>Revenue %</th>
                        <th>Visual</th>
                    </tr>
                </thead>
                <tbody>
"""
    
    # Add segment rows
    max_revenue = segment_summary['total_revenue'].max()
    for seg in segment_data:
        bar_width = (seg['total_revenue'] / max_revenue) * 300
        html_content += f"""
                    <tr>
                        <td><strong>{seg['segment']}</strong></td>
                        <td>{seg['customer_count']:,}</td>
                        <td>₹{seg['total_revenue']:,.2f}</td>
                        <td>{seg['revenue_pct']:.1f}%</td>
                        <td><div class="revenue-bar" style="width: {bar_width}px;"></div></td>
                    </tr>
"""
    
    html_content += """
                </tbody>
            </table>
        </div>
        
        <!-- Top Customers -->
        <div class="top-customers">
            <h2>🏆 Top 10 Customers</h2>
            
            <table>
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Customer ID</th>
                        <th>Total Spent</th>
                        <th>Purchases</th>
                        <th>Segment</th>
                    </tr>
                </thead>
                <tbody>
"""
    
    # Add top customers
    for idx, customer in top_customers.head(10).iterrows():
        html_content += f"""
                    <tr>
                        <td><strong>#{idx+1}</strong></td>
                        <td>{customer['customer_id']}</td>
                        <td>₹{customer['monetary']:,.2f}</td>
                        <td>{int(customer['frequency'])}</td>
                        <td>{customer['segment']}</td>
                    </tr>
"""
    
    html_content += """
                </tbody>
            </table>
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <p><strong>Retail Customer Intelligence Dashboard</strong></p>
            <p>Developed by: Akshay Tiwari | Email: akshay.tiwari@example.com</p>
            <p>© 2026 College Analytics Project</p>
        </div>
    </div>
</body>
</html>
"""
    
    # Save file
    filename = 'dashboard.html'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ Saved: {filename}")
    print("  → Open in browser to view dashboard")
    
    return filename
