"""
===============================================================================
    STUDENT PERFORMANCE & RECORD MANAGEMENT SYSTEM
    ------------------------------------------------
    A console-based Python mini project for college lab manual.

    Python Concepts Covered:
        Variables, Input/Output, Conditionals, For/While/Nested Loops,
        Strings, String Traversal, Substring Checking,
        Lists (append, insert, slicing), len(), max(), min(), sum(), sorted(),
        Tuples, Tuple Concatenation, Functions (multiple returns, default args),
        Dictionaries (key checking, adding key-value pairs),
        File Handling (read, write, with open),
        Classes (__init__, self, instance methods),
        NumPy Arrays, Pandas DataFrame
===============================================================================
"""

# ========================== IMPORTS ==========================
# NumPy — used for numerical analysis on marks (MODULE 11)
# Pandas — used for tabular data analysis (MODULE 12)
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("[Warning] NumPy not installed. Install with: pip install numpy")

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("[Warning] Pandas not installed. Install with: pip install pandas")


# ========================== GLOBAL DATA ==========================
# We use a dictionary to store all students.
# Key   = student_id (string)
# Value = dictionary with student details
# Example:
#   students["101"] = {
#       "name": "Alice",
#       "age": 20,
#       "department": "CSE",
#       "year": 2,
#       "marks": [85, 90, 78, 92, 88]
#   }

students = {}  # Main data store (dictionary of dictionaries)

# Subject list — used when entering/displaying marks
SUBJECTS = ["Mathematics", "Physics", "Chemistry", "English", "Computer Science"]


# ========================== MODULE 10 — OOP VERSION ==========================
# Concept: Classes, __init__ constructor, self, instance methods, object creation

class Student:
    """
    A class to represent a student.

    WHY use a class?
        A class bundles data (attributes) and behaviour (methods) together.
        Instead of keeping a student's info in a separate dictionary and
        writing standalone functions, we put everything inside one 'Student'
        object. This makes the code organised and reusable.

    Attributes:
        student_id (str) : Unique identifier
        name       (str) : Student's full name
        age        (int) : Student's age
        department (str) : Department code (e.g. CSE, ECE)
        year       (int) : Current year of study
        marks      (list): List of integer marks for each subject
    """

    # __init__ is the CONSTRUCTOR — it runs automatically when we create
    # a new Student object.  'self' refers to the object being created.
    def __init__(self, student_id, name, age, department, year, marks):
        self.student_id = student_id    # instance attribute
        self.name = name
        self.age = age
        self.department = department
        self.year = year
        self.marks = marks              # list of marks

    # ---- Instance Methods ----
    # These are functions that belong to the Student class.
    # They use 'self' to access the object's own data.

    def calculate_total(self):
        """Return the sum of all marks using the built-in sum()."""
        return sum(self.marks)          # Concept: sum()

    def calculate_average(self):
        """Return the average marks."""
        if len(self.marks) == 0:        # Concept: len()
            return 0.0
        return sum(self.marks) / len(self.marks)

    def calculate_grade(self):
        """
        Return a letter grade based on average marks.
        Concept: Conditional statements (if/elif/else)
        """
        avg = self.calculate_average()
        if avg >= 90:
            return "A+"
        elif avg >= 80:
            return "A"
        elif avg >= 70:
            return "B"
        elif avg >= 60:
            return "C"
        elif avg >= 50:
            return "D"
        else:
            return "F"

    def display_details(self):
        """
        Print all details of this student.
        Concept: String formatting, loops
        """
        print(f"\n  Student ID  : {self.student_id}")
        print(f"  Name        : {self.name}")
        print(f"  Age         : {self.age}")
        print(f"  Department  : {self.department}")
        print(f"  Year        : {self.year}")
        print(f"  Marks       : {self.marks}")
        print(f"  Total       : {self.calculate_total()}")
        print(f"  Average     : {self.calculate_average():.2f}")
        print(f"  Grade       : {self.calculate_grade()}")


# ========================== MODULE 1 — STUDENT REGISTRATION ==========================
# Concepts: input(), variables, dictionaries, lists, list append(), functions, validation

