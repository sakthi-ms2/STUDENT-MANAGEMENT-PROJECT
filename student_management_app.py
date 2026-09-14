"""
==============================================================================
  STUDENT PERFORMANCE & RECORD MANAGEMENT SYSTEM
  Full-Stack Single-File Application
  ----------------------------------
  Backend  : Python + Flask (REST API)
  Frontend : HTML + CSS + JavaScript (embedded)
  Storage  : JSON file
  Analysis : NumPy + Pandas

  HOW TO RUN:
      pip install flask flask-cors numpy pandas
      python student_management_app.py

  Then open: http://localhost:5000
==============================================================================

  Python Lab Concepts Covered:
      Variables, Input/Output, Conditionals, For/While/Nested Loops,
      Strings, Substring Checking, Lists (append, insert, slicing),
      len(), max(), min(), sum(), sorted(),
      Tuples, Tuple Concatenation,
      Functions (multiple returns, default args),
      Dictionaries (key checking, adding pairs),
      File Handling (open, read, write, with, try/except, JSON),
      Classes (__init__, self, instance methods, object creation),
      NumPy Arrays, Pandas DataFrame
==============================================================================
"""

# ========================== IMPORTS ==========================
import json
import os

from flask import Flask, request, jsonify, Response
from flask_cors import CORS

# NumPy and Pandas are optional - app works without them
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


# ========================== STUDENT CLASS (OOP) ==========================
# Concepts: class, __init__, self, instance methods, sum(), len(), max(),
#           min(), conditionals, tuples (multiple returns), dictionaries

class Student:
    """
    Represents a student with personal details and academic marks.

    WHY use a class?
        A class bundles data (attributes) and behaviour (methods) together.
        Each Student object holds its own data and can calculate its own
        performance metrics.
    """

    # Class variable - shared by all Student objects
    SUBJECTS = ["Mathematics", "Physics", "Chemistry", "English", "Computer Science"]

    def __init__(self, student_id, name, age, department, year, marks):
        """Constructor - runs automatically when creating a Student object."""
        self.student_id = student_id   # str
        self.name = name               # str
        self.age = age                 # int
        self.department = department   # str (e.g. "CSE")
        self.year = year               # int (1-4)
        self.marks = marks             # list of ints

    def calculate_total(self):
        """Return sum of all marks. Concept: sum()"""
        return sum(self.marks)

    def calculate_average(self):
        """Return average marks. Concept: sum(), len()"""
        if len(self.marks) == 0:
            return 0.0
        return sum(self.marks) / len(self.marks)

    def calculate_grade(self):
        """Return letter grade. Concept: if/elif/else"""
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
        """
        total = self.calculate_total()
        average = self.calculate_average()
        highest = max(self.marks) if self.marks else 0   # Concept: max()
        lowest = min(self.marks) if self.marks else 0    # Concept: min()
        grade = self.calculate_grade()
        return (total, average, highest, lowest, grade)  # Concept: tuple

    def get_details(self):
        """Return all details as a dictionary (used for JSON API responses)."""
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
        """Convert to simple dictionary for file storage."""
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


# ========================== STUDENT MANAGER ==========================
# Concepts: Dictionaries (key checking, adding pairs), Lists (append),
#           Loops, String operations, Substring checking, Functions,
#           Default arguments, Validation

class StudentManager:
    """Manages a collection of Student objects using a dictionary."""

    def __init__(self):
        self.students = {}  # key=student_id, value=Student object

    def add_student(self, data):
        """
        Add a new student after validation.
        Returns: tuple (success: bool, message: str)
        Concept: Functions returning multiple values
        """
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
            return (False, "Student ID '" + student_id + "' already exists.")

        # Validate age
        try:
            age = int(data.get("age", 0))
            if age < 15 or age > 60:
                return (False, "Age must be between 15 and 60.")
        except (ValueError, TypeError):
            return (False, "Age must be a valid number.")

        # Validate year
        try:
            year = int(data.get("year", 0))
            if year < 1 or year > 4:
                return (False, "Year must be between 1 and 4.")
        except (ValueError, TypeError):
            return (False, "Year must be a valid number.")

        # Validate marks
        marks = data.get("marks", [])
        if not isinstance(marks, list) or len(marks) != len(Student.SUBJECTS):
            return (False, "Exactly " + str(len(Student.SUBJECTS)) + " marks are required.")

        validated_marks = []
        for i, mark in enumerate(marks):  # Concept: for loop with enumerate
            try:
                m = int(mark)
                if m < 0 or m > 100:
                    return (False, "Mark for " + Student.SUBJECTS[i] + " must be 0-100.")
                validated_marks.append(m)  # Concept: list append()
            except (ValueError, TypeError):
                return (False, "Mark for " + Student.SUBJECTS[i] + " must be a number.")

        # Create and store Student object
        student = Student(student_id, name, age, department, year, validated_marks)
        self.students[student_id] = student  # Concept: adding key-value pair
        return (True, "Student '" + name + "' added successfully!")

    def get_student(self, student_id):
        """Get a single student's details. Concept: Dictionary key checking"""
        if student_id in self.students:
            return self.students[student_id].get_details()
        return None

    def get_all_students(self):
        """Get all students as a list of dictionaries. Concept: for loop"""
        result = []
        for student in self.students.values():
            result.append(student.get_details())
        return result

    def update_student(self, student_id, data):
        """Update an existing student. Returns: tuple (bool, str)"""
        if student_id not in self.students:
            return (False, "Student not found.")

        student = self.students[student_id]

        name = data.get("name", "").strip()
        if name:
            student.name = name

        if "age" in data:
            try:
                age = int(data["age"])
                if 15 <= age <= 60:
                    student.age = age
                else:
                    return (False, "Age must be between 15 and 60.")
            except (ValueError, TypeError):
                return (False, "Age must be a valid number.")

        dept = data.get("department", "").strip()
        if dept:
            student.department = dept.upper()

        if "year" in data:
            try:
                year = int(data["year"])
                if 1 <= year <= 4:
                    student.year = year
                else:
                    return (False, "Year must be between 1 and 4.")
            except (ValueError, TypeError):
                return (False, "Year must be a valid number.")

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
                            return (False, "Mark for " + Student.SUBJECTS[i] + " must be 0-100.")
                    except (ValueError, TypeError):
                        return (False, "Mark for " + Student.SUBJECTS[i] + " must be a number.")
                student.marks = validated
            else:
                return (False, "Exactly " + str(len(Student.SUBJECTS)) + " marks required.")

        return (True, "Student '" + student.name + "' updated successfully!")

    def delete_student(self, student_id):
        """Delete a student. Concept: del keyword, dict key checking"""
        if student_id not in self.students:
            return (False, "Student not found.")
        name = self.students[student_id].name
        del self.students[student_id]  # Concept: del keyword
        return (True, "Student '" + name + "' deleted successfully!")

    def search_students(self, query, search_type="all"):
        """
        Search by ID or name. Concept: substring checking, default arguments
        """
        query = query.strip().lower()
        results = []
        for sid, student in self.students.items():
            matched = False
            if search_type in ("id", "all"):
                if query in sid.lower():  # Concept: substring checking
                    matched = True
            if search_type in ("name", "all"):
                if query in student.name.lower():
                    matched = True
            if matched:
                results.append(student.get_details())
        return results

    def get_all_as_dicts(self):
        """Return all students as simple dicts for file saving."""
        return [s.to_dict() for s in self.students.values()]

    def load_from_dicts(self, data_list):
        """Load students from list of dicts. Concept: for loop, object creation"""
        for data in data_list:
            try:
                student = Student.from_dict(data)
                self.students[student.student_id] = student
            except (KeyError, TypeError):
                continue


# ========================== FILE HANDLING ==========================
# Concepts: open(), read(), write(), with open(), json, try/except,
#           default arguments, os module

DATA_FILE = os.path.join("data", "students.json")

