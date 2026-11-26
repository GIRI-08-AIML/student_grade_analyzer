"""
Student Grade Analyzer
----------------------
A command-line Python application that records student marks, calculates
totals and averages, assigns grades, determines pass/fail status and
prints individual and class-wide performance reports.

Concepts used: variables, data types, conditionals, loops, functions,
lists, dictionaries, input validation and file export (CSV).
"""

import csv

# ---------------------------------------------------------------------------
# Configuration (constants)
# ---------------------------------------------------------------------------
SUBJECTS = ["Maths", "Science", "English", "Computer", "Social"]   # list
MAX_MARKS = 100                                                     # int
PASS_MARK = 40                                                      # int

# Grade boundaries as a list of (minimum average, grade) tuples, highest first
GRADE_SCALE = [
    (90, "A+"),
    (80, "A"),
    (70, "B"),
    (60, "C"),
    (50, "D"),
    (40, "E"),
    (0,  "F"),
]

# All students are stored here: a list of dictionaries
students = []


# ---------------------------------------------------------------------------
# Core calculation functions
# ---------------------------------------------------------------------------
def calculate_total(marks):
    """Return the sum of all subject marks."""
    total = 0
    for subject in marks:
        total += marks[subject]
    return total


def calculate_average(marks):
    """Return the average mark rounded to 2 decimal places."""
    if len(marks) == 0:
        return 0.0
    return round(calculate_total(marks) / len(marks), 2)


def get_grade(average):
    """Map an average mark to a letter grade using GRADE_SCALE."""
    for minimum, grade in GRADE_SCALE:
        if average >= minimum:
            return grade
    return "F"


def get_status(marks):
    """A student passes only if every subject is at or above PASS_MARK."""
    for subject, score in marks.items():
        if score < PASS_MARK:
            return "FAIL"
    return "PASS"


def failed_subjects(marks):
    """Return a list of subjects the student scored below PASS_MARK in."""
    return [subject for subject, score in marks.items() if score < PASS_MARK]


def build_student(name, roll_no, marks):
    """Create a student dictionary with all computed results."""
    average = calculate_average(marks)
    return {
        "name": name,
        "roll_no": roll_no,
        "marks": marks,
        "total": calculate_total(marks),
        "average": average,
        "grade": get_grade(average),
        "status": get_status(marks),
    }


# ---------------------------------------------------------------------------
# Input helpers (with validation)
# ---------------------------------------------------------------------------
def read_marks(subject):
    """Keep asking until the user enters a valid mark between 0 and MAX_MARKS."""
    while True:
        value = input(f"  {subject} (0-{MAX_MARKS}): ").strip()
        try:
            mark = float(value)
        except ValueError:
            print("  ! Please enter a number.")
            continue
        if 0 <= mark <= MAX_MARKS:
            return int(mark) if mark.is_integer() else mark
        print(f"  ! Marks must be between 0 and {MAX_MARKS}.")


