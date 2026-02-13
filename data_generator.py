"""
Retail Transaction Data Generator
Generate realistic customer purchase data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


def generate_retail_data(num_transactions=8000):
    """
    Generate retail transaction data
    Simple and realistic
    """
    
    print(f"Generating {num_transactions} retail transactions...")
    
    # Product categories
    categories = ['Electronics', 'Clothing', 'Home & Kitchen', 
                 'Books', 'Sports', 'Beauty']
    
    # Start date: 2 years ago
    start_date = datetime.now() - timedelta(days=730)
    
    # Generate customers (some will buy multiple times)
    num_customers = int(num_transactions * 0.4)  # ~3,200 customers
    customer_ids = [f"CUST_{i:05d}" for i in range(1, num_customers + 1)]
    
    transactions = []
    transaction_id = 1
    
    # Customer buying behavior
    # Some customers are loyal (buy often)
    # Some buy once and never return
    
    for customer_id in customer_ids:
        # How many times will this customer buy?
        # Most customers: 1-3 purchases
        # Some loyal: 5-15 purchases
        
        if random.random() < 0.15:  # 15% are loyal customers
            num_purchases = random.randint(5, 15)
        else:
            num_purchases = random.randint(1, 3)
        
        # Generate purchases for this customer
        current_date = start_date + timedelta(days=random.randint(0, 600))
        
        for _ in range(num_purchases):
            # Random date within last 2 years
            current_date = current_date + timedelta(days=random.randint(7, 90))
            
            # Ensure date is not in future
            if current_date > datetime.now():
                current_date = datetime.now() - timedelta(days=random.randint(1, 30))
            
            # Product category
            category = random.choice(categories)
            
            # Amount based on category
            if category == 'Electronics':
                amount = round(random.uniform(5000, 50000), 2)
            elif category == 'Clothing':
                amount = round(random.uniform(500, 5000), 2)
            elif category == 'Home & Kitchen':
                amount = round(random.uniform(1000, 10000), 2)
            elif category == 'Books':
                amount = round(random.uniform(200, 2000), 2)
            elif category == 'Sports':
                amount = round(random.uniform(1000, 15000), 2)
            else:  # Beauty
                amount = round(random.uniform(500, 3000), 2)
            
            # Quantity
            quantity = random.randint(1, 5)
            
            transaction = {
                'transaction_id': f"TXN_{transaction_id:06d}",
                'customer_id': customer_id,
                'date': current_date.strftime('%Y-%m-%d'),
                'category': category,
                'amount': amount,
                'quantity': quantity
            }
            
            transactions.append(transaction)
            transaction_id += 1
            
            if transaction_id > num_transactions:
                break
        
        if transaction_id > num_transactions:
            break
        
        # Progress
        if transaction_id % 1000 == 0:
            print(f"  Generated {transaction_id} transactions...")
    
    # Create dataframe
    df = pd.DataFrame(transactions)
    df = df.sort_values('date').reset_index(drop=True)
    
    print(f"\n✓ Generated {len(df)} transactions successfully!")
    
    return df


def save_data(df, filename='data/transactions.csv'):
    """Save to CSV"""
    df.to_csv(filename, index=False)
    print(f"✓ Saved to {filename}")


if __name__ == "__main__":
    # Generate data
    data = generate_retail_data(8000)
    
    # Save
    save_data(data)
    
    # Summary
    print("\n" + "="*50)
    print("DATA SUMMARY")
    print("="*50)
    print(f"Total Transactions: {len(data):,}")
    print(f"Unique Customers: {data['customer_id'].nunique():,}")
    print(f"Date Range: {data['date'].min()} to {data['date'].max()}")
    print(f"Total Revenue: ₹{data['amount'].sum():,.2f}")
    print(f"\nCategory Breakdown:")
    print(data['category'].value_counts())
    print("="*50)
