import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import urllib.parse
import math
import re

##################################################
# Constants
##################################################
GB_PER_TB = 1024
SUPPORTED_UNITS = ["GB", "TB"]

##################################################
# Model Definition
##################################################
class DiskSpaceModel:
    def __init__(self):
        # All values are stored internally in GB
        self.total_space_gb = 0.0
        self.current_free_space_gb = 0.0
        self.target_free_percentage = None

    def set_total_space_gb(self, value_gb):
        self.total_space_gb = value_gb

    def set_free_space_gb(self, value_gb):
        self.current_free_space_gb = value_gb

    def get_used_space_gb(self):
        return self.total_space_gb - self.current_free_space_gb

    def get_free_percentage(self):
        if self.total_space_gb == 0:
            return 0
        return (self.current_free_space_gb / self.total_space_gb) * 100

    def get_used_percentage(self):
        return 100 - self.get_free_percentage()

    def get_additional_space_needed_gb(self):
        if self.target_free_percentage is None or self.total_space_gb == 0:
            return None
        P = self.target_free_percentage / 100.0
        T = self.total_space_gb
        F = self.current_free_space_gb

        if P >= 1.0:
            return None  # Cannot have 100% or more free space

        denominator = 1.0 - P
        if denominator == 0:
            return None  # Prevent division by zero

        A = (T * P - F) / denominator

        if A > 0:
            return math.ceil(A)
        else:
            return 0

##################################################
# Helper Functions
##################################################
def safe_float(s):
    s = s.strip()
    if s == '' or s == '.':
        return None
    try:
        return float(s)
    except ValueError:
        return None

def convert_to_gb(value, unit):
    """Converts value to GB based on the unit."""
    if unit == "GB":
        return value
    elif unit == "TB":
        return value * GB_PER_TB
    else:
        raise ValueError(f"Unsupported unit: {unit}")

def convert_from_gb(value_gb, unit):
    """Converts value from GB to the specified unit."""
    if unit == "GB":
        return value_gb
    elif unit == "TB":
        return value_gb / GB_PER_TB
    else:
        raise ValueError(f"Unsupported unit: {unit}")

def make_email_body(server_name, volume_name, model, total_unit, free_unit, used_unit, cleanup_ran=False):
    
    used_gb = model.get_used_space_gb()
    free_gb = model.current_free_space_gb

    total_str = f"{convert_from_gb(model.total_space_gb, total_unit):.2f} {total_unit}"
    free_str = f"{convert_from_gb(free_gb, free_unit):.2f} {free_unit}"
    used_str = f"{convert_from_gb(used_gb, used_unit):.2f} {used_unit}"

    free_pct = model.get_free_percentage()
    used_pct = model.get_used_percentage()

    additional_needed_gb = model.get_additional_space_needed_gb()
    additional_str = f"{additional_needed_gb} GB" if additional_needed_gb else "0 GB"

    target_perc = model.target_free_percentage if model.target_free_percentage else 0.0

    # Status line changes based on the checkbox
    status_line = (
        "After running cleanup tools, we were unable to free enough space to clear the alert.\n\n"
        if cleanup_ran else
        "Would you like us to run clean up tools or add additional space?\n\n"
    )

    return (
        "Hello,\n\n"
        f"We received an alert for low space on {server_name} Volume {volume_name}\n\n"
        "Current volume details:\n"
        f"Total Capacity: {total_str}\n"
        f"Total Used/Free: {used_str} / {free_str}\n"
        f"Percent Used/Free: {used_pct:.2f}% / {free_pct:.2f}%\n\n"
        f"{status_line}"
        f"Adding or Clearing {additional_str} will get the volume to {target_perc:.2f}% free space.\n\n"
        "Please let us know how you would like to proceed.\n\n"
        "Thank you"
    )