def read_non_empty(prompt):
    """Keep asking until the user types something."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  ! This field cannot be empty.")


def find_student(roll_no):
    """Return the student dictionary with this roll number, or None."""
    for student in students:
        if student["roll_no"].lower() == roll_no.lower():
            return student
    return None


# ---------------------------------------------------------------------------
# Menu actions
# ---------------------------------------------------------------------------
def add_student():
    print("\n--- Add Student ---")
    name = read_non_empty("Student name: ")
    roll_no = read_non_empty("Roll number: ")
    if find_student(roll_no):
        print(f"! A student with roll number {roll_no} already exists.")
        return

    marks = {}
    print("Enter marks:")
    for subject in SUBJECTS:
        marks[subject] = read_marks(subject)

    student = build_student(name, roll_no, marks)
    students.append(student)
    print(f"\n✔ Added {name} — Average: {student['average']}, "
          f"Grade: {student['grade']}, Status: {student['status']}")


def print_report_card(student):
    """Print a detailed report for one student."""
    line = "=" * 44
    print(f"\n{line}")
    print(f" REPORT CARD — {student['name']} (Roll {student['roll_no']})")
    print(line)
    print(f" {'Subject':<15}{'Marks':>8}{'Result':>12}")
    print("-" * 44)
    for subject, score in student["marks"].items():
        result = "Pass" if score >= PASS_MARK else "Fail"
        print(f" {subject:<15}{score:>8}{result:>12}")
    print("-" * 44)
    max_total = MAX_MARKS * len(student["marks"])
    print(f" Total      : {student['total']} / {max_total}")
    print(f" Average    : {student['average']}%")
    print(f" Grade      : {student['grade']}")
    print(f" Status     : {student['status']}")
    weak = failed_subjects(student["marks"])
    if weak:
        print(f" Needs work : {', '.join(weak)}")
    print(line)


def view_student():
    if not students:
        print("\nNo students added yet.")
        return
    roll_no = read_non_empty("\nEnter roll number: ")
    student = find_student(roll_no)
    if student:
        print_report_card(student)
    else:
        print(f"! No student found with roll number {roll_no}.")


def view_all_students():
    if not students:
        print("\nNo students added yet.")
        return
    ranked = sorted(students, key=lambda s: s["average"], reverse=True)
    print(f"\n{'Rank':<6}{'Roll':<8}{'Name':<18}{'Total':>7}"
          f"{'Avg':>8}{'Grade':>7}{'Status':>8}")
    print("-" * 62)
    for rank, s in enumerate(ranked, start=1):
        print(f"{rank:<6}{s['roll_no']:<8}{s['name']:<18}{s['total']:>7}"
              f"{s['average']:>8}{s['grade']:>7}{s['status']:>8}")


def class_summary():
    if not students:
        print("\nNo students added yet.")
        return

    count = len(students)
    passed = [s for s in students if s["status"] == "PASS"]
    class_avg = round(sum(s["average"] for s in students) / count, 2)
    topper = max(students, key=lambda s: s["average"])
    lowest = min(students, key=lambda s: s["average"])

    print("\n========== CLASS PERFORMANCE SUMMARY ==========")
    print(f" Students        : {count}")
    print(f" Passed / Failed : {len(passed)} / {count - len(passed)}")
    print(f" Pass percentage : {round(len(passed) / count * 100, 2)}%")
    print(f" Class average   : {class_avg}%")
    print(f" Topper          : {topper['name']} ({topper['average']}%)")
    print(f" Lowest average  : {lowest['name']} ({lowest['average']}%)")

    # Subject-wise statistics
    print("\n Subject-wise analysis:")
    print(f"  {'Subject':<12}{'Avg':>8}{'High':>7}{'Low':>7}")
    for subject in SUBJECTS:
        scores = [s["marks"][subject] for s in students]
        avg = round(sum(scores) / len(scores), 2)
        print(f"  {subject:<12}{avg:>8}{max(scores):>7}{min(scores):>7}")

    # Grade distribution using a dictionary as a counter
    distribution = {grade: 0 for _, grade in GRADE_SCALE}
    for s in students:
        distribution[s["grade"]] += 1
    print("\n Grade distribution:")
    for grade, number in distribution.items():
        bar = "█" * number
        print(f"  {grade:<3} {bar} {number}")
    print("===============================================")


def export_to_csv(filename="grade_report.csv"):
    if not students:
        print("\nNo students to export.")
        return
    headers = ["Roll No", "Name"] + SUBJECTS + ["Total", "Average", "Grade", "Status"]
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for s in students:
            row = [s["roll_no"], s["name"]]
            row += [s["marks"][subject] for subject in SUBJECTS]
            row += [s["total"], s["average"], s["grade"], s["status"]]
            writer.writerow(row)
    print(f"\n✔ Report exported to {filename}")


def load_sample_data():
    """Load demo students so the app can be tried quickly."""
    sample = [
        ("Aarav",  "101", [92, 88, 95, 99, 85]),
        ("Diya",   "102", [76, 81, 69, 88, 72]),
        ("Kabir",  "103", [35, 52, 61, 47, 58]),
        ("Meera",  "104", [64, 70, 58, 75, 66]),
        ("Rohan",  "105", [48, 39, 55, 42, 50]),
    ]
    added = 0
    for name, roll_no, scores in sample:
        if find_student(roll_no):
            continue
        marks = dict(zip(SUBJECTS, scores))
        students.append(build_student(name, roll_no, marks))
        added += 1
    print(f"\n✔ Loaded {added} sample student(s).")


# ---------------------------------------------------------------------------
# Main menu loop
# ---------------------------------------------------------------------------
def main():
    menu = {
        "1": ("Add student", add_student),
        "2": ("View student report card", view_student),
        "3": ("View all students (ranked)", view_all_students),
        "4": ("Class performance summary", class_summary),
        "5": ("Export results to CSV", export_to_csv),
        "6": ("Load sample data", load_sample_data),
        "0": ("Exit", None),
    }

    print("==============================")
    print("   STUDENT GRADE ANALYZER")
    print("==============================")

    while True:
        print("\nMenu:")
        for key, (label, _) in menu.items():
            print(f" {key}. {label}")
        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Goodbye!")
            break
        elif choice in menu:
            menu[choice][1]()
        else:
            print("! Invalid choice, try again.")


if __name__ == "__main__":
    main()
