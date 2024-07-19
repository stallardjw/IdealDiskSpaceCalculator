import tkinter as tk
from tkinter import messagebox
import webbrowser
import urllib.parse

def convert_units(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    if from_unit == "GB" and to_unit == "TB":
        return value / 1024
    if from_unit == "TB" and to_unit == "GB":
        return value * 1024

def calculate_additional_space(*args):
    try:
        total_space = convert_units(float(total_space_var.get()), total_space_unit_var.get(), "GB")
        current_free_space = convert_units(float(current_free_space_var.get()), current_space_unit_var.get(), "GB")
        current_used_space = total_space - current_free_space
        current_used_space_var.set(f"{convert_units(current_used_space, 'GB', current_space_unit_var.get()):.2f}")

        target_free_percentage = float(target_free_percentage_var.get()) if target_free_percentage_var.get() else None

        current_free_percentage = (current_free_space / total_space) * 100
        current_used_percentage = (current_used_space / total_space) * 100

        result = f"Current Free Space: {current_free_percentage:.2f}%\nCurrent Used Space: {current_used_percentage:.2f}%"

        if target_free_percentage is not None:
            target_free_space = total_space * (target_free_percentage / 100)
            additional_space_needed = target_free_space - current_free_space

            if additional_space_needed < 0:
                additional_space_needed = 0

            result += f"\nYou need to add {convert_units(additional_space_needed, 'GB', total_space_unit_var.get()):.2f} {total_space_unit_var.get()} to reach {target_free_percentage:.2f}% free space."

        result_var.set(result)
    except ValueError:
        result_var.set("Please enter valid numeric values.")
    except ZeroDivisionError:
        result_var.set("Total disk space cannot be zero.")

def on_free_space_change(*args):
    try:
        if float(current_free_space_var.get()) < 0:
            current_free_space_var.set("0")
        total_space = convert_units(float(total_space_var.get()), total_space_unit_var.get(), "GB")
        current_free_space = convert_units(float(current_free_space_var.get()), current_space_unit_var.get(), "GB")
        current_used_space = total_space - current_free_space
        if current_used_space < 0:
            result_var.set("Free space cannot exceed total disk space.")
            return
        current_used_space_var.set(f"{convert_units(current_used_space, 'GB', current_space_unit_var.get()):.2f}")
        calculate_additional_space()
    except ValueError:
        result_var.set("Please enter valid numeric values.")
    except ZeroDivisionError:
        result_var.set("Total disk space cannot be zero.")

def on_used_space_change(*args):
    try:
        if float(current_used_space_var.get()) < 0:
            current_used_space_var.set("0")
        total_space = convert_units(float(total_space_var.get()), total_space_unit_var.get(), "GB")
        current_used_space = convert_units(float(current_used_space_var.get()), current_space_unit_var.get(), "GB")
        current_free_space = total_space - current_used_space
        if current_free_space < 0:
            result_var.set("Used space cannot exceed total disk space.")
            return
        current_free_space_var.set(f"{convert_units(current_free_space, 'GB', current_space_unit_var.get()):.2f}")
        calculate_additional_space()
    except ValueError:
        result_var.set("Please enter valid numeric values.")
    except ZeroDivisionError:
        result_var.set("Total disk space cannot be zero.")

def on_total_space_change(*args):
    try:
        if float(total_space_var.get()) < 0:
            total_space_var.set("0")
        total_space = convert_units(float(total_space_var.get()), total_space_unit_var.get(), "GB")
        if current_free_space_var.get():
            current_free_space = convert_units(float(current_free_space_var.get()), current_space_unit_var.get(), "GB")
            current_used_space = total_space - current_free_space
            if current_used_space < 0:
                result_var.set("Free space cannot exceed total disk space.")
                return
            current_used_space_var.set(f"{convert_units(current_used_space, 'GB', current_space_unit_var.get()):.2f}")
        elif current_used_space_var.get():
            current_used_space = convert_units(float(current_used_space_var.get()), current_space_unit_var.get(), "GB")
            current_free_space = total_space - current_used_space
            if current_free_space < 0:
                result_var.set("Used space cannot exceed total disk space.")
                return
            current_free_space_var.set(f"{convert_units(current_free_space, 'GB', current_space_unit_var.get()):.2f}")
        calculate_additional_space()
    except ValueError:
        result_var.set("Please enter valid numeric values.")
    except ZeroDivisionError:
        result_var.set("Total disk space cannot be zero.")

def on_unit_change(*args):
    calculate_additional_space()

def clear_all():
    total_space_var.set("")
    current_free_space_var.set("")
    current_used_space_var.set("")
    target_free_percentage_var.set("")
    result_var.set("")
    total_space_unit_var.set("GB")
    current_space_unit_var.set("GB")

def generate_email():
    if not all([total_space_var.get(), current_free_space_var.get(), current_used_space_var.get(), target_free_percentage_var.get()]):
        messagebox.showerror("Input Error", "Please fill in all fields before generating the email.")
        return

    def submit_email_info():
        server_name = entry_server_name_popup.get()
        volume_name = entry_volume_name_popup.get()

        if not server_name or not volume_name:
            messagebox.showerror("Input Error", "Please fill in both server and volume names.")
            return

        total_space = "{} {}".format(total_space_var.get(), total_space_unit_var.get())
        current_free_space = "{} {}".format(current_free_space_var.get(), current_space_unit_var.get())
        current_used_space = "{} {}".format(current_used_space_var.get(), current_space_unit_var.get())
        target_free_percentage = target_free_percentage_var.get()

        total_space_gb = convert_units(float(total_space_var.get()), total_space_unit_var.get(), "GB")
        current_free_space_gb = convert_units(float(current_free_space_var.get()), current_space_unit_var.get(), "GB")
        current_used_space_gb = convert_units(float(current_used_space_var.get()), current_space_unit_var.get(), "GB")

        current_free_percentage = (current_free_space_gb / total_space_gb) * 100
        current_used_percentage = 100 - current_free_percentage

        target_free_space_gb = total_space_gb * (float(target_free_percentage) / 100)
        additional_space_needed = target_free_space_gb - current_free_space_gb

        if additional_space_needed < 0:
            additional_space_needed = 0

        email_body = (
            "Hello,\n\n"
            "We received an alert for low space on {} Volume {}\n\n"
            "Current volume details:\n"
            "Total Capacity: {}\n"
            "Total Used/Free: {} / {}\n"
            "Percent Used/Free: {:.2f}% / {:.2f}%\n\n"
            "Adding {:.2f} {} will get the volume to {:.2f}% free space.\n\n"
            "Please let us know how you would like to proceed.\n\n"
            "Thank you"
        ).format(
            server_name, 
            volume_name, 
            total_space, 
            current_used_space, 
            current_free_space, 
            current_used_percentage, 
            current_free_percentage, 
            additional_space_needed, 
            total_space_unit_var.get(), 
            float(target_free_percentage)
        )

        subject = "Low Disk Space Alert on {} Volume {}".format(server_name, volume_name)
        mailto_link = "mailto:?subject={}&body={}".format(urllib.parse.quote(subject), urllib.parse.quote(email_body))
        webbrowser.open(mailto_link)

        popup.destroy()

    popup = tk.Toplevel(root)
    popup.title("Enter Server and Volume Information")

    tk.Label(popup, text="Server Name:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
    entry_server_name_popup = tk.Entry(popup, font=("Arial", 12))
    entry_server_name_popup.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    tk.Label(popup, text="Volume Name:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
    entry_volume_name_popup = tk.Entry(popup, font=("Arial", 12))
    entry_volume_name_popup.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    submit_button = tk.Button(popup, text="Submit", font=("Arial", 12), command=submit_email_info)
    submit_button.grid(row=2, column=0, columnspan=2, pady=10)

root = tk.Tk()
root.title("Disk Space Calculator")
root.geometry("600x650")

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=2)
root.columnconfigure(2, weight=1)

total_space_var = tk.StringVar()
current_free_space_var = tk.StringVar()
current_used_space_var = tk.StringVar()
target_free_percentage_var = tk.StringVar()
result_var = tk.StringVar()

total_space_var.trace("w", on_total_space_change)
current_free_space_var.trace("w", on_free_space_change)
current_used_space_var.trace("w", on_used_space_change)
target_free_percentage_var.trace("w", calculate_additional_space)

total_space_unit_var = tk.StringVar(value="GB")
total_space_unit_var.trace("w", on_unit_change)
current_space_unit_var = tk.StringVar(value="GB")
current_space_unit_var.trace("w", on_unit_change)

padx, pady = 10, 10

tk.Label(root, text="Total Disk Space:", font=("Arial", 12)).grid(row=0, column=0, padx=padx, pady=pady, sticky="e")
entry_total_space = tk.Entry(root, font=("Arial", 12), textvariable=total_space_var)
entry_total_space.grid(row=0, column=1, padx=padx, pady=pady, sticky="w")
unit_frame_total = tk.Frame(root)
unit_frame_total.grid(row=0, column=2, padx=padx, pady=pady, sticky="w")
tk.Radiobutton(unit_frame_total, text="GB", variable=total_space_unit_var, value="GB", font=("Arial", 12)).pack(side=tk.LEFT)
tk.Radiobutton(unit_frame_total, text="TB", variable=total_space_unit_var, value="TB", font=("Arial", 12)).pack(side=tk.LEFT)

tk.Label(root, text="Current Free Disk Space:", font=("Arial", 12)).grid(row=1, column=0, padx=padx, pady=pady, sticky="e")
entry_current_free_space = tk.Entry(root, font=("Arial", 12), textvariable=current_free_space_var)
entry_current_free_space.grid(row=1, column=1, padx=padx, pady=pady, sticky="w")

tk.Label(root, text="Current Used Disk Space:", font=("Arial", 12)).grid(row=2, column=0, padx=padx, pady=pady, sticky="e")
entry_current_used_space = tk.Entry(root, font=("Arial", 12), textvariable=current_used_space_var)
entry_current_used_space.grid(row=2, column=1, padx=padx, pady=pady, sticky="w")

unit_frame_current = tk.Frame(root)
unit_frame_current.grid(row=1, column=2, rowspan=2, padx=padx, pady=pady, sticky="w")
tk.Radiobutton(unit_frame_current, text="GB", variable=current_space_unit_var, value="GB", font=("Arial", 12)).pack(side=tk.LEFT)
tk.Radiobutton(unit_frame_current, text="TB", variable=current_space_unit_var, value="TB", font=("Arial", 12)).pack(side=tk.LEFT)

tk.Label(root, text="Target Free Space Percentage (%):", font=("Arial", 12)).grid(row=3, column=0, padx=padx, pady=pady, sticky="e")
entry_target_free_percentage = tk.Entry(root, font=("Arial", 12), textvariable=target_free_percentage_var)
entry_target_free_percentage.grid(row=3, column=1, padx=padx, pady=pady, sticky="w")

instructions = (
    "Instructions:\n"
    "1. Enter the total disk space.\n"
    "2. Enter either the current free disk space or the current used disk space.\n"
    "3. Optionally, enter the target free space percentage.\n"
    "4. Select the unit for total and current free/used disk space (GB or TB).\n"
    "5. See the results update in real-time as you input values."
)
tk.Label(root, text=instructions, font=("Arial", 10), justify="left").grid(row=4, column=0, columnspan=3, padx=padx, pady=pady, sticky="w")

result_frame = tk.Frame(root, borderwidth=2, relief="sunken")
result_frame.grid(row=5, column=0, columnspan=3, padx=padx, pady=pady, sticky="nsew")
result_label = tk.Label(result_frame, textvariable=result_var, font=("Arial", 14), justify="left", anchor="w", padx=10, pady=10, wraplength=550)
result_label.pack(fill="both", expand=True)

clear_button = tk.Button(root, text="Clear", font=("Arial", 12), command=clear_all)
clear_button.grid(row=6, column=0, columnspan=3, pady=10)

generate_email_button = tk.Button(root, text="Generate Email", font=("Arial", 12), command=generate_email)
generate_email_button.grid(row=7, column=0, columnspan=3, pady=10)

tk.Label(root, text="Disk Space Calculator by Jonathan Stallard", font=("Arial", 10, "italic")).grid(row=8, column=0, columnspan=3, pady=(10, 0))
tk.Label(root, text="Version 1.0", font=("Arial", 10, "italic")).grid(row=9, column=0, columnspan=3)

# Run the main event loop
root.mainloop()
