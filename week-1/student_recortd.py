def filter_student_by_department(students,department):
    list = []
    for i in students:
        if i["department"] == department:
           print(i["name"])


def main():
    students = [
        {"name": "Arun Kumar", "department": "CSE", "year": 3, "gpa": 8.5},
        {"name": "Priya Sharma", "department": "ECE", "year": 2, "gpa": 9.0},
        {"name": "Rahul Verma", "department": "CSE", "year": 4, "gpa": 8.2}
    ]

    department = input()
    print("Students in",department)
    filter_student_by_department(students,department)

if __name__ == "__main__":
    main()
