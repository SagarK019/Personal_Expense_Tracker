
import json
import os
from datetime import datetime

# ==========================================
# FILE CONFIGURATION
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

EXPENSE_FILE = os.path.join(BASE_DIR, "expenses.json")
BUDGET_FILE = os.path.join(BASE_DIR, "budget.json")

expenses = []
budgets = {}


# ==========================================
# DATE AND INPUT HELPERS
# ==========================================

def parse_date(date_text):
    formats = ["%d-%m-%Y", "%Y-%m-%d", "%d/%m/%Y"]

    for date_format in formats:
        try:
            return datetime.strptime(date_text, date_format)
        except ValueError:
            pass

    return None


def get_amount(message):
    while True:
        try:
            amount = float(input(message))

            if amount <= 0:
                print("Amount must be greater than zero.")
                continue

            return round(amount, 2)

        except ValueError:
            print("Please enter a valid number.")


def get_month():
    while True:
        month = input("Enter month (YYYY-MM): ").strip()

        try:
            datetime.strptime(month, "%Y-%m")
            return month
        except ValueError:
            print("Invalid format. Example: 2026-10")


# ==========================================
# FILE HANDLING
# ==========================================

def load_data():
    global expenses, budgets

    try:
        with open(EXPENSE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            expenses = data if isinstance(data, list) else []

    except FileNotFoundError:
        expenses = []

    except (json.JSONDecodeError, OSError) as error:
        print("Could not load expenses:", error)
        expenses = []

    try:
        with open(BUDGET_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            budgets = data if isinstance(data, dict) else {}

    except FileNotFoundError:
        budgets = {}

    except (json.JSONDecodeError, OSError) as error:
        print("Could not load budgets:", error)
        budgets = {}


def save_expenses():
    try:
        with open(EXPENSE_FILE, "w", encoding="utf-8") as file:
            json.dump(expenses, file, indent=4)

    except OSError as error:
        print("Error saving expenses:", error)


def save_budgets():
    try:
        with open(BUDGET_FILE, "w", encoding="utf-8") as file:
            json.dump(budgets, file, indent=4)

    except OSError as error:
        print("Error saving budgets:", error)


# ==========================================
# 1. ADD EXPENSE
# ==========================================

def add_expense():
    print("\n--- ADD EXPENSE ---")

    name = input("Enter expense name: ").strip()

    if not name:
        print("Expense name cannot be empty.")
        return

    category = input("Enter category: ").strip()

    if not category:
        print("Category cannot be empty.")
        return

    amount = get_amount("Enter amount (Rs.): ")

    date_text = input(
        "Enter date (DD-MM-YYYY), or press Enter for today: "
    ).strip()

    if not date_text:
        date_text = datetime.today().strftime("%d-%m-%Y")
    else:
        parsed = parse_date(date_text)

        if parsed is None:
            print("Invalid date. Expense was not added.")
            return

        date_text = parsed.strftime("%d-%m-%Y")

    expense = {
        "name": name,
        "category": category,
        "amount": amount,
        "date": date_text
    }

    expenses.append(expense)
    save_expenses()

    print("Expense added successfully!")


# ==========================================
# 2. VIEW ALL EXPENSES
# ==========================================

def view_expenses():
    print("\n--- ALL EXPENSES ---")

    if not expenses:
        print("No expenses available.")
        return

    for number, item in enumerate(expenses, start=1):
        print(
            f"{number}. {item['name']} | "
            f"{item['category']} | "
            f"Rs. {float(item['amount']):.2f} | "
            f"{item['date']}"
        )


# ==========================================
# 3. TOTAL EXPENSES
# ==========================================

def total_expenses():
    total = sum(float(item["amount"]) for item in expenses)

    print("\n--- TOTAL EXPENSES ---")
    print(f"Total amount spent: Rs. {total:.2f}")


# ==========================================
# 4. SEARCH BY CATEGORY
# ==========================================

def search_category():
    print("\n--- SEARCH BY CATEGORY ---")

    category = input("Enter category: ").strip().lower()

    found = [
        item for item in expenses
        if item["category"].lower() == category
    ]

    if not found:
        print("No expenses found in this category.")
        return

    for item in found:
        print(
            f"{item['name']} | "
            f"Rs. {float(item['amount']):.2f} | "
            f"{item['date']}"
        )


# ==========================================
# 5. CATEGORY-WISE SUMMARY
# ==========================================

def category_summary():
    print("\n--- CATEGORY-WISE SUMMARY ---")

    if not expenses:
        print("No expenses available.")
        return

    summary = {}

    for item in expenses:
        category = item["category"]
        amount = float(item["amount"])

        summary[category] = summary.get(category, 0) + amount

    for category, amount in sorted(summary.items()):
        print(f"{category}: Rs. {amount:.2f}")


# ==========================================
# 6. MONTHLY REPORT
# ==========================================

def monthly_report():
    print("\n--- MONTHLY REPORT ---")

    month = get_month()
    monthly_expenses = []

    for item in expenses:
        date = parse_date(item["date"])

        if date and date.strftime("%Y-%m") == month:
            monthly_expenses.append(item)

    if not monthly_expenses:
        print("No expenses found for this month.")
        return

    total = 0

    for item in monthly_expenses:
        amount = float(item["amount"])
        total += amount

        print(
            f"{item['name']} | "
            f"{item['category']} | "
            f"Rs. {amount:.2f} | "
            f"{item['date']}"
        )

    print("-----------------------------")
    print(f"Monthly total: Rs. {total:.2f}")


# ==========================================
# 7. EDIT EXPENSE
# ==========================================

def edit_expense():
    print("\n--- EDIT EXPENSE ---")

    view_expenses()

    if not expenses:
        return

    try:
        number = int(input("Enter expense number to edit: "))

        if number < 1 or number > len(expenses):
            print("Invalid expense number.")
            return

    except ValueError:
        print("Please enter a valid number.")
        return

    item = expenses[number - 1]

    print("Press Enter to keep the existing value.")

    name = input(f"New name [{item['name']}]: ").strip()
    category = input(
        f"New category [{item['category']}]: "
    ).strip()

    amount_text = input(
        f"New amount [{item['amount']}]: "
    ).strip()

    date_text = input(
        f"New date [{item['date']}]: "
    ).strip()

    if amount_text:
        try:
            amount = float(amount_text)

            if amount <= 0:
                print("Amount must be greater than zero.")
                return

            item["amount"] = round(amount, 2)

        except ValueError:
            print("Invalid amount.")
            return

    if date_text:
        parsed = parse_date(date_text)

        if parsed is None:
            print("Invalid date.")
            return

        item["date"] = parsed.strftime("%d-%m-%Y")

    if name:
        item["name"] = name

    if category:
        item["category"] = category

    save_expenses()
    print("Expense updated successfully!")


# ==========================================
# 8. DELETE EXPENSE
# ==========================================

def delete_expense():
    print("\n--- DELETE EXPENSE ---")

    view_expenses()

    if not expenses:
        return

    try:
        number = int(input("Enter expense number to delete: "))

        if number < 1 or number > len(expenses):
            print("Invalid expense number.")
            return

    except ValueError:
        print("Please enter a valid number.")
        return

    deleted = expenses.pop(number - 1)

    save_expenses()

    print(f"Deleted expense: {deleted['name']}")


# ==========================================
# 9. SET MONTHLY BUDGET
# ==========================================

def set_budget():
    print("\n--- SET MONTHLY BUDGET ---")

    month = get_month()
    amount = get_amount("Enter monthly budget (Rs.): ")

    budgets[month] = amount

    save_budgets()

    print(f"Budget for {month} saved successfully!")


# ==========================================
# 10. VIEW MONTHLY BUDGET
# ==========================================

def view_budget():
    print("\n--- MONTHLY BUDGET ---")

    month = get_month()

    if month not in budgets:
        print("No budget set for this month.")
        return

    budget = float(budgets[month])
    spent = 0

    for item in expenses:
        date = parse_date(item["date"])

        if date and date.strftime("%Y-%m") == month:
            spent += float(item["amount"])

    remaining = budget - spent

    print(f"Monthly budget: Rs. {budget:.2f}")
    print(f"Total spent: Rs. {spent:.2f}")
    print(f"Remaining budget: Rs. {remaining:.2f}")

    if remaining < 0:
        print("Warning: You have exceeded your budget!")
    else:
        print("You are within your budget.")


# ==========================================
# MAIN MENU
# ==========================================

def main():
    load_data()

    while True:
        print("\n" + "=" * 45)
        print("       PERSONAL EXPENSE TRACKER")
        print("=" * 45)

        print("1.  Add Expense")
        print("2.  View All Expenses")
        print("3.  Total Expenses")
        print("4.  Search by Category")
        print("5.  Category-wise Summary")
        print("6.  Monthly Report")
        print("7.  Edit Expense")
        print("8.  Delete Expense")
        print("9.  Set Monthly Budget")
        print("10. View Monthly Budget")
        print("11. Exit")

        print("=" * 45)

        choice = input("Enter a choice: ").strip()

        if choice == "1":
            add_expense()

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            total_expenses()

        elif choice == "4":
            search_category()

        elif choice == "5":
            category_summary()

        elif choice == "6":
            monthly_report()

        elif choice == "7":
            edit_expense()

        elif choice == "8":
            delete_expense()

        elif choice == "9":
            set_budget()

        elif choice == "10":
            view_budget()

        elif choice == "11":
            print("\nThank you for using Personal Expense Tracker!")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 11.")


# ==========================================
# PROGRAM START
# ==========================================

if __name__ == "__main__":
    main()