def get_valid_marks():
    """
    Ask the user to enter marks for each subject.
    Validates that each mark is a number between 0 and 100.

    Concepts practised:
        - for loop (iterate over subjects)
        - while loop (keep asking until valid input)
        - input() and int() conversion
        - try/except for error handling
        - list append()

    Returns:
        list: A list of integer marks
    """
    marks = []  # empty list — we will append marks one by one

    for subject in SUBJECTS:  # Concept: for loop over a list
        while True:  # Concept: while loop for validation
            try:
                mark = int(input(f"    Enter marks for {subject} (0-100): "))
                if 0 <= mark <= 100:  # Concept: conditional check
                    marks.append(mark)  # Concept: list append()
                    break
                else:
                    print("    [!] Marks must be between 0 and 100.")
            except ValueError:
                print("    [!] Please enter a valid number.")

    return marks


def add_student():
    """
    Register a new student by collecting all details from the user.

    Concepts practised:
        - input() for user input
        - Variables to store data
        - String methods (.strip(), .upper())
        - Dictionary — adding key-value pairs
        - Dictionary key checking (using 'in')
        - Functions
        - Validation with conditionals
    """
    print("\n--- ADD NEW STUDENT ---")

    # --- Get Student ID ---
    student_id = input("  Enter Student ID: ").strip()

    # Validate: ID must not be empty
    if student_id == "":  # Concept: string comparison
        print("  [!] Student ID cannot be empty.")
        return

    # Validate: ID must not already exist
    # Concept: Dictionary key checking using 'in'
    if student_id in students:
        print(f"  [!] Student ID '{student_id}' already exists.")
        return

    # --- Get Name ---
    name = input("  Enter Name: ").strip()
    if name == "":
        print("  [!] Name cannot be empty.")
        return

    # --- Get Age ---
    try:
        age = int(input("  Enter Age: "))
        if age < 15 or age > 60:
            print("  [!] Age must be between 15 and 60.")
            return
    except ValueError:
        print("  [!] Please enter a valid age.")
        return

    # --- Get Department ---
    department = input("  Enter Department (e.g. CSE, ECE, ME): ").strip().upper()
    if department == "":
        print("  [!] Department cannot be empty.")
        return

    # --- Get Year ---
    try:
        year = int(input("  Enter Year (1-4): "))
        if year < 1 or year > 4:
            print("  [!] Year must be between 1 and 4.")
            return
    except ValueError:
        print("  [!] Please enter a valid year.")
        return

    # --- Get Marks ---
    print(f"\n  Enter marks for {len(SUBJECTS)} subjects:")
    marks = get_valid_marks()

    # --- Store in dictionary ---
    # Concept: Adding a new key-value pair to a dictionary
    # The value itself is another dictionary (nested dictionary)
    students[student_id] = {
        "name": name,
        "age": age,
        "department": department,
        "year": year,
        "marks": marks
    }

    print(f"\n  [✓] Student '{name}' (ID: {student_id}) added successfully!")


# ========================== MODULE 2 — STUDENT DISPLAY ==========================
# Concepts: for loops, nested loops, dictionaries, string formatting, functions

def view_all_students():
    """
    Display all students in a formatted table.

    Concepts practised:
        - Dictionary iteration (.items())
        - for loop
        - String formatting (f-strings)
        - len() to count students
    """
    print("\n--- ALL STUDENTS ---")

    if len(students) == 0:  # Concept: len() on dictionary
        print("  No students found.")
        return

    print(f"  {'ID':<8} {'Name':<20} {'Dept':<8} {'Year':<6} {'Total':<8} {'Avg':<8} {'Grade'}")
    print("  " + "-" * 72)

    # Concept: for loop over dictionary items
    for sid, info in students.items():
        total = sum(info["marks"])          # Concept: sum()
        avg = total / len(info["marks"])    # Concept: len()
        grade = get_grade(avg)              # Calling our function
        print(f"  {sid:<8} {info['name']:<20} {info['department']:<8} {info['year']:<6} {total:<8} {avg:<8.2f} {grade}")

    print(f"\n  Total students: {len(students)}")


