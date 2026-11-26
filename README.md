# 🎓 Student Grade Analyzer (Python)

A command-line Python application that records student marks, calculates totals and averages, assigns grades, determines pass/fail status and generates individual and class-wide performance reports.

Built as **Week 1** of my internship.

## ✨ Features

- Add students with marks for 5 subjects, with input validation (numbers only, 0–100, no duplicate roll numbers)
- Automatic **total**, **average**, **letter grade** and **pass/fail** status
- Detailed **report card** per student, highlighting subjects that need work
- **Ranked list** of all students by average
- **Class summary**: pass percentage, class average, topper, subject-wise average/high/low and a grade distribution chart
- **Export to CSV** for use in Excel / Google Sheets
- Built-in **sample data** for a quick demo

## 🧠 Concepts Used

| Concept | Where |
|---|---|
| Variables & data types | Constants like `PASS_MARK`, marks as `int`/`float`, names as `str` |
| Conditionals | Grade assignment, pass/fail logic, menu choices |
| Loops | Input validation (`while`), totals and reports (`for`) |
| Functions | `calculate_total`, `calculate_average`, `get_grade`, `get_status`, ... |
| Lists | `SUBJECTS`, `students`, failed subjects |
| Dictionaries | Each student record, subject → marks, grade distribution, menu |

## 📊 Grading Scale

| Average | Grade |
|---|---|
| 90–100 | A+ |
| 80–89 | A |
| 70–79 | B |
| 60–69 | C |
| 50–59 | D |
| 40–49 | E |
| Below 40 | F |

A student **passes** only if they score at least **40 in every subject**.

## ▶️ How to Run

**VS Code / terminal** (Python 3.8+, no external libraries needed):

```bash
python grade_analyzer.py
```

**Google Colab:** upload `grade_analyzer.py`, then run `!python grade_analyzer.py` in a cell — or paste the code into a cell and run it.

Choose option `6` to load sample data, then try options `2`–`5`.

## 🖥️ Sample Output

```
Rank  Roll    Name                Total     Avg  Grade  Status
--------------------------------------------------------------
1     101     Aarav                 459    91.8     A+    PASS
2     102     Diya                  386    77.2      B    PASS
3     104     Meera                 333    66.6      C    PASS
4     103     Kabir                 253    50.6      D    FAIL
5     105     Rohan                 234    46.8      E    FAIL
```

## 🚀 Possible Improvements

- Save and load data from a file between runs
- Edit or delete student records
- Charts with matplotlib
- A web interface using Flask or Streamlit

## 📁 Project Structure

```
student-grade-analyzer/
├── grade_analyzer.py
└── README.md
```
