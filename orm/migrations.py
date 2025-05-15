from models import University, Course, Teacher, Student


def run_migrations():
    # Create tables in the correct order to satisfy foreign key constraints
    University.create_table()
    Course.create_table()
    Teacher.create_table()
    Student.create_table()
    print("Migrations applied successfully.")


if __name__ == "__main__":
    run_migrations()
