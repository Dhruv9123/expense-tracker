from expense import Expense        # Importing Expense class from expense module
import datetime
import calendar
import matplotlib.pyplot as plt
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')          # Setting stdout encoding to UTF-8

def main():
     print(f"🎯 Running Expense Tracker!")
     expense_file="expenses.csv"
     
     # Loop until the user provides a valid input
     clear_file = ''
     while clear_file not in ['yes', 'no']:
          clear_file = input("💡 Do you want to clear the existing expense list and start fresh? (yes/no): ").lower()
          if clear_file == "yes":
               open(expense_file, 'w').close()  # Clearing the file by opening it in write mode
          elif clear_file == "no":
               pass  # Proceed without clearing the file
          else:
               print("❌ Invalid input. Please enter 'yes' or 'no'.")
     budget=float(input('Enter the budget at the beginning of the month: '))
                         
     # Main loop for the expense tracker
     while True:
          print("\n 📝 Options:")
          print("1. Insert a new expenditure")
          print("2. Check budget")
          print("3. Add loan")
          print("4. Pay off loan")
          print("5. Exit")
          choice = input(" 👉 Enter your choice (1/2/3/4/5): ")
        
          if choice == "1":
               expense = get_user_expense()
               save_expense(expense, expense_file)
          elif choice == "2":
               summarize(expense_file, budget)
          elif choice == "3":
               add_loan(expense_file, budget) 
          elif choice == "4":
               check_loan_status(expense_file, budget)
          elif choice == "5":
               print(" 👋 Exiting Expense Tracker. Goodbye! 👋 ")
               break
          else:
               print(" ❌ Invalid choice. Please enter 1, 2, or 3.")
    

def get_user_expense():            #function to get the input of expenses from the user
     print(f"🎯 Getting the expense from user.")
     e_name=input('Enter expense name: ')
     e_amount=float(input('Enter the expense amount: '))
     
     e_categories=['🍔Food', '🏠Home', '💼Work', '🎉Fun', '❇️ Misc', '💸Loan']
     
     # Loop until the user provides a valid category number
     while True:
          print(' 🔍 Select category: ')
          for i, c_name in enumerate(e_categories):
               print(f'{i+1}. {c_name}')
          value_range =f'[1 - {len(e_categories)}]'
          selected_index=int(input(f'Enter category number {value_range}: '))-1
          if selected_index in range(len(e_categories)):
               selected_category=e_categories[selected_index]
               new_expense=Expense(name=e_name, category=selected_category, amount=e_amount)
               return new_expense
          else:
               print(' ❌ Invalid category. Please try again!')
          
def save_expense(expense: Expense, expense_file):           #function to save the expenses into a file
     print(f"🎯 Saving the expenses in a file: {expense} to {expense_file}")
     with open(expense_file,"a", encoding="utf-8") as f:
          f.write(f'{expense.name}, {expense.category}, {expense.amount}\n')

