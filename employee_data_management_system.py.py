import csv
import os
import re
import sys
from pathlib import Path

class EmployeeManager:
    FIELDS = ["ID", "Name", "Position", "Salary", "Email"]

    def __init__(self, filename=None):
        # Get the folder where the script is located
        current_folder = Path(__file__).parent

        # Auto-detect CSV file in the same folder
        if filename is None:
            csv_files = list(current_folder.glob("*.csv"))
            if csv_files:
                self.filename = str(csv_files[0])  # Use first CSV found
                print(f"📂 Found existing CSV: {self.filename}")
            else:
                self.filename = str(current_folder / "employees.csv")
                print(f"📄 No CSV found, will create new: {self.filename}")
        else:
            self.filename = str(current_folder / filename)

        self.employees = {}
        self.load()

    def load(self):
        """Retrieve Data: Load employees from CSV into memory."""
        self.employees = {}
        if os.path.exists(self.filename) and os.path.getsize(self.filename) > 0:
            with open(self.filename, mode="r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get("ID"):
                        self.employees[row["ID"]] = {
                            "Name": row.get("Name", ""),
                            "Position": row.get("Position", ""),
                            "Salary": row.get("Salary", ""),
                            "Email": row.get("Email", ""),
                        }

    def save_all(self):
        """Save Data: Write all employees from memory to CSV."""
        temp_name = self.filename + ".tmp"
        with open(temp_name, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.FIELDS)
            writer.writeheader()
            for emp_id, data in self.employees.items():
                row = {"ID": emp_id, **data}
                writer.writerow(row)
        os.replace(temp_name, self.filename)

    # --- Validation functions ---
    def validate_id(self, emp_id):
        """Ensure ID is numeric, not empty, and unique."""
        return emp_id.isdigit() and emp_id != "" and emp_id not in self.employees

    def validate_existing_id(self, emp_id):
        """Ensure ID exists in the system."""
        return emp_id in self.employees

    def validate_salary(self, salary_str):
        """Ensure salary is a valid non-negative number."""
        try:
            val = float(salary_str)
            return val >= 0
        except (ValueError, TypeError):
            return False

    def validate_email(self, email):
        """Validate email format using regex."""
        if not email:
            return False
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email) is not None

    def get_input_with_retry(self, prompt, validate_fn=None, error_msg="⚠️ Invalid value.", max_attempts=3, allow_empty=False):
        """Prompt the user for input with up to max_attempts retries."""
        attempts = 0
        while attempts < max_attempts:
            value = input(prompt).strip()
            if allow_empty and value == "":
                return value
            if validate_fn is None or validate_fn(value):
                return value
            else:
                print(error_msg)
                attempts += 1
        print("❌ Maximum attempts reached. Returning to main menu.")
        return None

    # ----- CRUD operations -----
    def add(self):
        print("\n➕ Add New Employee")
        emp_id = self.get_input_with_retry(
            "Enter Employee ID (numbers only): ",
            validate_fn=self.validate_id,
            error_msg="⚠️ Invalid ID (must be numeric, unique, and not empty)."
        )
        if emp_id is None:
            return

        name = self.get_input_with_retry(
            "Enter Employee Name: ",
            validate_fn=lambda v: v != "",
            error_msg="⚠️ Name cannot be empty."
        )
        if name is None:
            return

        position = self.get_input_with_retry(
            "Enter Position: ",
            validate_fn=lambda v: v != "",
            error_msg="⚠️ Position cannot be empty."
        )
        if position is None:
            return

        salary = self.get_input_with_retry(
            "Enter Salary: ",
            validate_fn=self.validate_salary,
            error_msg="⚠️ Salary must be a valid non-negative number."
        )
        if salary is None:
            return

        email = self.get_input_with_retry(
            "Enter Email: ",
            validate_fn=self.validate_email,
            error_msg="⚠️ Invalid email format."
        )
        if email is None:
            return

        self.employees[emp_id] = {
            "Name": name,
            "Position": position,
            "Salary": str(salary),
            "Email": email,
        }
        self.save_all()
        print(f"✅ Employee {name} added successfully.")
        print("-" * 60)

    def list(self):
        print("\n📋 Employee List")
        if not self.employees:
            print("No employees found.")
            return
        print(f"{'ID':<10} {'Name':<20} {'Position':<20} {'Salary':<12} {'Email'}")
        print("-" * 80)
        for emp_id, d in sorted(self.employees.items()):
            print(f"{emp_id:<10} {d['Name'][:20]:<20} {d['Position'][:20]:<20} {d['Salary']:<12} {d['Email']}")
        print("-" * 60)

    def search(self):
        print("\n🔍 Search Employee")
        emp_id = self.get_input_with_retry(
            "Enter Employee ID to search: ",
            validate_fn=self.validate_existing_id,
            error_msg="❌ Employee not found."
        )
        if emp_id is None:
            return
        emp = self.employees[emp_id]
        print("Employee Details:")
        print(f"ID: {emp_id}")
        print(f"Name: {emp['Name']}")
        print(f"Position: {emp['Position']}")
        print(f"Salary: {emp['Salary']}")
        print(f"Email: {emp['Email']}")
        print("-" * 60)

    def update(self):
        print("\n✏️ Update Employee")
        emp_id = self.get_input_with_retry(
            "Enter Employee ID to update: ",
            validate_fn=self.validate_existing_id,
            error_msg="❌ Employee not found."
        )
        if emp_id is None:
            return
        current = self.employees[emp_id]
        print("Leave the field empty if you don't want to change it.")

        new_name = self.get_input_with_retry(f"Name [{current['Name']}]: ", allow_empty=True)
        if new_name is None:
            return
        new_pos = self.get_input_with_retry(f"Position [{current['Position']}]: ", allow_empty=True)
        if new_pos is None:
            return
        new_salary = self.get_input_with_retry(
            f"Salary [{current['Salary']}]: ",
            validate_fn=self.validate_salary,
            error_msg="⚠️ Invalid salary.",
            allow_empty=True
        )
        if new_salary is None:
            return
        new_email = self.get_input_with_retry(
            f"Email [{current['Email']}]: ",
            validate_fn=self.validate_email,
            error_msg="⚠️ Invalid email format.",
            allow_empty=True
        )
        if new_email is None:
            return

        if new_name:
            current['Name'] = new_name
        if new_pos:
            current['Position'] = new_pos
        if new_salary:
            current['Salary'] = str(new_salary)
        if new_email:
            current['Email'] = new_email
        self.save_all()
        print("✅ Employee updated successfully.")
        print("-" * 60)

    def delete(self):
        print("\n🗑 Delete Employee")
        emp_id = self.get_input_with_retry(
            "Enter Employee ID to delete: ",
            validate_fn=self.validate_existing_id,
            error_msg="❌ Employee not found."
        )
        if emp_id is None:
            return
        confirm = input(f"Are you sure you want to delete {self.employees[emp_id]['Name']}? (y/n): ").strip().lower()
        if confirm == 'y':
            del self.employees[emp_id]
            self.save_all()
            print("✅ Employee deleted.")
        else:
            print("❌ Delete cancelled.")
        print("-" * 60)

    def run(self):
        """Start the Program."""
        print("=" * 60)
        print("👋 Welcome to the Employee Management System")
        print("Available actions: add, update, delete, search, list, exit")
        print("=" * 60)
        try:
            while True:
                print("\nMenu:")
                print("1. add")
                print("2. update")
                print("3. delete")
                print("4. search")
                print("5. list")
                print("6. exit")
                choice = input("Choose an option: ").strip()
                if choice == '1':
                    self.add()
                elif choice == '2':
                    self.update()
                elif choice == '3':
                    self.delete()
                elif choice == '4':
                    self.search()
                elif choice == '5':
                    self.list()
                elif choice == '6':
                    print("👋 Goodbye.")
                    break
                else:
                    print("⚠️ Invalid choice, please try again.")
        except KeyboardInterrupt:
            print("\n👋 Goodbye.")
            sys.exit(0)


if __name__ == "__main__":
    manager = EmployeeManager()
    manager.run()
