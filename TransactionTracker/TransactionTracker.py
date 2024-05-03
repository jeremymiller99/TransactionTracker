import pandas as pd

def load_and_categorize_transactions(file_path):
    df = pd.read_excel(file_path)
    categories = {
        'Groceries': ['walmart', 'market', 'grocery'],
        'Utilities': ['electric', 'water', 'utility'],
        'Dining': ['restaurant', 'cafe', 'diner'],
    }
    def categorize_transaction(description):
        for category, keywords in categories.items():
            if any(keyword.lower() in description.lower() for keyword in keywords):
                return category
        return 'Other'
    df['Category'] = df['Description'].apply(categorize_transaction)
    return df.to_dict('records')

def filter_transactions(transactions, category=None):
    if category:
        return [transaction for transaction in transactions if transaction['Category'] == category]
    return transactions

def display_transactions(transactions):
    for transaction in transactions:
        print(transaction)

def main():
    file_path = 'TransactionHistory.xlsx'  # Update this to your file's path
    transactions = load_and_categorize_transactions(file_path)
    
    while True:
        print("\n--- Transaction Filter Menu ---")
        print("1. View All Transactions")
        print("2. Filter by Category")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            display_transactions(transactions)
        elif choice == '2':
            category = input("Enter category (Groceries, Utilities, Dining, Other): ")
            filtered_transactions = filter_transactions(transactions, category)
            display_transactions(filtered_transactions)
        elif choice == '3':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

if __name__ == "__main__":
    main()
