from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
from datetime import datetime

app = Flask(__name__)

CATEGORIES = ['Business Supplies', 'Business Operations', 'Utilities', 'Transportation', 'Other']

# Placeholder for storing transactions in memory
transactions = []

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            df = pd.read_excel(file)
            # Ensure your Excel file has the necessary columns; you might need to adjust these names
            # Initialize user category and tag with empty strings
            df['UserCategory'] = ''  
            df['UserTag'] = ''
            # Convert date to string format for consistency
            df['Date'] = pd.to_datetime(df.get('Date', pd.Timestamp('today'))).dt.strftime('%Y-%m-%d')
            global transactions
            transactions = df.to_dict('records')
            return redirect(url_for('view_transactions'))
    return render_template('upload.html')

@app.route('/view', methods=['GET', 'POST'])
def view_transactions():
    search_query = request.form.get('search', '')  # Get search term from the form
    filtered_transactions = [transaction for transaction in transactions if search_query.lower() in transaction['Description'].lower()]
    return render_template('transactions.html', transactions=filtered_transactions, categories=CATEGORIES)

@app.route('/update-transaction', methods=['POST'])
def update_transaction():
    transaction_id = int(request.form.get('transaction_id'))
    new_category = request.form.get('category', '')
    new_tag = request.form.get('tag', '')

    if 0 <= transaction_id < len(transactions):
        transactions[transaction_id]['UserCategory'] = new_category
        transactions[transaction_id]['UserTag'] = new_tag

    return redirect(url_for('view_transactions'))

@app.route('/tag-transaction', methods=['POST'])
def tag_transaction():
    # Retrieve the transaction ID and new tag/category from the submitted form data
    transaction_id = int(request.form.get('transaction_id'))
    new_category = request.form.get('category', '')
    new_tag = request.form.get('tag', '')

    # Ensure the transaction ID is within bounds
    if 0 <= transaction_id < len(transactions):
        # Update the specific transaction with the new category and tag
        transactions[transaction_id]['UserCategory'] = new_category
        transactions[transaction_id]['UserTag'] = new_tag
    else:
        # Handle the case where the transaction ID is not valid (optional)
        print(f"Invalid transaction ID: {transaction_id}")

    # Redirect to the transaction view page to see the updates
    return redirect(url_for('view_transactions'))

@app.route('/update-multiple-transactions', methods=['POST'])
def update_multiple_transactions():
    transaction_ids = request.form.getlist('transaction_ids')  # Gets a list of selected transaction IDs
    new_category = request.form.get('category', '')
    new_tag = request.form.get('tag', '')

    for transaction_id in transaction_ids:
        transaction_id = int(transaction_id)  # Convert to integer
        if 0 <= transaction_id < len(transactions):
            transactions[transaction_id]['UserCategory'] = new_category
            transactions[transaction_id]['UserTag'] = new_tag
        else:
            print(f"Invalid transaction ID: {transaction_id}")

    return redirect(url_for('view_transactions'))

if __name__ == '__main__':
    app.run(debug=True)
