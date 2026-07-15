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
export.add_argument('--output', type=str, metavar='', required=False)

args = parser.parse_args()

def create_expense(args, expenses, budget_data):
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

def list_expenses(args, expenses):
    if args.category == 'all':
        categories = set(expense["category"] for expense in expenses)
        print("All categories:")
        for cat in sorted(categories):
            print(f"  - {cat}")
    elif args.category:
        filtered = [e for e in expenses if e["category"].lower() == args.category.lower()]
        if not filtered:
            print(f"No expenses found for category '{args.category}'")
    else:
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
            if len(expense["date"]) > date_len:  date_len = len(str(expense["date"])) 

        headers = f"{'ID':<{id_len}} {'Description':<{description_len}} {'Amount':<{amount_len}} {'Category':<{category_len}} {'Date':<{category_len}}"

        if not expenses:
            print("No tasks found!")
        else:
            print("List of all tasks:")
            print(headers)
            for expense in expenses:
                print(f"{expense["id"]:<{id_len}} {expense["description"]:<{description_len}} {expense["amount"]:<{amount_len}} {expense["category"]:<{category_len}} {expense["date"][:19].replace("T", " "):<25}")

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
    for year in budget_data:
        year_sum = 0
        for expense in expenses:
            date = datetime.datetime.fromisoformat(expense["date"])
            if int(year) == date.year: 
                year_sum += expense["amount"]
        if budget_data[year]['budget'] < year_sum and budget_data[year]['budget'] != 0:
            print(f"Budget for {year} exeeded! Year budget is ${budget_data[year]['budget']}, but you spent ${year_sum}!")    
        for month, amount in budget_data[year]["months"].items():
            month_sum = 0
            for expense in expenses:
                date = datetime.datetime.fromisoformat(expense["date"])
                if int(month) == date.month:
                    month_sum += expense["amount"]
            if budget_data[year]["months"][month] < month_sum and budget_data[year]["months"][month] != 0:  
                print(f"Budget for {calendar.month_name[int(month)]} {year} exceeded! Month budget is ${amount}, but you spent ${month_sum}!")

def export_csv(args, expenses):
    with open("expenses.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "description", "amount", "date", "category"])
        writer.writeheader()
        writer.writerows(expenses)

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
        export_csv(args, expenses)

# Save to JSON
    with open("expenses.json", "w") as file:
        json.dump(expenses, file, indent=4)
    with open("budgets.json", "w") as file:
        json.dump(budget_data, file, indent=4)