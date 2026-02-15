import csv
from datetime import datetime

FILE_NAME = "expenses.csv"


# ---------------------------
# Create CSV file if not exists
# ---------------------------
def initialize_file():
    try:
        with open(FILE_NAME, "r", newline="") as file:
            pass
    except FileNotFoundError:
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Amount", "Category", "Note"])


# ---------------------------
# Add Expense
# ---------------------------
def add_expense():
    print("\n--- Add Expense ---")

    date_input = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
    if date_input == "":
        date_input = datetime.today().strftime("%Y-%m-%d")

    try:
        datetime.strptime(date_input, "%Y-%m-%d")
    except ValueError:
        print("❌ Invalid date format. Please use YYYY-MM-DD.")
        return

    try:
        amount = float(input("Enter amount: ₹").strip())
        if amount <= 0:
            print("❌ Amount must be greater than 0.")
            return
    except ValueError:
        print("❌ Please enter a valid amount.")
        return

    category = input("Enter category (Food/Travel/Shopping/etc): ").strip()
    if category == "":
        category = "Other"

    note = input("Enter note (optional): ").strip()

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date_input, amount, category, note])

    print("✅ Expense added successfully!")


# ---------------------------
# View All Expenses
# ---------------------------
def view_expenses():
    print("\n--- All Expenses ---")

    try:
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            rows = list(reader)

        if len(rows) <= 1:
            print("⚠️ No expenses found.")
            return

        print("\nDate         | Amount   | Category     | Note")
        print("-" * 55)

        for row in rows[1:]:
            date, amount, category, note = row
            print(f"{date} | ₹{float(amount):7.2f} | {category:12} | {note}")

    except FileNotFoundError:
        print("⚠️ No file found. Add an expense first.")


# ---------------------------
# Total Spending
# ---------------------------
def total_spending():
    print("\n--- Total Spending ---")

    total = 0.0
    try:
        with open(FILE_NAME, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                total += float(row["Amount"])

        print(f"💰 Total Spending: ₹{total:.2f}")

    except FileNotFoundError:
        print("⚠️ No expenses found.")


# ---------------------------
# Category Summary
# ---------------------------
def category_summary():
    print("\n--- Category Summary ---")

    summary = {}

    try:
        with open(FILE_NAME, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                category = row["Category"]
                amount = float(row["Amount"])
                summary[category] = summary.get(category, 0) + amount

        if not summary:
            print("⚠️ No expenses found.")
            return

        print("\nCategory       | Total")
        print("-" * 30)

        for cat, amt in sorted(summary.items(), key=lambda x: x[1], reverse=True):
            print(f"{cat:14} | ₹{amt:.2f}")

    except FileNotFoundError:
        print("⚠️ No expenses found.")


# ---------------------------
# Search by Category
# ---------------------------
def search_by_category():
    print("\n--- Search Expenses by Category ---")
    search_cat = input("Enter category name: ").strip().lower()

    found = False

    try:
        with open(FILE_NAME, "r") as file:
            reader = csv.DictReader(file)

            print("\nDate         | Amount   | Category     | Note")
            print("-" * 55)

            for row in reader:
                if row["Category"].lower() == search_cat:
                    found = True
                    print(
                        f'{row["Date"]} | ₹{float(row["Amount"]):7.2f} | {row["Category"]:12} | {row["Note"]}'
                    )

        if not found:
            print("⚠️ No expenses found for this category.")

    except FileNotFoundError:
        print("⚠️ No expenses found.")


# ---------------------------
# Main Menu
# ---------------------------
def main():
    initialize_file()

    while True:
        print("\n==============================")
        print("      EXPENSE TRACKER APP     ")
        print("==============================")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Total Spending")
        print("4. Category Summary")
        print("5. Search by Category")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            total_spending()
        elif choice == "4":
            category_summary()
        elif choice == "5":
            search_by_category()
        elif choice == "6":
            print("👋 Exiting... Thank you for using Expense Tracker!")
            break
        else:
            print("❌ Invalid choice. Please enter 1 to 6.")


if __name__ == "__main__":
    main()