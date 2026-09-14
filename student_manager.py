"""
Student Manager Module
======================
Python Concepts: Dictionaries (key checking, adding pairs), Lists (append),
                 Loops (for), String operations (strip, lower),
                 Substring checking ('in'), Functions, Validation,
                 Default arguments

This module handles all CRUD operations on student data.
"""

from student import Student


class StudentManager:
    """
    Manages a collection of Student objects.

    Stores students in a dictionary:
        Key   = student_id (string)
        Value = Student object
    """

    def __init__(self):
        """Initialize with empty dictionary."""
        self.students = {}  # Concept: Dictionary as main data store

    def add_student(self, data):
        """
        Add a new student after validation.

        Concepts: Dictionary key checking ('in'), validation,
                  conditionals, functions returning multiple values

        Parameters:
            data (dict): Student data from API request

        Returns:
            tuple: (success: bool, message: str)
        """
        # --- Validate required fields ---
        student_id = str(data.get("student_id", "")).strip()
        name = str(data.get("name", "")).strip()
        department = str(data.get("department", "")).strip().upper()

        if not student_id:
            return (False, "Student ID is required.")

        if not name:
            return (False, "Name is required.")

        if not department:
            return (False, "Department is required.")

        # Concept: Dictionary key checking with 'in'
        if student_id in self.students:
            return (False, f"Student ID '{student_id}' already exists.")

        # --- Validate age ---
        try:
            age = int(data.get("age", 0))
            if age < 15 or age > 60:
                return (False, "Age must be between 15 and 60.")
        except (ValueError, TypeError):
            return (False, "Age must be a valid number.")

        # --- Validate year ---
        try:
            year = int(data.get("year", 0))
            if year < 1 or year > 4:
                return (False, "Year must be between 1 and 4.")
        except (ValueError, TypeError):
            return (False, "Year must be a valid number.")

        # --- Validate marks ---
        marks = data.get("marks", [])
        if not isinstance(marks, list) or len(marks) != len(Student.SUBJECTS):
            return (False, f"Exactly {len(Student.SUBJECTS)} marks are required.")

        validated_marks = []
        for i, mark in enumerate(marks):  # Concept: for loop with enumerate
            try:
                m = int(mark)
                if m < 0 or m > 100:
                    return (False, f"Mark for {Student.SUBJECTS[i]} must be 0-100.")
                validated_marks.append(m)  # Concept: list append()
            except (ValueError, TypeError):
                return (False, f"Mark for {Student.SUBJECTS[i]} must be a number.")

        # --- Create Student object and store ---
        student = Student(student_id, name, age, department, year, validated_marks)
        self.students[student_id] = student  # Concept: Adding key-value pair

        return (True, f"Student '{name}' added successfully!")

    def get_student(self, student_id):
        """
        Get a single student's details.

        Concept: Dictionary key checking, direct access

        Returns:
            dict or None: Student details or None if not found
        """
        if student_id in self.students:
            return self.students[student_id].get_details()
        return None

    def get_all_students(self):
        """
        Get all students as a list of dictionaries.

        Concept: for loop, list building
        """
        result = []
        for student in self.students.values():  # Concept: dict.values()
            result.append(student.get_details())
        return result

    def update_student(self, student_id, data):
        """
        Update an existing student's details.

        Concepts: Dictionary access, conditionals, validation

        Returns:
            tuple: (success: bool, message: str)
        """
        if student_id not in self.students:
            return (False, "Student not found.")

        student = self.students[student_id]

        # Update name if provided
        name = data.get("name", "").strip()
        if name:
            student.name = name

        # Update age if provided
        if "age" in data:
            try:
                age = int(data["age"])
                if 15 <= age <= 60:
                    student.age = age
                else:
                    return (False, "Age must be between 15 and 60.")
            except (ValueError, TypeError):
                return (False, "Age must be a valid number.")

        # Update department if provided
        dept = data.get("department", "").strip()
        if dept:
            student.department = dept.upper()

        # Update year if provided
        if "year" in data:
            try:
                year = int(data["year"])
                if 1 <= year <= 4:
                    student.year = year
                else:
                    return (False, "Year must be between 1 and 4.")
            except (ValueError, TypeError):
                return (False, "Year must be a valid number.")

        # Update marks if provided
        if "marks" in data:
            marks = data["marks"]
            if isinstance(marks, list) and len(marks) == len(Student.SUBJECTS):
                validated = []
                for i, m in enumerate(marks):
                    try:
                        val = int(m)
                        if 0 <= val <= 100:
                            validated.append(val)
                        else:
                            return (False, f"Mark for {Student.SUBJECTS[i]} must be 0-100.")
                    except (ValueError, TypeError):
                        return (False, f"Mark for {Student.SUBJECTS[i]} must be a number.")
                student.marks = validated
            else:
                return (False, f"Exactly {len(Student.SUBJECTS)} marks required.")

        return (True, f"Student '{student.name}' updated successfully!")

    def delete_student(self, student_id):
        """
        Delete a student by ID.

        Concept: Dictionary deletion with 'del', key checking

        Returns:
            tuple: (success: bool, message: str)
        """
        if student_id not in self.students:
            return (False, "Student not found.")

        name = self.students[student_id].name
        del self.students[student_id]  # Concept: del keyword
        return (True, f"Student '{name}' deleted successfully!")

    def search_students(self, query, search_type="all"):
        """
        Search students by ID or name.

        Concepts: String methods (.lower()), substring checking ('in'),
                  string traversal, default arguments

        Parameters:
            query       (str): Search term
            search_type (str): 'id', 'name', or 'all' (default)

        Returns:
            list: Matching students
        """
        query = query.strip().lower()
        results = []

        for sid, student in self.students.items():  # Concept: dict.items()
            matched = False

            if search_type in ("id", "all"):
                # Concept: Substring checking with 'in'
                if query in sid.lower():
                    matched = True

            if search_type in ("name", "all"):
                # Concept: Substring checking — partial name match
                if query in student.name.lower():
                    matched = True

            if matched:
                results.append(student.get_details())

        return results

    def get_all_as_dicts(self):
        """Return all students as simple dicts for file saving."""
        return [s.to_dict() for s in self.students.values()]

    def load_from_dicts(self, data_list):
        """
        Load students from a list of dictionaries (from file).

        Concept: for loop, object creation from data
        """
        for data in data_list:
            try:
                student = Student.from_dict(data)
                self.students[student.student_id] = student
            except (KeyError, TypeError):
                continue  # Skip malformed records