def view_single_student():
    """
    Display details for one student.

    Concepts practised:
        - input()
        - Dictionary key checking ('in')
        - Nested loops (marks with subject names)
    """
    print("\n--- VIEW STUDENT DETAILS ---")
    student_id = input("  Enter Student ID: ").strip()

    if student_id not in students:  # Concept: dictionary key checking
        print(f"  [!] Student ID '{student_id}' not found.")
        return

    info = students[student_id]

    print(f"\n  Student ID  : {student_id}")
    print(f"  Name        : {info['name']}")
    print(f"  Age         : {info['age']}")
    print(f"  Department  : {info['department']}")
    print(f"  Year        : {info['year']}")

    # Display marks with subject names
    # Concept: Nested loop — for loop with index (using enumerate or zip)
    print("\n  Subject-wise Marks:")
    for i in range(len(SUBJECTS)):  # Concept: for loop with range and len
        print(f"    {SUBJECTS[i]:<20} : {info['marks'][i]}")

    # Calculate performance using our function that returns multiple values
    total, avg, highest, lowest, grade = calculate_performance(info["marks"])

    print(f"\n  Total       : {total}")
    print(f"  Average     : {avg:.2f}")
    print(f"  Highest     : {highest}")
    print(f"  Lowest      : {lowest}")
    print(f"  Grade       : {grade}")


def display_students_menu():
    """Sub-menu for viewing students."""
    print("\n--- VIEW STUDENTS ---")
    print("  1. View All Students")
    print("  2. View Single Student")
    choice = input("  Enter choice (1/2): ").strip()

    if choice == "1":
        view_all_students()
    elif choice == "2":
        view_single_student()
    else:
        print("  [!] Invalid choice.")


# ========================== MODULE 3 — SEARCH ==========================
# Concepts: dictionary lookup, string comparison, substring checking, string traversal

def search_by_id():
    """
    Search for a student by exact Student ID.

    Concepts practised:
        - Dictionary key checking using 'in'
        - Direct dictionary access
    """
    student_id = input("  Enter Student ID to search: ").strip()

    if student_id in students:  # Concept: dictionary key lookup
        info = students[student_id]
        print(f"\n  [✓] Student found!")
        print(f"  ID: {student_id}, Name: {info['name']}, Dept: {info['department']}")
    else:
        print(f"  [!] No student found with ID '{student_id}'.")


def search_by_name():
    """
    Search for students whose name contains a given substring.

    Concepts practised:
        - String traversal (iterating through characters)
        - Substring checking using 'in' operator on strings
        - String method .lower() for case-insensitive search
        - for loop over dictionary
    """
    search_name = input("  Enter name (or part of name) to search: ").strip().lower()

    if search_name == "":
        print("  [!] Search term cannot be empty.")
        return

    # --- Demonstrate string traversal ---
    # Let's show the user what characters they're searching for
    print(f"  Searching for characters: ", end="")
    for char in search_name:  # Concept: String traversal (iterating character by character)
        print(f"'{char}' ", end="")
    print()

    # --- Search using substring checking ---
    found = []  # list to collect matching results

    for sid, info in students.items():
        # Concept: Substring checking using 'in' with strings
        # "ali" in "Alice".lower() → "ali" in "alice" → True
        if search_name in info["name"].lower():
            found.append((sid, info["name"], info["department"]))  # Concept: tuple, list append

    if len(found) > 0:
        print(f"\n  [✓] Found {len(found)} student(s):")
        for sid, name, dept in found:  # Concept: unpacking a tuple
            print(f"    ID: {sid}, Name: {name}, Department: {dept}")
    else:
        print(f"  [!] No students found matching '{search_name}'.")


def search_student():
    """Sub-menu for search options."""
    print("\n--- SEARCH STUDENT ---")
    print("  1. Search by Student ID")
    print("  2. Search by Name")
    choice = input("  Enter choice (1/2): ").strip()

    if choice == "1":
        search_by_id()
    elif choice == "2":
        search_by_name()
    else:
        print("  [!] Invalid choice.")


# ========================== MODULE 4 — UPDATE STUDENT ==========================
# Concepts: dictionary update, modifying values, functions

