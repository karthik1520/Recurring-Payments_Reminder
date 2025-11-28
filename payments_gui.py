import json
import os
import tkinter as tk
from tkinter import messagebox

# Locate payments.json next to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAYMENTS_PATH = os.path.join(BASE_DIR, "payments.json")


class PaymentsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Recurring Payments Editor")

        # ---- 💡 FIX: Set proper window size ----
        self.root.geometry("750x450")     # width x height
        self.root.resizable(False, False) # lock window so nothing spills out
        # -----------------------------------------

        # Left side: listbox
        self.listbox = tk.Listbox(root, width=40, height=18)
        self.listbox.grid(row=0, column=0, rowspan=10, padx=15, pady=15, sticky="ns")
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        # Right side: input fields
        label_pad = {"padx": 5, "pady": 3}

        tk.Label(root, text="Name").grid(row=0, column=1, sticky="w", **label_pad)
        self.name_entry = tk.Entry(root, width=45)
        self.name_entry.grid(row=0, column=2, **label_pad)

        tk.Label(root, text="Amount").grid(row=1, column=1, sticky="w", **label_pad)
        self.amount_entry = tk.Entry(root, width=45)
        self.amount_entry.grid(row=1, column=2, **label_pad)

        tk.Label(root, text="Currency").grid(row=2, column=1, sticky="w", **label_pad)
        self.currency_entry = tk.Entry(root, width=45)
        self.currency_entry.grid(row=2, column=2, **label_pad)

        tk.Label(root, text="Day (1-31)").grid(row=3, column=1, sticky="w", **label_pad)
        self.day_entry = tk.Entry(root, width=45)
        self.day_entry.grid(row=3, column=2, **label_pad)

        tk.Label(root, text="Notes").grid(row=4, column=1, sticky="w", **label_pad)
        self.notes_entry = tk.Entry(root, width=45)
        self.notes_entry.grid(row=4, column=2, **label_pad)

        # Buttons
        self.add_button = tk.Button(root, text="Add New", width=20, command=self.add_payment)
        self.add_button.grid(row=5, column=2, pady=8, sticky="e")

        self.update_button = tk.Button(root, text="Update Selected", width=20, command=self.update_payment)
        self.update_button.grid(row=6, column=2, pady=8, sticky="e")

        self.delete_button = tk.Button(root, text="Delete Selected", width=20, command=self.delete_payment)
        self.delete_button.grid(row=7, column=2, pady=8, sticky="e")

        self.save_button = tk.Button(root, text="Save to payments.json", width=25, command=self.save_payments)
        self.save_button.grid(row=8, column=2, pady=10, sticky="e")

        # Load data
        self.payments = []
        self.load_payments()

    def load_payments(self):
        if not os.path.exists(PAYMENTS_PATH):
            messagebox.showwarning("Warning", f"{PAYMENTS_PATH} not found. Starting with empty list.")
            self.payments = []
            return

        with open(PAYMENTS_PATH, "r") as f:
            self.payments = json.load(f)

        self.refresh_listbox()

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for p in self.payments:
            display = f"{p['day']:02d} - {p['name']} ({p['amount']} {p.get('currency', '')})"
            self.listbox.insert(tk.END, display)

    def on_select(self, event):
        selection = self.listbox.curselection()
        if not selection:
            return
        index = selection[0]
        p = self.payments[index]

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, p["name"])

        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, str(p["amount"]))

        self.currency_entry.delete(0, tk.END)
        self.currency_entry.insert(0, p.get("currency", ""))

        self.day_entry.delete(0, tk.END)
        self.day_entry.insert(0, str(p["day"]))

        self.notes_entry.delete(0, tk.END)
        self.notes_entry.insert(0, p.get("notes", ""))

    def add_payment(self):
        try:
            name = self.name_entry.get().strip()
            amount = float(self.amount_entry.get())
            currency = self.currency_entry.get().strip()
            day = int(self.day_entry.get())
            notes = self.notes_entry.get().strip()

            if not name:
                raise ValueError("Name is required.")
            if not (1 <= day <= 31):
                raise ValueError("Day must be between 1 and 31.")

            new_payment = {
                "name": name,
                "amount": amount,
                "currency": currency or "EUR",
                "day": day,
                "notes": notes,
            }
            self.payments.append(new_payment)
            self.refresh_listbox()
        except Exception as e:
            messagebox.showerror("Error adding payment", str(e))

    def update_payment(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showinfo("Info", "Select a payment to update.")
            return

        index = selection[0]
        try:
            name = self.name_entry.get().strip()
            amount = float(self.amount_entry.get())
            currency = self.currency_entry.get().strip()
            day = int(self.day_entry.get())
            notes = self.notes_entry.get().strip()

            if not name:
                raise ValueError("Name is required.")
            if not (1 <= day <= 31):
                raise ValueError("Day must be between 1 and 31.")

            self.payments[index] = {
                "name": name,
                "amount": amount,
                "currency": currency or "EUR",
                "day": day,
                "notes": notes,
            }
            self.refresh_listbox()
        except Exception as e:
            messagebox.showerror("Error updating payment", str(e))

    def delete_payment(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showinfo("Info", "Select a payment to delete.")
            return

        index = selection[0]
        del self.payments[index]
        self.refresh_listbox()

    def save_payments(self):
        try:
            with open(PAYMENTS_PATH, "w") as f:
                json.dump(self.payments, f, indent=2)
            messagebox.showinfo("Saved", f"Payments saved to {PAYMENTS_PATH}")
        except Exception as e:
            messagebox.showerror("Error saving payments", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    PaymentsGUI(root)
    root.mainloop()