##################################################
# Controller Class
##################################################
class DiskSpaceCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Disk Space Calculator")
        self.root.geometry("600x600")
        self.root.minsize(500, 500)
        self.root.resizable(True, True)

        self.model = DiskSpaceModel()

        # Variables
        self.vars = {
            'total': tk.StringVar(),
            'free': tk.StringVar(),
            'used': tk.StringVar(),
            'target': tk.StringVar()
        }

        self.units = {
            'total': tk.StringVar(value="GB"),
            'free': tk.StringVar(value="GB"),
            'used': tk.StringVar(value="GB")
        }

        self.result_var = tk.StringVar()

        # Validation: only digits and one decimal point
        vcmd = (self.root.register(self.validate_input), '%P')

        # Menubar
        menubar = tk.Menu(root)
        root.config(menu=menubar)

        # About menu with GitHub link
        about_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="About", menu=about_menu)
        about_menu.add_command(label="About", command=self.show_about)
        about_menu.add_command(label="GitHub", command=lambda: webbrowser.open("https://github.com/stallardjw/IdealDiskSpaceCalculator"))

        # Main Frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(expand=True, fill="both")

        # Configure grid weights for main_frame
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=0)  # Buttons don't need to expand

        # Disk Information Frame
        disk_frame = ttk.LabelFrame(main_frame, text="Disk Space Information", padding="20")
        disk_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        disk_frame.columnconfigure(1, weight=1)
        disk_frame.columnconfigure(3, weight=1)  # For better spacing

        # Configure grid weights for disk_frame
        for i in range(4):
            disk_frame.rowconfigure(i, weight=1)
        for i in range(3):
            disk_frame.columnconfigure(i, weight=1)

        # Total Disk Space
        ttk.Label(disk_frame, text="Total Disk Space:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        entry_total = ttk.Entry(disk_frame, textvariable=self.vars['total'], validate='key', validatecommand=vcmd)
        entry_total.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        combo_total = ttk.Combobox(disk_frame, textvariable=self.units['total'], values=SUPPORTED_UNITS, state="readonly", width=5)
        combo_total.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        # Current Free Space
        ttk.Label(disk_frame, text="Current Free Space:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        entry_free = ttk.Entry(disk_frame, textvariable=self.vars['free'], validate='key', validatecommand=vcmd)
        entry_free.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        combo_free = ttk.Combobox(disk_frame, textvariable=self.units['free'], values=SUPPORTED_UNITS, state="readonly", width=5)
        combo_free.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        # Current Used Space
        ttk.Label(disk_frame, text="Current Used Space:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        entry_used = ttk.Entry(disk_frame, textvariable=self.vars['used'], validate='key', validatecommand=vcmd)
        entry_used.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        combo_used = ttk.Combobox(disk_frame, textvariable=self.units['used'], values=SUPPORTED_UNITS, state="readonly", width=5)
        combo_used.grid(row=2, column=2, padx=5, pady=5, sticky="w")

        # Target Free Space Percentage
        ttk.Label(disk_frame, text="Target Free Space %:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        entry_target = ttk.Entry(disk_frame, textvariable=self.vars['target'], validate='key', validatecommand=vcmd)
        entry_target.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Results Frame using Text with Scrollbar
        result_frame = ttk.LabelFrame(main_frame, text="Results", padding="20")
        result_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)

        # Adding a Text widget with Scrollbar for Results (Improved Display)
        self.result_text = tk.Text(result_frame, wrap="word", height=10, state="disabled", font=("Helvetica", 10))
        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        self.result_text.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Buttons Frame
        button_frame = ttk.Frame(main_frame, padding="10")
        button_frame.grid(row=2, column=0, sticky="e", padx=10, pady=10)
        button_frame.columnconfigure(0, weight=1)

        ttk.Button(button_frame, text="Clear", command=self.clear_all).pack(side="right", padx=5)
        ttk.Button(button_frame, text="Generate Email", command=self.generate_email_popup).pack(side="right", padx=5)

        # Refresh flag to prevent recursive updates
        self.refreshing = False

        # Attach separate trace handlers using lambda functions
        self.vars['total'].trace_add('write', lambda *args: self.on_space_change('total'))
        self.vars['free'].trace_add('write', lambda *args: self.on_space_change('free'))
        self.vars['used'].trace_add('write', lambda *args: self.on_space_change('used'))
        self.vars['target'].trace_add('write', lambda *args: self.on_target_change())

        self.units['total'].trace_add('write', lambda *args: self.on_unit_change('total'))
        self.units['free'].trace_add('write', lambda *args: self.on_unit_change('free'))
        self.units['used'].trace_add('write', lambda *args: self.on_unit_change('used'))

    def validate_input(self, new_value):
        """Allow only digits and a single decimal point."""
        return bool(re.match(r'^\d*\.?\d*$', new_value))

    def on_space_change(self, space_type):
        if self.refreshing:
            return
        self.refreshing = True

        space_val = safe_float(self.vars[space_type].get())
        total_val = safe_float(self.vars['total'].get())

        if space_val is not None and total_val is not None:
            space_gb = convert_to_gb(space_val, self.units[space_type].get())
            total_gb = convert_to_gb(total_val, self.units['total'].get())

            if space_gb > total_gb:
                self.update_result_display(f"Error: {space_type.capitalize()} space cannot exceed Total Disk Space.")
                self.refreshing = False
                return

            if space_type == 'total':
                self.model.set_total_space_gb(space_gb)
            elif space_type == 'free':
                self.model.set_free_space_gb(space_gb)
                used_gb = self.model.get_used_space_gb()
                used_display = convert_from_gb(used_gb, self.units['used'].get())
                self.vars['used'].set(f"{used_display:.2f}")
            elif space_type == 'used':
                free_gb = total_gb - space_gb
                self.model.set_free_space_gb(free_gb)
                free_display = convert_from_gb(free_gb, self.units['free'].get())
                self.vars['free'].set(f"{free_display:.2f}")

        self.update_results()
        self.refreshing = False

    def on_target_change(self):
        if self.refreshing:
            return
        self.refreshing = True
        target_val = safe_float(self.vars['target'].get())
        if target_val is not None:
            if target_val < 0:
                self.update_result_display("Error: Target percentage cannot be negative.")
                self.model.target_free_percentage = None
                self.refreshing = False
                return
            elif target_val >= 100.0:
                self.update_result_display("Error: Target free space percentage must be less than 100%.")
                self.model.target_free_percentage = None
                self.refreshing = False
                return
            else:
                self.model.target_free_percentage = target_val
        else:
            self.model.target_free_percentage = None
        self.update_results()
        self.refreshing = False

    def on_unit_change(self, unit_type):
        if self.refreshing:
            return
        self.refreshing = True
        try:
            if unit_type == 'total':
                total_val = safe_float(self.vars['total'].get())
                if total_val is not None:
                    # Convert to GB
                    total_gb = convert_to_gb(total_val, self.units['total'].get())
                    self.model.set_total_space_gb(total_gb)
                    # Update display in new unit
                    converted_total = convert_from_gb(total_gb, self.units['total'].get())
                    self.vars['total'].set(f"{converted_total:.2f}")
            elif unit_type == 'free':
                free_val = safe_float(self.vars['free'].get())
                if free_val is not None:
                    # Convert to GB
                    free_gb = convert_to_gb(free_val, self.units['free'].get())
                    self.model.set_free_space_gb(free_gb)
                    # Update display in new unit
                    converted_free = convert_from_gb(free_gb, self.units['free'].get())
                    self.vars['free'].set(f"{converted_free:.2f}")
            elif unit_type == 'used':
                used_val = safe_float(self.vars['used'].get())
                if used_val is not None:
                    # Convert to GB
                    used_gb = convert_to_gb(used_val, self.units['used'].get())
                    if used_gb > self.model.total_space_gb:
                        messagebox.showerror("Input Error", "Used space cannot exceed Total Disk Space.")
                        self.refreshing = False
                        return
                    # Set free space as total - used
                    free_gb = self.model.total_space_gb - used_gb
                    self.model.set_free_space_gb(free_gb)
                    # Update display in new unit
                    converted_free = convert_from_gb(free_gb, self.units['free'].get())
                    self.vars['free'].set(f"{converted_free:.2f}")
        except ValueError:
            messagebox.showerror("Unit Error", f"Unsupported unit for {unit_type.capitalize()} Space.")
            self.refreshing = False
            return

        self.update_results()
        self.refreshing = False

    def update_results(self):
        """Recalculate and update the results based on current inputs."""
        # Clear the result text widget
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)

        result_text = ""

        # Validate Total Disk Space
        total_val = self.model.total_space_gb
        if total_val == 0:
            self.result_text.config(state="disabled")
            return

        # Validate Free and Used spaces
        free_val = self.model.current_free_space_gb
        used_val = self.model.get_used_space_gb()

        if free_val < 0 or used_val < 0:
            result_text = "Error: Free or Used space cannot be negative."
            self.result_text.insert(tk.END, result_text)
            self.result_text.config(state="disabled")
            return

        if (self.vars['free'].get() and self.vars['used'].get()) and not math.isclose(free_val + used_val, total_val, rel_tol=1e-3):
            result_text = "Error: Free + Used does not equal Total Disk Space."
            self.result_text.insert(tk.END, result_text)
            self.result_text.config(state="disabled")
            return

        # Calculate percentages
        free_pct = self.model.get_free_percentage()
        used_pct = self.model.get_used_percentage()

        result_text += f"Current Free Space: {free_pct:.2f}%\n"
        result_text += f"Current Used Space: {used_pct:.2f}%"

        # Handle Target Percentage
        if self.model.target_free_percentage is not None:
            additional_needed_gb = self.model.get_additional_space_needed_gb()
            if additional_needed_gb is not None:
                if additional_needed_gb > 0:
                    result_text += f"\nYou need to add {additional_needed_gb} GB to reach {self.model.target_free_percentage:.2f}% free space."
                else:
                    result_text += f"\nYou have already met or exceeded the target free space of {self.model.target_free_percentage:.2f}%."

        # Insert the result into the Text widget
        self.result_text.insert(tk.END, result_text)
        self.result_text.config(state="disabled")

    def update_result_display(self, message):
        """Helper function to display error or other messages in the result area."""
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, message)
        self.result_text.config(state="disabled")

    def clear_all(self):
        """Clear all input fields and results."""
        self.refreshing = True
        self.vars['total'].set("")
        self.vars['free'].set("")
        self.vars['used'].set("")
        self.vars['target'].set("")
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.config(state="disabled")
        self.units['total'].set("GB")
        self.units['free'].set("GB")
        self.units['used'].set("GB")
        self.model = DiskSpaceModel()
        self.refreshing = False

    def generate_email_popup(self):
        """Open a popup to collect server and volume information and generate an email."""
        # Check if all required fields are filled
        if not all([self.vars['total'].get(), self.vars['free'].get(), self.vars['used'].get(), self.vars['target'].get()]):
            messagebox.showerror("Input Error", "Please fill in all fields before generating the email.")
            return

        def submit_email_info():
            server_name = entry_server_name_popup.get().strip()
            volume_name = entry_volume_name_popup.get().strip()
            client_abbreviation = entry_client_abbreviation_popup.get().strip()

            # This boolean indicates whether the user checked the 'cleanup tools ran' box
            cleanup_ran = cleanup_var.get()

            if not server_name or not volume_name or not client_abbreviation:
                messagebox.showerror("Input Error", "Please fill in all fields: server name, volume name, and client abbreviation.")
                return

            email_body = make_email_body(
                server_name, 
                volume_name, 
                self.model, 
                self.units['total'].get(), 
                self.units['free'].get(), 
                self.units['used'].get(),
                cleanup_ran=cleanup_ran  # Pass the new flag here
            )
            subject = f"[{client_abbreviation}] Low Disk Space Alert on {server_name} Volume {volume_name}"
            mailto_link = f"mailto:?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(email_body)}"
            webbrowser.open(mailto_link)
            popup.destroy()

        # Create popup window
        popup = tk.Toplevel(self.root)
        popup.title("Enter Server and Volume Information")
        popup.geometry("450x320")
        popup.resizable(False, False)

        # Center the popup window
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() - popup.winfo_reqwidth()) // 2
        y = (popup.winfo_screenheight() - popup.winfo_reqheight()) // 2
        popup.geometry(f"+{x}+{y}")

        pframe = ttk.Frame(popup, padding="20")
        pframe.pack(expand=True, fill="both")

        # Server Name
        ttk.Label(pframe, text="Server Name:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        entry_server_name_popup = ttk.Entry(pframe, width=30)
        entry_server_name_popup.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Volume Name
        ttk.Label(pframe, text="Volume Name:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        entry_volume_name_popup = ttk.Entry(pframe, width=30)
        entry_volume_name_popup.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Client Abbreviation
        ttk.Label(pframe, text="Client Abbreviation:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        entry_client_abbreviation_popup = ttk.Entry(pframe, width=30)
        entry_client_abbreviation_popup.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Checkbutton for "Already ran cleanup tools"
        cleanup_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(pframe, text="Already ran cleanup tools", variable=cleanup_var).grid(row=3, column=0, columnspan=2, pady=5)

        # Submit Button
        submit_button = ttk.Button(pframe, text="Submit", command=submit_email_info)
        submit_button.grid(row=4, column=0, columnspan=2, pady=20)

        # Configure grid weights for pframe
        pframe.columnconfigure(1, weight=1)

    def show_about(self):
        """Display the About information."""
        about_text = (
            "Disk Space Calculator\n"
            "Version 1.10\n\n"
            "Calculates additional space needed to reach a desired free space percentage.\n\n"
            "Built by Jonathan Stallard\n"
        )
        messagebox.showinfo("About", about_text)

##################################################
# Main Execution
##################################################
if __name__ == "__main__":
    root = tk.Tk()
    app = DiskSpaceCalculatorApp(root)
    root.mainloop()
