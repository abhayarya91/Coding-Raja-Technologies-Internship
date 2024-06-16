import tkinter as tk
from tkinter import messagebox
import json

class Transaction:
    def __init__(self, amount, category):
        self.amount = amount
        self.category = category

class BudgetTracker:
    def __init__(self):
        self.income = []
        self.expenses = []

    def add_income(self, amount, category):
        self.income.append(Transaction(amount, category))

    def add_expense(self, amount, category):
        self.expenses.append(Transaction(amount, category))

    def calculate_budget(self):
        total_income = sum(item.amount for item in self.income)
        total_expenses = sum(item.amount for item in self.expenses)
        return total_income - total_expenses

    def analyze_expenses(self):
        categories = {}
        for expense in self.expenses:
            if expense.category in categories:
                categories[expense.category] += expense.amount
            else:
                categories[expense.category] = expense.amount
        return categories

    def save_to_file(self, filename):
        data = {
            "income": [{"amount": item.amount, "category": item.category} for item in self.income],
            "expenses": [{"amount": item.amount, "category": item.category} for item in self.expenses],
        }
        with open(filename, 'w') as f:
            json.dump(data, f)

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.income = [Transaction(item["amount"], item["category"]) for item in data["income"]]
                self.expenses = [Transaction(item["amount"], item["category"]) for item in data["expenses"]]
        except FileNotFoundError:
            pass

class BudgetTrackerApp:
    def __init__(self, root):
        self.tracker = BudgetTracker()
        self.tracker.load_from_file('budget_data.json')
        self.root = root
        self.root.title("Budget Tracker")

        self.amount_label = tk.Label(root, text="Amount:")
        self.amount_label.grid(row=0, column=0, padx=10, pady=10)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=0, column=1, padx=10, pady=10)

        self.category_label = tk.Label(root, text="Category:")
        self.category_label.grid(row=1, column=0, padx=10, pady=10)
        self.category_entry = tk.Entry(root)
        self.category_entry.grid(row=1, column=1, padx=10, pady=10)

        self.add_income_button = tk.Button(root, text="Add Income", command=self.add_income)
        self.add_income_button.grid(row=2, column=0, padx=10, pady=10)
        self.add_expense_button = tk.Button(root, text="Add Expense", command=self.add_expense)
        self.add_expense_button.grid(row=2, column=1, padx=10, pady=10)

        self.calculate_button = tk.Button(root, text="Calculate Budget", command=self.calculate_budget)
        self.calculate_button.grid(row=3, column=0, padx=10, pady=10)
        self.analyze_button = tk.Button(root, text="Analyze Expenses", command=self.analyze_expenses)
        self.analyze_button.grid(row=3, column=1, padx=10, pady=10)

        self.save_button = tk.Button(root, text="Save and Exit", command=self.save_and_exit)
        self.save_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def add_income(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_entry.get()
            if category:
                self.tracker.add_income(amount, category)
                messagebox.showinfo("Success", "Income added successfully")
            else:
                messagebox.showerror("Error", "Category cannot be empty")
        except ValueError:
            messagebox.showerror("Error", "Invalid amount")

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_entry.get()
            if category:
                self.tracker.add_expense(amount, category)
                messagebox.showinfo("Success", "Expense added successfully")
            else:
                messagebox.showerror("Error", "Category cannot be empty")
        except ValueError:
            messagebox.showerror("Error", "Invalid amount")

    def calculate_budget(self):
        budget = self.tracker.calculate_budget()
        messagebox.showinfo("Remaining Budget", f"Remaining budget: ${budget:.2f}")

    def analyze_expenses(self):
        analysis = self.tracker.analyze_expenses()
        analysis_text = "\n".join(f"{category}: ${amount:.2f}" for category, amount in analysis.items())
        messagebox.showinfo("Expense Analysis", analysis_text if analysis_text else "No expenses to analyze")

    def save_and_exit(self):
        self.tracker.save_to_file('budget_data.json')
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetTrackerApp(root)
    root.mainloop()