def save_students(students_data, filename=DATA_FILE):
    """
    Save records to JSON file.
    Concept: with open() mode 'w', json.dump(), default argument
    """
    try:
        directory = os.path.dirname(filename)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(filename, "w") as file:
            json.dump(students_data, file, indent=2)
        return (True, "Data saved.")
    except Exception as e:
        return (False, "Error saving: " + str(e))

def load_students(filename=DATA_FILE):
    """
    Load records from JSON file.
    Concept: with open() mode 'r', json.load(), try/except
    """
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
    except Exception:
        return []

def create_sample_data():
    """Create sample student data if file doesn't exist."""
    if os.path.exists(DATA_FILE):
        return
    sample = [
        {"student_id": "STU001", "name": "Aarav Sharma", "age": 20,
         "department": "CSE", "year": 2, "marks": [88, 92, 78, 95, 90]},
        {"student_id": "STU002", "name": "Priya Patel", "age": 19,
         "department": "ECE", "year": 1, "marks": [75, 82, 90, 68, 85]},
        {"student_id": "STU003", "name": "Rahul Kumar", "age": 21,
         "department": "CSE", "year": 3, "marks": [95, 98, 92, 88, 96]},
        {"student_id": "STU004", "name": "Sneha Reddy", "age": 20,
         "department": "ME", "year": 2, "marks": [62, 58, 70, 65, 72]},
        {"student_id": "STU005", "name": "Vikram Singh", "age": 22,
         "department": "ECE", "year": 4, "marks": [45, 52, 48, 55, 40]},
        {"student_id": "STU006", "name": "Ananya Gupta", "age": 19,
         "department": "CSE", "year": 1, "marks": [82, 78, 85, 90, 88]},
    ]
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(sample, f, indent=2)


# ========================== ANALYSIS ==========================
# Concepts: NumPy arrays, Pandas DataFrame, sum(), max(), min(),
#           sorted() with key, loops, dictionaries

def get_statistics(students):
    """Class-level statistics using built-in Python."""
    if not students:
        return {"total_students": 0, "class_average": 0, "highest_average": 0,
                "lowest_average": 0, "top_student": None, "grade_distribution": {},
                "pass_rate": 0}

    averages = []
    totals = []
    grade_count = {}  # Concept: dictionary for counting

    for student in students:
        avg = student.calculate_average()
        total = student.calculate_total()
        grade = student.calculate_grade()
        averages.append(avg)
        totals.append(total)
        # Concept: dictionary key checking and adding pairs
        if grade in grade_count:
            grade_count[grade] = grade_count[grade] + 1
        else:
            grade_count[grade] = 1

    # Concept: sorted() with key function
    sorted_students = sorted(students, key=lambda s: s.calculate_average(), reverse=True)
    top_student = sorted_students[0]

    pass_count = 0
    for student in students:
        if student.calculate_grade() != "F":
            pass_count += 1
    pass_rate = round((pass_count / len(students)) * 100, 1)

    return {
        "total_students": len(students),
        "class_average": round(sum(averages) / len(averages), 2),
        "highest_average": round(max(averages), 2),
        "lowest_average": round(min(averages), 2),
        "highest_total": max(totals),
        "lowest_total": min(totals),
        "top_student": top_student.get_details(),
        "grade_distribution": grade_count,
        "pass_rate": pass_rate
    }

def get_analytics(students):
    """Advanced analytics with NumPy and Pandas."""
    if not students:
        return {"subject_averages": {}, "department_averages": {},
                "top_students": [], "numpy_stats": {}, "pandas_summary": {},
                "year_distribution": {}, "department_count": {},
                "subject_numpy": {}, "pandas_head": []}

    result = {}

    # Subject averages (Concept: nested loops, dictionary building)
    subject_averages = {}
    for i, subject in enumerate(Student.SUBJECTS):
        subject_marks = []
        for student in students:
            if i < len(student.marks):
                subject_marks.append(student.marks[i])
        if subject_marks:
            subject_averages[subject] = round(sum(subject_marks) / len(subject_marks), 2)
        else:
            subject_averages[subject] = 0
    result["subject_averages"] = subject_averages

    # Department averages
    dept_data = {}
    for student in students:
        dept = student.department
        if dept not in dept_data:
            dept_data[dept] = []
        dept_data[dept].append(student.calculate_average())
    result["department_averages"] = {d: round(sum(v)/len(v), 2) for d, v in dept_data.items()}

    # Department count
    dept_count = {}
    for student in students:
        d = student.department
        dept_count[d] = dept_count.get(d, 0) + 1
    result["department_count"] = dept_count

    # Year distribution
    year_dist = {}
    for student in students:
        y = str(student.year)
        year_dist[y] = year_dist.get(y, 0) + 1
    result["year_distribution"] = year_dist

    # Top 5 (Concept: sorted with key, list slicing)
    sorted_students = sorted(students, key=lambda s: s.calculate_average(), reverse=True)
    result["top_students"] = [s.get_details() for s in sorted_students[:5]]

    # NumPy Analysis
    if NUMPY_AVAILABLE:
        all_marks = []
        for student in students:
            for mark in student.marks:
                all_marks.append(mark)
        marks_array = np.array(all_marks)  # Concept: NumPy array creation
        result["numpy_stats"] = {
            "mean": round(float(np.mean(marks_array)), 2),
            "median": round(float(np.median(marks_array)), 2),
            "std_deviation": round(float(np.std(marks_array)), 2),
            "variance": round(float(np.var(marks_array)), 2),
            "max": int(np.max(marks_array)),
            "min": int(np.min(marks_array)),
            "total_marks_analysed": len(all_marks)
        }
        subject_numpy = {}
        for i, subject in enumerate(Student.SUBJECTS):
            sm = [s.marks[i] for s in students if i < len(s.marks)]
            if sm:
                arr = np.array(sm)
                subject_numpy[subject] = {
                    "mean": round(float(np.mean(arr)), 2),
                    "std": round(float(np.std(arr)), 2),
                    "max": int(np.max(arr)),
                    "min": int(np.min(arr))
                }
        result["subject_numpy"] = subject_numpy
    else:
        result["numpy_stats"] = {"error": "NumPy not installed"}
        result["subject_numpy"] = {}

    # Pandas Analysis
    if PANDAS_AVAILABLE:
        data_rows = []
        for student in students:
            row = {"ID": student.student_id, "Name": student.name,
                   "Age": student.age, "Department": student.department,
                   "Year": student.year, "Total": student.calculate_total(),
                   "Average": round(student.calculate_average(), 2),
                   "Grade": student.calculate_grade()}
            for i, subj in enumerate(Student.SUBJECTS):
                if i < len(student.marks):
                    row[subj] = student.marks[i]
            data_rows.append(row)
        df = pd.DataFrame(data_rows)
        numeric_df = df.select_dtypes(include="number")
        if len(numeric_df.columns) > 0:
            describe_dict = {}
            desc = numeric_df.describe()
            for col in desc.columns:
                describe_dict[col] = {}
                for idx in desc.index:
                    describe_dict[col][idx] = round(float(desc.loc[idx, col]), 2)
            result["pandas_summary"] = describe_dict
        else:
            result["pandas_summary"] = {}
        head_data = []
        for _, row in df.head().iterrows():
            head_data.append(row.to_dict())
        result["pandas_head"] = head_data
    else:
        result["pandas_summary"] = {"error": "Pandas not installed"}
        result["pandas_head"] = []

    return result


# ========================== HTML FRONTEND (EMBEDDED) ==========================
# The entire frontend is a single HTML string with inline CSS and JavaScript.
# Flask serves this when you visit http://localhost:5000

