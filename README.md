# 🛍️ Retail Customer Intelligence

AI-Driven Customer Segmentation & Retention Strategy using RFM Analysis

## 📊 Project Overview

A retail analytics project analyzing 8,000 transactions to segment customers, identify high-value segments, and develop retention strategies.

**Key Results:**
- ✅ RFM-based customer segmentation
- ✅ Top 20% customers contribute ~55% revenue
- ✅ Customer Lifetime Value (CLV) calculation
- ✅ HTML Dashboard + Excel Reports

## 🎯 Features

### RFM Analysis
- **R**ecency: Days since last purchase
- **F**requency: Number of purchases
- **M**onetary: Total amount spent
- Simple 1-5 scoring system

### Customer Segments
- **Champions**: Best customers (R=5, F=5, M=5)
- **Loyal**: Regular customers
- **Potential Loyalists**: New customers
- **At Risk**: Haven't bought recently
- **Lost**: Churned customers

### Key Metrics
- Customer Lifetime Value (CLV)
- Revenue Contribution Ratio
- Repeat Purchase Rate
- Average Order Value
- Segment-wise performance

### Outputs
- **Excel Reports** (3 files)
- **HTML Dashboard** (Power BI style)
- **Charts** (4 visualizations)
- **Business Recommendations**

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python main.py

# Select Option 8: "Run Complete Analysis"
```

## 📈 Sample Results

```
Total Customers: 3,500
Total Revenue: ₹4,250,000

Customer Segments:
  Champions:    350 (10%)  →  ₹2,100,000 (49%)
  Loyal:        525 (15%)  →  ₹1,020,000 (24%)
  At Risk:      525 (15%)  →  ₹510,000 (12%)
  
Top 20% Customers contribute: 55% of revenue ✅
```

## 🛍️ RFM Scoring

**Recency (R):**
- Score 5: < 30 days (Recent buyer)
- Score 1: > 365 days (Long time ago)

**Frequency (F):**
- Score 5: 10+ purchases
- Score 1: 1 purchase

**Monetary (M):**
- Score 5: High spender
- Score 1: Low spender

## 💡 Business Recommendations

### 1. Loyalty Program
- Target: Champions segment
- Offer: VIP benefits, exclusive discounts
- Expected: 15-20% increase in repeat purchases

### 2. Re-engagement Campaign
- Target: At-Risk customers
- Strategy: Personalized offers
- Expected Recovery: 20-30%

### 3. Nurture New Customers
- Target: Potential Loyalists
- Goal: Convert to Champions
- Expected Conversion: 25-35%

## 💻 Tech Stack

```
Python:  Pandas (RFM calculations)
Excel:   openpyxl (Reports)
Charts:  Matplotlib, Seaborn
SQL:     SQLite (Queries)
Dashboard: HTML/CSS (Power BI style)
```

## 📁 Project Structure

```
retail-intelligence/
├── data/
│   └── transactions.csv
├── src/
│   ├── data_generator.py
│   ├── database.py
│   ├── rfm_analysis.py
│   ├── visualization.py
│   ├── excel_report.py
│   └── dashboard_generator.py
├── excel/
│   ├── customer_rfm.xlsx
│   ├── segment_summary.xlsx
│   └── top_customers.xlsx
├── output/
│   └── charts/
├── dashboard.html
├── main.py
└── README.md
```

## 📊 Generated Files

### Excel Reports
1. **customer_rfm.xlsx** - All customers with RFM scores
2. **segment_summary.xlsx** - Segment performance
3. **top_customers.xlsx** - Top 50 customers

### Charts
1. Segment distribution (pie chart)
2. Revenue by segment (bar chart)
3. RFM distribution (histograms)
4. Top customers (bar chart)

### Dashboard
- **dashboard.html** - Interactive HTML dashboard
- Opens in any browser
- Power BI style design
- Key metrics cards
- Segment analysis table
- Top customers list

## 🎓 Academic Value

**Skills Demonstrated:**
- RFM Analysis methodology
- Customer segmentation
- CLV calculation
- Data visualization
- Excel reporting
- Dashboard creation

**Perfect for:**
- Retail analytics portfolio
- Marketing analytics projects
- Customer intelligence studies
- Resume showcase

## 📋 RFM Segments Explained

| Segment | R | F | M | Action |
|---------|---|---|---|--------|
| Champions | 5 | 5 | 5 | Reward, engage |
| Loyal | 4-5 | 4-5 | 4-5 | Upsell, cross-sell |
| Potential | 5 | 1-2 | 3-5 | Nurture, educate |
| At Risk | 1-2 | 4-5 | 4-5 | Win back, re-engage |
| Lost | 1 | 1 | 1-5 | Ignore or win back |

## 📝 License

MIT License - see [LICENSE](LICENSE) file

---

## 👨‍💻 Developer

**Akshay Tiwari**
- Data Analyst | Buisness Intelligence 
- Email: tiwariaksh25@gmail.com

**Ayush patidar**
- Web Developer | Software Tester 
- Email: ayushpatidar@gmail.com

---

## 🎓 Academic Information

**Institution:** Medicaps University 

**Program:** Data Analytics / Business intelligence 

**Year:** 2025 

**Project Type:** Learning Purpose 

---

## 🙏 Acknowledgments

- Python community for amazing libraries
- SQLite for lightweight database
- Plotly for interactive visualizations
- College professors for guidance
- Streamlit cloud for deployment 

---

## 📞 Support

For questions or issues:
- 📧 Email: tiwariaksh25@gmail.com
- 🐛 GitHub Issues: [Create Issue]
- 📖 Documentation: See setup guides

---

**© 2025 Akshay Tiwari | Aayush Patidar. All Rights Reserved.**

*Built with 💙 for data analytics*

