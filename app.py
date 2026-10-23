
import csv
import os
from flask import Flask, render_template, request

app = Flask(__name__)

def get_students():
    filename = os.path.join(
        os.path.dirname(__file__), "students.tsv"
    )
    students = []

    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter="\t")

        for row in reader:
            if len(row) >= 8 and row[0].strip().isdigit():
                students.append((
                    row[0].strip(),
                    row[1].strip(),
                    row[2].strip(),
                    row[3].strip(),
                    float(row[4]),
                    float(row[5]),
                    float(row[6]),
                    float(row[7])
                ))

    return students


@app.route("/", methods=["GET", "POST"])
def index():
    students = []
    stats = [0, 0, 0, 0]
    error = None
    search = request.form.get("search", "").strip().lower()

    try:
        all_students = get_students()
        count = len(all_students)

        if count:
            avg_attendance = sum(s[4] for s in all_students) / count
            avg_marks = sum(
                (s[5] + s[6] + s[7]) / 3
                for s in all_students
            ) / count
            departments = len(set(s[2] for s in all_students))

            stats = [
                count, avg_attendance, avg_marks, departments
            ]

        students = [
            s for s in all_students
            if not search
            or search in s[0].lower()
            or search in s[1].lower()
        ]

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
    app.run()

