import json
import os
from datetime import date

DATA_FILE = "employees.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []


def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


def add_employee():
    employees = load_data()

    emp_id = input("Enter Employee ID: ").strip()

    if any(emp["id"] == emp_id for emp in employees):
        print("Employee ID already exists.")
        return

    name = input("Enter Employee Name: ").strip()
    department = input("Enter Department: ").strip()

    employee = {
        "id": emp_id,
        "name": name,
        "department": department,
        "attendance": []
    }

    employees.append(employee)
    save_data(employees)

    print("Employee added successfully.")


def view_employees():
    employees = load_data()

    if not employees:
        print("No employees found.")
        return

    print("\n--- Employee List ---")

    for emp in employees:
        print(
            f"ID: {emp['id']} | "
            f"Name: {emp['name']} | "
            f"Department: {emp['department']}"
        )


def find_employee(emp_id):
    employees = load_data()

    for employee in employees:
        if employee["id"] == emp_id:
            return employee

    return None


def mark_attendance():
    employees = load_data()

    emp_id = input("Enter Employee ID: ").strip()

    employee = None

    for emp in employees:
        if emp["id"] == emp_id:
            employee = emp
            break

    if employee is None:
        print("Employee not found.")
        return

    print("\n1. Present")
    print("2. Absent")

    choice = input("Enter choice: ").strip()

    if choice == "1":
        status = "Present"
    elif choice == "2":
        status = "Absent"
    else:
        print("Invalid choice.")
        return

    today = str(date.today())

    for record in employee["attendance"]:
        if record["date"] == today:
            print("Attendance already marked for today.")
            return

    employee["attendance"].append({
        "date": today,
        "status": status
    })

    save_data(employees)

    print(f"Attendance marked as {status}.")


def view_attendance():
    emp_id = input("Enter Employee ID: ").strip()

    employee = find_employee(emp_id)

    if employee is None:
        print("Employee not found.")
        return

    print(f"\n--- Attendance: {employee['name']} ---")

    if not employee["attendance"]:
        print("No attendance records found.")
        return

    for record in employee["attendance"]:
        print(f"{record['date']} - {record['status']}")


def attendance_percentage():
    emp_id = input("Enter Employee ID: ").strip()

    employee = find_employee(emp_id)

    if employee is None:
        print("Employee not found.")
        return

    records = employee["attendance"]

    if not records:
        print("No attendance records found.")
        return

    total_days = len(records)
    present_days = sum(
        1 for record in records
        if record["status"] == "Present"
    )

    percentage = (present_days / total_days) * 100

    print(f"\nEmployee: {employee['name']}")
    print(f"Total Days: {total_days}")
    print(f"Present: {present_days}")
    print(f"Absent: {total_days - present_days}")
    print(f"Attendance: {percentage:.2f}%")


def search_employee():
    employees = load_data()

    keyword = input("Enter employee name or ID: ").strip().lower()

    results = [
        emp for emp in employees
        if keyword in emp["name"].lower()
        or keyword in emp["id"].lower()
    ]

    if not results:
        print("No employee found.")
        return

    print("\n--- Search Results ---")

    for emp in results:
        print(
            f"ID: {emp['id']} | "
            f"Name: {emp['name']} | "
            f"Department: {emp['department']}"
        )


def delete_employee():
    employees = load_data()

    emp_id = input("Enter Employee ID to delete: ").strip()

    employee = next(
        (emp for emp in employees if emp["id"] == emp_id),
        None
    )

    if employee is None:
        print("Employee not found.")
        return

    employees.remove(employee)
    save_data(employees)

    print("Employee deleted successfully.")


def main():
    while True:
        print("\n" + "=" * 40)
        print("   EMPLOYEE ATTENDANCE MANAGER")
        print("=" * 40)

        print("1. Add Employee")
        print("2. View Employees")
        print("3. Mark Attendance")
        print("4. View Attendance")
        print("5. Attendance Percentage")
        print("6. Search Employee")
        print("7. Delete Employee")
        print("8. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            add_employee()

        elif choice == "2":
            view_employees()

        elif choice == "3":
            mark_attendance()

        elif choice == "4":
            view_attendance()

        elif choice == "5":
            attendance_percentage()

        elif choice == "6":
            search_employee()

        elif choice == "7":
            delete_employee()

        elif choice == "8":
            print("Thank you for using Employee Attendance Manager.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
