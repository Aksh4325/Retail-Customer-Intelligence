"""
Data Validation Module
Validate and clean data quality issues
"""

import pandas as pd


class DataValidator:
    """Validate transaction data quality"""
    
    def __init__(self, df):
        self.df = df.copy()
        self.issues = []
    
    def check_required_columns(self):
        """Check if all required columns exist"""
        
        required = ['transaction_id', 'customer_id', 'date', 'amount']
        missing = [col for col in required if col not in self.df.columns]
        
        if missing:
            self.issues.append(f"Missing columns: {missing}")
            return False
        
        print("✓ All required columns present")
        return True
    
    def check_null_values(self):
        """Check for null values"""
        
        null_counts = self.df.isnull().sum()
        
        if null_counts.any():
            print("\n⚠ Null values found:")
            for col, count in null_counts[null_counts > 0].items():
                print(f"  {col}: {count} nulls")
                self.issues.append(f"{col} has {count} null values")
            return False
        
        print("✓ No null values")
        return True
    
    def check_duplicates(self):
        """Check for duplicate transactions"""
        
        duplicates = self.df.duplicated(subset=['transaction_id'])
        dup_count = duplicates.sum()
        
        if dup_count > 0:
            print(f"\n⚠ Found {dup_count} duplicate transactions")
            self.issues.append(f"{dup_count} duplicate transaction IDs")
            return False
        
        print("✓ No duplicate transactions")
        return True
    
    def check_data_types(self):
        """Check if data types are correct"""
        
        # Amount should be numeric
        if not pd.api.types.is_numeric_dtype(self.df['amount']):
            print("⚠ Amount column is not numeric")
            self.issues.append("Amount is not numeric")
            return False
        
        print("✓ Data types are correct")
        return True
    
    def check_value_ranges(self):
        """Check if values are in expected ranges"""
        
        # Check for negative amounts
        negative = self.df[self.df['amount'] < 0]
        if len(negative) > 0:
            print(f"\n⚠ Found {len(negative)} negative amounts")
            self.issues.append(f"{len(negative)} negative amounts")
        
        # Check for zero amounts
        zero = self.df[self.df['amount'] == 0]
        if len(zero) > 0:
            print(f"⚠ Found {len(zero)} zero amounts")
            self.issues.append(f"{len(zero)} zero amounts")
        
        # Check for extremely high amounts (outliers)
        q99 = self.df['amount'].quantile(0.99)
        outliers = self.df[self.df['amount'] > q99 * 3]
        if len(outliers) > 0:
            print(f"⚠ Found {len(outliers)} potential outliers")
        
        if len(negative) == 0 and len(zero) == 0:
            print("✓ All amounts are positive")
            return True
        
        return False
    
    def check_date_consistency(self):
        """Check date format and consistency"""
        
        try:
            self.df['date'] = pd.to_datetime(self.df['date'])
            
            # Check for future dates
            today = pd.Timestamp.now()
            future = self.df[self.df['date'] > today]
            
            if len(future) > 0:
                print(f"\n⚠ Found {len(future)} future dates")
                self.issues.append(f"{len(future)} future dates")
                return False
            
            print("✓ Dates are valid")
            return True
            
        except:
            print("⚠ Date column has invalid formats")
            self.issues.append("Invalid date formats")
            return False
    
    def run_all_checks(self):
        """Run all validation checks"""
        
        print("\n" + "="*60)
        print("DATA VALIDATION")
        print("="*60 + "\n")
        
        self.check_required_columns()
        self.check_null_values()
        self.check_duplicates()
        self.check_data_types()
        self.check_value_ranges()
        self.check_date_consistency()
        
        print("\n" + "="*60)
        
        if self.issues:
            print(f"\n⚠ Found {len(self.issues)} issues:")
            for issue in self.issues:
                print(f"  - {issue}")
        else:
            print("\n✓ All validation checks passed!")
        
        return len(self.issues) == 0
    
    def get_data_quality_report(self):
        """Generate data quality report"""
        
        report = {
            'total_rows': len(self.df),
            'total_columns': len(self.df.columns),
            'null_count': self.df.isnull().sum().sum(),
            'duplicate_count': self.df.duplicated().sum(),
            'issues': self.issues
        }
        
        return report
