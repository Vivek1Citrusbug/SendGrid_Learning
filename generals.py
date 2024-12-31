import json

def load_data():
    with open("student_database.json", "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("Error: student_database.json is empty or invalid.")
            return []


def save_data(exam_data):
    with open("student_database.json", "w") as f:
        json.dump(exam_data, f, indent=4)