"""
Analysis Module
===============
Python Concepts: NumPy arrays, Pandas DataFrames, sum(), max(), min(),
                 sorted(), loops, dictionaries, list operations

This module provides statistical analysis and analytics using:
    - Built-in Python functions
    - NumPy for numerical operations
    - Pandas for tabular data analysis
"""

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

from student import Student


def get_statistics(students):
    """
    Calculate class-level statistics.

    Concepts: Loops, dictionaries, len(), sum(), max(), min(),
              sorted() with key function, list append()

    Parameters:
        students (list): List of Student objects

    Returns:
        dict: Class statistics
    """
    if not students:
        return {
            "total_students": 0,
            "class_average": 0,
            "highest_average": 0,
            "lowest_average": 0,
            "highest_total": 0,
            "lowest_total": 0,
            "top_student": None,
            "grade_distribution": {},
            "pass_rate": 0
        }

    # Collect averages and totals using loops
    averages = []   # Concept: list to collect data
    totals = []
    grade_count = {}  # Concept: dictionary for counting

    for student in students:  # Concept: for loop
        avg = student.calculate_average()
        total = student.calculate_total()
        grade = student.calculate_grade()

        averages.append(avg)    # Concept: list append()
        totals.append(total)

        # Concept: Dictionary key checking and adding pairs
        if grade in grade_count:
            grade_count[grade] = grade_count[grade] + 1
        else:
            grade_count[grade] = 1

    # Concept: sorted() with key function to find top student
    sorted_students = sorted(
        students,
        key=lambda s: s.calculate_average(),
        reverse=True
    )
    top_student = sorted_students[0]  # Highest average
    bottom_student = sorted_students[-1]  # Lowest average

    # Count passing students (grade != F)
    pass_count = 0
    for student in students:
        if student.calculate_grade() != "F":
            pass_count = pass_count + 1

    pass_rate = round((pass_count / len(students)) * 100, 1)

    return {
        "total_students": len(students),       # Concept: len()
        "class_average": round(sum(averages) / len(averages), 2),  # Concept: sum()
        "highest_average": round(max(averages), 2),  # Concept: max()
        "lowest_average": round(min(averages), 2),   # Concept: min()
        "highest_total": max(totals),
        "lowest_total": min(totals),
        "top_student": top_student.get_details(),
        "bottom_student": bottom_student.get_details(),
        "grade_distribution": grade_count,
        "pass_rate": pass_rate
    }


def get_analytics(students):
    """
    Perform advanced analytics using NumPy and Pandas.

    Concepts:
        - NumPy: array creation, np.mean(), np.max(), np.min(), np.std()
        - Pandas: DataFrame creation, describe(), column selection
        - Loops, dictionaries, sorted()

    Parameters:
        students (list): List of Student objects

    Returns:
        dict: Comprehensive analytics data
    """
    if not students:
        return {
            "subject_averages": {},
            "department_averages": {},
            "top_students": [],
            "numpy_stats": {},
            "pandas_summary": {},
            "year_distribution": {}
        }

    result = {}

    # ---- Subject-wise Averages ----
    # Concept: Nested loops, dictionary building
    subject_averages = {}
    for i, subject in enumerate(Student.SUBJECTS):  # Concept: enumerate
        subject_marks = []
        for student in students:
            if i < len(student.marks):
                subject_marks.append(student.marks[i])
        if subject_marks:
            subject_averages[subject] = round(sum(subject_marks) / len(subject_marks), 2)
        else:
            subject_averages[subject] = 0
    result["subject_averages"] = subject_averages

    # ---- Department-wise Averages ----
    dept_data = {}  # Concept: nested dictionary
    for student in students:
        dept = student.department
        if dept not in dept_data:
            dept_data[dept] = []
        dept_data[dept].append(student.calculate_average())

    dept_averages = {}
    for dept, avgs in dept_data.items():
        dept_averages[dept] = round(sum(avgs) / len(avgs), 2)
    result["department_averages"] = dept_averages

    # ---- Department student count ----
    dept_count = {}
    for student in students:
        dept = student.department
        if dept in dept_count:
            dept_count[dept] = dept_count[dept] + 1
        else:
            dept_count[dept] = 1
    result["department_count"] = dept_count

    # ---- Year Distribution ----
    year_dist = {}
    for student in students:
        yr = str(student.year)
        if yr in year_dist:
            year_dist[yr] = year_dist[yr] + 1
        else:
            year_dist[yr] = 1
    result["year_distribution"] = year_dist

    # ---- Top 5 Students ----
    # Concept: sorted() with key function
    sorted_students = sorted(
        students,
        key=lambda s: s.calculate_average(),
        reverse=True
    )
    top_5 = []
    for student in sorted_students[:5]:  # Concept: list slicing
        top_5.append(student.get_details())
    result["top_students"] = top_5

    # ---- NumPy Analysis (MODULE 11) ----
    if NUMPY_AVAILABLE:
        all_marks = []  # Flat list of all marks
        for student in students:
            for mark in student.marks:  # Concept: nested loop
                all_marks.append(mark)

        # Concept: Creating a 1D NumPy array from a Python list
        marks_array = np.array(all_marks)

        result["numpy_stats"] = {
            "mean": round(float(np.mean(marks_array)), 2),
            "median": round(float(np.median(marks_array)), 2),
            "std_deviation": round(float(np.std(marks_array)), 2),
            "variance": round(float(np.var(marks_array)), 2),
            "max": int(np.max(marks_array)),
            "min": int(np.min(marks_array)),
            "total_marks_analysed": len(all_marks)
        }

        # Per-subject NumPy stats
        subject_numpy = {}
        for i, subject in enumerate(Student.SUBJECTS):
            subj_marks = []
            for student in students:
                if i < len(student.marks):
                    subj_marks.append(student.marks[i])
            if subj_marks:
                arr = np.array(subj_marks)
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

    # ---- Pandas Analysis (MODULE 12) ----
    if PANDAS_AVAILABLE:
        # Concept: Creating a DataFrame from a list of dictionaries
        data_rows = []
        for student in students:
            row = {
                "ID": student.student_id,
                "Name": student.name,
                "Age": student.age,
                "Department": student.department,
                "Year": student.year,
                "Total": student.calculate_total(),
                "Average": round(student.calculate_average(), 2),
                "Grade": student.calculate_grade()
            }
            for i, subj in enumerate(Student.SUBJECTS):
                if i < len(student.marks):
                    row[subj] = student.marks[i]
            data_rows.append(row)

        df = pd.DataFrame(data_rows)  # Concept: DataFrame creation

        # Concept: describe() — basic statistics
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

        # Concept: head() — first few rows
        head_data = []
        for _, row in df.head().iterrows():
            head_data.append(row.to_dict())
        result["pandas_head"] = head_data
    else:
        result["pandas_summary"] = {"error": "Pandas not installed"}
        result["pandas_head"] = []

    return result
