"""
Flask Application - Entry Point
================================
Python Concepts: Functions, dictionaries, conditionals, imports
Web Concepts   : REST API, HTTP methods, JSON, CORS, routing

This file creates the Flask web server and defines all API endpoints.
It also serves the frontend HTML/CSS/JS files.

WHAT IS A REST API?
    REST = Representational State Transfer
    It's a way for the frontend (browser) and backend (Python) to
    communicate using HTTP requests and JSON data.

    GET    = Retrieve data
    POST   = Create new data
    PUT    = Update existing data
    DELETE = Remove data

WHAT IS CORS?
    Cross-Origin Resource Sharing. Browsers block requests between
    different origins (e.g., localhost:3000 -> localhost:5000) for
    security. Flask-CORS tells the browser: "It's OK, allow it."
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

from student_manager import StudentManager
from file_handler import save_students, load_students
from analysis import get_statistics, get_analytics

# ---- Create Flask App ----
app = Flask(__name__, static_folder="static")
CORS(app)  # Enable CORS for all routes

# ---- Initialize Student Manager ----
manager = StudentManager()

# ---- Load existing data from file on startup ----
existing_data = load_students()
if existing_data:
    manager.load_from_dicts(existing_data)
    print(f"[OK] Loaded {len(existing_data)} student(s) from file.")
else:
    print("[i] No existing data found. Starting fresh.")


# ========================== FRONTEND ROUTES ==========================

@app.route("/")
def serve_frontend():
    """Serve the main HTML page."""
    return send_from_directory("static", "index.html")


@app.route("/static/<path:path>")
def serve_static(path):
    """Serve static files (CSS, JS)."""
    return send_from_directory("static", path)


# ========================== API ROUTES ==========================

# ---- GET /api/students ----
@app.route("/api/students", methods=["GET"])
def api_get_students():
    """
    Get all students or search students.

    Query parameters:
        search (str): Optional search term
        search_type (str): 'id', 'name', or 'all' (default)
    """
    search = request.args.get("search", "").strip()
    search_type = request.args.get("search_type", "all")

    if search:
        results = manager.search_students(search, search_type)
        return jsonify({"success": True, "data": results, "count": len(results)})

    students = manager.get_all_students()
    return jsonify({"success": True, "data": students, "count": len(students)})


# ---- GET /api/students/<id> ----
@app.route("/api/students/<student_id>", methods=["GET"])
def api_get_student(student_id):
    """Get a single student by ID."""
    student = manager.get_student(student_id)
    if student:
        return jsonify({"success": True, "data": student})
    return jsonify({"success": False, "message": "Student not found."}), 404


# ---- POST /api/students ----
@app.route("/api/students", methods=["POST"])
def api_add_student():
    """
    Add a new student.

    Expects JSON body with: student_id, name, age, department, year, marks
    """
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Invalid JSON data."}), 400

    success, message = manager.add_student(data)

    if success:
        # Auto-save to file after adding
        save_students(manager.get_all_as_dicts())
        return jsonify({"success": True, "message": message}), 201

    return jsonify({"success": False, "message": message}), 400


# ---- PUT /api/students/<id> ----
@app.route("/api/students/<student_id>", methods=["PUT"])
def api_update_student(student_id):
    """Update an existing student's details."""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Invalid JSON data."}), 400

    success, message = manager.update_student(student_id, data)

    if success:
        save_students(manager.get_all_as_dicts())
        return jsonify({"success": True, "message": message})

    return jsonify({"success": False, "message": message}), 400


# ---- DELETE /api/students/<id> ----
@app.route("/api/students/<student_id>", methods=["DELETE"])
def api_delete_student(student_id):
    """Delete a student by ID."""
    success, message = manager.delete_student(student_id)

    if success:
        save_students(manager.get_all_as_dicts())
        return jsonify({"success": True, "message": message})

    return jsonify({"success": False, "message": message}), 404


# ---- GET /api/statistics ----
@app.route("/api/statistics", methods=["GET"])
def api_statistics():
    """Get class-level statistics."""
    students = list(manager.students.values())
    stats = get_statistics(students)
    return jsonify({"success": True, "data": stats})


# ---- GET /api/analytics ----
@app.route("/api/analytics", methods=["GET"])
def api_analytics():
    """Get detailed analytics (NumPy + Pandas)."""
    students = list(manager.students.values())
    analytics = get_analytics(students)
    return jsonify({"success": True, "data": analytics})


# ========================== ERROR HANDLERS ==========================

@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "message": "Endpoint not found."}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"success": False, "message": "Internal server error."}), 500


# ========================== START SERVER ==========================

if __name__ == "__main__":
    print("\n" + "=" * 55)
    print("   STUDENT PERFORMANCE MANAGEMENT SYSTEM - API")
    print("=" * 55)
    print("   Frontend : http://localhost:5000")
    print("   API Base : http://localhost:5000/api")
    print("=" * 55 + "\n")
    app.run(debug=True, host="0.0.0.0", port=5000)
