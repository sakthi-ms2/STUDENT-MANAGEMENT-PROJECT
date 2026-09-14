"""
Student Class Module
====================
Python Concepts: Classes, __init__, self, instance methods,
                 sum(), len(), max(), min(), conditionals,
                 tuples (multiple return values), dictionaries

This module defines the Student class — the core data model.
"""


class Student:
    """
    Represents a student with personal details and academic marks.

    WHY use a class?
        A class bundles data (attributes) and behaviour (methods) together.
        Each Student object holds its own data and can calculate its own
        performance metrics.
    """

    # Class variable — shared by all Student objects
    SUBJECTS = ["Mathematics", "Physics", "Chemistry", "English", "Computer Science"]

    def __init__(self, student_id, name, age, department, year, marks):
        """
        Constructor — runs automatically when creating a Student object.

        Concepts: __init__, self, instance attributes
        """
        self.student_id = student_id   # str  — unique identifier
        self.name = name               # str  — full name
        self.age = age                 # int  — age
        self.department = department   # str  — e.g. "CSE"
        self.year = year               # int  — year of study (1-4)
        self.marks = marks             # list — marks for each subject

    # ---- Instance Methods ----

    def calculate_total(self):
        """Return sum of all marks. Concept: sum()"""
        return sum(self.marks)

    def calculate_average(self):
        """Return average marks. Concept: sum(), len()"""
        if len(self.marks) == 0:
            return 0.0
        return sum(self.marks) / len(self.marks)

    def calculate_grade(self):
        """
        Return letter grade. Concept: if/elif/else
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

    def get_performance(self):
        """
        Return multiple performance metrics.

        Concept: Function returning MULTIPLE values (tuple)

        Returns:
            tuple: (total, average, highest, lowest, grade)
        """
        total = self.calculate_total()
        average = self.calculate_average()
        highest = max(self.marks) if self.marks else 0
        lowest = min(self.marks) if self.marks else 0
        grade = self.calculate_grade()
        return (total, average, highest, lowest, grade)

    def get_details(self):
        """
        Return all details as a dictionary (used for JSON API responses).

        Concept: Dictionaries, method calls
        """
        total, average, highest, lowest, grade = self.get_performance()
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "department": self.department,
            "year": self.year,
            "marks": self.marks,
            "subjects": self.SUBJECTS,
            "total": total,
            "average": round(average, 2),
            "highest": highest,
            "lowest": lowest,
            "grade": grade
        }

    def to_dict(self):
        """Convert to a simple dictionary for file storage."""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "department": self.department,
            "year": self.year,
            "marks": self.marks
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Student from a dictionary (loaded from file)."""
        return cls(
            student_id=data["student_id"],
            name=data["name"],
            age=data["age"],
            department=data["department"],
            year=data["year"],
            marks=data["marks"]
        )