HTML_PAGE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Student Performance Management System</title>
<meta name="description" content="Student Performance & Record Management System - Python Lab Project">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
/* ========== DESIGN TOKENS ========== */
:root {
  --bg-primary: #07071a;
  --bg-secondary: #0d0d2b;
  --bg-card: rgba(255,255,255,0.03);
  --bg-card-hover: rgba(255,255,255,0.06);
  --bg-input: rgba(255,255,255,0.05);
  --border: rgba(255,255,255,0.07);
  --border-hover: rgba(255,255,255,0.15);
  --text-primary: #e8e8f4;
  --text-secondary: #9999bb;
  --text-muted: #5a5a7e;
  --text-inv: #07071a;
  --purple: #7c5cfc;
  --cyan: #00d4ff;
  --pink: #ff6b9d;
  --orange: #ffa040;
  --green: #00e676;
  --red: #ff4757;
  --grad1: linear-gradient(135deg,#7c5cfc,#00d4ff);
  --grad-ok: linear-gradient(135deg,#00e676,#00d4ff);
  --grad-bad: linear-gradient(135deg,#ff4757,#ff6b9d);
  --grad-warm: linear-gradient(135deg,#ffa040,#ff6b9d);
  --grad-card: linear-gradient(145deg,rgba(124,92,252,0.08),rgba(0,212,255,0.04));
  --sidebar-w: 260px;
  --topbar-h: 64px;
  --radius: 14px;
  --radius-sm: 10px;
  --radius-xs: 6px;
  --shadow: 0 4px 24px rgba(0,0,0,0.3);
  --transition: all .3s cubic-bezier(.4,0,.2,1);
}
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
html{font-size:15px;scroll-behavior:smooth}
body{font-family:'Inter',-apple-system,sans-serif;background:var(--bg-primary);color:var(--text-primary);line-height:1.6;min-height:100vh;overflow-x:hidden;-webkit-font-smoothing:antialiased}
body::before{content:'';position:fixed;top:-50%;left:-50%;width:200%;height:200%;background:radial-gradient(ellipse at 20% 50%,rgba(124,92,252,.06) 0%,transparent 50%),radial-gradient(ellipse at 80% 20%,rgba(0,212,255,.04) 0%,transparent 50%),radial-gradient(ellipse at 50% 80%,rgba(255,107,157,.03) 0%,transparent 50%);z-index:-1;animation:bgShift 20s ease-in-out infinite alternate}
@keyframes bgShift{0%{transform:translate(0,0)}100%{transform:translate(-2%,-2%) rotate(3deg)}}

/* ========== LAYOUT ========== */
.app{display:flex;min-height:100vh}
.sidebar{width:var(--sidebar-w);background:var(--bg-secondary);border-right:1px solid var(--border);display:flex;flex-direction:column;position:fixed;top:0;left:0;bottom:0;z-index:100;transition:var(--transition)}
.sidebar-header{padding:24px 20px;border-bottom:1px solid var(--border)}
.logo{display:flex;align-items:center;gap:12px}
.logo-icon{font-size:2rem;filter:drop-shadow(0 0 8px rgba(124,92,252,.4))}
.logo-text h1{font-size:1.2rem;font-weight:700;background:var(--grad1);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1.2}
.logo-text span{font-size:.7rem;color:var(--text-muted);letter-spacing:.5px}
.sidebar-nav{flex:1;padding:16px 12px;display:flex;flex-direction:column;gap:4px}
.nav-item{display:flex;align-items:center;gap:12px;padding:12px 16px;border-radius:var(--radius-sm);color:var(--text-secondary);text-decoration:none;font-size:.9rem;font-weight:500;cursor:pointer;transition:var(--transition);border:1px solid transparent}
.nav-item:hover{background:var(--bg-card-hover);color:var(--text-primary);border-color:var(--border)}
.nav-item.active{background:var(--grad-card);color:var(--purple);border-color:rgba(124,92,252,.2);box-shadow:0 0 30px rgba(124,92,252,.15)}
.nav-icon{font-size:1.15rem;width:24px;text-align:center}
.sidebar-footer{padding:16px 20px;border-top:1px solid var(--border);text-align:center;font-size:.7rem;color:var(--text-muted);letter-spacing:1px;text-transform:uppercase}

/* ========== MAIN ========== */
.main-content{flex:1;margin-left:var(--sidebar-w);min-height:100vh;transition:var(--transition)}
.topbar{height:var(--topbar-h);display:flex;align-items:center;gap:16px;padding:0 28px;border-bottom:1px solid var(--border);background:rgba(7,7,26,.6);backdrop-filter:blur(20px) saturate(180%);position:sticky;top:0;z-index:50}
.menu-toggle{display:none;background:none;border:1px solid var(--border);color:var(--text-primary);font-size:1.3rem;cursor:pointer;padding:6px 10px;border-radius:var(--radius-xs)}
.topbar-search{flex:1;max-width:480px}
.topbar-search input{width:100%;padding:10px 16px;background:var(--bg-input);border:1px solid var(--border);border-radius:50px;color:var(--text-primary);font-family:inherit;font-size:.85rem;outline:none;transition:var(--transition)}
.topbar-search input:focus{border-color:var(--purple);box-shadow:0 0 0 3px rgba(124,92,252,.15)}
.topbar-search input::placeholder{color:var(--text-muted)}
.status-badge{font-size:.75rem;color:var(--green);font-weight:500}

/* ========== VIEWS ========== */
.view{display:none;padding:28px;animation:fadeIn .4s ease}
.view.active{display:block}
@keyframes fadeIn{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
.view-header{margin-bottom:28px}
.view-header h2{font-size:1.7rem;font-weight:700;margin-bottom:4px;background:var(--grad1);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.view-header p{color:var(--text-secondary);font-size:.9rem}

/* ========== STAT CARDS ========== */
.stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:20px;margin-bottom:28px}
.stat-card{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius);padding:22px;position:relative;overflow:hidden;transition:var(--transition)}
.stat-card:hover{border-color:var(--border-hover);transform:translateY(-2px);box-shadow:var(--shadow)}
.stat-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;border-radius:var(--radius) var(--radius) 0 0}
.stat-card.purple::before{background:var(--grad1)}.stat-card.green::before{background:var(--grad-ok)}.stat-card.pink::before{background:var(--grad-bad)}.stat-card.orange::before{background:var(--grad-warm)}
.stat-icon{font-size:1.6rem;margin-bottom:10px}
.stat-value{font-size:2rem;font-weight:800;line-height:1;margin-bottom:4px}
.stat-card.purple .stat-value{color:var(--purple)}.stat-card.green .stat-value{color:var(--green)}.stat-card.pink .stat-value{color:var(--pink)}.stat-card.orange .stat-value{color:var(--orange)}
.stat-label{font-size:.8rem;color:var(--text-secondary);font-weight:500;text-transform:uppercase;letter-spacing:.8px}

/* ========== DASHBOARD GRID ========== */
.dashboard-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.card{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius);padding:24px;transition:var(--transition)}
.card:hover{border-color:var(--border-hover)}
.card h3{font-size:1.05rem;font-weight:600;margin-bottom:18px}

/* ========== GRADE CHART ========== */
.chart-container{display:flex;flex-direction:column;gap:12px}
.chart-bar-row{display:flex;align-items:center;gap:12px}
.chart-bar-label{width:36px;font-size:.85rem;font-weight:600;text-align:center}
.chart-bar-track{flex:1;height:28px;background:var(--bg-input);border-radius:50px;overflow:hidden}
.chart-bar-fill{height:100%;border-radius:50px;display:flex;align-items:center;padding-left:12px;font-size:.75rem;font-weight:600;color:var(--text-inv);transition:width 1s cubic-bezier(.4,0,.2,1)}
.chart-bar-fill.grade-a-plus{background:var(--grad-ok)}.chart-bar-fill.grade-a{background:linear-gradient(135deg,#00d4ff,#7c5cfc)}.chart-bar-fill.grade-b{background:var(--grad1)}.chart-bar-fill.grade-c{background:var(--grad-warm)}.chart-bar-fill.grade-d{background:linear-gradient(135deg,#ffa040,#ff4757)}.chart-bar-fill.grade-f{background:var(--grad-bad)}
.chart-bar-count{width:30px;text-align:right;font-size:.85rem;color:var(--text-secondary);font-weight:600}

/* ========== TOP STUDENTS ========== */
.top-student-item{display:flex;align-items:center;gap:14px;padding:12px 0;border-bottom:1px solid var(--border)}
.top-student-item:last-child{border-bottom:none}
.top-rank{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:.8rem;font-weight:700;flex-shrink:0}
.top-rank.rank-1{background:var(--grad-warm);color:var(--text-inv)}.top-rank.rank-2{background:rgba(0,212,255,.2);color:var(--cyan);border:1px solid rgba(0,212,255,.3)}.top-rank.rank-3{background:rgba(124,92,252,.2);color:var(--purple);border:1px solid rgba(124,92,252,.3)}.top-rank.rank-other{background:var(--bg-input);color:var(--text-secondary)}
.top-student-info{flex:1}.top-student-info .name{font-weight:600;font-size:.9rem}.top-student-info .dept{font-size:.75rem;color:var(--text-muted)}
.top-student-avg{font-weight:700;font-size:1rem;color:var(--cyan)}

/* ========== TABLE ========== */
.table-controls{display:flex;gap:12px;margin-bottom:18px;align-items:center}
.table-controls input{flex:1;max-width:360px;padding:10px 16px;background:var(--bg-input);border:1px solid var(--border);border-radius:var(--radius-sm);color:var(--text-primary);font-family:inherit;font-size:.85rem;outline:none;transition:var(--transition)}
.table-controls input:focus{border-color:var(--purple);box-shadow:0 0 0 3px rgba(124,92,252,.15)}
.table-wrapper{overflow-x:auto;border:1px solid var(--border);border-radius:var(--radius);background:var(--bg-card)}
.data-table{width:100%;border-collapse:collapse;font-size:.88rem}
.data-table thead{background:rgba(124,92,252,.06)}
.data-table th{padding:14px 18px;text-align:left;font-weight:600;font-size:.78rem;text-transform:uppercase;letter-spacing:.8px;color:var(--text-secondary);border-bottom:1px solid var(--border);white-space:nowrap}
.data-table td{padding:13px 18px;border-bottom:1px solid rgba(255,255,255,.03);white-space:nowrap}
.data-table tbody tr{transition:all .15s ease}.data-table tbody tr:hover{background:var(--bg-card-hover)}
.data-table tbody tr:last-child td{border-bottom:none}

/* ========== BADGES ========== */
.grade-badge{display:inline-block;padding:3px 12px;border-radius:50px;font-size:.75rem;font-weight:700;letter-spacing:.5px}
.grade-badge.grade-a-plus{background:rgba(0,230,118,.15);color:var(--green);border:1px solid rgba(0,230,118,.3)}
.grade-badge.grade-a{background:rgba(0,212,255,.12);color:var(--cyan);border:1px solid rgba(0,212,255,.25)}
.grade-badge.grade-b{background:rgba(124,92,252,.12);color:var(--purple);border:1px solid rgba(124,92,252,.25)}
.grade-badge.grade-c{background:rgba(255,160,64,.12);color:var(--orange);border:1px solid rgba(255,160,64,.25)}
.grade-badge.grade-d{background:rgba(255,107,157,.12);color:var(--pink);border:1px solid rgba(255,107,157,.25)}
.grade-badge.grade-f{background:rgba(255,71,87,.12);color:var(--red);border:1px solid rgba(255,71,87,.25)}

/* ========== ACTION BUTTONS ========== */
.action-btns{display:flex;gap:6px}
.action-btn{padding:5px 10px;border:1px solid var(--border);border-radius:var(--radius-xs);background:transparent;color:var(--text-secondary);cursor:pointer;font-size:.8rem;transition:all .15s ease}
.action-btn:hover{background:var(--bg-card-hover);color:var(--text-primary)}
.action-btn.view-btn:hover{color:var(--cyan)}.action-btn.edit-btn:hover{color:var(--purple)}.action-btn.delete-btn:hover{color:var(--red)}

/* ========== BUTTONS ========== */
.btn{padding:10px 24px;border:none;border-radius:var(--radius-sm);font-family:inherit;font-size:.88rem;font-weight:600;cursor:pointer;transition:var(--transition);display:inline-flex;align-items:center;gap:8px}
.btn-primary{background:var(--grad1);color:#fff;box-shadow:0 4px 15px rgba(124,92,252,.3)}
.btn-primary:hover{transform:translateY(-1px);box-shadow:0 6px 25px rgba(124,92,252,.4)}
.btn-secondary{background:var(--bg-input);color:var(--text-secondary);border:1px solid var(--border)}
.btn-secondary:hover{background:var(--bg-card-hover);color:var(--text-primary)}

/* ========== FORM ========== */
.student-form{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius);padding:28px;max-width:820px}
.form-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:18px;margin-bottom:24px}
.marks-title{font-size:1rem;font-weight:600;margin-bottom:16px;color:var(--text-secondary);padding-top:8px;border-top:1px solid var(--border)}
.marks-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:18px;margin-bottom:24px}
.form-group{display:flex;flex-direction:column;gap:6px}
.form-group label{font-size:.8rem;font-weight:500;color:var(--text-secondary);letter-spacing:.3px}
.form-group input,.form-group select{padding:10px 14px;background:var(--bg-input);border:1px solid var(--border);border-radius:var(--radius-xs);color:var(--text-primary);font-family:inherit;font-size:.88rem;outline:none;transition:var(--transition)}
.form-group input:focus,.form-group select:focus{border-color:var(--purple);box-shadow:0 0 0 3px rgba(124,92,252,.12)}
.form-group select{cursor:pointer}.form-group select option{background:var(--bg-secondary);color:var(--text-primary)}
.form-actions{display:flex;gap:12px;padding-top:8px}

/* ========== ANALYTICS ========== */
.analytics-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(380px,1fr));gap:20px}
.analytics-card{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius);padding:24px}
.analytics-card h3{font-size:1rem;font-weight:600;margin-bottom:18px;display:flex;align-items:center;gap:8px}
.h-bar-chart{display:flex;flex-direction:column;gap:14px}
.h-bar-item{display:flex;align-items:center;gap:12px}
.h-bar-item .label{width:140px;font-size:.82rem;color:var(--text-secondary);text-align:right;flex-shrink:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.h-bar-item .bar-track{flex:1;height:22px;background:var(--bg-input);border-radius:50px;overflow:hidden}
.h-bar-item .bar-fill{height:100%;border-radius:50px;background:var(--grad1);transition:width 1.2s cubic-bezier(.4,0,.2,1)}
.h-bar-item .value{width:50px;font-size:.85rem;font-weight:600;color:var(--cyan)}

/* ========== NUMPY / PANDAS ========== */
.numpy-grid,.pandas-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:20px}
.stat-block{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius);padding:24px}
.stat-block h3{font-size:1rem;font-weight:600;margin-bottom:16px;display:flex;align-items:center;gap:8px}
.stat-row{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid rgba(255,255,255,.04)}
.stat-row:last-child{border-bottom:none}
.stat-row .key{font-size:.85rem;color:var(--text-secondary)}.stat-row .val{font-size:.95rem;font-weight:600;color:var(--cyan)}
.pandas-table-wrapper{overflow-x:auto;margin-top:12px}
.pandas-table{width:100%;border-collapse:collapse;font-size:.82rem}
.pandas-table th{padding:10px 14px;text-align:left;font-weight:600;color:var(--text-secondary);border-bottom:1px solid var(--border);background:rgba(124,92,252,.05);white-space:nowrap;font-size:.76rem;text-transform:uppercase;letter-spacing:.5px}
.pandas-table td{padding:9px 14px;border-bottom:1px solid rgba(255,255,255,.03);white-space:nowrap}
.pandas-table tbody tr:hover{background:var(--bg-card-hover)}