def update_student():
    """
    Update an existing student's details.

    Concepts practised:
        - Dictionary key checking
        - Modifying dictionary values
        - Conditional statements
        - Functions calling other functions
    """
    print("\n--- UPDATE STUDENT ---")
    student_id = input("  Enter Student ID to update: ").strip()

    if student_id not in students:
        print(f"  [!] Student ID '{student_id}' not found.")
        return

    info = students[student_id]
    print(f"  Current details for '{info['name']}':")
    print(f"    1. Name        : {info['name']}")
    print(f"    2. Age         : {info['age']}")
    print(f"    3. Department  : {info['department']}")
    print(f"    4. Marks       : {info['marks']}")

    print("\n  What do you want to update?")
    print("    1. Name")
    print("    2. Age")
    print("    3. Department")
    print("    4. Marks")
    choice = input("  Enter choice (1-4): ").strip()

    if choice == "1":
        new_name = input("  Enter new name: ").strip()
        if new_name != "":
            students[student_id]["name"] = new_name  # Concept: dictionary value update
            print(f"  [✓] Name updated to '{new_name}'.")
        else:
            print("  [!] Name cannot be empty.")

    elif choice == "2":
        try:
            new_age = int(input("  Enter new age: "))
            if 15 <= new_age <= 60:
                students[student_id]["age"] = new_age
                print(f"  [✓] Age updated to {new_age}.")
            else:
                print("  [!] Age must be between 15 and 60.")
        except ValueError:
            print("  [!] Invalid age.")

    elif choice == "3":
        new_dept = input("  Enter new department: ").strip().upper()
        if new_dept != "":
            students[student_id]["department"] = new_dept
            print(f"  [✓] Department updated to '{new_dept}'.")
        else:
            print("  [!] Department cannot be empty.")

    elif choice == "4":
        print("  Re-enter marks for all subjects:")
        new_marks = get_valid_marks()
        students[student_id]["marks"] = new_marks
        print("  [✓] Marks updated successfully.")

    else:
        print("  [!] Invalid choice.")


# ========================== MODULE 5 — DELETE STUDENT ==========================
# Concepts: dictionary deletion (del keyword), key checking

def delete_student():
    """
    Delete a student by Student ID.

    Concepts practised:
        - Dictionary key checking
        - del keyword to remove a key-value pair from a dictionary

    HOW DELETION WORKS INTERNALLY:
        Dictionaries in Python are hash tables. When you use 'del dict[key]',
        Python finds the key's location using its hash, removes the key-value
        pair from memory, and adjusts the internal structure. The key is no
        longer accessible after deletion.
    """
    print("\n--- DELETE STUDENT ---")
    student_id = input("  Enter Student ID to delete: ").strip()

    if student_id not in students:
        print(f"  [!] Student ID '{student_id}' not found.")
        return

    name = students[student_id]["name"]

    # Confirm before deleting
    confirm = input(f"  Are you sure you want to delete '{name}' (ID: {student_id})? (y/n): ").strip().lower()

    if confirm == "y":
        del students[student_id]  # Concept: del keyword removes key from dictionary
        print(f"  [✓] Student '{name}' (ID: {student_id}) deleted successfully.")
    else:
        print("  [✗] Deletion cancelled.")


# ========================== MODULE 6 — MARKS & GRADE CALCULATION ==========================
# Concepts: functions, multiple return values, tuples, sum(), max(), min(), sorted(),
#           default arguments, tuple concatenation

def get_grade(average):
    """
    Return a letter grade based on average.

    Concept: Function with a single parameter and return value.
    """
    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    else:
        return "F"


def calculate_performance(marks):
    """
    Calculate total, average, highest, lowest, and grade from a list of marks.

    Concepts practised:
        - Function returning MULTIPLE values (as a tuple)
        - sum(), max(), min(), len()
        - Calling another function (get_grade)

    Parameters:
        marks (list): List of integer marks

    Returns:
        tuple: (total, average, highest, lowest, grade)

    WHY return multiple values?
        Sometimes a function needs to give back more than one result.
        Python lets you return a tuple of values, which the caller can
        unpack into separate variables:
            total, avg, high, low, grade = calculate_performance(marks)
    """
    total = sum(marks)          # Concept: sum()
    average = total / len(marks)  # Concept: len()
    highest = max(marks)        # Concept: max()
    lowest = min(marks)         # Concept: min()
    grade = get_grade(average)

    # Concept: Returning multiple values as a tuple
    return (total, average, highest, lowest, grade)


def get_sorted_marks(marks, reverse_order=False):
    """
    Return marks sorted in ascending or descending order.

    Concepts practised:
        - sorted() built-in function
        - Default function arguments (reverse_order defaults to False)

    Parameters:
        marks (list)        : List of marks
        reverse_order (bool): If True, sort descending. Defaults to False.

    Returns:
        list: Sorted list of marks
    """
    # Concept: sorted() returns a NEW sorted list (does not change the original)
    # Concept: Default argument — reverse_order=False means ascending by default
    return sorted(marks, reverse=reverse_order)


