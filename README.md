# 📊 Personal Expense Tracker CLI Tool

A lightweight, automated command-line interface (CLI) tool written in Python to manage personal finances, log transactions, track budgets, and view structural text-based analytical reports.

## 🚀 How to Run the Commands
Interact with the tool using the following arguments directly in the terminal:

### 1. Set Monthly Budget Target
```bash
python cli.py set-budget --limit 1500
```

### 2. Log New Income Source
```bash
python cli.py add-income --source Salary --amount 2500 --date "01/10/2026"
```

### 3. Log New Categorized Expense
```bash
python cli.py add-expense --category Food --amount 75.50 --date "05/10/2026"
```

### 4. Generate Analytics Report & Charts
```bash
python cli.py report
```

### 5. Delete an Entry
```bash
python cli.py delete --type expenses --index 1
```

## 🛡️ Robustness Mechanisms Implemented
- **Input Validation**: Enforces strict positive numerical types for currency amounts to block logic breaking.
- **Fail-Safe I/O**: Wrapped with standard `try-except` blocks to handle malformed files or runtime parsing crashes safely without hard crashing.
