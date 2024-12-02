
import csv
from datetime import datetime

def process_shb_file(input_file):
    # Initialize lists to store data
    transactions = []
    
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as file:
        # Skip header line
        next(file)
        
        # Process each line
        for line in file:
            # Split by semicolon
            fields = line.strip().split(';')
            
            if len(fields) >= 6:
                date = fields[0]
                service = fields[1]
                currency = fields[2]
                amount = fields[3].replace(',', '')
                status = fields[4]
                reference = fields[5]
                
                # Convert date to datetime object
                try:
                    date_obj = datetime.strptime(date, '%d/%m/%Y')
                except ValueError:
                    continue
                    
                # Create transaction dictionary
                transaction = {
                    'date': date_obj,
                    'service': service,
                    'currency': currency,
                    'amount': float(amount),
                    'status': status,
                    'reference': reference
                }
                
                transactions.append(transaction)
    
    return transactions

def generate_summary(transactions):
    # Calculate total amount
    total_amount = sum(t['amount'] for t in transactions)
    
    # Count transactions by status
    status_count = {}
    for t in transactions:
        status = t['status']
        status_count[status] = status_count.get(status, 0) + 1
        
    # Get date range
    dates = [t['date'] for t in transactions]
    start_date = min(dates)
    end_date = max(dates)
    
    return {
        'total_amount': total_amount,
        'transaction_count': len(transactions),
        'status_count': status_count,
        'date_range': (start_date, end_date)
    }

Generates a transaction summary report from the processed SHB transactions.

The `main()` function reads an input file, processes the transactions, generates a summary, and prints the results. The summary includes the date range, total number of transactions, total amount, and a breakdown of transactions by status.
def main():
    input_file = 'SHB_20241202043634.txt'
    
    # Process transactions
    transactions = process_shb_file(input_file)
    
    # Generate summary
    summary = generate_summary(transactions)
    
    # Print results
    print(f"Transaction Summary")
    print(f"=================")
    print(f"Date Range: {summary['date_range'][0].date()} to {summary['date_range'][1].date()}")
    print(f"Total Transactions: {summary['transaction_count']}")
    print(f"Total Amount: {summary['total_amount']:,.0f} VND")
    print("\nStatus Breakdown:")
    for status, count in summary['status_count'].items():
        print(f"- {status}: {count}")

if __name__ == "__main__":
    main()
