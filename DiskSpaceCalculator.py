import tkinter as tk
from tkinter import messagebox

def calculate_additional_space(total_space, current_free_space, target_free_percentage=None, total_space_unit="GB", current_free_space_unit="GB"):
    # Convert units to GB if necessary
    if total_space_unit == "TB":
        total_space *= 1024
    if current_free_space_unit == "TB":
        current_free_space *= 1024

    # Calculate the current percentages of free and used space
    current_free_percentage = (current_free_space / total_space) * 100
    current_used_percentage = 100 - current_free_percentage

    result = f"Current Free Space: {current_free_percentage:.2f}%\nCurrent Used Space: {current_used_percentage:.2f}%"

    if target_free_percentage is not None:
        # Calculate the target free space in GB
        target_free_space_gb = total_space * (target_free_percentage / 100)

        # Calculate the additional space needed in GB
        additional_space_needed_gb = target_free_space_gb - current_free_space

        # Ensure the additional space needed is non-negative
        if additional_space_needed_gb < 0:
            additional_space_needed_gb = 0

        result += f"\nYou need to add {additional_space_needed_gb:.2f} GB of space to reach {target_free_percentage}% free space."

    return result

def on_calculate():
    try:
        total_space = float(entry_total_space.get())
        current_free_space = float(entry_current_free_space.get())
        target_free_percentage_text = entry_target_free_percentage.get()
        total_space_unit = total_space_unit_var.get()
        current_free_space_unit = current_free_space_unit_var.get()

        target_free_percentage = float(target_free_percentage_text) if target_free_percentage_text else None

        result_message = calculate_additional_space(total_space, current_free_space, target_free_percentage, total_space_unit, current_free_space_unit)
        messagebox.showinfo("Result", result_message)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")

root = tk.Tk()
root.title("Disk Space Calculator")
root.geometry("500x400")

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=2)

padx = 10
pady = 5

tk.Label(root, text="Total Disk Space:", font=("Arial", 12)).grid(row=0, column=0, padx=padx, pady=pady, sticky="e")
entry_total_space = tk.Entry(root, font=("Arial", 12))
entry_total_space.grid(row=0, column=1, padx=padx, pady=pady, sticky="w")
total_space_unit_var = tk.StringVar(value="GB")
unit_frame_total = tk.Frame(root)
unit_frame_total.grid(row=0, column=2, padx=padx, pady=pady, sticky="w")
tk.Radiobutton(unit_frame_total, text="GB", variable=total_space_unit_var, value="GB", font=("Arial", 12)).pack(side=tk.LEFT)
tk.Radiobutton(unit_frame_total, text="TB", variable=total_space_unit_var, value="TB", font=("Arial", 12)).pack(side=tk.LEFT)

tk.Label(root, text="Current Free Disk Space:", font=("Arial", 12)).grid(row=1, column=0, padx=padx, pady=pady, sticky="e")
entry_current_free_space = tk.Entry(root, font=("Arial", 12))
entry_current_free_space.grid(row=1, column=1, padx=padx, pady=pady, sticky="w")
current_free_space_unit_var = tk.StringVar(value="GB")
unit_frame_current = tk.Frame(root)
unit_frame_current.grid(row=1, column=2, padx=padx, pady=pady, sticky="w")
tk.Radiobutton(unit_frame_current, text="GB", variable=current_free_space_unit_var, value="GB", font=("Arial", 12)).pack(side=tk.LEFT)
tk.Radiobutton(unit_frame_current, text="TB", variable=current_free_space_unit_var, value="TB", font=("Arial", 12)).pack(side=tk.LEFT)

tk.Label(root, text="Target Free Space Percentage (%):", font=("Arial", 12)).grid(row=2, column=0, padx=padx, pady=pady, sticky="e")
entry_target_free_percentage = tk.Entry(root, font=("Arial", 12))
entry_target_free_percentage.grid(row=2, column=1, padx=padx, pady=pady, sticky="w")

instructions = (
    "Instructions:\n"
    "1. Enter the total disk space.\n"
    "2. Enter the current free disk space.\n"
    "3. Optionally, enter the target free space percentage.\n"
    "4. Select the unit for total and current free disk space (GB or TB).\n"
    "5. Click 'Calculate' to see the current free and used space percentages.\n"
    "   If the target free space percentage is provided, the additional space needed\n"
    "   to reach that target will also be displayed."
)
tk.Label(root, text=instructions, font=("Arial", 10), justify="left").grid(row=3, column=0, columnspan=3, padx=padx, pady=pady, sticky="w")

calculate_button = tk.Button(root, text="Calculate", font=("Arial", 12), command=on_calculate)
calculate_button.grid(row=4, column=0, columnspan=3, pady=20)

tk.Label(root, text="Disk Space Calculator by Jonathan Stallard", font=("Arial", 10, "italic")).grid(row=5, column=0, columnspan=3, pady=(10, 0))
tk.Label(root, text="Version 0.4", font=("Arial", 10, "italic")).grid(row=6, column=0, columnspan=3)

# Run the main event loop
root.mainloop()
