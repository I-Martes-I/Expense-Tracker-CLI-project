# Expense Tracker CLI

A simple command line interface (CLI) to track and manage your personal finances. Built with Python using only the standard library.

## Features

- Add, update, and delete expenses
- View all expenses in a formatted table
- Filter expenses by category, month, or year
- View a summary of expenses for a specific month or year
- Set monthly and yearly budgets with warnings when exceeded
- Export expenses to a CSV file

## Usage

```bash
expense_tracker <command> [options]
```

### Commands

#### Add an expense
```bash
python expense_tracker.py add --description "Lunch" --amount 20 --category Food --date 2026-07-14
```
Output:
```
Expense added successfully (ID: 1)
```

#### Update an expense
```bash
python expense_tracker.py update --id 1 --description "Dinner" --amount 30 --category Food
```
Output:
```
Expense updated successfully
```

#### Delete an expense
```bash
python expense_tracker.py delete --id 1
```
Output:
```
Expense deleted successfully
```

#### List expenses
```bash
# List all expenses
python expense_tracker.py list

# List all categories
python expense_tracker.py list --category

# List expenses by category
python expense_tracker.py list --category Food

# List expenses by month or year
python expense_tracker.py list --month 7
python expense_tracker.py list --year 2026

# Combine filters
python expense_tracker.py list --category Food --month 7 --year 2026
```

#### View summary
```bash
# Total of all expenses
python expense_tracker.py summary

# Total for a specific month
python expense_tracker.py summary --month 7

# Total for a specific year
python expense_tracker.py summary --year 2026

# Total for a specific month and year
python expense_tracker.py summary --month 7 --year 2026
```
Output:
```
Total expenses for July 2026: $150
```

#### Set or view budget
```bash
# Set yearly budget
python expense_tracker.py budget --amount 5000

# Set monthly budget
python expense_tracker.py budget --month 7 --amount 1000

# Set budget for a specific year
python expense_tracker.py budget --year 2026 --amount 5000

# View all budgets
python expense_tracker.py budget
```

#### Export to CSV
```bash
# Export files (expenses.csv and budget.csv)
python expense_tracker.py export --e --b

```

## Budget Warnings

When adding or updating an expense, the app automatically checks if the current month or year budget has been exceeded and shows a warning:

```
Budget for July 2026 exceeded! Month budget is $1000, but you spent $1200!
```

## Data Storage

Expenses are stored in `expenses.json` and budgets in `budgets.json` in the current directory. Both files are created automatically on first use and are listed in `.gitignore`.

## Notes

- Amounts must be positive numbers.
- Dates must be in ISO format: `2026-07-14` or `2026-07-14T12:00:00`.
- Month numbers are 1-12.