/* ========== MODAL ========== */
.modal-overlay{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.65);backdrop-filter:blur(8px);display:none;align-items:center;justify-content:center;z-index:1000;padding:20px}
.modal-overlay.active{display:flex}
.modal{background:var(--bg-secondary);border:1px solid var(--border);border-radius:var(--radius);width:100%;max-width:580px;max-height:85vh;overflow-y:auto;box-shadow:0 8px 48px rgba(0,0,0,.4);animation:modalIn .3s cubic-bezier(.4,0,.2,1)}
@keyframes modalIn{from{opacity:0;transform:scale(.95) translateY(10px)}to{opacity:1;transform:scale(1) translateY(0)}}
.modal-header{display:flex;justify-content:space-between;align-items:center;padding:20px 24px;border-bottom:1px solid var(--border)}
.modal-header h3{font-size:1.1rem;font-weight:600}
.modal-close{background:none;border:1px solid var(--border);color:var(--text-secondary);width:32px;height:32px;border-radius:50%;cursor:pointer;font-size:.9rem;display:flex;align-items:center;justify-content:center;transition:all .15s ease}
.modal-close:hover{background:rgba(255,71,87,.15);color:var(--red)}
.modal-body{padding:24px}
.modal-body .detail-row{display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid rgba(255,255,255,.04)}
.modal-body .detail-row:last-child{border-bottom:none}
.modal-body .detail-row .label{color:var(--text-secondary);font-size:.88rem}
.modal-body .detail-row .value{font-weight:600;font-size:.88rem}
.modal-marks-section{margin-top:16px;padding-top:16px;border-top:1px solid var(--border)}
.modal-marks-section h4{font-size:.9rem;margin-bottom:12px;color:var(--text-secondary)}

