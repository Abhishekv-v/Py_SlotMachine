import tkinter as tk
from tkinter import messagebox
import random

MAX_LINES = 3
MIN_BET = 1
MAX_BET = 100
ROWS = 3
COLS = 3

SYMBOL_COUNT = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

SYMBOL_VALUE = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}

def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, count in symbols.items():
        all_symbols.extend([symbol] * count)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)
    return columns

def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            if column[line] != symbol:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)
    return winnings, winning_lines

def check_jackpot(columns):
    middle_row = [column[1] for column in columns]
    if all(symbol == middle_row[0] for symbol in middle_row):
        return True, middle_row[0]  
    return False, None

class SlotMachineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Slot Machine 🎰")
        self.root.geometry("400x400")
        self.balance = 0

        self.create_widgets()

    def create_widgets(self):
        # Balance
        self.balance_label = tk.Label(self.root, text="Balance: $0", font=('Arial', 14))
        self.balance_label.pack(pady=5)

        # Deposit Entry
        self.deposit_entry = tk.Entry(self.root)
        self.deposit_entry.pack()
        tk.Button(self.root, text="Deposit", command=self.deposit).pack()

        # Lines
        self.lines_label = tk.Label(self.root, text="Lines to Bet On (1-3):")
        self.lines_label.pack()
        self.lines_entry = tk.Entry(self.root)
        self.lines_entry.insert(0, "1")
        self.lines_entry.pack()

        # Bet per line
        self.bet_label = tk.Label(self.root, text="Bet per line:")
        self.bet_label.pack()
        self.bet_entry = tk.Entry(self.root)
        self.bet_entry.insert(0, "1")
        self.bet_entry.pack()

        # Spin button
        self.spin_button = tk.Button(self.root, text="Spin!", command=self.spin)
        self.spin_button.pack(pady=10)

        # Result display
        self.slot_display = tk.Label(self.root, text="", font=("Courier", 16))
        self.slot_display.pack()
        self.result_label = tk.Label(self.root, text="", font=('Arial', 12), fg="green")
        self.result_label.pack(pady=5)

    def deposit(self):
        try:
            amount = int(self.deposit_entry.get())
            if amount > 0:
                self.balance += amount
                self.update_balance()
                self.deposit_entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Invalid", "Please enter an amount greater than 0.")
        except ValueError:
            messagebox.showwarning("Invalid", "Please enter a number.")

    def update_balance(self):
        self.balance_label.config(text=f"Balance: ${self.balance}")

    def spin(self):
        if self.balance <= 0:
            messagebox.showinfo("Out of Balance", "You have no balance left!")
            return

        try:
            lines = int(self.lines_entry.get())
            bet = int(self.bet_entry.get())
        except ValueError:
            messagebox.showwarning("Invalid input", "Please enter valid numbers.")
            return

        if not (1 <= lines <= MAX_LINES):
            messagebox.showwarning("Invalid lines", f"Enter lines between 1 and {MAX_LINES}.")
            return

        if not (MIN_BET <= bet <= MAX_BET):
            messagebox.showwarning("Invalid bet", f"Bet must be between ${MIN_BET} and ${MAX_BET}.")
            return

        total_bet = bet * lines
        if total_bet > self.balance:
            messagebox.showwarning("Low Balance", "Not enough balance.")
            return

        self.balance -= total_bet

        slots = get_slot_machine_spin(ROWS, COLS, SYMBOL_COUNT)
        self.display_slots(slots)

        winnings, winning_lines = check_winnings(slots, lines, bet, SYMBOL_VALUE)
        is_jackpot, jackpot_symbol = check_jackpot(slots)
        jackpot_amount = 0

        if is_jackpot:
            jackpot_amount = 100 
            winnings += jackpot_amount

        self.balance += winnings

        # Prepare result text
        win_text = ""
        if winnings > 0:
            win_text += f" You won ${winnings}!\n"
            if winning_lines:
                win_text += f"Winning lines: {', '.join(map(str, winning_lines))}\n"
        else:
            win_text += "No winning lines. Try again!"

        if is_jackpot:
            win_text += f" JACKPOT! 3x '{jackpot_symbol}' in the middle row! +${jackpot_amount}"

        self.result_label.config(text=win_text.strip())
        self.balance_label.config(text=f"Balance: ${self.balance}")

    def display_slots(self, columns):
        output = ""
        for row in range(ROWS):
            output += " | ".join(column[row] for column in columns) + "\n"
        self.slot_display.config(text=output)


root = tk.Tk()
app = SlotMachineApp(root)
root.mainloop()