def is_loan_added(expense_file):        #Function to check if a loan is already added in the expenses file
    with open(expense_file, "r",encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            if ", 💸Loan," in line:
                return True
    return False

def add_loan(expense_file, budget):
    # Function to add a loan expense
    # Loop until the user provides a valid input
    has_loan = ''
    while has_loan not in ['yes', 'no']:
        has_loan = input('💰💰 Do you have a loan? (yes/no): ').lower()
        if has_loan == 'yes':
            loan_name = input('Enter the loan name: ')
            loan_amount = float(input('💸 Enter the loan amount: '))
            save_expense(Expense(name=loan_name, category="💸Loan", amount=loan_amount), expense_file)
            budget -= loan_amount  # Subtract loan amount from budget
            print(orange(f"💰 Loan '{loan_name}' added successfully."))
            break
        elif has_loan == 'no':
            print('💰 No loans to be paid.')
            break
        else:
            print('❌ Invalid input. Please try again')

def check_loan_status(expense_file, budget):
    # Function to check the status of a loan
    # Loop until the user provides a valid input
    paid_off = ''
    while paid_off not in ['yes', 'no']:
        paid_off = input("💰 Have you paid off the loan completely or partially? (yes/no): ").lower()
        if paid_off == "yes":
            remove_loan(expense_file, budget)
        elif paid_off == "no":
            print(orange("💰 Keep track of your loan payments. Let us know when it's paid off."))
        else:
            print(red("❌ Invalid input. Please enter 'yes' or 'no'."))

def remove_loan(expense_file, budget):
    # Function to remove a loan expense
    loan_name = input('Enter the name of the loan: ')
    loan_found = False
    # Read the file and process each line
    with open(expense_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if ", 💸Loan," in line:
            name, _, loan = line.strip().split(",")
            current_loan_name = name.strip()
            if current_loan_name.lower() == loan_name.strip().lower():
                loan_found = True
                loan_amount = float(loan)
                paid_amount = float(input(f"💰 Enter the amount paid for the loan '{current_loan_name}': "))
                if paid_amount <= loan_amount:
                    if paid_amount == loan_amount:
                        print(orange(f"💰 Loan '{current_loan_name}' fully paid off. Removing it from the file."))
                    else:
                        remaining_loan = loan_amount - paid_amount
                        budget += paid_amount  # Add paid amount back to budget
                        print(purple(f"💰 Partial payment of ${paid_amount} made. Remaining loan amount for '{current_loan_name}': ${remaining_loan}"))
                        new_line = f'{current_loan_name}, 💸Loan, {remaining_loan}\n'
                        new_lines.append(new_line)
                else:
                    print(red("❌ Paid amount exceeds the loan amount. Please enter the correct amount."))
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    if not loan_found:
        print("❌ No active loan found with the specified name.")

    # Write the updated lines back to the file
    with open(expense_file, "w", encoding="utf-8") as f:
        f.writelines(new_lines)


def visualize_expenses(expenses):       #Function to visualize expenses
    categories = [expense.category for expense in expenses]
    amounts = [expense.amount for expense in expenses]
    
    df = pd.DataFrame({'Category': categories, 'Amount': amounts})
    grouped = df.groupby('Category').sum()
    plt.figure(figsize=(8, 8))
    plt.pie(grouped['Amount'], labels=grouped.index, autopct='%1.1f%%', startangle=140)
    plt.title('Expense Distribution by Category')
    plt.axis('equal')
    plt.show()



def summarize(expense_file, budget):         #Function that analyzes the budget (the main functionality)
     print(f"🎯 Summarising the expense.")
     expenses: list[Expense]=[]
     with open(expense_file, "r", encoding="utf-8") as f:
          lines=f.readlines()
          for line in lines:
               e_name, e_category, e_amount=line.strip().split(",")
               line_expense=Expense(name=e_name, category=e_category, amount=float(e_amount))
               expenses.append(line_expense)
     visualize_expenses(expenses)
     
     total_spent = sum([ex.amount for ex in expenses])
     print(f'💰 You have spent ${total_spent:.2f} this month')

     amount_category={}
     for expense in expenses:
          key=expense.category
          if key in amount_category:
               amount_category[key]+=expense.amount
          else:
               amount_category[key]=expense.amount
               
     print('Expenses by category📈: ')
     for key, amount in amount_category.items():
          print(f' {key}: ${amount:.2f}')
     
     total_spent=sum([ex.amount for ex in expenses])
     print(f'You have spent ${total_spent:.2f} this month')
     
     left_amount=budget-total_spent
     if total_spent > budget:
          print("📉 You have overspent your budget. Consider reducing expenses in certain categories.")
          p_left_amount=(-1)*left_amount
          print(red(f'📉You have overspent this month by ${p_left_amount}'))
     elif left_amount==0:
          print('🚫You have spent your entire budget and have $0 left.')
     elif total_spent > (budget * 0.8):
          print(yellow("📈 You have spent more than 80 percent 0f your budget. Consider allocating funds to only wwwessential categories."))
          
          now=datetime.datetime.now()
          days_in_month=calendar.monthrange(now.year, now.month)[1]
          remaining_days=days_in_month-now.day
          daily_budget=left_amount/remaining_days
          print(green((f'👉Budget Per Day for the rest of the month is: ${daily_budget:.2f}')))
     else:
          print(f'✅Budget remaining: ${left_amount:.2f}')
          
          now=datetime.datetime.now()
          days_in_month=calendar.monthrange(now.year, now.month)[1]
          remaining_days=days_in_month-now.day
          daily_budget=left_amount/remaining_days
          print(green((f'👉Budget Per Day for the rest of the month is: ${daily_budget:.2f}')))
     
     # Loop until the user provides a valid input
     while True:
          increase_budget = input("💡 Do you want to increase your budget? (yes/no): ").lower()
          if increase_budget == "yes":
               increase_amount = float(input("Enter the amount by which you want to increase the budget: "))
               budget += increase_amount
               print(orange((f"New budget: ${budget:.2f}")))
               break
          elif increase_budget == "no":
               break
          else:
               print("❌ Invalid input. Please enter 'yes' or 'no'.")
          
def green(text):
     return f'\033[92m{text}\033[0m'

def purple(text):
    return f'\033[95m{text}\033[0m'

def red(text):
    return f'\033[91m{text}\033[0m'

def yellow(text):
    return f'\033[93m{text}\033[0m'

def orange(text):
    return f'\033[33m{text}\033[0m'

               
if __name__=="__main__":
     main()