def calculate_performance_menu():
    """Sub-menu for performance calculation."""
    print("\n--- CALCULATE PERFORMANCE ---")
    student_id = input("  Enter Student ID: ").strip()

    if student_id not in students:
        print(f"  [!] Student ID '{student_id}' not found.")
        return

    info = students[student_id]
    marks = info["marks"]

    # Call the function that returns multiple values
    total, avg, highest, lowest, grade = calculate_performance(marks)

    # Demonstrate sorted() with default argument
    marks_ascending = get_sorted_marks(marks)               # uses default: ascending
    marks_descending = get_sorted_marks(marks, True)        # override: descending

    # --- Demonstrate Tuple Concatenation ---
    # Concept: Tuples are immutable sequences. You can join two tuples with +
    basic_stats = (total, avg)
    extra_stats = (highest, lowest, grade)
    all_stats = basic_stats + extra_stats  # Concept: Tuple concatenation
    print(f"\n  All stats (tuple concatenation): {all_stats}")

    print(f"\n  Student     : {info['name']}")
    print(f"  Marks       : {marks}")
    print(f"  Sorted (↑)  : {marks_ascending}")
    print(f"  Sorted (↓)  : {marks_descending}")
    print(f"  Total       : {total}")
    print(f"  Average     : {avg:.2f}")
    print(f"  Highest     : {highest}")
    print(f"  Lowest      : {lowest}")
    print(f"  Grade       : {grade}")

    # --- Demonstrate List Slicing ---
    # Concept: list[start:end] gives a sub-list (slice)
    if len(marks) >= 3:
        top_3 = get_sorted_marks(marks, True)[:3]  # Concept: List slicing — first 3 elements
        print(f"  Top 3 marks : {top_3}")

    # --- Demonstrate List insert() ---
    # Concept: list.insert(index, value) — insert at a specific position
    marks_copy = marks.copy()
    marks_copy.insert(0, -1)  # Insert a placeholder at position 0
    print(f"  Marks with placeholder at index 0: {marks_copy}")
    marks_copy.pop(0)  # Remove the placeholder
    print(f"  Marks after removing placeholder  : {marks_copy}")


# ========================== MODULE 7 — STUDENT RANKING ==========================
# Concepts: sorted() with key function, custom sorting, list of tuples

def rank_students():
    """
    Sort and display students based on their average marks (highest first).

    Concepts practised:
        - sorted() with a key function
        - Custom sorting logic using lambda
        - for loop with enumerate for ranking numbers

    HOW sorted() WORKS WITH key:
        sorted(iterable, key=function) sorts items based on the value
        returned by the key function.

        Example:
            sorted(students.items(), key=lambda x: sum(x[1]["marks"]))
            For each item, the lambda calculates the total marks.
            sorted() uses these totals to decide the order.
    """
    print("\n--- STUDENT RANKING ---")

    if len(students) == 0:
        print("  No students to rank.")
        return

    # Create a list of (student_id, info_dict) sorted by average marks (descending)
    # Concept: sorted() with key parameter
    # lambda x: ... is a small anonymous function
    # x is each (id, info) pair from students.items()
    ranked = sorted(
        students.items(),
        key=lambda x: sum(x[1]["marks"]) / len(x[1]["marks"]),
        reverse=True  # Highest first
    )

    print(f"  {'Rank':<6} {'ID':<8} {'Name':<20} {'Total':<8} {'Average':<10} {'Grade'}")
    print("  " + "-" * 60)

    # Concept: enumerate gives us the index (used as rank number)
    for rank, (sid, info) in enumerate(ranked, start=1):
        total = sum(info["marks"])
        avg = total / len(info["marks"])
        grade = get_grade(avg)
        print(f"  {rank:<6} {sid:<8} {info['name']:<20} {total:<8} {avg:<10.2f} {grade}")


# ========================== MODULE 8 — CLASS STATISTICS ==========================
# Concepts: loops, dictionaries, lists, built-in functions, nested loops

