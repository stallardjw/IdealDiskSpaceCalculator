# Disk Space Calculator


**Disk Space Calculator** is a simple desktop application developed for the **Ideal Integrations NOC Team**. It helps with calculating additional space needed to reach desired free space percentages.

## Features

- **Unit Selection:** Input disk space in Gigabytes (GB) or Terabytes (TB).
- **Real-Time Calculations:** Automatically updates used or free space based on inputs.
- **Target Free Space:** Calculates additional space required to achieve target free space percentage.
- **Email Generation:** Creates a preformatted email with disk space details.
- **User-Friendly Interface:** Clean and responsive UI built with Tkinter.

## Installation

### Prerequisites

- **Python 3.6+**: Download from [Python.org](https://www.python.org/downloads/).
- **Tkinter**: Usually included with Python. If not, install via your package manager.

### Steps

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/stallardjw/IdealDiskSpaceCalculator.git
    ```

2. **Navigate to the Directory:**

    ```bash
    cd IdealDiskSpaceCalculator
    ```

3. **Run the Application:**

    ```bash
    python disk_space_calculator.py
    ```

## Usage

1. **Launch the Application:**
   - Run the `disk_space_calculator.py` script.

2. **Enter Disk Information:**
   - **Total Disk Space:** Input total capacity and select unit (GB/TB).
   - **Current Free Space:** Input current free space; used space updates automatically.
   - **Current Used Space:** Alternatively, input used space; free space updates automatically.
   - **Target Free Space %:** Specify desired free space percentage.

3. **View Results:**
   - The **Results** section displays current free and used percentages and additional space needed.

4. **Generate Email:**
   - Click **"Generate Email"**, enter server and volume names, and a preformatted email will open in your default email client.

5. **Clear Inputs:**
   - Click **"Clear"** to reset all fields.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your enhancements or fixes.

## License

This project is licensed under the [MIT License](LICENSE).