/* ========== TOASTS ========== */
.toast-container{position:fixed;bottom:24px;right:24px;z-index:2000;display:flex;flex-direction:column-reverse;gap:10px}
.toast{padding:14px 20px;border-radius:var(--radius-sm);font-size:.88rem;font-weight:500;min-width:280px;max-width:420px;box-shadow:0 8px 48px rgba(0,0,0,.4);animation:toastIn .4s cubic-bezier(.4,0,.2,1);display:flex;align-items:center;gap:10px;border:1px solid}
.toast.success{background:rgba(0,230,118,.1);color:var(--green);border-color:rgba(0,230,118,.25)}
.toast.error{background:rgba(255,71,87,.1);color:var(--red);border-color:rgba(255,71,87,.25)}
.toast.info{background:rgba(0,212,255,.1);color:var(--cyan);border-color:rgba(0,212,255,.25)}
@keyframes toastIn{from{opacity:0;transform:translateX(60px)}to{opacity:1;transform:translateX(0)}}
@keyframes toastOut{from{opacity:1;transform:translateX(0)}to{opacity:0;transform:translateX(60px)}}
.loading{display:flex;align-items:center;justify-content:center;padding:40px;color:var(--text-muted);gap:10px}
.spinner{width:22px;height:22px;border:3px solid var(--border);border-top-color:var(--purple);border-radius:50%;animation:spin .7s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.empty-state{text-align:center;padding:48px 20px;color:var(--text-muted)}.empty-state .icon{font-size:3rem;margin-bottom:12px;opacity:.4}

/* ========== RESPONSIVE ========== */
@media(max-width:900px){.sidebar{transform:translateX(-100%)}.sidebar.open{transform:translateX(0)}.main-content{margin-left:0}.menu-toggle{display:block}.dashboard-grid,.analytics-grid{grid-template-columns:1fr}.form-grid{grid-template-columns:1fr}.marks-grid{grid-template-columns:1fr 1fr}}
@media(max-width:600px){.view{padding:16px}.topbar{padding:0 16px}.stats-grid{grid-template-columns:1fr 1fr}.marks-grid{grid-template-columns:1fr}.table-controls{flex-direction:column}.table-controls input{max-width:100%}.h-bar-item .label{width:80px;font-size:.75rem}}
::-webkit-scrollbar{width:6px;height:6px}::-webkit-scrollbar-track{background:transparent}::-webkit-scrollbar-thumb{background:rgba(255,255,255,.1);border-radius:3px}::-webkit-scrollbar-thumb:hover{background:rgba(255,255,255,.2)}
</style>
</head>
<body>
<div class="app">
  <!-- Sidebar -->
  <aside class="sidebar" id="sidebar">
    <div class="sidebar-header"><div class="logo"><span class="logo-icon">&#127891;</span><div class="logo-text"><h1>StudentPro</h1><span>Management System</span></div></div></div>
    <nav class="sidebar-nav">
      <a class="nav-item active" data-view="dashboard" onclick="switchView('dashboard')"><span class="nav-icon">&#128202;</span><span>Dashboard</span></a>
      <a class="nav-item" data-view="students" onclick="switchView('students')"><span class="nav-icon">&#128101;</span><span>Students</span></a>
      <a class="nav-item" data-view="add-student" onclick="switchView('add-student')"><span class="nav-icon">&#10133;</span><span>Add Student</span></a>
      <a class="nav-item" data-view="analytics" onclick="switchView('analytics')"><span class="nav-icon">&#128200;</span><span>Analytics</span></a>
      <a class="nav-item" data-view="numpy" onclick="switchView('numpy')"><span class="nav-icon">&#128290;</span><span>NumPy Stats</span></a>
      <a class="nav-item" data-view="pandas" onclick="switchView('pandas')"><span class="nav-icon">&#128060;</span><span>Pandas View</span></a>
    </nav>
    <div class="sidebar-footer"><span>Python Lab Project</span></div>
  </aside>

  <main class="main-content">
    <!-- Top Bar -->
    <header class="topbar">
      <button class="menu-toggle" onclick="toggleSidebar()" id="menuToggle">&#9776;</button>
      <div class="topbar-search"><input type="text" id="globalSearch" placeholder="Search students by name or ID... (press Enter)" onkeyup="handleGlobalSearch(event)"></div>
      <div class="topbar-actions"><span class="status-badge" id="statusBadge">&#9679; Connected</span></div>
    </header>

    <!-- Dashboard -->
    <section class="view active" id="view-dashboard">
      <div class="view-header"><h2>Dashboard</h2><p>Overview of student performance and class statistics</p></div>
      <div class="stats-grid" id="statsGrid"></div>
      <div class="dashboard-grid">
        <div class="card"><h3>Grade Distribution</h3><div class="chart-container" id="gradeChart"></div></div>
        <div class="card"><h3>Top Performers</h3><div id="topStudentsList"></div></div>
      </div>
    </section>

    <!-- Students -->
    <section class="view" id="view-students">
      <div class="view-header"><h2>All Students</h2><p>Manage and view student records</p></div>
      <div class="table-controls">
        <input type="text" id="studentSearch" placeholder="Filter students..." oninput="filterStudents()">
        <button class="btn btn-primary" onclick="switchView('add-student')">+ Add New</button>
      </div>
      <div class="table-wrapper"><table class="data-table"><thead><tr><th>ID</th><th>Name</th><th>Dept</th><th>Year</th><th>Total</th><th>Average</th><th>Grade</th><th>Actions</th></tr></thead><tbody id="studentsTableBody"></tbody></table></div>
    </section>

    <!-- Add/Edit Student -->
    <section class="view" id="view-add-student">
      <div class="view-header"><h2 id="formTitle">Add New Student</h2><p id="formSubtitle">Enter student details and marks</p></div>
      <form class="student-form" id="studentForm" onsubmit="handleFormSubmit(event)">
        <input type="hidden" id="editMode" value="add">
        <div class="form-grid">
          <div class="form-group"><label>Student ID *</label><input type="text" id="studentId" placeholder="e.g., STU007" required></div>
          <div class="form-group"><label>Full Name *</label><input type="text" id="studentName" placeholder="e.g., John Doe" required></div>
          <div class="form-group"><label>Age *</label><input type="number" id="studentAge" placeholder="15-60" min="15" max="60" required></div>
          <div class="form-group"><label>Department *</label><select id="studentDept" required><option value="">Select</option><option value="CSE">CSE</option><option value="ECE">ECE</option><option value="ME">ME</option><option value="CE">CE</option><option value="EE">EE</option><option value="IT">IT</option></select></div>
          <div class="form-group"><label>Year *</label><select id="studentYear" required><option value="">Select</option><option value="1">1st</option><option value="2">2nd</option><option value="3">3rd</option><option value="4">4th</option></select></div>
        </div>
        <h3 class="marks-title">Subject Marks (0-100)</h3>
        <div class="marks-grid">
          <div class="form-group"><label>Mathematics *</label><input type="number" id="markMath" placeholder="0-100" min="0" max="100" required></div>
          <div class="form-group"><label>Physics *</label><input type="number" id="markPhysics" placeholder="0-100" min="0" max="100" required></div>
          <div class="form-group"><label>Chemistry *</label><input type="number" id="markChemistry" placeholder="0-100" min="0" max="100" required></div>
          <div class="form-group"><label>English *</label><input type="number" id="markEnglish" placeholder="0-100" min="0" max="100" required></div>
          <div class="form-group"><label>Computer Science *</label><input type="number" id="markCS" placeholder="0-100" min="0" max="100" required></div>
        </div>
        <div class="form-actions">
          <button type="submit" class="btn btn-primary" id="submitBtn">Add Student</button>
          <button type="button" class="btn btn-secondary" onclick="resetForm()">Reset</button>
        </div>
      </form>
    </section>

    <!-- Analytics -->
    <section class="view" id="view-analytics"><div class="view-header"><h2>Analytics</h2><p>Subject and department performance analysis</p></div><div class="analytics-grid" id="analyticsContent"></div></section>

    <!-- NumPy -->
    <section class="view" id="view-numpy"><div class="view-header"><h2>NumPy Analysis</h2><p>Numerical analysis using Python NumPy arrays</p></div><div id="numpyContent"></div></section>

    <!-- Pandas -->
    <section class="view" id="view-pandas"><div class="view-header"><h2>Pandas DataFrame</h2><p>Tabular analysis using Python Pandas</p></div><div id="pandasContent"></div></section>
  </main>
</div>

<!-- Modal -->
<div class="modal-overlay" id="modalOverlay" onclick="closeModal()">
  <div class="modal" onclick="event.stopPropagation()">
    <div class="modal-header"><h3 id="modalTitle">Student Details</h3><button class="modal-close" onclick="closeModal()">&#10005;</button></div>
    <div class="modal-body" id="modalBody"></div>
  </div>
</div>
<div class="toast-container" id="toastContainer"></div>

<script>
/* ========== FRONTEND APPLICATION ========== */
const API = '/api';
let allStudents = [];
let currentView = 'dashboard';

document.addEventListener('DOMContentLoaded', () => { loadDashboard(); });

/* ---- Navigation ---- */
function switchView(v) {
  document.querySelectorAll('.view').forEach(el => el.classList.remove('active'));
  const t = document.getElementById('view-' + v);
  if (t) t.classList.add('active');
  document.querySelectorAll('.nav-item').forEach(n => {
    n.classList.remove('active');
    if (n.getAttribute('data-view') === v) n.classList.add('active');
  });
  currentView = v;
  if (v === 'dashboard') loadDashboard();
  else if (v === 'students') loadStudents();
  else if (v === 'add-student' && document.getElementById('editMode').value === 'add') resetForm();
  else if (v === 'analytics') loadAnalytics();
  else if (v === 'numpy') loadNumpyAnalysis();
  else if (v === 'pandas') loadPandasAnalysis();
  document.getElementById('sidebar').classList.remove('open');
}
function toggleSidebar() { document.getElementById('sidebar').classList.toggle('open'); }

/* ---- API Helper ---- */
async function apiFetch(endpoint, options = {}) {
  try {
    const r = await fetch(API + endpoint, { headers: {'Content-Type':'application/json'}, ...options });
    return await r.json();
  } catch(e) { console.error('API Error:', e); showToast('Connection error. Is the server running?', 'error'); return {success:false}; }
}

/* ---- Dashboard ---- */
async function loadDashboard() {
  const [stats, analytics] = await Promise.all([apiFetch('/statistics'), apiFetch('/analytics')]);
  if (stats.success) { renderStatsCards(stats.data); renderGradeChart(stats.data.grade_distribution); }
  if (analytics.success && analytics.data.top_students) renderTopStudents(analytics.data.top_students);
}
function renderStatsCards(s) {
  document.getElementById('statsGrid').innerHTML =
    `<div class="stat-card purple"><div class="stat-icon">&#128101;</div><div class="stat-value">${s.total_students}</div><div class="stat-label">Total Students</div></div>` +
    `<div class="stat-card green"><div class="stat-icon">&#128202;</div><div class="stat-value">${s.class_average||0}</div><div class="stat-label">Class Average</div></div>` +
    `<div class="stat-card orange"><div class="stat-icon">&#127942;</div><div class="stat-value">${s.highest_average||0}</div><div class="stat-label">Highest Average</div></div>` +
    `<div class="stat-card pink"><div class="stat-icon">&#128201;</div><div class="stat-value">${s.lowest_average||0}</div><div class="stat-label">Lowest Average</div></div>`;
}
function renderGradeChart(d) {
  const c = document.getElementById('gradeChart');
  if (!d || Object.keys(d).length === 0) { c.innerHTML = '<div class="empty-state"><div class="icon">&#128202;</div><p>No data yet</p></div>'; return; }
  const grades = ['A+','A','B','C','D','F'], mx = Math.max(...Object.values(d), 1);
  let h = '';
  for (const g of grades) {
    const n = d[g]||0, w = (n/mx)*100, gc = 'grade-'+g.toLowerCase().replace('+','-plus');
    h += `<div class="chart-bar-row"><span class="chart-bar-label">${g}</span><div class="chart-bar-track"><div class="chart-bar-fill ${gc}" style="width:${w}%">${n>0?n:''}</div></div><span class="chart-bar-count">${n}</span></div>`;
  }
  c.innerHTML = h;
}
function renderTopStudents(ts) {
  const c = document.getElementById('topStudentsList');
  if (!ts||!ts.length) { c.innerHTML = '<div class="empty-state"><div class="icon">&#127942;</div><p>No students yet</p></div>'; return; }
  let h = '';
  ts.forEach((s,i) => {
    const rc = i<3 ? 'rank-'+(i+1) : 'rank-other';
    h += `<div class="top-student-item"><div class="top-rank ${rc}">${i+1}</div><div class="top-student-info"><div class="name">${s.name}</div><div class="dept">${s.department} - Year ${s.year}</div></div><div class="top-student-avg">${s.average}</div></div>`;
  });
  c.innerHTML = h;
}

/* ---- Students Table ---- */
async function loadStudents() {
  const r = await apiFetch('/students');
  if (r.success) { allStudents = r.data; renderStudentsTable(allStudents); }
}
function renderStudentsTable(students) {
  const tb = document.getElementById('studentsTableBody');
  if (!students||!students.length) { tb.innerHTML = '<tr><td colspan="8"><div class="empty-state"><div class="icon">&#128101;</div><p>No students found. Add one!</p></div></td></tr>'; return; }
  let h = '';
  for (const s of students) {
    const gc = gradeClass(s.grade);
    h += `<tr><td><strong>${s.student_id}</strong></td><td>${s.name}</td><td>${s.department}</td><td>${s.year}</td><td>${s.total}</td><td>${s.average}</td><td><span class="grade-badge ${gc}">${s.grade}</span></td><td><div class="action-btns"><button class="action-btn view-btn" onclick="viewStudent('${s.student_id}')">&#128065;</button><button class="action-btn edit-btn" onclick="editStudent('${s.student_id}')">&#9998;</button><button class="action-btn delete-btn" onclick="deleteStudent('${s.student_id}','${s.name.replace(/'/g,"\\'")}')">&#128465;</button></div></td></tr>`;
  }
  tb.innerHTML = h;
}
function gradeClass(g) { return {'A+':'grade-a-plus','A':'grade-a','B':'grade-b','C':'grade-c','D':'grade-d','F':'grade-f'}[g]||''; }
function filterStudents() {
  const q = document.getElementById('studentSearch').value.toLowerCase().trim();
  if (!q) { renderStudentsTable(allStudents); return; }
  renderStudentsTable(allStudents.filter(s => s.name.toLowerCase().includes(q) || s.student_id.toLowerCase().includes(q) || s.department.toLowerCase().includes(q)));
}

/* ---- View Student Modal ---- */
async function viewStudent(id) {
  const r = await apiFetch('/students/' + id);
  if (!r.success) { showToast('Student not found.', 'error'); return; }
  const s = r.data, gc = gradeClass(s.grade);
  let mh = '';
  if (s.subjects && s.marks) for (let i=0;i<s.subjects.length;i++) mh += `<div class="detail-row"><span class="label">${s.subjects[i]}</span><span class="value">${s.marks[i]}</span></div>`;
  document.getElementById('modalTitle').textContent = s.name;
  document.getElementById('modalBody').innerHTML =
    `<div class="detail-row"><span class="label">Student ID</span><span class="value">${s.student_id}</span></div>`+
    `<div class="detail-row"><span class="label">Age</span><span class="value">${s.age}</span></div>`+
    `<div class="detail-row"><span class="label">Department</span><span class="value">${s.department}</span></div>`+
    `<div class="detail-row"><span class="label">Year</span><span class="value">${s.year}</span></div>`+
    `<div class="detail-row"><span class="label">Total</span><span class="value">${s.total}</span></div>`+
    `<div class="detail-row"><span class="label">Average</span><span class="value">${s.average}</span></div>`+
    `<div class="detail-row"><span class="label">Highest</span><span class="value">${s.highest}</span></div>`+
    `<div class="detail-row"><span class="label">Lowest</span><span class="value">${s.lowest}</span></div>`+
    `<div class="detail-row"><span class="label">Grade</span><span class="value"><span class="grade-badge ${gc}">${s.grade}</span></span></div>`+
    `<div class="modal-marks-section"><h4>Subject-wise Marks</h4>${mh}</div>`;
  document.getElementById('modalOverlay').classList.add('active');
}
function closeModal() { document.getElementById('modalOverlay').classList.remove('active'); }

/* ---- Add / Edit ---- */
async function handleFormSubmit(e) {
  e.preventDefault();
  const mode = document.getElementById('editMode').value;
  const id = document.getElementById('studentId').value.trim();
  const marks = [parseInt(document.getElementById('markMath').value), parseInt(document.getElementById('markPhysics').value), parseInt(document.getElementById('markChemistry').value), parseInt(document.getElementById('markEnglish').value), parseInt(document.getElementById('markCS').value)];
  for (let i=0;i<marks.length;i++) if (isNaN(marks[i])||marks[i]<0||marks[i]>100) { showToast('All marks must be 0-100.','error'); return; }
  const payload = { student_id:id, name:document.getElementById('studentName').value.trim(), age:parseInt(document.getElementById('studentAge').value), department:document.getElementById('studentDept').value, year:parseInt(document.getElementById('studentYear').value), marks };
  let r;
  if (mode==='edit') r = await apiFetch('/students/'+id, {method:'PUT', body:JSON.stringify(payload)});
  else r = await apiFetch('/students', {method:'POST', body:JSON.stringify(payload)});
  if (r.success) { showToast(r.message,'success'); resetForm(); switchView('students'); } else showToast(r.message,'error');
}
async function editStudent(id) {
  const r = await apiFetch('/students/'+id);
  if (!r.success) { showToast('Not found.','error'); return; }
  const s = r.data;
  document.getElementById('editMode').value = 'edit';
  document.getElementById('formTitle').textContent = 'Edit Student';
  document.getElementById('formSubtitle').textContent = 'Modify student details';
  document.getElementById('submitBtn').textContent = 'Update Student';
  document.getElementById('studentId').value = s.student_id;
  document.getElementById('studentId').disabled = true;
  document.getElementById('studentName').value = s.name;
  document.getElementById('studentAge').value = s.age;
  document.getElementById('studentDept').value = s.department;
  document.getElementById('studentYear').value = s.year;
  if (s.marks&&s.marks.length>=5) { document.getElementById('markMath').value=s.marks[0]; document.getElementById('markPhysics').value=s.marks[1]; document.getElementById('markChemistry').value=s.marks[2]; document.getElementById('markEnglish').value=s.marks[3]; document.getElementById('markCS').value=s.marks[4]; }
  switchView('add-student');
}
function resetForm() {
  document.getElementById('studentForm').reset();
  document.getElementById('editMode').value='add';
  document.getElementById('formTitle').textContent='Add New Student';
  document.getElementById('formSubtitle').textContent='Enter student details and marks';
  document.getElementById('submitBtn').textContent='Add Student';
  document.getElementById('studentId').disabled=false;
}

/* ---- Delete ---- */
async function deleteStudent(id, name) {
  if (!confirm('Delete "'+name+'" ('+id+')?')) return;
  const r = await apiFetch('/students/'+id, {method:'DELETE'});
  if (r.success) { showToast(r.message,'success'); loadStudents(); if(currentView==='dashboard') loadDashboard(); } else showToast(r.message,'error');
}

/* ---- Global Search ---- */
async function handleGlobalSearch(e) {
  if (e.key!=='Enter') return;
  const q = document.getElementById('globalSearch').value.trim();
  if (!q) return;
  const r = await apiFetch('/students?search='+encodeURIComponent(q));
  if (r.success) { allStudents=r.data; switchView('students'); renderStudentsTable(r.data); showToast('Found '+r.count+' student(s)','info'); }
}

/* ---- Analytics ---- */
async function loadAnalytics() {
  const c = document.getElementById('analyticsContent');
  c.innerHTML = '<div class="loading"><div class="spinner"></div>Loading...</div>';
  const r = await apiFetch('/analytics');
  if (!r.success) { c.innerHTML = '<div class="empty-state"><p>Failed to load</p></div>'; return; }
  const d = r.data; let h = '';
  if (d.subject_averages && Object.keys(d.subject_averages).length) {
    let bars=''; for (const[s,a] of Object.entries(d.subject_averages)) bars+=`<div class="h-bar-item"><span class="label">${s}</span><div class="bar-track"><div class="bar-fill" style="width:${a}%"></div></div><span class="value">${a}</span></div>`;
    h+=`<div class="analytics-card"><h3>&#128218; Subject Averages</h3><div class="h-bar-chart">${bars}</div></div>`;
  }
  if (d.department_averages && Object.keys(d.department_averages).length) {
    let bars=''; for (const[dept,a] of Object.entries(d.department_averages)) bars+=`<div class="h-bar-item"><span class="label">${dept}</span><div class="bar-track"><div class="bar-fill" style="width:${a}%;background:var(--grad-warm)"></div></div><span class="value">${a}</span></div>`;
    h+=`<div class="analytics-card"><h3>&#127963; Department Averages</h3><div class="h-bar-chart">${bars}</div></div>`;
  }
  if (d.department_count && Object.keys(d.department_count).length) {
    let rows=''; for (const[dept,n] of Object.entries(d.department_count)) rows+=`<div class="stat-row"><span class="key">${dept}</span><span class="val">${n} student(s)</span></div>`;
    h+=`<div class="analytics-card"><h3>&#128101; Department Strength</h3>${rows}</div>`;
  }
  if (d.year_distribution && Object.keys(d.year_distribution).length) {
    let rows=''; for (const[y,n] of Object.entries(d.year_distribution)) rows+=`<div class="stat-row"><span class="key">Year ${y}</span><span class="val">${n} student(s)</span></div>`;
    h+=`<div class="analytics-card"><h3>&#128197; Year Distribution</h3>${rows}</div>`;
  }
  c.innerHTML = h || '<div class="empty-state"><p>No data. Add students first.</p></div>';
}

/* ---- NumPy ---- */
async function loadNumpyAnalysis() {
  const c = document.getElementById('numpyContent');
  c.innerHTML = '<div class="loading"><div class="spinner"></div>Loading NumPy...</div>';
  const r = await apiFetch('/analytics');
  if (!r.success) { c.innerHTML='<div class="empty-state"><p>Failed</p></div>'; return; }
  const d=r.data; let h='<div class="numpy-grid">';
  if (d.numpy_stats && !d.numpy_stats.error) {
    const s=d.numpy_stats;
    h+=`<div class="stat-block"><h3>&#128290; Overall NumPy Statistics</h3>`+
      `<div class="stat-row"><span class="key">Mean</span><span class="val">${s.mean}</span></div>`+
      `<div class="stat-row"><span class="key">Median</span><span class="val">${s.median}</span></div>`+
      `<div class="stat-row"><span class="key">Std Deviation</span><span class="val">${s.std_deviation}</span></div>`+
      `<div class="stat-row"><span class="key">Variance</span><span class="val">${s.variance}</span></div>`+
      `<div class="stat-row"><span class="key">Maximum</span><span class="val">${s.max}</span></div>`+
      `<div class="stat-row"><span class="key">Minimum</span><span class="val">${s.min}</span></div>`+
      `<div class="stat-row"><span class="key">Marks Analysed</span><span class="val">${s.total_marks_analysed}</span></div></div>`;
  } else h+='<div class="stat-block"><h3>NumPy</h3><div class="empty-state"><p>NumPy not installed</p></div></div>';
  if (d.subject_numpy && Object.keys(d.subject_numpy).length) {
    let rows=''; for (const[subj,s] of Object.entries(d.subject_numpy)) rows+=`<div class="stat-row"><span class="key">${subj}</span><span class="val">avg=${s.mean} std=${s.std} max=${s.max} min=${s.min}</span></div>`;
    h+=`<div class="stat-block"><h3>&#128202; Per-Subject Analysis</h3>${rows}</div>`;
  }
  h+='</div>'; c.innerHTML=h;
}

/* ---- Pandas ---- */
async function loadPandasAnalysis() {
  const c = document.getElementById('pandasContent');
  c.innerHTML = '<div class="loading"><div class="spinner"></div>Loading Pandas...</div>';
  const r = await apiFetch('/analytics');
  if (!r.success) { c.innerHTML='<div class="empty-state"><p>Failed</p></div>'; return; }
  const d=r.data; let h='<div class="pandas-grid">';
  if (d.pandas_head && d.pandas_head.length) {
    const cols=Object.keys(d.pandas_head[0]);
    let t='<table class="pandas-table"><thead><tr>'; for(const c of cols) t+=`<th>${c}</th>`; t+='</tr></thead><tbody>';
    for(const row of d.pandas_head) { t+='<tr>'; for(const c of cols) { let v=row[c]; if(typeof v==='number'&&!Number.isInteger(v)) v=v.toFixed(2); t+=`<td>${v}</td>`; } t+='</tr>'; }
    t+='</tbody></table>';
    h+=`<div class="stat-block" style="grid-column:1/-1"><h3>&#128060; DataFrame - head()</h3><p style="color:var(--text-muted);font-size:.82rem;margin-bottom:12px">First 5 rows</p><div class="pandas-table-wrapper">${t}</div></div>`;
  }
  if (d.pandas_summary && !d.pandas_summary.error && Object.keys(d.pandas_summary).length) {
    const dc=Object.keys(d.pandas_summary), dr=Object.keys(d.pandas_summary[dc[0]]||{});
    let t='<table class="pandas-table"><thead><tr><th>Stat</th>'; for(const c of dc) t+=`<th>${c}</th>`; t+='</tr></thead><tbody>';
    for(const row of dr) { t+=`<tr><td><strong>${row}</strong></td>`; for(const c of dc) { const v=d.pandas_summary[c][row]; t+=`<td>${typeof v==='number'?v.toFixed(2):v}</td>`; } t+='</tr>'; }
    t+='</tbody></table>';
    h+=`<div class="stat-block" style="grid-column:1/-1"><h3>&#128203; DataFrame - describe()</h3><p style="color:var(--text-muted);font-size:.82rem;margin-bottom:12px">Statistical summary</p><div class="pandas-table-wrapper">${t}</div></div>`;
  }
  h+='</div>'; c.innerHTML=h||'<div class="empty-state"><p>No Pandas data</p></div>';
}

/* ---- Toasts ---- */
function showToast(msg, type='info') {
  const icons={success:'&#10003;',error:'&#10007;',info:'&#8505;'};
  const t=document.createElement('div'); t.className='toast '+type; t.innerHTML=`<span>${icons[type]||'&#8505;'}</span> ${msg}`;
  document.getElementById('toastContainer').appendChild(t);
  setTimeout(()=>{t.style.animation='toastOut .3s ease forwards';setTimeout(()=>t.remove(),300);},4000);
}

document.addEventListener('keydown', e => { if(e.key==='Escape') closeModal(); });
</script>
</body>
</html>'''


# ========================== FLASK APP & ROUTES ==========================

app = Flask(__name__)
CORS(app)

# Initialize manager and load data
create_sample_data()
manager = StudentManager()
existing_data = load_students()
if existing_data:
    manager.load_from_dicts(existing_data)
    print("[OK] Loaded " + str(len(existing_data)) + " student(s) from file.")
else:
    print("[i] No existing data. Starting fresh.")


@app.route("/")
def index():
    """Serve the embedded HTML frontend."""
    return Response(HTML_PAGE, content_type="text/html; charset=utf-8")


@app.route("/api/students", methods=["GET"])
def api_get_students():
    search = request.args.get("search", "").strip()
    search_type = request.args.get("search_type", "all")
    if search:
        results = manager.search_students(search, search_type)
        return jsonify({"success": True, "data": results, "count": len(results)})
    students = manager.get_all_students()
    return jsonify({"success": True, "data": students, "count": len(students)})


@app.route("/api/students/<student_id>", methods=["GET"])
def api_get_student(student_id):
    student = manager.get_student(student_id)
    if student:
        return jsonify({"success": True, "data": student})
    return jsonify({"success": False, "message": "Student not found."}), 404


@app.route("/api/students", methods=["POST"])
def api_add_student():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Invalid JSON data."}), 400
    success, message = manager.add_student(data)
    if success:
        save_students(manager.get_all_as_dicts())
        return jsonify({"success": True, "message": message}), 201
    return jsonify({"success": False, "message": message}), 400


@app.route("/api/students/<student_id>", methods=["PUT"])
def api_update_student(student_id):
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Invalid JSON data."}), 400
    success, message = manager.update_student(student_id, data)
    if success:
        save_students(manager.get_all_as_dicts())
        return jsonify({"success": True, "message": message})
    return jsonify({"success": False, "message": message}), 400


@app.route("/api/students/<student_id>", methods=["DELETE"])
def api_delete_student(student_id):
    success, message = manager.delete_student(student_id)
    if success:
        save_students(manager.get_all_as_dicts())
        return jsonify({"success": True, "message": message})
    return jsonify({"success": False, "message": message}), 404


@app.route("/api/statistics", methods=["GET"])
def api_statistics():
    students = list(manager.students.values())
    stats = get_statistics(students)
    return jsonify({"success": True, "data": stats})


@app.route("/api/analytics", methods=["GET"])
def api_analytics():
    students = list(manager.students.values())
    analytics = get_analytics(students)
    return jsonify({"success": True, "data": analytics})


@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "message": "Endpoint not found."}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"success": False, "message": "Internal server error."}), 500


# ========================== START ==========================

if __name__ == "__main__":
    print("")
    print("=" * 55)
    print("   STUDENT PERFORMANCE MANAGEMENT SYSTEM")
    print("=" * 55)
    print("   Open in browser : http://localhost:5000")
    print("   API endpoint    : http://localhost:5000/api")
    print("=" * 55)
    print("")
    app.run(debug=True, host="0.0.0.0", port=5000)
