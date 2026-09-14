"""
File Handler Module
===================
Python Concepts: File handling (open, read, write, with),
                 JSON conversion, try/except, default arguments,
                 os module for directory creation

WHY use file handling?
    Data stored in variables (RAM) is lost when the program closes.
    Files let us save data permanently on disk.
"""

import json
import os


def save_students(students_data, filename="data/students.json"):
    """
    Save student records to a JSON file.

    Concepts:
        - open() with mode 'w' (write)
        - json.dump() to convert Python data to JSON
        - with open() — automatically closes the file
        - os.makedirs() — create directories if missing
        - Default function argument (filename)

    Parameters:
        students_data (list): List of student dictionaries
        filename      (str) : File path (default: data/students.json)

    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        # Create the directory if it doesn't exist
        directory = os.path.dirname(filename)
        if directory:
            os.makedirs(directory, exist_ok=True)

        # Concept: 'with open()' — auto-closes file when done
        # Mode 'w' = write (creates or overwrites)
        with open(filename, "w") as file:
            # Concept: json.dump() writes Python data as JSON
            json.dump(students_data, file, indent=2)

        return (True, f"Data saved to '{filename}'.")

    except Exception as e:
        return (False, f"Error saving data: {str(e)}")


def load_students(filename="data/students.json"):
    """
    Load student records from a JSON file.

    Concepts:
        - open() with mode 'r' (read)
        - json.load() to convert JSON to Python data
        - with open()
        - try/except for FileNotFoundError
        - Default function argument

    Parameters:
        filename (str): File path (default: data/students.json)

    Returns:
        list: List of student dictionaries (empty if file missing)
    """
    try:
        # Concept: with open() in read mode
        with open(filename, "r") as file:
            # Concept: json.load() reads JSON and returns Python data
            data = json.load(file)
            return data

    except FileNotFoundError:
        # Concept: Exception handling — file doesn't exist yet
        return []

    except json.JSONDecodeError:
        # Concept: Exception handling — file has invalid JSON
        return []

    except Exception:
        return []
