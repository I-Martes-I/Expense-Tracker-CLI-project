import argparse

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

args = parser.parse_args()

if __name__ == "__main__":
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
        if args.description and args.amount and args.category and args.date:
            print(f"Updated: {args.id} {args.description} {args.amount} {args.category} {args.date}")
        elif args.description:
            print(f"Updated: {args.description}")
        elif args.amount:
            print(f"Updated: {args.amount}")
        elif args.category:
            print(f"Updated: {args.category}")
        elif args.date:
            print(f"Updated: {args.date}")

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