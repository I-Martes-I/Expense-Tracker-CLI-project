import argparse
import sys
import json
import datetime

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
update.add_argument('--date', '--t', type=str, metavar='', required=False, help="Expense creaton date")

#   "delete" subcommand
delete = subparsers.add_parser("delete")
delete.add_argument('--id', type=int, metavar='', required=True, help="Expense ID")

#   "list" subcommand
list_parser = subparsers.add_parser("list")
list_parser.add_argument('--category', '--c', type=str, metavar='', required=False, help="Expenses by category")
list_parser.add_argument('--mouth', '--m', type=int, metavar='', required=False, help="Expenses by mounth")
list_parser.add_argument('--year', '--y', type=int, metavar='', required=False, help="Expenses by year")

#   "budget" subcommand
budget = subparsers.add_parser("budget")
budget.add_argument('--mouth', '--m', type=int, metavar='', required=False, help="Mounth budget")
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
        new_id = 0
        
    new_expense = {
        "id": new_id,
        "description": args.description,
        "amount": args.amount,
        "date": args.date if args.date else datetime.datetime.now().isoformat(),
        "category": args.category if args.category else "default"
    }
    expenses.append(new_expense)
    print(f"Expense added successfully (ID: {args.id})")


if __name__ == "__main__":
    try:
        with open("expenses.json", "r") as file:
            expenses = json.load(file)
    except FileNotFoundError:
        expenses = []
    except json.JSONDecodeError:
        expenses = []

    if args.command == "add":
        if args.date and args.category:
            print(f"Added: {args.description} {args.amount} {args.category} {args.date}")
        elif args.date:
            print(f"Added: {args.description} {args.amount} {args.date}")
        elif args.category:
            print(f"Added: {args.description} {args.amount} {args.category}")
        else:
            print(f"Added: {args.description} {args.amount}")

    elif args.command == "update":
        updated = []
        if args.description: updated.append(f"description='{args.description}'")
        if args.amount: updated.append(f"amount={args.amount}")
        if args.category: updated.append(f"category='{args.category}'")
        if args.date: updated.append(f"date='{args.date}'")

        if updated:
            print(f"Updated ID {args.id}: {', '.join(updated)}")
        else:
            print("Nothing to update!")

    elif args.command == "delete":
        print(f"Delete ID: {args.id}")

    elif args.command == "list":
        if args.category:
            print(f"List by category: {args.category}")
        elif args.mouth:
            print(f"List by mounth: {args.mouth}")
        elif args.year:
            print(f"List by year: {args.year}")
        else:
            print(f"List: All Expenses")

    elif args.command == "budget":
        if args.mouth:
            print(f"Set Mounth budget: {args.mouth}")
        elif args.year:
            print(f"Set Year  budget: {args.year}")

    elif args.command == "summary":
        if args.mouth:
            print(f"Mounth summary: {args.mouth}")
        elif args.year:
            print(f"Year  summary: {args.year}")