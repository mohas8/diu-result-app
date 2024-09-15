# app.py

from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

def get_semester_id(year, semester):
    semester_codes = {'spring': '1', 'summer': '2', 'fall': '3'}
    year_part = str(year)[-2:]  # Last two digits of the year
    semester_code = semester_codes.get(semester.lower())
    if semester_code:
        return f"{year_part}{semester_code}"
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        year = request.form['year']
        semester = request.form['semester']
        student_id = request.form['student_id']
        return redirect(url_for('results', year=year, semester=semester, student_id=student_id))
    return render_template('index.html')

@app.route('/results')
def results():
    year = request.args.get('year')
    semester = request.args.get('semester')
    student_id = request.args.get('student_id')
    semester_id = get_semester_id(year, semester)

    if not semester_id:
        return "Invalid semester provided."

    # Fetch student info
    student_info_url = f"http://software.diu.edu.bd:8006/result/studentInfo?studentId={student_id}"
    student_info_response = requests.get(student_info_url)
    if student_info_response.status_code == 200:
        student_info = student_info_response.json()
    else:
        student_info = None

    # Fetch results
    url = f"http://203.190.10.22:8189/result?grecaptcha&semesterId={semester_id}&studentId={student_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            # Compute SGPA
            total_credits = 0
            total_points = 0
            for course in data:
                credit = course['totalCredit']
                grade_point = course['pointEquivalent']
                total_credits += credit
                total_points += credit * grade_point
            if total_credits > 0:
                sgpa = round(total_points / total_credits, 2)
            else:
                sgpa = None
        else:
            sgpa = None
            total_credits = 0
        return render_template('results.html', data=data, student_info=student_info, student_id=student_id, year=year, semester=semester.capitalize(), sgpa=sgpa, total_credits=total_credits)
    else:
        return "Error fetching data."

if __name__ == '__main__':
    app.run(debug=True)
