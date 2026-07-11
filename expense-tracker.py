import argparse

parser = argparse.ArgumentParser(description="Expense Tracker")
parser.add_argument('--d', '--description', type=str, metavar='', required=True, help="Expense description")
parser.add_argument('--a', '--amount', type=int, metavar='', required=True, help="Expense description")
args = parser.parse_args()

if __name__ == "__main__":
    print(f"{args.description} {args.amount}")