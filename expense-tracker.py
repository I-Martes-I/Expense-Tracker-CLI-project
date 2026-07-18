import argparse
import sys
import json
import csv
import datetime
import calendar

parser = argparse.ArgumentParser(description="Expense Tracker")
subparsers = parser.add_subparsers(dest="command")

#   "add" subcommand
add = subparsers.add_parser("add")
add.add_argument('--description', '--d', type=str, metavar='', required=True, help="Expense description")
add.add_argument('--amount', '--a', type=int, metavar='', required=True, help="Expense description")
add.add_argument('--category', '--c', type=str, metavar='', required=False, help="Expense category")
add.add_argument('--date', '--t', type=str, metavar='', required=False, help="Expense creaton date")

#   "update" subcommand
update = subparsers.add_parser("update")
update.add_argument('--id', type=int, metavar='', required=True, help="Expense ID")
update.add_argument('--description', '--d', type=str, metavar='', required=False, help="Expense description")
update.add_argument('--amount', '--a', type=int, metavar='', required=False, help="Expense description")
update.add_argument('--category', '--c', type=str, metavar='', required=False, help="Expense category")
update.add_argument('--date', '--t', type=int, metavar='', required=False, help="Expense creaton date")

#   "delete" subcommand
delete = subparsers.add_parser("delete")
delete.add_argument('--id', type=int, metavar='', required=True, help="Expense ID")

#   "list" subcommand
list_parser = subparsers.add_parser("list")
list_parser.add_argument('--category', '--c', nargs='?', const='all', default=None, metavar='', help="Filter by category")
list_parser.add_argument('--month', '--m', type=int, metavar='', required=False, help="Expenses by month")
list_parser.add_argument('--year', '--y', type=int, metavar='', required=False, help="Expenses by year")

#   "budget" subcommand
budget = subparsers.add_parser("budget")
budget.add_argument('--month', '--m', type=int, metavar='', required=False, help="Month budget")
budget.add_argument('--year', '--y', type=int, metavar='', required=False, help="Year budget")
budget.add_argument('--amount', '--a', type=int, metavar='', required=False, help="Budget amount")

#   "summary" subcommand
summary = subparsers.add_parser("summary")
summary.add_argument('--month', type=int, metavar='', required=False)
summary.add_argument('--year', type=int, metavar='', required=False)

#   "export" subcommand
export = subparsers.add_parser("export")
export.add_argument('--expenses', '--e', action='store_true', help="Export expenses")
export.add_argument('--budget', '--b', action='store_true', help="Export budget")
export.add_argument('--output', '--o', type=str, metavar='', required=False, help="Output filename")

args = parser.parse_args()

def create_expense(args, expenses, budget_data):
    if args.amount <= 0:
        print("Amount must be a positive number!")
        return
    if args.date:
        try:
            datetime.datetime.fromisoformat(args.date)
        except ValueError:
            print("Invalid date format! Use ISO format: 2026-07-14")
            return
    if expenses:
        new_id = max(expense["id"] for expense in expenses) + 1
    else:
        new_id = 1
        
    new_expense = {
        "id": new_id,
        "description": args.description,
        "amount": args.amount,
        "date": args.date if args.date else datetime.datetime.now().isoformat(),
        "category": args.category if args.category else "default"
    }
    expenses.append(new_expense)
    print(f"Expense added successfully (ID: {new_id})")
    budget_warn(budget_data, expenses)

def delete_expense(args, expenses):
    id_exists = any(expense.get('id') == args.id for expense in expenses)
    if id_exists:
        print("Expense deleted successfully")
        return [expense for expense in expenses if expense["id"] != args.id]
    else:
        print("Expense with such ID wasn't found")
        return expenses

def update_expense(args, expenses, budget_data):
    if args.amount and args.amount <= 0:
        print("Amount must be a positive number!")
        return
    if args.date:
        try:
            datetime.datetime.fromisoformat(args.date)
        except ValueError:
            print("Invalid date format! Use ISO format: 2026-07-14")
            return
    id_exists = False
    for expense in expenses:
        if expense["id"] == args.id:
            id_exists = True
            if args.description: expense["description"] = args.description
            if args.amount: expense["amount"] = args.amount
            if args.category: expense["category"] = args.category
            if args.date: expense["date"] = args.date
            break
    if id_exists:
        print(f"Expense updated successfully")
    else:
        print("Expense whith such ID wasn't found")
    budget_warn(budget_data, expenses)

def print_expenses_table(expenses):
    if not expenses:
        print("No expenses found!")
        return
    id_len = 4
    description_len = 12
    amount_len = 8
    category_len = 8
    date_len = 10
    for expense in expenses:
        if len(str(expense["id"])) > id_len: id_len = len(str(expense["id"]))
        if len(expense["description"]) > description_len: description_len = len(expense["description"])
        if len(str(expense["amount"])) > amount_len: amount_len = len(str(expense["amount"]))
        if len(expense["category"]) > category_len: category_len = len(expense["category"])
        if len(expense["date"]) > date_len: date_len = len(str(expense["date"]))
    headers = f"{'ID':<{id_len}} {'Description':<{description_len}} {'Amount':<{amount_len}} {'Category':<{category_len}} {'Date':<{date_len}}"
    print(headers)
    for expense in expenses:
        print(f"{expense['id']:<{id_len}} {expense['description']:<{description_len}} {expense['amount']:<{amount_len}} {expense['category']:<{category_len}} {expense['date'][:19].replace('T', ' '):<{date_len}}")