def class_statistics():
    """
    Display class-level statistics.

    Concepts practised:
        - Loops over dictionaries
        - Building a new dictionary (grade_count)
        - max(), min() on computed values
        - len(), sum() for aggregation
    """
    print("\n--- CLASS STATISTICS ---")

    if len(students) == 0:
        print("  No students available.")
        return

    all_averages = []       # list to store all averages
    grade_count = {}        # dictionary to count students in each grade
    top_student = None
    top_avg = -1

    # Concept: for loop over dictionary
    for sid, info in students.items():
        marks = info["marks"]
        avg = sum(marks) / len(marks)
        all_averages.append(avg)    # Concept: list append()
        grade = get_grade(avg)

        # Concept: Dictionary key checking and adding key-value pairs
        if grade in grade_count:
            grade_count[grade] = grade_count[grade] + 1
        else:
            grade_count[grade] = 1  # Concept: adding a new key-value pair

        # Track top student
        if avg > top_avg:
            top_avg = avg
            top_student = info["name"]

    # Calculate class-level stats
    class_avg = sum(all_averages) / len(all_averages)  # Concept: sum(), len()
    highest_avg = max(all_averages)                     # Concept: max()
    lowest_avg = min(all_averages)                      # Concept: min()

    print(f"\n  Number of Students  : {len(students)}")
    print(f"  Class Average       : {class_avg:.2f}")
    print(f"  Highest Average     : {highest_avg:.2f}")
    print(f"  Lowest Average      : {lowest_avg:.2f}")
    print(f"  Top Student         : {top_student} ({top_avg:.2f})")

    print("\n  Grade Distribution:")
    # Concept: sorted() on dictionary keys for neat display
    for grade in sorted(grade_count.keys()):
        count = grade_count[grade]
        bar = "█" * count  # simple visual bar
        print(f"    Grade {grade:<3} : {count} student(s) {bar}")


# ========================== MODULE 9 — FILE HANDLING ==========================
# Concepts: open(), read(), write(), close(), with open(), file modes

def save_to_file(filename="students.txt"):
    """
    Save all student records to a text file.

    Concepts practised:
        - open() with mode 'w' (write)
        - write() method
        - with open() — auto-closes the file
        - Default function argument (filename)
        - for loop to write each student
        - String formatting for file storage

    WHY use file handling?
        When you close the program, all data in variables (RAM) is lost.
        Files let you save data permanently on disk so it persists
        between program runs.

    FILE FORMAT (one line per student):
        student_id|name|age|department|year|mark1,mark2,mark3,mark4,mark5
    """
    print("\n--- SAVE DATA ---")

    if len(students) == 0:
        print("  No data to save.")
        return

    # Concept: 'with open()' — automatically closes the file when done
    # Mode 'w' = write (creates file or overwrites existing)
    with open(filename, "w") as file:
        for sid, info in students.items():
            # Convert marks list to comma-separated string
            marks_str = ",".join(str(m) for m in info["marks"])

            # Create one line with fields separated by '|'
            line = f"{sid}|{info['name']}|{info['age']}|{info['department']}|{info['year']}|{marks_str}\n"

            file.write(line)  # Concept: write() method

    print(f"  [✓] {len(students)} student(s) saved to '{filename}'.")


def load_from_file(filename="students.txt"):
    """
    Load student records from a text file.

    Concepts practised:
        - open() with mode 'r' (read)
        - read() / readlines()
        - with open()
        - String split() to parse data
        - try/except for file-not-found error
        - List comprehension (simple form)

    Parameters:
        filename (str): Name of the file. Defaults to 'students.txt'.
    """
    print("\n--- LOAD DATA ---")

    try:
        # Concept: 'with open()' with mode 'r' (read)
        with open(filename, "r") as file:
            lines = file.readlines()  # Concept: readlines() returns a list of lines

        count = 0
        for line in lines:
            line = line.strip()  # Remove newline character
            if line == "":
                continue

            # Concept: String split() — break the line into parts
            parts = line.split("|")

            if len(parts) != 6:
                print(f"  [!] Skipping malformed line: {line}")
                continue

            student_id = parts[0]
            name = parts[1]
            age = int(parts[2])
            department = parts[3]
            year = int(parts[4])
            marks = [int(m) for m in parts[5].split(",")]  # Convert strings to ints

            # Store in our dictionary
            students[student_id] = {
                "name": name,
                "age": age,
                "department": department,
                "year": year,
                "marks": marks
            }
            count += 1

        print(f"  [✓] {count} student(s) loaded from '{filename}'.")

    except FileNotFoundError:
        # Concept: Exception handling — catching specific errors
        print(f"  [!] File '{filename}' not found. No data loaded.")
    except Exception as e:
        print(f"  [!] Error reading file: {e}")


