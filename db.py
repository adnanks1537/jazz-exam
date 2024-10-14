from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Database setup
def init_db():
    conn = sqlite3.connect('exam_portal.db')
    cursor = conn.cursor()
    
    # Create students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    
    # Create exams table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            total_marks INTEGER NOT NULL
        )
    ''')
    
    # Create results table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            exam_id INTEGER,
            score INTEGER,
            FOREIGN KEY(student_id) REFERENCES students(id),
            FOREIGN KEY(exam_id) REFERENCES exams(id)
        )
    ''')
    
    # Create assigned_exams table for assigning exams to students
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assigned_exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exam_id INTEGER,
            student_id INTEGER,
            FOREIGN KEY(exam_id) REFERENCES exams(id),
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
    ''')
    
    conn.commit()
    conn.close()

init_db()

# Handle Students
@app.route('/students', methods=['GET', 'POST'])
def handle_students():
    if request.method == 'GET':
        conn = sqlite3.connect('exam_portal.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students')
        students = cursor.fetchall()
        conn.close()
        return jsonify(students)

    if request.method == 'POST':
        new_student = request.json
        conn = sqlite3.connect('exam_portal.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO students (name, email) VALUES (?, ?)', 
                       (new_student['name'], new_student['email']))
        conn.commit()
        conn.close()
        return jsonify(new_student), 201

# Handle Exams
@app.route('/exams', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handle_exams():
    conn = sqlite3.connect('exam_portal.db')
    cursor = conn.cursor()
    
    if request.method == 'GET':
        cursor.execute('SELECT * FROM exams')
        exams = cursor.fetchall()
        conn.close()
        return jsonify(exams)

    if request.method == 'POST':
        new_exam = request.json
        cursor.execute('INSERT INTO exams (subject, total_marks) VALUES (?, ?)', 
                       (new_exam['subject'], new_exam['total_marks']))
        conn.commit()
        conn.close()
        return jsonify(new_exam), 201

    if request.method == 'PUT':
        exam_id = request.json.get('id')
        updated_exam = request.json
        cursor.execute('UPDATE exams SET subject = ?, total_marks = ? WHERE id = ?', 
                       (updated_exam['subject'], updated_exam['total_marks'], exam_id))
        conn.commit()
        conn.close()
        return jsonify(updated_exam), 200

    if request.method == 'DELETE':
        exam_id = request.args.get('id')
        cursor.execute('DELETE FROM exams WHERE id = ?', (exam_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Exam deleted successfully'}), 204

# Handle Results
@app.route('/results', methods=['GET', 'POST'])
def handle_results():
    if request.method == 'GET':
        conn = sqlite3.connect('exam_portal.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM results')
        results = cursor.fetchall()
        conn.close()
        return jsonify(results)

    if request.method == 'POST':
        new_result = request.json
        conn = sqlite3.connect('exam_portal.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO results (student_id, exam_id, score) VALUES (?, ?, ?)', 
                       (new_result['student_id'], new_result['exam_id'], new_result['score']))
        conn.commit()
        conn.close()
        return jsonify(new_result), 201

# Assign exam to a student
@app.route('/exams/<int:exam_id>/assign', methods=['POST'])
def assign_exam_to_student(exam_id):
    student_data = request.json
    conn = sqlite3.connect('exam_portal.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO assigned_exams (exam_id, student_id) VALUES (?, ?)', 
                   (exam_id, student_data['student_id']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Exam assigned successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)