def list_expenses(args, expenses):
    filtered = expenses
    if args.month or args.year:
        filtered = []
        for expense in expenses:
            date = datetime.datetime.fromisoformat(expense["date"])
            if args.month and args.month != date.month:
                continue
            if args.year and args.year != date.year:
                continue
            filtered.append(expense)

    if args.category == 'all':
        categories = set(expense["category"] for expense in filtered)
        print("All categories:")
        for cat in sorted(categories):
            print(f"  - {cat}")
    elif args.category:
        filtered = [e for e in filtered if e["category"].lower() == args.category.lower()]
        print(f"Expenses for category '{args.category}':")
        print_expenses_table(filtered)
    else:
        print("List of all expenses:")
        print_expenses_table(filtered)

def list_summary(args, expenses):
    count = 0
    if args.year and args.month:
        for expense in expenses:
            date = datetime.datetime.fromisoformat(expense["date"])
            if args.year == date.year and args.month == date.month: 
                count += expense["amount"]
        print(f"Total expenses for {list(calendar.month_name)[args.month]} {args.year}: ${count}")
    elif args.month:
        for expense in expenses:
            date = datetime.datetime.fromisoformat(expense["date"])
            if args.month == date.month: 
                count += expense["amount"]
        print(f"Total expenses for {list(calendar.month_name)[args.month]}: ${count}")
    elif args.year:
        for expense in expenses:
            date = datetime.datetime.fromisoformat(expense["date"])
            if args.year == date.year: 
                count += expense["amount"]
        print(f"Total expenses for year {args.year}: ${count}")
    else: 
        for expense in expenses:
            count += expense["amount"]
        print(f"Total expenses: ${count}")

def set_budget(args, budget_data):
    now = datetime.datetime.now()
    year = str(args.year if args.year else now.year)
    month = str(args.month) if args.month else None
    if args.amount:
        # Set budget
        if year not in budget_data:
            budget_data[year] = {"budget": 0, "months": {}}
        if month:
            budget_data[year]["months"][month] = args.amount
            print(f"Budget for {calendar.month_name[int(month)]} {year} set to ${args.amount}")
        else:
            budget_data[year]["budget"] = args.amount
            print(f"Budget for {year} set to ${args.amount}")
    else:
        # Show budget
        for year in sorted(budget_data.keys()):
            print(f"Budget for {year}: ${budget_data[year]['budget']}")
            for month, amount in sorted(budget_data[year]["months"].items(), key=lambda x: int(x[0])):
                print(f"  {calendar.month_name[int(month)]}: ${amount}")

def budget_warn(budget_data, expenses):
    now = datetime.datetime.now()
    current_year = str(now.year)
    current_month = str(now.month)

    if current_year not in budget_data:
        return

    year_sum = 0
    for expense in expenses:
        date = datetime.datetime.fromisoformat(expense["date"])
        if now.year == date.year:
            year_sum += expense["amount"]
    if budget_data[current_year]['budget'] < year_sum and budget_data[current_year]['budget'] != 0:
        print(f"Budget for {current_year} exceeded! Year budget is ${budget_data[current_year]['budget']}, but you spent ${year_sum}!")

    if current_month not in budget_data[current_year]["months"]:
        return
    month_sum = 0
    for expense in expenses:
        date = datetime.datetime.fromisoformat(expense["date"])
        if now.year == date.year and now.month == date.month:
            month_sum += expense["amount"]
    month_budget = budget_data[current_year]["months"][current_month]
    if month_budget < month_sum and month_budget != 0:
        print(f"Budget for {calendar.month_name[now.month]} {current_year} exceeded! Month budget is ${month_budget}, but you spent ${month_sum}!")

def export_csv(args, expenses, budget_data):
    if not args.expenses and not args.budget:
        print("Specify --expenses or --budget (or both)")
        return
    
    if args.expenses:
        filename = args.output if args.output else "expenses.csv"
        with open(filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["id", "description", "amount", "date", "category"])
            writer.writeheader()
            writer.writerows(expenses)
        print(f"Expenses exported to {filename}")

    if args.budget:
        filename = args.output if args.output else "budget.csv"
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["year", "yearly_budget", "month", "monthly_budget"])
            for year, data in sorted(budget_data.items()):
                writer.writerow([year, data["budget"], "", ""])
                for month, amount in sorted(data["months"].items(), key=lambda x: int(x[0])):
                    writer.writerow(["", "", calendar.month_name[int(month)], amount])
        print(f"Budget exported to {filename}")

if __name__ == "__main__":
# Open JSON
    try:
        with open("expenses.json", "r") as file:
            expenses = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        expenses = []

    try:
        with open("budgets.json", "r") as file:
            budget_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        budget_data = {}

# If no command 
    if args.command is None:
        parser.print_help()
        sys.exit(1)

# Main commands
    if args.command == "add":
        create_expense(args, expenses, budget_data)

    elif args.command == "update":
        update_expense(args, expenses, budget_data)

    elif args.command == "delete":
        expenses = delete_expense(args, expenses)

    elif args.command == "list":
        list_expenses(args, expenses)

    elif args.command == "budget":
        set_budget(args, budget_data)

    elif args.command == "summary":
        list_summary(args, expenses)

    elif args.command == "export":
        export_csv(args, expenses, budget_data)

# Save to JSON
    with open("expenses.json", "w") as file:
        json.dump(expenses, file, indent=4)
    with open("budgets.json", "w") as file:
        json.dump(budget_data, file, indent=4)