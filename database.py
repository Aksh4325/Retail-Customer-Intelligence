"""
Database Operations
Simple SQL queries for retail analysis
"""

import sqlite3
import pandas as pd


class RetailDB:
    """Simple database for retail transactions"""
    
    def __init__(self, db_path='database/retail.db'):
        self.db_path = db_path
        self.conn = None
    
    def connect(self):
        """Connect to database"""
        self.conn = sqlite3.connect(self.db_path)
        print("✓ Connected to database")
    
    def load_data(self, csv_path):
        """Load CSV into database"""
        df = pd.read_csv(csv_path)
        df.to_sql('transactions', self.conn, if_exists='replace', index=False)
        print(f"✓ Loaded {len(df)} transactions")
    
    # ========== SIMPLE SQL QUERIES ==========
    
    def get_overall_stats(self):
        """Basic statistics"""
        query = """
        SELECT 
            COUNT(*) as total_transactions,
            COUNT(DISTINCT customer_id) as total_customers,
            SUM(amount) as total_revenue,
            AVG(amount) as avg_transaction_value,
            MIN(date) as first_date,
            MAX(date) as last_date
        FROM transactions
        """
        return pd.read_sql_query(query, self.conn)
    
    def get_revenue_by_category(self):
        """Revenue breakdown by category"""
        query = """
        SELECT 
            category,
            COUNT(*) as transactions,
            SUM(amount) as revenue,
            ROUND(AVG(amount), 2) as avg_amount
        FROM transactions
        GROUP BY category
        ORDER BY revenue DESC
        """
        return pd.read_sql_query(query, self.conn)
    
    def get_customer_stats(self):
        """Customer purchase statistics"""
        query = """
        SELECT 
            customer_id,
            COUNT(*) as purchase_count,
            SUM(amount) as total_spent,
            AVG(amount) as avg_purchase,
            MIN(date) as first_purchase,
            MAX(date) as last_purchase
        FROM transactions
        GROUP BY customer_id
        """
        return pd.read_sql_query(query, self.conn)
    
    def get_monthly_revenue(self):
        """Monthly revenue trends"""
        query = """
        SELECT 
            strftime('%Y-%m', date) as month,
            COUNT(*) as transactions,
            SUM(amount) as revenue
        FROM transactions
        GROUP BY month
        ORDER BY month
        """
        return pd.read_sql_query(query, self.conn)
    
    def get_repeat_customers(self):
        """Identify repeat customers"""
        query = """
        SELECT 
            customer_id,
            COUNT(*) as purchase_count
        FROM transactions
        GROUP BY customer_id
        HAVING COUNT(*) > 1
        """
        return pd.read_sql_query(query, self.conn)
    
    def get_top_customers(self, limit=20):
        """Top customers by revenue"""
        query = f"""
        SELECT 
            customer_id,
            COUNT(*) as transactions,
            SUM(amount) as total_revenue,
            ROUND(AVG(amount), 2) as avg_purchase
        FROM transactions
        GROUP BY customer_id
        ORDER BY total_revenue DESC
        LIMIT {limit}
        """
        return pd.read_sql_query(query, self.conn)
    
    def close(self):
        """Close connection"""
        if self.conn:
            self.conn.close()
            print("✓ Database closed")
