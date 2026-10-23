
from flask import Flask, render_template, request
from pyhive import hive

app = Flask(__name__)

def get_connection():
    return hive.Connection(
        host="localhost",
        port=10000,
        username="student",
        database="student_db",
        auth="NONE"
    )

@app.route("/", methods=["GET", "POST"])
def index():
    students = []
    stats = [0, 0, 0, 0]
    error = None
    search = ""

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM student_performance LIMIT 1000"
        )
        all_students = cursor.fetchall()
        cursor.close()
        conn.close()

        count = len(all_students)

        if count:
            avg_attendance = sum(float(s[4]) for s in all_students) / count
            avg_marks = sum(
                (int(s[5]) + int(s[6]) + int(s[7])) / 3
                for s in all_students
            ) / count
            departments = len(set(s[2] for s in all_students))

            stats = [
                count,
                avg_attendance,
                avg_marks,
                departments
            ]

        search = request.form.get("search", "").strip().lower()

        if search:
            students = [
                s for s in all_students
                if search in str(s[0]).lower()
                or search in str(s[1]).lower()
            ]
        else:
            students = all_students

    except Exception as e:
        error = str(e)

    return render_template(
        "index.html",
        students=students,
        stats=stats,
        error=error,
        search=search
    )

if __name__ == "__main__":
    app.run(debug=True)

