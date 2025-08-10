# Employee Management System (Python)

##  Project Description
This is a **menu-based Employee Data Management System** built in Python.  
It allows users to **add, update, delete, search, and list employees** using a CSV file for persistent storage.

The project is implemented using a single class `EmployeeManager` and demonstrates:
- Object-Oriented Programming (OOP) principles
- File handling with the `csv` module
- Data validation and error handling
- A user-friendly Command Line Interface (CLI)

---

## 🛠 Features
1. **Add Employee**
   - Enter Employee ID, Name, Position, Salary, and Email.
   - Validates that:
     - ID is numeric and unique
     - Salary is numeric and non-negative
     - Email has a valid format
   - Saves data to memory and CSV.

2. **Update Employee**
   - Modify one or more fields of an existing employee.
   - Leave a field blank to keep the old value.
   - Validates new data before saving.

3. **Delete Employee**
   - Remove an employee by ID.
   - Updates the CSV file automatically.

4. **Search Employee**
   - Find employee details by ID.
   - Displays "not found" if ID does not exist.

5. **List Employees**
   - Displays all employees in a clean tabular format.

6. **Exit**
   - Cleanly terminates the program.

---

## 📂 How It Works
1. **Start the Program:**  
   The user is presented with a menu of actions: `add`, `update`, `delete`, `search`, `list`, `exit`.

2. **Perform an Action:**  
   Depending on the selection, the program executes the corresponding function.

3. **Save Data:**  
   All changes are saved to a CSV file to ensure persistence.

4. **Retrieve Data:**  
   On startup, the program automatically:
   - Detects any CSV file in the same folder as the script and loads it.
   - Creates a new `employees.csv` if none exists.

---

## 📊 Technical Requirements Fulfilled
- ✅ Single class `EmployeeManager`
- ✅ Dictionary to store employee data in memory
- ✅ CSV file handling using the `csv` module
- ✅ Input validation for numeric salary, unique numeric IDs, and valid email format
- ✅ Error handling with up to 3 retries for invalid input
- ✅ Persistent storage between program runs

---

## 🏆 Bonus Points
- **Validation:** Checks for valid email, numeric salary, and unique numeric ID.  
- **User Experience:**  
  - Clear menu and instructions  
  - Emoji indicators for success, error, and actions  
  - Automatic CSV detection in the script's folder
## 🎯 Additional Bonus Feature
In addition to the main project requirements, this program includes an **extra bonus feature**:

- **Three Retry Attempts for Invalid Input**  
  When the user enters incorrect information (such as an invalid email format, a non-numeric salary, or an already existing ID), the program:
  1. Notifies the user of the error.
  2. Allows up to **three attempts** to correct the input.
  3. Returns to the main menu if all attempts fail.

This improves **user experience** by giving users multiple chances to fix mistakes without restarting the program.

---

## 📋 Requirements
- Python 3.7+
- No additional packages required (uses only Python's standard library)

---

## 🚀 How to Run
1. Clone this repository or download the `.py` file.
2. Ensure Python is installed:
   ```bash
   python --version
