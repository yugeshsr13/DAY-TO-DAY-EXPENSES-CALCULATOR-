import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('transactions.db')
cursor = conn.cursor()

# Create transactions table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT,
                    amount REAL,
                    type TEXT
                )''')

def add_transaction(transaction_type):
    description = input("Enter transaction description: ")
    amount = float(input("Enter transaction amount: "))
    cursor.execute("INSERT INTO transactions (description, amount, type) VALUES (?, ?, ?)", (description, amount, transaction_type))
    conn.commit()
    print("Transaction added successfully!")

def delete_history():
    choice = input("Are you sure you want to delete transaction history? (y/n): ")
    if choice.lower() == "y":
        cursor.execute("DELETE FROM transactions")
        conn.commit()
        print("Transaction history deleted.")
    else:
        print("Deletion canceled.")

def calculate_total_expenses():
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='expense'")
    total_expenses = cursor.fetchone()[0]
    return total_expenses if total_expenses else 0

def calculate_total_income():
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='income'")
    total_income = cursor.fetchone()[0]
    return total_income if total_income else 0

def display_transactions():
    cursor.execute("SELECT id, description, amount, type FROM transactions")
    transactions = cursor.fetchall()

    print("Transactions:")
    for transaction in transactions:
        print(f"{transaction[0]} - {transaction[1]}: ${transaction[2]} ({transaction[3]})")

    total_expenses = calculate_total_expenses()
    total_income = calculate_total_income()
    net_balance = total_income - total_expenses
    print("Total expenses:", total_expenses)
    print("Total income:", total_income)
    print("Net balance:", net_balance)

def main():
    while True:
        print("\nExpense and Income Tracker")
        print("1. Add Expense")
        print("2. Add Income")
        print("3. Display Transactions")
        print("4. Delete Transaction History")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_transaction("expense")
        elif choice == "2":
            add_transaction("income")
        elif choice == "3":
            display_transactions()
        elif choice == "4":
            delete_history()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()
