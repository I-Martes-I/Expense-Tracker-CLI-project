import argparse
import sys
import json
import datetime
import calendar

parser = argparse.ArgumentParser(description="Expense Tracker")
subparsers = parser.add_subparsers(dest="command")

#   "add" subcommand
add = subparsers.add_parser("add")
add.add_argument('--description', '--d', type=str, metavar='', required=True, help="Expense description")
add.add_argument('--amount', '--a', type=int, metavar='', required=True, help="Expense description")
add.add_argument('--category', '--c', type=str, metavar='', required=False, help="Expense category")
add.add_argument('--date', '--t', type=int, metavar='', required=False, help="Expense creaton date")

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
list_parser.add_argument('--category', '--c', type=str, metavar='', required=False, help="Expenses by category")
list_parser.add_argument('--month', '--m', type=int, metavar='', required=False, help="Expenses by month")
list_parser.add_argument('--year', '--y', type=int, metavar='', required=False, help="Expenses by year")

#   "budget" subcommand
budget = subparsers.add_parser("budget")
budget.add_argument('--month', '--m', type=int, metavar='', required=False, help="Month budget")
budget.add_argument('--year', '--y', type=int, metavar='', required=False, help="Year budget")

#   "summary" subcommand
summary = subparsers.add_parser("summary")
summary.add_argument('--month', type=int, metavar='', required=False)
summary.add_argument('--year', type=int, metavar='', required=False)

args = parser.parse_args()

def create_expense(args, expenses):
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

def delete_expense(args, expenses):
    id_exists = any(expense.get('id') == args.id for expense in expenses)
    if id_exists:
        print("Expense deleted successfully")
        return [expense for expense in expenses if expense["id"] != args.id]
    else:
        print("Expense with such ID wasn't found")
        return expenses

def update_expense(args, expenses):
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

def list_expenses(args, expenses):
    if args.category:
        if not expenses:
            print("No categories found!")
        else:
            print("List of all categories:")
            for expense in expenses:
                print(f"{expense["category"]}")
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
    elif args.year and args.month:
        for expense in expenses:
            date = datetime.datetime.fromisoformat(expense["date"])
            if args.year == date.year and args.month == date.month: 
                count += expense["amount"]
        print(f"Total expenses for {list(calendar.month_name)[args.month]} {args.year}: ${count}")
    else: 
        for expense in expenses:
            count += expense["amount"]
        print(f"Total expenses: ${count}")

if __name__ == "__main__":

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

    if args.command == "add":
        create_expense(args, expenses)

    elif args.command == "update":
        update_expense(args, expenses)

    elif args.command == "delete":
        expenses = delete_expense(args, expenses)

    elif args.command == "list":
        list_expenses(args, expenses)

    elif args.command == "budget":
        if args.month:
            print(f"Set Month budget: {args.month}")
        elif args.year:
            print(f"Set Year  budget: {args.year}")

    elif args.command == "summary":
        list_summary(args, expenses)

    # Save to JSON
    with open("expenses.json", "w") as file:
        json.dump(expenses, file, indent=4)
    with open("budgets.json", "w") as file:
        json.dump(budgets, file, indent=4)