# ========================== MODULE 10 — OOP DEMO ==========================
# (Student class is defined above; this function demonstrates using it)

def oop_demo():
    """
    Demonstrate the Student class using existing data.

    Concepts practised:
        - Object creation (instantiation)
        - Calling instance methods
        - class, __init__, self
    """
    print("\n--- OOP DEMONSTRATION ---")

    if len(students) == 0:
        print("  No students available. Add a student first.")
        return

    print("  Converting dictionary data to Student objects...\n")

    # Create Student objects from our dictionary data
    student_objects = []  # list of Student objects

    for sid, info in students.items():
        # Concept: Object creation — calling the class like a function
        obj = Student(
            student_id=sid,
            name=info["name"],
            age=info["age"],
            department=info["department"],
            year=info["year"],
            marks=info["marks"]
        )
        student_objects.append(obj)

    # Display details using the instance method
    for obj in student_objects:
        print("  " + "=" * 40)
        obj.display_details()  # Concept: calling an instance method
        print()

    print(f"  Total Student objects created: {len(student_objects)}")


# ========================== MODULE 11 — NUMPY ANALYSIS ==========================
# Concepts: NumPy array creation, basic numerical operations

def numpy_analysis():
    """
    Perform numerical analysis on marks using NumPy.

    Concepts practised:
        - Creating a 1D NumPy array from a list
        - np.mean(), np.max(), np.min(), np.std()
        - Array arithmetic (e.g., scaling marks)

    WHY use NumPy?
        NumPy is optimised for numerical computations. It can process
        large arrays of numbers much faster than regular Python lists.
        For this small project, the speed difference is negligible,
        but we practise NumPy because it's essential for data science.
    """
    print("\n--- NUMPY ANALYSIS ---")

    if not NUMPY_AVAILABLE:
        print("  [!] NumPy is not installed. Run: pip install numpy")
        return

    if len(students) == 0:
        print("  No students available.")
        return

    # Collect all marks into one flat list
    all_marks = []
    for sid, info in students.items():
        for mark in info["marks"]:
            all_marks.append(mark)

    # Concept: Creating a 1D NumPy array from a Python list
    marks_array = np.array(all_marks)

    print(f"  NumPy Array   : {marks_array}")
    print(f"  Shape         : {marks_array.shape}")
    print(f"  Data Type     : {marks_array.dtype}")
    print(f"  Mean          : {np.mean(marks_array):.2f}")       # Concept: np.mean()
    print(f"  Maximum       : {np.max(marks_array)}")             # Concept: np.max()
    print(f"  Minimum       : {np.min(marks_array)}")             # Concept: np.min()
    print(f"  Std Deviation : {np.std(marks_array):.2f}")         # Concept: np.std()
    print(f"  Sum           : {np.sum(marks_array)}")             # Concept: np.sum()

    # Concept: Array arithmetic — operations apply to every element
    scaled = marks_array / 100.0 * 10  # Convert percentage to GPA scale (out of 10)
    print(f"\n  Marks scaled to GPA (out of 10):")
    print(f"  {scaled}")

    # Per-student analysis
    print("\n  Per-Student NumPy Analysis:")
    print(f"  {'ID':<8} {'Name':<20} {'Mean':<10} {'Max':<6} {'Min':<6}")
    print("  " + "-" * 52)

    for sid, info in students.items():
        student_marks = np.array(info["marks"])  # Concept: creating array
        print(f"  {sid:<8} {info['name']:<20} {np.mean(student_marks):<10.2f} {np.max(student_marks):<6} {np.min(student_marks):<6}")


# ========================== MODULE 12 — PANDAS ANALYSIS ==========================
# Concepts: DataFrame creation, head(), column selection, row selection, basic stats

