import argparse
import json
import os
import sys

DATA_FILE = "expenses_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Error: Data file is corrupted. Initializing new database.", file=sys.stderr)
    return {"income": [], "expenses": [], "budget": 0}

def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except IOError:
        print("⚠️ Error: Could not save data to disk.", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="📊 Personal Expense Tracker CLI Automation Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: add-income
    inc_parser = subparsers.add_parser("add-income", help="Record a new income source")
    inc_parser.add_argument("--source", required=True, help="Source of income (e.g., Salary)")
    inc_parser.add_argument("--amount", required=True, type=float, help="Amount received")
    inc_parser.add_argument("--date", required=True, help="Date of transaction (DD/MM/YYYY)")

    # Command: add-expense
    exp_parser = subparsers.add_parser("add-expense", help="Record a new expense category")
    exp_parser.add_argument("--category", required=True, help="Category (e.g., Food, Rent)")
    exp_parser.add_argument("--amount", required=True, type=float, help="Amount spent")
    exp_parser.add_argument("--date", required=True, help="Date of transaction (DD/MM/YYYY)")

    # Command: set-budget
    budget_parser = subparsers.add_parser("set-budget", help="Set monthly target budget limit")
    budget_parser.add_argument("--limit", required=True, type=float, help="Budget maximum limit")

    # Command: report
    subparsers.add_parser("report", help="Generate full financial summary analysis and charts")

    # Command: delete
    del_parser = subparsers.add_parser("delete", help="Delete a specific record")
    del_parser.add_argument("--type", choices=["income", "expenses"], required=True, help="Record database type")
    del_parser.add_argument("--index", type=int, required=True, help="The line index number to delete")

    try:
        args = parser.parse_args()
    except SystemExit:
        return

    data = load_data()

    if hasattr(args, 'amount') and args.amount is not None:
        if args.amount <= 0:
            print("❌ Robustness Error: Amount must be a positive value greater than zero.", file=sys.stderr)
            return

    if args.command == "add-income":
        data["income"].append({"source": args.source, "amount": args.amount, "date": args.date})
        save_data(data)
        print(f"✅ Success: Income from '{args.source}' added successfully.")

    elif args.command == "add-expense":
        total_expense = sum(item["amount"] for item in data["expenses"]) + args.amount
        data["expenses"].append({"category": args.category, "amount": args.amount, "date": args.date})
        save_data(data)
        print(f"✅ Success: Expense under '{args.category}' added successfully.")
        
        if data["budget"] > 0:
            if total_expense > data["budget"]:
                print(f"⚠️ CRITICAL ALERT: Monthly budget exceeded! (Spent: {total_expense}/{data['budget']})")
            elif total_expense >= data["budget"] * 0.8:
                print(f"⚠️ BUDGET WARNING: You have spent over 80% of your designated monthly budget limit.")

    elif args.command == "set-budget":
        if args.limit < 0:
            print("❌ Error: Budget limit cannot be negative.", file=sys.stderr)
            return
        data["budget"] = args.limit
        save_data(data)
        print(f"✅ Success: Monthly budget target updated to: ${args.limit}")

    elif args.command == "report":
        total_income = sum(item["amount"] for item in data["income"])
        total_expense = sum(item["amount"] for item in data["expenses"])
        remaining = total_income - total_expense

        print("\n" + "="*55)
        print("📊 PERSONAL FINANCIAL REPORT & ANALYTICS SUMMARY")
        print("="*55)
        print(f"💵 Total Income Overall : ${total_income}")
        print(f"💸 Total Expenses Logged: ${total_expense}")
        print(f"⚖️ Remaining Net Cash   : ${remaining}")
        print(f"📅 Set Budget Target    : ${data['budget']}")
        print("-" * 55)

        if not data["expenses"]:
            print("ℹ️ No expenses available to map charts.")
            return

        categories = {}
        for exp in data["expenses"]:
            cat = exp["category"]
            categories[cat] = categories.get(cat, 0) + exp["amount"]

        print("\n📈 VISUAL EXPENSE DISTRIBUTION CHART:")
        for cat, amount in categories.items():
            percentage = (amount / total_expense) * 100
            bar = "#" * int(percentage // 5)
            print(f"  [{cat:<12}] ${amount:>6.2f} | {bar} ({percentage:.1f}%)")
        print("="*55)

    elif args.command == "delete":
        target_list = data["income"] if args.type == "income" else data["expenses"]
        idx = args.index - 1
        if 0 <= idx < len(target_list):
            target_list.pop(idx)
            save_data(data)
            print(f"✅ Success: Removed entry index {args.index} successfully.")
        else:
            print(f"❌ Error: Index position {args.index} out of bounds.", file=sys.stderr)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