def pandas_analysis():
    """
    Analyse student data using Pandas DataFrame.

    Concepts practised:
        - Creating a DataFrame from a list of dictionaries
        - head() — view first few rows
        - Selecting columns (df["column"] or df[["col1","col2"]])
        - Selecting rows (df.loc, df.iloc)
        - describe() — basic statistics
        - Accessing individual values

    WHY use Pandas?
        Pandas makes tabular data easy to work with. It's like having
        an Excel spreadsheet in Python. You can filter, sort, group,
        and analyse data with just a few lines of code.

    WHAT is a DataFrame?
        A DataFrame is a 2D table with rows and columns, similar to
        a spreadsheet or a database table. Each column can have a name.
    """
    print("\n--- PANDAS ANALYSIS ---")

    if not PANDAS_AVAILABLE:
        print("  [!] Pandas is not installed. Run: pip install pandas")
        return

    if len(students) == 0:
        print("  No students available.")
        return

    # --- Concept: Creating a DataFrame from a list of dictionaries ---
    data_list = []
    for sid, info in students.items():
        row = {
            "Student_ID": sid,
            "Name": info["name"],
            "Age": info["age"],
            "Department": info["department"],
            "Year": info["year"],
            "Total": sum(info["marks"]),
            "Average": sum(info["marks"]) / len(info["marks"]),
            "Grade": get_grade(sum(info["marks"]) / len(info["marks"]))
        }
        # Add individual subject marks as columns
        for i, subject in enumerate(SUBJECTS):
            row[subject] = info["marks"][i]

        data_list.append(row)

    df = pd.DataFrame(data_list)  # Concept: DataFrame creation

    # --- Concept: head() — display first few rows ---
    print("\n  DataFrame (head):")
    print(df.head().to_string(index=False))

    # --- Concept: Selecting specific columns ---
    print("\n  Selected Columns (Name, Total, Grade):")
    selected = df[["Name", "Total", "Grade"]]  # Concept: column selection
    print(selected.to_string(index=False))

    # --- Concept: Selecting rows using iloc (by position) ---
    if len(df) > 0:
        print(f"\n  First student (iloc[0]):")
        print(df.iloc[0])  # Concept: row selection by index position

    # --- Concept: Accessing an individual value ---
    if len(df) > 0:
        first_name = df.loc[0, "Name"]  # Concept: accessing specific cell
        print(f"\n  First student's name (df.loc[0, 'Name']): {first_name}")

    # --- Concept: Basic statistics using describe() ---
    print("\n  Basic Statistics (describe):")
    numeric_cols = df.select_dtypes(include="number")
    print(numeric_cols.describe().to_string())

    # --- Optional: Department-wise average ---
    print("\n  Department-wise Average Marks:")
    dept_avg = df.groupby("Department")["Average"].mean()
    print(dept_avg.to_string())


# ========================== MAIN MENU ==========================
# Concepts: while loop, input(), if/elif/else, function calls

def show_menu():
    """
    Display the main menu.
    Concept: Functions, print(), string formatting
    """
    print("\n" + "=" * 55)
    print("   STUDENT PERFORMANCE & RECORD MANAGEMENT SYSTEM")
    print("=" * 55)
    print("   1.  Add Student")
    print("   2.  View Students")
    print("   3.  Search Student")
    print("   4.  Update Student")
    print("   5.  Delete Student")
    print("   6.  Calculate Performance")
    print("   7.  Student Ranking")
    print("   8.  Class Statistics")
    print("   9.  Save Data to File")
    print("  10.  Load Data from File")
    print("  11.  NumPy Analysis")
    print("  12.  Pandas Analysis")
    print("  13.  OOP Demonstration")
    print("  14.  Exit")
    print("=" * 55)


def main():
    """
    Main function — runs the menu loop.

    Concepts practised:
        - while True loop (keeps program running)
        - input() to read user's choice
        - if/elif/else to route to the correct function
        - break to exit the loop
    """
    print("\n  Welcome to the Student Performance & Record Management System!")
    print("  This is a Python mini project for college lab practice.")

    # Concept: while True — infinite loop that runs until 'break'
    while True:
        show_menu()
        choice = input("\n  Enter your choice (1-14): ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            display_students_menu()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            calculate_performance_menu()
        elif choice == "7":
            rank_students()
        elif choice == "8":
            class_statistics()
        elif choice == "9":
            save_to_file()
        elif choice == "10":
            load_from_file()
        elif choice == "11":
            numpy_analysis()
        elif choice == "12":
            pandas_analysis()
        elif choice == "13":
            oop_demo()
        elif choice == "14":
            print("\n  Thank you for using the system. Goodbye! 👋")
            break  # Concept: break — exit the while loop
        else:
            print("  [!] Invalid choice. Please enter a number between 1 and 14.")


# ========================== ENTRY POINT ==========================
# This ensures main() runs only when we execute this file directly,
# not when it's imported as a module by another file.

if __name__ == "__main__":
    main()
